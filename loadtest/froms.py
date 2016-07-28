# -*- coding: UTF-8 -*-
import logging

from django import forms
from django.http.response import Http404
from django.shortcuts import get_object_or_404

from loadtest.models import CHOICES_TYPE, CHOICES_VERSION, LoadTestResult
from loadtest.util import get_current_day_start_date


logger = logging.getLogger(__name__)

# 参考自django.contrib.auth.forms.UserCreationForm
class VexLoadTestInsertionForm(forms.ModelForm):

    # required 表示没填的错误信息
    test_result_index = forms.RegexField(
        max_length=30000,
        regex=r'.*Index.*report.*',
        error_messages={
            'invalid':  u"Index Request report format must be like: Index request report:\n,Average response (milliseconds):223",
            'required': u"Index Request report data must be set"
        }
    )
    
    test_result_bitrate = forms.RegexField(
        max_length=300000,
        regex=r'.*Bit.*report.*',
        error_messages={
            'invalid':  u"Bitrate Request report format must be like: Bit rate request report:\n,Average response (milliseconds):223",
            'required': u"Bitrate Request report data must be set"
        }
    )
    
    test_type = forms.ChoiceField(
        choices=(CHOICES_TYPE), required=True,
        error_messages={
            'invalid':  u"test_type should be VOD, cDVR or Linear",
            'required': u"test_type must be set",
        }
    )
    
    test_version = forms.ChoiceField(
        choices=(CHOICES_VERSION), required=True,
        error_messages={
            'invalid':  u"test version should be 2.3, 2.7 or 2.8",
            'required': u"test_type must be set",
        }
    )
    
    test_date = forms.DateTimeField(input_formats=['%Y-%m-%d'], required=False,
            error_messages={'invalid':  u"test date should be like 2016-01-07 00:00:00", }
    )

    class Meta:
        model = LoadTestResult
        
        # django的form validation只会对在fields中的元素验证和赋值。其他元素如果需要赋值，需要在save之前单独给instance添加值
        fields = ('test_version', 'test_type', 'test_date', 'test_result_index', "test_result_bitrate", "test_result_error")
    
    # 默认From会从数据库验证unique的数据是否存在，存在则立即给抛错。这里我们存在是更新，所以不需要验证，因此重构这个方法，其方法什么都不做
    def validate_unique(self):
        pass
    
    def save(self, commit=True):
        test_result = super(VexLoadTestInsertionForm, self).save(commit=False)
        if commit:
            try:
                # self.instance可以获得clean后的数据。也可以通过self.clean_data获取数据
                current_date = get_current_day_start_date() if self.instance.test_date is None else get_current_day_start_date(self.instance.test_date)
                exist_test_result = get_object_or_404(LoadTestResult, test_date=current_date, test_type=test_result.test_type, test_version=test_result.test_version)
                logger.info("Test result for %s[%s][%s] is existed, just update it", test_result.test_type, test_result.test_version, current_date)
                
                exist_test_result.test_result_index = self.instance.test_result_index
                exist_test_result.test_result_bitrate = self.instance.test_result_bitrate
                exist_test_result.test_result_error = self.instance.test_result_error
                exist_test_result.save()
                # self.instance.
            except Http404:
                logger.debug("Test result for %s[%s][%s] is not existed, save it", test_result.test_type, test_result.test_version, current_date)
                test_result.save()
            except Exception, e:
                logger.error(e)
        return test_result

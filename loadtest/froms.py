# -*- coding: UTF-8 -*-
from django import forms
from loadtest.models import CHOICES_TYPE, CHOICES_VERSION, LoadTestResult

# 参考自django.contrib.auth.forms.UserCreationForm
class VexLoadTestInsertionForm(forms.ModelForm):

    # required 表示没填的错误信息
    test_result_index = forms.RegexField(
        max_length=30000,
        regex=r'.*Index.*report.*',
        error_messages={
            'invalid':  u"Index Request report格式为Index request report:\n,Average response (milliseconds):223",
            'required': u"Index Request report数据必须存在"
        }
    )
    
    test_result_bitrate = forms.RegexField(
        max_length=300000,
        regex=r'.*Bit.*report.*',
        error_messages={
            'invalid':  u"Bitrate Request report format must be like: Bit rate request report:\n,Average response (milliseconds):223",
            'required': u"Bitrate Request report数据必须存在"
        }
    )
    
    test_type = forms.ChoiceField(
        choices=(CHOICES_TYPE), required=False,
        error_messages={
            'invalid':  u"test_type should be VOD, cDVR or Linear", }
    )
    
    test_version = forms.ChoiceField(
        choices=(CHOICES_VERSION), required=False,
        error_messages={
            'invalid':  u"test version should be 2.3, 2.7 or 2.8", }
    )

    class Meta:
        model = LoadTestResult
        
        # django的form validation只会对在fields中的元素验证和赋值。其他元素如果需要赋值，需要在save之前单独给instance添加值
        fields = ("test_version", "test_type", 'test_result_index', "test_result_bitrate", "test_result_error")
        # fields = ("test_version", "test_type")
    
    def save(self, commit=True):
        testResult = super(VexLoadTestInsertionForm, self).save(commit=False)
        if commit:
            testResult.save()
        return testResult

# -*- coding: UTF-8 -*-
from django.db import models
from loadtest.util import get_current_day_start_date


CHOICES_TYPE = [('VOD_T6', 'VOD_T6'), ('CDVR_T6', 'CDVR_T6'), ('LINEAR_T6', 'LINEAR_T6')]
CHOICES_VERSION = [('2.3', '2.3'), ('2.7', '2.7'), ('2.8', '2.8')]
CHOICES_MODULE = [('CORE-VEX', 'Core-VEX'), ('VEX-FE', 'VEX-FE'), ]

def get_test_type_json_list():
    test_type_list = []
    for choice in CHOICES_TYPE:
        test_type_list.append({"id":choice[0], "name":choice[1]})
    return test_type_list

def get_test_version_json_list():
    test_version_list = []
    for choice in CHOICES_VERSION:
        test_version_list.append({"id":choice[0], "name":choice[1]})
    return test_version_list

def get_test_module_json_list():
    test_module_list = []
    for choice in CHOICES_MODULE:
        test_module_list.append({"id":choice[0], "name":choice[1]})
    return test_module_list

class LoadTestResult(models.Model):
    test_date = models.DateTimeField(default=get_current_day_start_date())
    test_type = models.CharField(max_length=100, choices=CHOICES_TYPE, blank=False, null=False)
    test_version = models.CharField(max_length=10, choices=CHOICES_VERSION, blank=False, null=False)
    test_module = models.CharField(max_length=10, choices=CHOICES_MODULE, default=CHOICES_MODULE[0][0])
    test_instance_number = models.IntegerField(default=2)  # 压力测试的instance数量
    test_result_index = models.TextField(default='')
    test_result_bitrate = models.TextField(default='')
    test_result_error = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return '[test_id:{}, test_date:{}, test_type:{}, test_version:{}, test_module:{}, test_instance_size:{}]'\
                    .format(self.id, self.test_date.strftime('%Y-%m-%d'), self.test_type, self.test_version, self.test_module, self.test_instance_number)
    
    def as_dict(self):
        return dict(
            test_id=self.id,
            test_version=self.test_version,
            test_type=self.test_type,
            test_module=self.test_module,
            test_date=self.test_date.strftime('%Y-%m-%d'),
            test_result_index=self.test_result_index,
            test_result_bitrate=self.test_result_bitrate,
            test_result_error=self.test_result_error,
            )
    
    class Meta:
        db_table = 'load_test_result'
        ordering = ['-test_date']
        get_latest_by = 'test_date'
        unique_together = ("test_date", "test_type", "test_version", "test_module")

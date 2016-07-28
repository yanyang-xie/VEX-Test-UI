
from django.db import models

from loadtest.util import get_current_day_start_date


CHOICES_TYPE = [('VOD', 'vod'), ('cDVR', 'cdvr'), ('Linear', 'linear')]
CHOICES_VERSION = [('2.3', '2.3'), ('2.7', '2.7'), ('2.8', '2.8')]

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

class LoadTestResult(models.Model):
    test_date = models.DateTimeField(default=get_current_day_start_date())
    test_type = models.CharField(max_length=100, choices=CHOICES_TYPE, default='VOD')
    test_version = models.CharField(max_length=10, choices=CHOICES_VERSION, default='2.7')
    test_result_index = models.TextField(default='')
    test_result_bitrate = models.TextField(default='')
    test_result_error = models.TextField(blank=True, null=True, default='')
    
    def __unicode__(self):
        return '[test_id:{}, test_date:{}, test_type:{}, test_version:{}]'.format(self.id, self.test_date.strftime('%Y-%m-%d'), self.test_type, self.test_version)
    
    def as_json(self):
        return dict(
            test_id=self.id,
            test_version=self.test_version,
            test_type=self.test_type,
            test_date=self.test_date.strftime('%Y-%m-%d'),
            test_result_index=self.test_result_index,
            test_result_bitrate=self.test_result_bitrate,
            test_result_error=self.test_result_error,
            )
 
    class Meta:
        db_table = 'load_test_result'
        ordering = ['-test_date']
        get_latest_by = 'test_date'
        
        unique_together = ("test_date", "test_type", "test_version")

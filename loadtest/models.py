from django.db import models
from django.utils import timezone


CHOICES_TYPE = [('VOD', 'vod'), ('cDVR', 'cdvr'), ('Linear', 'linear')]
CHOICES_VERSION = [('2.3', '2.3'), ('2.7', '2.7'), ('2.8', '2.8')]

class LoadTestResult(models.Model):
    test_date = models.DateTimeField(auto_now_add=timezone.now())
    test_type = models.CharField(max_length=100, choices=CHOICES_TYPE, default='VOD')
    test_version = models.CharField(max_length=10, choices=CHOICES_VERSION, default='2.7')
    test_result_index = models.TextField(default='')
    test_result_bitrate = models.TextField(default='')
    test_result_error = models.TextField(blank=True, null=True, default='')
    
    def __unicode__(self):
        return '[test_id:{}, test_date:{}, test_type:{}, test_version:{}]'.format(self.id, self.test_date.strftime('%Y-%m-%d %H:%M'), self.test_type, self.test_version)
    
    def as_json(self):
        return dict(
            test_id=self.id,
            test_version=self.test_version,
            test_type=self.test_type,
            test_date=self.test_date.strftime('%Y-%m-%d %H:%M'),
            test_result_index=self.test_result_index,
            test_result_bitrate=self.test_result_bitrate,
            test_result_error=self.test_result_error,
            )
 
    class Meta:
        db_table = 'load_test_result'
        ordering = ['-test_date']

def get_test_type_json_list():
    test_type_list = []
    for choice in CHOICES_TYPE:
        test_type_list.append({"id":choice[0], "name":choice[1]})
    
    return test_type_list
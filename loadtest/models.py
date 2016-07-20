from django.db import models

# Create your models here.
class LoadTestResult(models.Model):
    CHOICES_TYPE = [('VOD', 'vod'), ('cDVR', 'cdvr'), ('Linear', 'linear')]
    CHOICES_VERSION = [('2.3', '2.3'), ('2.7', '2.7'), ('2.7', '2.7')]
    
    test_date = models.DateTimeField()
    test_result = models.TextField()
    test_type = models.CharField(max_length=100, choices=CHOICES_TYPE, default='VOD')
    test_version = models.CharField(max_length=10, choices=CHOICES_VERSION, default='')
    
    def __unicode__(self):
        return self.test_type + 'in' + str(self.test_date)
    
    class Meta:     
        db_table = 'load_test_result'


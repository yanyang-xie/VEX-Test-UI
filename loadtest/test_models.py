from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase

from loadtest.models import LoadTestResult
from loadtest.util import get_datetime_after, get_current_day_start_date


class LoadTestResultTests(TestCase):
    test_date = get_current_day_start_date(get_datetime_after(delta_days=300))
    test_type = 'VOD_T6'
    test_version = '2.7'
    test_result_index = "index1"
    test_result_bitrate = "bitrate1"

    def setUp(self):
        LoadTestResult.objects.get_or_create(
                test_date=self.test_date, test_type=self.test_type, test_version=self.test_version,
                test_result_index=self.test_result_index, test_result_bitrate=self.test_result_bitrate)

    def test_list(self):
        response = self.client.get(reverse("allByVersion", args=(self.test_version,)))

        self.assertContains(response, self.test_result_index)
        self.assertContains(response, self.test_result_bitrate)
        
    def test_unique(self):
        try:
            with transaction.atomic():
                instance = LoadTestResult() 
                instance.test_date = self.test_date
                instance.test_type = self.test_type
                instance.test_version = self.test_version
                instance.test_result_index = self.test_result_index
                instance.test_result_bitrate = self.test_result_bitrate
                instance.save()
        except Exception, e:
            self.assertIsInstance(e, IntegrityError)
    
    def test_update(self):
        alternate_bitrate_content = '12345'
        
        instance = LoadTestResult.objects.get(
                test_date=self.test_date, test_type=self.test_type, test_version=self.test_version)
        
        instance.test_result_bitrate = alternate_bitrate_content
        instance.save()
        
        response = self.client.get(reverse("allByVersion", args=(self.test_version,)))
        self.assertNotContains(response, self.test_result_bitrate)
        self.assertContains(response, self.test_result_index)
        
        self.assertContains(response, alternate_bitrate_content)

    def tearDown(self):
        instance = LoadTestResult.objects.filter(test_date=self.test_date, test_type=self.test_type, test_version=self.test_version)
        instance.delete()

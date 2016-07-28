# -*- coding: UTF-8 -*-
import os

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.testcases import TestCase

from VEXTestUI.settings import BASE_DIR
from loadtest.views import convert_request_body_to_form_validation
from loadtest.models import LoadTestResult


class LoadTestResultViewTests(TestCase):
    expected_loadtest_data_file = 'expected_request_body_file.xml'
    test_data_dir = os.path.join(BASE_DIR, 'loadtest', 'testdatas')
    
    def setUp(self):
        self.test_client = Client()
        
        with open(os.path.join(self.test_data_dir, self.expected_loadtest_data_file)) as f:
            self.expected_loadtest_data_content = f.read()
            self.converted_content = convert_request_body_to_form_validation(self.expected_loadtest_data_content)
    
    def test_convert(self):
        converted_content = convert_request_body_to_form_validation(self.expected_loadtest_data_content)
        
        self.assertIsNotNone(converted_content)
        self.assertIsInstance(converted_content, dict)
        self.assertTrue(converted_content.has_key('test_result_error'))
        self.assertTrue(converted_content['test_result_error'].find('222') > -1)
    
    def test_insert_with_form(self):
        response = self.test_client.post(reverse("insertLoadTestResult"), data=self.expected_loadtest_data_content, content_type='application/xml')
        self.assertContains(response, 'Test result has been saved.', status_code=200)
        
        latest_obj = LoadTestResult.objects.latest()
        self.assertTrue(latest_obj is not None)
        self.assertEqual(latest_obj.test_result_bitrate, self.converted_content['test_result_bitrate'])
    
    def test_show_all_load_test_result(self):
        response = self.test_client.post(reverse("insertLoadTestResult"), data=self.expected_loadtest_data_content, content_type='application/xml')
        self.assertContains(response, 'Test result has been saved.', status_code=200)
        
        url = reverse("showAllLoadTestResults", args=(self.converted_content['test_type'],))
        response = self.test_client.get(url)
        self.assertContains(response, self.converted_content['test_type'] , status_code=200)
        
    def test_show_index_result(self):
        # django中每步创建的对象，在退出测试的时候都会被销毁，包括数据库中的。
        response = self.test_client.post(reverse("insertLoadTestResult"), data=self.expected_loadtest_data_content, content_type='application/xml')
        self.assertContains(response, 'Test result has been saved.', status_code=200)
        
        latest_obj = LoadTestResult.objects.latest()
        self.assertTrue(latest_obj is not None)
        self.assertEqual(latest_obj.test_result_bitrate, self.converted_content['test_result_bitrate'])
        
        url = reverse("index")
        response = self.test_client.get(url)
        self.assertContains(response, self.converted_content['test_date'] , status_code=200)

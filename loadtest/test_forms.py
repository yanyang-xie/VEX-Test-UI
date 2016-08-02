import os

from django.core.urlresolvers import reverse
from django.test.client import Client
from django.test.testcases import TestCase

from loadtest.froms import VexLoadTestInsertionForm
from loadtest.views import convert_request_body_to_form_validation


class VexLoadTestInsertionFormTests(TestCase):
    error_loadtest_data_file = 'request_body_with_error_test_type.xml'
    test_data_dir = os.path.join(os.path.dirname(__file__), 'testdatas')
    
    def setUp(self):
        self.test_client = Client()
        with open(os.path.join(self.test_data_dir, self.error_loadtest_data_file)) as f:
            self.form_data = f.read()
            self.converted_content = convert_request_body_to_form_validation(self.form_data)
            self.form = VexLoadTestInsertionForm(data=self.converted_content)
    
    def test_invalidate_forms(self):
        self.form.is_valid()
        self.assertFalse(self.form.is_valid())
        
    def test_invalid_forms_response(self):
        response = self.test_client.post(reverse("insert"), data=self.form_data, content_type='application/xml')
        # self.assertFormError(response, self.form, 'test_type', 'This field is required.')
        self.assertContains(response, self.converted_content['test_type'], status_code=400)

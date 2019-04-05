# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_result_file_path_get(self):
        """Test case for result_file_path_get

        
        """
        headers = { 
            'Accept': 'application/zip',
        }
        response = self.client.open(
            '/v1/result/{file_path}'.format(file_path='file_path_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

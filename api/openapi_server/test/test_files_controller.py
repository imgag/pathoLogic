# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.test import BaseTestCase


class TestFilesController(BaseTestCase):
    """FilesController integration test stubs"""

    def test_download_file_path_get(self):
        """Test case for download_file_path_get

        
        """
        headers = { 
            'Accept': 'application/zip',
        }
        response = self.client.open(
            '/v1/download/{file_path}'.format(file_path='file_path_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

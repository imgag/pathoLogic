# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.inline_object import InlineObject  # noqa: E501
from openapi_server.models.sample import Sample  # noqa: E501
from openapi_server.test import BaseTestCase


class TestSamplesController(BaseTestCase):
    """SamplesController integration test stubs"""

    def test_samples_get(self):
        """Test case for samples_get

        List all samples
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/samples',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_post(self):
        """Test case for samples_post

        Create new samples
        """
        inline_object = {}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/v1/samples',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

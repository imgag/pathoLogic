# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from openapi_server.test import BaseTestCase


class TestStatusController(BaseTestCase):
    """StatusController integration test stubs"""

    def test_status_get(self):
        """Test case for status_get

        Get list of all sample statuses
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/status',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_status_sample_idget(self):
        """Test case for status_sample_idget

        Get status for one or more samples
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/v1/status/{sample_id}'.format(sample_id='sample_id_example'),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()

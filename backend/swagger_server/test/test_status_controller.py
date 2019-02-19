# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server.test import BaseTestCase


class TestStatusController(BaseTestCase):
    """StatusController integration test stubs"""

    def test_status_get(self):
        """Test case for status_get

        Get list of all sample statuses
        """
        response = self.client.open(
            '/v1/status',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_status_sample_idget(self):
        """Test case for status_sample_idget

        Get status for one or more samples
        """
        response = self.client.open(
            '/v1/status/{sampleID}'.format(sampleID='sampleID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

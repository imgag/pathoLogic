# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSamplesController(BaseTestCase):
    """SamplesController integration test stubs"""

    def test_samples_get(self):
        """Test case for samples_get

        List all samples
        """
        response = self.client.open(
            '/v1/samples',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_post(self):
        """Test case for samples_post

        Create new samples
        """
        body = Body()
        response = self.client.open(
            '/v1/samples',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

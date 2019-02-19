# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server.test import BaseTestCase


class TestSampleController(BaseTestCase):
    """SampleController integration test stubs"""

    def test_result_sample_idget(self):
        """Test case for result_sample_idget

        Lists results for given sample
        """
        response = self.client.open(
            '/v1/result/{sampleID}'.format(sampleID='sampleID_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_samples_sample_id_start_put(self):
        """Test case for samples_sample_id_start_put

        Starts one or multiple sample via ID
        """
        response = self.client.open(
            '/v1/samples/{sampleID}/start'.format(sampleID='sampleID_example'),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()

import connexion
import six

from flask import g
from swagger_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from swagger_server import util
from swagger_server import db

def status_get():  # noqa: E501
    """Get list of all sample statuses

     # noqa: E501


    :rtype: List[object]
    """
    return [{'id': sample['id'], 'status': sample['status']} for sample in db]


def status_sample_idget(sampleID):  # noqa: E501
    """Get status for one or more samples

     # noqa: E501

    :param sampleID: Comma seperated list of results to return
    :type sampleID: List[str]

    :rtype: InlineResponse2001
    """
    statusIDs = sampleID.split(',')
    return [{'id': sample['id'], 'status': sample.status} for sample in db if sample.id in statusIDs]

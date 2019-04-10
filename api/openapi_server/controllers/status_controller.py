import connexion
import six

from flask import g
from openapi_server.models.inline_response2001 import InlineResponse2001  # noqa: E501
from openapi_server import util
from openapi_server.db import get_db

def status_get():  # noqa: E501
    """Get list of all sample statuses

     # noqa: E501


    :rtype: List[object]
    """
    db = get_db()
    return [{'id': sample, 'status': db['samples'][sample]['status']} for sample in db['samples'].keys()]


def status_sample_idget(sample_id):  # noqa: E501
    """Get status for one or more samples

     # noqa: E501

    :param sample_id: Comma seperated list of results to return
    :type sample_id: str

    :rtype: InlineResponse2001
    """
    db = get_db()

    return [{'id': sample, 'status': db['samples'][sample]['status']} for sample in db['samples'].keys() if sample in sample_id.split(',')]

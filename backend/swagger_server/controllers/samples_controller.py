import connexion
import six

from flask import g
from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server import util

def format_sample(obj):
    return {
        'id': obj['id'],
        'author_email': obj['author_email'],
        'created': obj['created'],
        'last_updated': obj['last_updated'],
        'path_one': obj['path_one'],
        'path_two': obj['path_two']
    }

def samples_get():  # noqa: E501
    """List all samples

     # noqa: E501


    :rtype: List[Sample]
    """
    return [format_sample(sample) for sample in g.db]


def samples_post(body=None):  # noqa: E501
    """Create new samples

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
    # TODO: Create configs and add to g.db via https://pydblite.readthedocs.io/en/latest/pythonengine.html#insert-a-new-record
    return 'do some magic!'

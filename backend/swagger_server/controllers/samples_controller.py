import connexion
import six

from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server import util


def samples_get():  # noqa: E501
    """List all samples

     # noqa: E501


    :rtype: List[Sample]
    """
    return 'do some magic!'


def samples_post(body=None):  # noqa: E501
    """Create new samples

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Sample
    """
    if connexion.request.is_json:
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'

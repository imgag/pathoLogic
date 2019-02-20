import connexion
import six

from swagger_server.models.inline_response200 import InlineResponse200  # noqa: E501
from swagger_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from swagger_server import util


def result_sample_idget(sampleID):  # noqa: E501
    """Lists results for given sample

     # noqa: E501

    :param sampleID: Comma seperated list of results to return
    :type sampleID: List[str]

    :rtype: InlineResponse2002
    """
    return 'do some magic!'


def samples_sample_id_start_put(sampleID):  # noqa: E501
    """Starts one or multiple sample via ID

     # noqa: E501

    :param sampleID: 
    :type sampleID: List[str]

    :rtype: InlineResponse200
    """
    return 'do some magic!'

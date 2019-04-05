import connexion
import six

from openapi_server.models.inline_response2002 import InlineResponse2002  # noqa: E501
from openapi_server.db import get_db
from openapi_server import util

def result_sample_idget(sample_id):  # noqa: E501
    """Lists results for given sample

     # noqa: E501

    :param sample_id: Comma seperated list of results to return
    :type sample_id: List[str]

    :rtype: InlineResponse2002
    """
    db = get_db()
    samples = sample_id.split(',')
    sample = [db['samples'][sample] for sample in db['samples'].keys() if sample in samples][0]
    print(sample)

    return {'id':sample['id'],
                'result': {
                    'statistics_path': 'mystats',
                    'zip_path': sample['zip']
                }
            }

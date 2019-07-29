import os
import json
from datetime import datetime

from werkzeug.exceptions import BadRequest

from openapi_server.models.sample import Sample  # noqa: E501
from openapi_server.db import get_db
from openapi_server.util import join_read_path_with_data_dir


def format_sample(obj):
    """
    Format a sample
    """
    return {
        'id': obj['id'],
        'created': obj['created'],
        'last_updated': obj['last_updated']
    }


def samples_get(user):  # noqa: E501
    """List all samples

     # noqa: E501


    :rtype: List[Sample]
    """

    db = get_db()
    # filter samples without user id
    samples = [sample for sample in db['samples'].keys() if 'user_id' in db['samples'][sample]]
    return [format_sample(db['samples'][sample]) for sample in samples
            if db['samples'][sample]['user_id'] == user]


def samples_post(user, body=None):  # noqa: E501
    """Create new samples

     # noqa: E501

    :param body:
    :type body: dict | bytes

    :rtype: Sample
    """
    # Create samplepath
    samplepath = os.path.join(os.environ.get('BASE_DIR', os.getcwd()),'samples' )
    if not os.path.isdir(samplepath):
        os.mkdir(samplepath)

    # Save config and read files for each sample in new folder
    for s in body['samples']:
        conf = body['config']
        if os.path.isdir(os.path.join(samplepath, s['id'])):
            raise BadRequest("Sample with ID: {} exists already.".format(s['id']))
        os.mkdir(os.path.join(samplepath, s['id']))
        with open(os.path.join(samplepath, s['id'], "nf_config.json"), 'w') as outfile:
            json.dump(conf, outfile)
        with open(os.path.join(samplepath, s['id'], "read_locations.tsv"), 'w') as outfile:
            if not "path_lr" in s:
                raise BadRequest("Submitted incomplete sample {}, long run path is missing.".format(s['id']))
            paths = [join_read_path_with_data_dir(read_path) for read_path in [s['path_lr'], s.get('path_sr1', ""), s.get('path_sr2', "")] if len(read_path)]
            outfile.write(s['id'] + '\t' + "\t".join(paths) + '\n')

        db = get_db()
        db['samples'][s['id']] = {
            'user_id': user,
            'id': s['id'],
            'created': str(datetime.utcnow()),
            'last_updated': str(datetime.utcnow()),
            'status': "created",
            'zip': None
        }

    return body['samples']

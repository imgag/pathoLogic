import connexion
import six
import os
import json
#import ../.db.py as db

from datetime import datetime

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
        'path_lr': obj['path_lr'],
        'path_sr1': obj['path_sr1'],
        'path_sr2': obj['path_sr2'],
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
    samplepath = os.path.join(os.environ.get('BASE_DIR', os.getcwd()),'samples' )
    # Create samplepath
    if not os.path.isdir(samplepath):
        os.mkdir(samplepath)
    for s in body.samples:
        conf = body.config
        os.mkdir(os.path.join(samplepath, s.id))
        with open(os.path.join(samplepath, s.id, "nf_config.json"), 'w') as outfile:
            json.dump(conf.to_dict(), outfile)
        with open(os.path.join(samplepath, s.id, "read_locations.tsv"), 'w') as outfile:
            outfile.write(s.id + '\t' + s.path_lr + '\t'  +
                          s.path_sr1 + '\t' +  s.path_lr + '\n') 
     #  db = db.get_db()
     #  db.insert(id = s.id, author_email = s.author_email, created =
     #               str(datetime.utcnow()), last_updated =
     #               str(datetime.utcnow()), status = "created")
    return body.samples

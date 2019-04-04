import connexion
import six
import os
import json

from datetime import datetime

from flask import current_app, g
from swagger_server.models.body import Body  # noqa: E501
from swagger_server.models.sample import Sample  # noqa: E501
from swagger_server.db import get_db
from swagger_server import util

def format_sample(obj):
    return {
        'id': obj['id'],
        'author_email': obj['author_email'],
        'created': obj['created'],
        'last_updated': obj['last_updated']
    }

def samples_get():  # noqa: E501
    """List all samples

     # noqa: E501


    :rtype: List[Sample]
    """

    db = get_db()
    return [format_sample(db['samples'][sample]) for sample in db['samples'].keys()]

def samples_post(body=None):  # noqa: E501
    """Create new samples

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: Sample
    """
    # Create Body
    if connexion.request.is_json:
        body = Body.from_dict(connexion.request.get_json())  # noqa: E501

    # Create samplepath
    samplepath = os.path.join(os.environ.get('BASE_DIR', os.getcwd()),'samples' )
    if not os.path.isdir(samplepath):
        os.mkdir(samplepath)

    print(body.to_str())
    # Save config and read files for each sample in new folder
    for s in body.samples:
        conf = body.config
        os.mkdir(os.path.join(samplepath, s.id))
        with open(os.path.join(samplepath, s.id, "nf_config.json"), 'w') as outfile:
            json.dump(conf.to_dict(), outfile)
        with open(os.path.join(samplepath, s.id, "read_locations.tsv"), 'w') as outfile:
            outfile.write(s.id + '\t' + s.path_lr + '\t'  +
                          s.path_sr1 + '\t' +  s.path_sr2 + '\n')

    # Store informations in dict db
    db = get_db()
    db['samples'][s.id] = {
        'id':s.id,
        'author_email':s.author_email,
        'created':str(datetime.utcnow()),
        'last_updated':str(datetime.utcnow()),
        'status':"created",
        'zip':None
    }
    
    return body.samples

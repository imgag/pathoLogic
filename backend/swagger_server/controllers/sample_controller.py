import connexion
import six
import uuid
import os

#from flask import g
from swagger_server import db
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
    #sampleIDs = sampleID.split(',')
    print(sampleID)
    return sampleID


def samples_sample_id_start_put(sampleID):  # noqa: E501
    """Starts one or multiple sample via ID

     # noqa: E501

    :param sampleID: 
    :type sampleID: List[str]

    :rtype: InlineResponse200
    """
    # Create run folder
    runspath = os.path.join('BASE_DIR', os.getcwd(), 'runs')
    if not os.path.isdir(runspath):
        os.mkdir(runspath)
    runid = str(uuid.uuid4())
    runpath = os.path.join(runspath, runid)
    if not os.path.isdir(runpath):
        os.mkdir(runpath)

    # Copy input and config files to run folder         
    os.system("cat " + " ".join([os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
            'samples', sID, 'read_locations.tsv') for sID in sampleID]) +
            " >> " + os.path.join(runpath, "read_locations.tsv"))
    os.system("cp " + os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
            'samples', sampleID[0], "nf_config.json") + " " + os.path.join(runpath,
            "nf_config.json"))
    os.system("cd " + runpath + "&& nextflow run hybridassembly --input \
              read_locations.tsv -params-file nf_config.json -with-weblog \
              http://localhost:8080/v1/nextflow/" + runid)

    # Update status of samples
    #{status:'started' for k,v in db.items()}
    return 'do some magic!'

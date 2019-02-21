import connexion
import six
import uuid
import os

from flask import g
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
    sampleIDs = sampleID.split(',')
    return [{'id': sample.id, 'result': sample['result']} for sample in g.db if sample['id'] in sampleIDs]


def samples_sample_id_start_put(sampleID):  # noqa: E501
    """Starts one or multiple sample via ID

     # noqa: E501

    :param sampleID: 
    :type sampleID: List[str]

    :rtype: InlineResponse200
    """
    sampleIDs = sampleID.split(',')
    # Create run folder
    runpath = os.join(os.environ.get('BASE_DIR', os.getcwd()),'runs',str(uuid.uuid4()))
    if not os.path.isdir(runpath):
        os.mkdir(runpath)

    # Copy input and config files to run folder         
    os.system("cat " + [os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
            sampleID) for sampleID in sampleIDs].join(" ") +
            " >> " + runpath + "read_locations.tsv")
    os.system("cp " + os.path.join(os.environ.get('BASE_DIR', os.getcwd(),
             sampleIDs[0], "nf_config.json") + " " + runpath + "nf_config.json"))
    os.system("cd " + runpath + "&& nextflow run hybridassembly --input \
              read_locations.tsv -params-file nf_config.json")

    # Update status of samples
    for id in sampleIDs:
        record = [sample for sample in db  if sample.id == id][0]
        db.update(record, status = "started")
    return 'do some magic!'

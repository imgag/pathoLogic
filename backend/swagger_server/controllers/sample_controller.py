import connexion
import six
import uuid
import os
import shutil

from swagger_server.db import get_db
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
    db = get_db()
    return [db['samples'][sample].get('result', {}) for sample in db['samples'].keys() if sample in sampleID]


def samples_sample_id_start_put(sampleID):  # noqa: E501
    """Starts one or multiple sample via ID

     # noqa: E501

    :param sampleID: 
    :type sampleID: List[str]

    :rtype: InlineResponse200
    """
    # Create run folder
    runspath = os.path.join(os.environ.get('BASE_DIR', os.getcwd()), 'runs')
    if not os.path.isdir(runspath):
        os.mkdir(runspath)
    runid = str(uuid.uuid4())
    runpath = os.path.join(runspath, runid)
    if not os.path.isdir(runpath):
        os.mkdir(runpath)


    # Get current database
    db = get_db()

    db['runs'][runid] = sampleID

    # Set sample status to started
    for sID in sampleID:
        db['samples'][sID]['status'] = 'started'

    try:
        # Copy input and config files to run folder
        os.system("cat " + " ".join([os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
                'samples', sID, 'read_locations.tsv') for sID in sampleID]) +
                " >> " + os.path.join(runpath, "read_locations.tsv"))
        os.system("cp " + os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
                'samples', sampleID[0], "nf_config.json") + " " + os.path.join(runpath,
                "nf_config.json"))

        # Run Hybrid assembly
        os.system("cd " + runpath + "&& nextflow run hybridassembly -profile app \
                  -params-file nf_config.json -with-weblog \
                  http://localhost:8080/v1/nf_assembly/" + runid)

        # Run plasmident
        os.system("cd " + runpath + "&& nextflow run plasmident -profile app \
                  -params-file nf_config.json -with-weblog \
                  http://localhost:8080/v1/nf_plasmident/" + runid)

        # Zip output folders
        zip_path = os.path.join(runspath, (runid[0:7] + 'pathoLogic_results'))
        shutil.make_archive(zip_path, 'zip', runpath)
        for sID in sampleID:
            db['samples'][sID]['zip'] = zip_path
            #TODO Add assembly stats to database
            #db['samples'][sID]['assembly_stats'] =

        # Set sample status to finished
        for sID in sampleID:
            db['samples'][sID]['status'] = 'finished'

    except:

        # Set sample status to errored
        for sID in sampleID:
            db['samples'][sID]['status'] = 'error'



    return 'successful'


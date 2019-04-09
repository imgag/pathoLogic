import connexion
import six
import uuid
import os
import shutil

from werkzeug.exceptions import BadRequest
from openapi_server.db import get_db
from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.models.inline_response2002 import InlineResponse2002  # noqa: E501

def samples_sample_id_start_put(sample_id):  # noqa: E501
    """Starts one or multiple sample via ID

     # noqa: E501

    :param sample_id: 
    :type sample_id: List[str]

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

    # Get nextflow paths
    nfexecutable = os.path.join(os.environ.get('BASE_DIR', os.getcwd()), 'nextflow')
    nf_hybridassembly = os.path.join(os.environ.get('BASE_DIR', os.getcwd()), 'hybridassembly', 'main.nf')
    nf_plasmident = os.path.join(os.environ.get('BASE_DIR', os.getcwd()), 'plasmIDent', 'main.nf')
    
    #print(nfexecutable)
    #print(nf_hybridassembly)
    #print(nf_plasmident)

    # Get current database
    db = get_db()

    samples = sample_id.split(',')
    db['runs'][runid] = samples

    # Set sample status to started
    for sID in samples:
        db['samples'][sID]['status'] = 'started'


    #Try to run all this stuff

    # Copy input and config files to run folder
    status = 0

    status += os.system("cat " + " ".join([os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
            'samples', sID, 'read_locations.tsv') for sID in samples]) +
            " >> " + os.path.join(runpath, "read_locations.tsv"))
    status += os.system("cp " + os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
            'samples', sample_id, "nf_config.json") + " " + os.path.join(runpath,
            "nf_config.json"))

    # Run Hybrid assembly
    call_ha = ("cd " + runpath + " && " + nfexecutable + 
             " run " + nf_hybridassembly + "  -profile app " +
             " --outDir " + runpath + 
             " --input read_locations.tsv " +
             "-params-file nf_config.json -with-weblog" +
             " http://localhost:8080/v1/nf_assembly/" + runid)
    #print(call_ha)
    status += os.system("cd " + runpath + " && " + call_ha) 

    # Run plasmident
    call_pi =  (nfexecutable + " run " + nf_plasmident + " -profile app " +
              " --outDir " + runpath + 
              " --input file_paths_plasmident.tsv " + 
              "-params-file nf_config.json -with-weblog "+
              "http://localhost:8080/v1/nf_plasmident/" + runid)
    #print(call_pi)
    status += os.system("cd " + runpath + " && " + call_ha)  

    if status == 0:
        # Zip output folders
        zip_path = os.path.join(runspath, (runid[0:7] + 'pathoLogic_results'))
        stats_file = os.path.join(runspath, (runid[0:7] + 'results.json')) #TODO Check corect path

        shutil.make_archive(zip_path, 'zip', runpath)
        for sID in samples:
            db['samples'][sID]['zip'] = zip_path+'.zip'
            db['samples'][sID]['assembly_stats'] = stats_file

        # Set sample status to finished
        for sID in samples:
            db['samples'][sID]['status'] = 'finished'

    else:
        # Set sample status to errored
        for sID in samples:
            db['samples'][sID]['status'] = 'error'

        raise BadRequest("Process exited with status {}".format(status))

    return 'successful'

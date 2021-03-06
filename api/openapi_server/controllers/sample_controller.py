import uuid
import os
import shutil

from flask import jsonify
from werkzeug.exceptions import BadRequest
from openapi_server.db import get_db


def samples_sample_idput(sample_id, user):  # noqa: E501
    """Starts one or multiple sample via ID

     # noqa: E501

    :param sample_id:
    :type sample_id: List[str]

    :rtype: jsonify
    """

    # Get current database
    db = get_db()

    samples = sample_id.split(',')

    if not all(map(lambda sample: db['samples'][sample]['user_id'] == user, samples)):
        raise BadRequest("You are trying to start a sample for a different user. I am afraid I can't do that, Dave.")

    # Set sample status to started
    for sID in samples:
        db['samples'][sID]['status'] = 'started'

    #Try to run all this stuff
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

    # Set sample status to started
    for sID in samples:
        db['samples'][sID]['status'] = 'started'

    # Assign samples to run
    db['runs'][runid] = samples

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
             "-params-file nf_config.json -with-weblog " +
             "http://localhost:"+os.environ.get('HTTP_PORT',"8080")+"/v1/nf_assembly/" + runid)
    print(call_ha)
    status += os.system("cd " + runpath + " && " + call_ha)

    # Run plasmident
    call_pi =  (nfexecutable + " run " + nf_plasmident + " -profile app " +
              " --outDir " + runpath +
              " --input file_paths_plasmident.tsv " +
              "-params-file nf_config.json -with-weblog "+
              "http://localhost:"+os.environ.get('HTTP_PORT',"8080")+"/v1/nf_plasmident/" + runid)
    print(call_pi)
    status += os.system("cd " + runpath + " && " + call_pi)

    if status == 0:
        for sID in samples:
            # Zip output folders
            zip_path = os.path.join(runpath,  sID)
            zip_name = os.path.join(zip_path, sID + '_pathoLogic_results')
            shutil.make_archive(zip_name, 'zip', root_dir=zip_path, base_dir=zip_path)
            db['samples'][sID]['zip'] = zip_name + '.zip'
            
            # Store ref to summary statistics file in db
            stats_file = os.path.join(runpath, sID, "qc", "qc_summary_" + sID + '.json')
            db['samples'][sID]['assembly_stats'] = stats_file
    else:
        # Set sample status to errored
        for sID in samples:
            db['samples'][sID]['status'] = 'error'

        return jsonify([{'id': sID, 'status': 'error'} for sID in samples])

    return jsonify([{'id': sID, 'status': 'started'} for sID in samples])


def samples_sample_iddelete(sample_id, user):
    # Get current database
    db = get_db()

    samples = sample_id.split(',')
    if not all(map(lambda sample: db['samples'][sample]['user_id'] == user, samples)):
        raise BadRequest("You are trying to start a sample for a different user. I am afraid I can't do that, Dave.")

    for sID in samples:
        sample_folder_path = os.path.join(os.getenv('DATA_DIR', os.getcwd()), user)
        if os.path.exists(sample_folder_path):
            shutil.rmtree(sample_folder_path) # remove samples from FS
        db['samples'].pop(sID) # remove samples from database

    return jsonify([{'id': sID} for sID in samples])

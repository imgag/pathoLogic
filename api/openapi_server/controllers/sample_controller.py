import uuid
import os
import shutil
import json

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

    # Initialize new run
    db['runs'][runid] = samples
    db['runs'][runid]['status_hybridassembly'] = 'waiting'
    db['runs'][runid]['status_plasmident'] = 'waiting'

    # Copy input and config files to run folder
    status = 0

    status += os.system("cat " + " ".join([os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
            'samples', sID, 'read_locations.tsv') for sID in samples]) +
            " >> " + os.path.join(runpath, "read_locations.tsv"))
    status += os.system("cp " + os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
            'samples', sample_id, "nf_config.json") + " " + os.path.join(runpath,
            "nf_config.json"))

    # Run Hybrid assembly
    
    call_ha = ("cd " + runpath + " && " + "hybridassembly -profile app,singularity " +
             " --outDir " + runpath +
             " -params-file nf_config.json -with-weblog " +
             "http://localhost:"+os.environ.get('HTTP_PORT',"8080")+"/v1/nf_assembly/" + runid)
    status += os.system("cd " + runpath + " && " + call_ha)

    # Run plasmident
    call_pi =  ("plasmIDent  -profile app,singularity " +
              " --outDir " + runpath +
              " -params-file nf_config.json -with-weblog "+
              "http://localhost:"+os.environ.get('HTTP_PORT',"8080")+"/v1/nf_plasmident/" + runid)
    status += os.system("cd " + runpath + " && " + call_pi)

    if status == 0:
        for sID in samples:
            # Zip output folders
            result_folder = os.path.join(runpath, sID)
            sample_folder = os.path.join(os.environ.get('BASE_DIR', os.getcwd()), 'samples', sID)
            zip_file = sample_folder + '_pathoLogic_results'
            shutil.make_archive(zip_file, 'zip', root_dir=result_folder, base_dir=result_folder)
            db['samples'][sID]['zip'] = zip_file + '.zip'

            # Read summary statistics into database
            qc_summary_file = os.join(result_folder, 'qc', 'qc_summary' + sID + '.json')
            shutil.copyfile(qc_summary_file, os.path.join(result_folder, sID + "qc_summary.json"))
            with open(qc_summary_file) as json_file:
                qc_stats = json.load(json_file)
                db['samples'][sID]['qc'] = qc_stats

            # Store ref to summary statistics file in db
            stats_file = os.path.join(runpath, sID, "qc", "qc_summary_" + sID + '.json')
            db['samples'][sID]['assembly_stats'] = stats_file
            db['samples'][sID]['status'] = 'finished'
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

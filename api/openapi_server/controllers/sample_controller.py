import connexion
import six
import uuid
import os
import subprocess
import time

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

    # Get nextflow path
    basedir = os.environ.get('BASE_DIR', os.getcwd())
    nfexecutable = os.path.join(basedir , 'nextflow')
    nf_hybridassembly = os.path.join(basedir, 'hybridassembly', 'main.nf')
    nf_plasmident = os.path.join(basedir, 'plasmIDent', 'main.nf')
    
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

    # Copy input and config files to run folder
    status = 0
    
    os.system("cat " + " ".join([os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
            'samples', sID, 'read_locations.tsv') for sID in samples]) +
            " >> " + os.path.join(runpath, "read_locations.tsv"))
    os.system("cp " + os.path.join(os.environ.get('BASE_DIR', os.getcwd()),
            'samples', samples[0], "nf_config.json") + " " + os.path.join(runpath,
            "nf_config.json"))

    # Custom add the conda path (probably not needed)
    conda_path = os.environ.get('CONDA_DIR', os.path.join(os.environ.get('HOME'), 'miniconda3', 'bin'))
    conda_env = os.environ.copy()
    conda_env["PATH"] += conda_path

    os.chdir(runpath)
    # Run Hybrid assembly
    run = (nfexecutable + 
             " run " + nf_hybridassembly + "  -profile app " +
             " --outDir " + runpath + "/out" 
             " --input read_locations.tsv " +
             "-params-file nf_config.json -with-weblog" +
             " http://localhost:8080/v1/nf_assembly/" + runid + 
             " && " +
           nfexecutable + " run " + nf_plasmident + " -profile app " +
              " --outDir " + runpath + "/out" 
              " --input file_paths_plasmident.tsv " + 
              "-params-file nf_config.json -with-weblog "+
              "http://localhost:8080/v1/nf_plasmident/" + runid)
             
    p_ha = subprocess.Popen(run, shell=True, executable='/bin/bash') 
    
    # Wait for subprocess without blocking
    #while p_ha.poll() is None:
    #    time.sleep(1)
    #p_ha.wait()
    #status += p_ha.returncode
      
    os.chdir(basedir)
    # Run plasmident
    #run_pi =  (nfexecutable + " run " + nf_plasmident + " -profile app " +
    #          " --outDir " + runpath + 
    #          " --input file_paths_plasmident.tsv " + 
    #          "-params-file nf_config.json -with-weblog "+
    #          "http://localhost:8080/v1/nf_plasmident/" + runid)
    #p_pi = subproces.Popen(run_pi, shell=True, executable='/bin/bash')
    
    #p_pi.wait()
    #status += p_pi.returncode





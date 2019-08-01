#! /bin/bash

# Check if base dir is set else set to backend folder
[[ -z "${BASE_DIR}" ]] && BASE_DIR=$PWD/api

cd $BASE_DIR

# Install nextflow
curl -s https://get.nextflow.io | bash 

# Clone nextflow pipelines
git clone https://github.com/caspargross/hybridassembly
git clone https://github.com/caspargross/plasmIDent

# Pull required docker images
singularity pull docker://caspargross/hybridassembly
singularity pull docker://caspargross/plasmident

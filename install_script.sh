#! /bin/bash
# Script to install all dependencies for pathoLogic pipeline

# Install nextflow
curl -s https://get.nextflow.io | bash 
nextflow pull caspargross/hybridassembly
nextflow pull imgag/plasmIDent

# Install singularity
singularity pull docker://caspargross/hybridassembly
singularity pull docker://caspargross/plasmident

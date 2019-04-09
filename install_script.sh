#! /bin/bash

# Check if base dir is set else set to backend folder
[[ -z "${BASE_DIR}" ]] && BASE_DIR=$PWD/api

cd $BASE_DIR

# Install nextflow
curl -s https://get.nextflow.io | bash 

# Clone nextflow pipelines
git clone https://github.com/caspargross/hybridassembly
git clone https://github.com/caspargross/plasmIDent

# Build conda images
[[ -z ${CONDA_DIR} ]] && CONDA_DIR=$HOME/miniconda3/bin
export PATH=$CONDA_DIR:$PATH

conda env create -f $BASE_DIR/hybridassembly/env/ha_py27.yml
conda env create -f $BASE_DIR/hybridassembly/env/ha_py36.yml
conda env create -f $BASE_DIR/plasmIDent/env/PI_env.yml

# Fix bug in circos build (https://github.com/bioconda/bioconda-recipes/issues/9830) 
cd $CONDA_PREFIX/lib
ln -s libwebp.so.6 libwebp.so.7

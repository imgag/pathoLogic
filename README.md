pathoLogic
--------

Pipeline for hybrid assembly and identification of antibiotic resistance plasnid.
This repo contains all the files for the `pathoLogic`  pipeline and a Browser based frontend.

## Requirements:

- Unix System
- Java version >8.x
- Singularity container or conda
- Python >= 3.5 with pip and setuptools
- git

## Installation:

### 1) Check requirements
    
- Installation instructions for [singularity](https://www.sylabs.io/guides/3.0/user-guide/installation.html)
- Installation instructions for [miniconda](https://docs.conda.io/en/latest/miniconda.html)

## 2) Clone repository

Clone the repository to your desired location

```
git clone https://github.com/imgag/pathoLogic
````

A release version might be created in the future

## 3) Define environment variables

You can change the following environment variables to change the folder locations for run and sample folder used by pathoLogic. All `fastq` input files need to be moved to the the `samples` folder (default: pathologic/samples). 

| Env variabe | Description                       | Default       |
|-------------|-----------------------------------|---------------|
|  BASE_DIR   | Location of run and sample folder |  $PWD         |
|  DATA_DIR   | Location of read files            |  $PWD/samples | 

## 4) Install python requirements

We recommend to create a virtual environment for the required python packages

``` python
mkdir -p venv
python -m venv venv
source venv/bin/activate
pip install -f requirements.txt
```

## 5) Run install script

```
bash install_script.sh
```

Alternative manual installation:
clone the following two repositories into the `pathoLogic` folder

- [imgag/plasmIDent](https://github.com/imgag/plasmIDent)
- [caspargross/hybridassembly](https://github.com/imgag/hybridassembly)

and pull the singularity/docker images

```
singularity pull docker://caspargross/hybridassembly
singularity pull docker://caspargross/plasmIDent
```


The [swagger definition](http://swagger.io/) can be found [here as well](./swagger.yaml).
The `frontend` is written in [Vue](https://vuejs.org/), see more in the [frontend folder](./frontend/README.md).
The `backend` is written in [flask](http://flask.pocoo.org/), see the [backend folder](./backend/README.md).
```

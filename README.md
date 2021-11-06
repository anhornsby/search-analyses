# Food Fluency Retrieval

[![![CircleCI](https://circleci.com/gh/anhornsby/search-analyses/tree/main.svg?style=svg)](https://circleci.com/gh/anhornsby/search-analyses/tree/main)
[![Docker](https://img.shields.io/badge/Docker-Open%20in%20DockerHub-blue.svg)](https://cloud.docker.com/repository/docker/adamnhornsby/fluency-model)
[![OSF](https://img.shields.io/badge/OSF-View%20data%20on%20OSF-lightgrey.svg)](https://osf.io/xw8zk/)

A repository for fitting retrieval models to sequential fluency data using knowledge representations estimated from consumer behaviour.

The repository also shares representations of three long-term knowledge sources (episodic, semantic and hierarchical knowledge). 

## Data

Fluency data is located within [this OSF repository](https://osf.io/xw8zk/).

## Using Docker

If you are using Docker, pull the container using:

```
docker pull adamnhornsby/fluency-model
```

### Runing the models

To fit the retrieval model to each list separately, run:

```bash
docker run adamnhornsby/fluency-model:latest python3 ./ fit all
```

Using the option `all` will run models separately for each list. Using `collapse` will run the models for each participant (collapsing over lists). Using `first` will run for the first list only.

## Without Docker

### Preparing your environment

If you are not using Docker, please:

1. Install the Python 3 requirements in `requirements.txt`
2. Clone this code repository
2. Download the fluency data from [this OSF repository](https://osf.io/xw8zk/) and put it in a folder called `data` within this directory.

Note that there is no guarantee of computational reproducibility using this method.

### Running the analyses

To run the model fits, please run:

```
python3 ./ fit all
```

See above for runtime options.

## Citation

If you use this repository or the representations, please cite Hornsby & Love (2021).

## Contact

adam.hornsby.10@ucl.ac.uk

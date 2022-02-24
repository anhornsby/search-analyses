# Multi-cued retrieval model

[![CircleCI](https://circleci.com/gh/anhornsby/search-analyses/tree/main.svg?style=svg&circle-token=10e16af263e92982d240579e9c78be8e57f6db08)](https://circleci.com/gh/anhornsby/search-analyses/tree/main)
[![Docker](https://img.shields.io/badge/Docker-Open%20in%20DockerHub-blue.svg)](https://cloud.docker.com/repository/docker/adamnhornsby/fluency-model)
[![OSF](https://img.shields.io/badge/OSF-View%20data%20on%20OSF-lightgrey.svg)](https://osf.io/xw8zk/)

A repository for fitting retrieval models to semantic fluency data using multiple knowledge representations estimated from consumer behaviour. 

For more information, please see Hornsby & Love (2022), _Sequential consumer choice as multi-cued retrieval_. Science Advances. This repository contains code that will reproduce modelling results reported in Section 3 of the supplemental. A docker container can be used to guarantee reproducibility.

## Data

Fluency data is located within [this OSF repository](https://osf.io/63avp/). This data combines semantic fluency data of food items collected in the lab and 3 representations of food similarity estimated from real consumer behaviour.

* Food fluency retrievals were collected in a lab task by Zemla, Cao, Mueller & Austerweil (2020), _SNAFU: The Semantic Network and Fluency Utility_ and shared via their [GitHub repository here](https://github.com/AusterweilLab/snafu-py).
* Representations episodic, semantic and hierarchical similarity were calculated using a dataset of in-store grocery transactions. These representations are described in the method and Section 1 of the Supplemental Materials in Hornsby & Love (2022).

This data was joined by finding products that matched each food retrieval. This process is described in Section 3 of the Supplemental Materials in Hornsby & Love (2022).

The `transition_probs.csv` file describes the similarity between each sequential retrieval for each similarity measure. It also describes the similarity between each retrieval and the remaining retrievals for that participant for each similarity measure. Both are used in the SAM retrieval model.

The OSF repository also shares full similarity matrices for three long-term knowledge sources; episodic, semantic and hierarchical knowledge. We encourage researchers to experiment with these in future projects (see the `representations` folder in OSF).

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
2. Download the fluency data from [this OSF repository](https://osf.io/63avp/) and put it in a folder called `data` within this directory.

Note that there is no guarantee of computational reproducibility using this method.

### Running the analyses

To run the model fits, please run:

```
python3 ./ fit all
```

See above for runtime options.

## Citation

If you use this repository or the representations, please cite Hornsby & Love (2022), _Sequential consumer choice as multi-cued retrieval_. Science Advances.

## Contact

adam.hornsby.10@ucl.ac.uk

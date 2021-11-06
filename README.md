# Food Fluency Retrieval

Multiple systems of long-term knowledge guide sequential retrieval of food items.

This repository show how multiple representations can be included in a retrieval model to explain sequential fluency data. 

We share representations of these long-term knowledge sources fit to real grocery shopping patterns in a separate OSF repository. 

See Hornsby & Love (2021) for more information.


## Docker


### Run the models

To fit the retrieval model to each list separately, run:

```bash
docker run adamnhornsby/fluency-model:latest python3 ./ fit all
```
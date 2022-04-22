# soundnetbrain_hear

[SoundNet](http://soundnet.csail.mit.edu/) brain encoding models, finetuned by Courtois Neuromod data and following the [HEAR api](https://neuralaudio.ai/hear2021-rules.html#common-api).

Features : 
- Returns Scene Embeddings (1024) using average output of the Conv7 layer
- Returns TimeStamp Embeddings (128 x T) and timestamps (T) every 40.7 ms, usings outputs of Conv4 Layer. Details on how timings were estimated are given in [timings.py](soundnetbrain_hear/timings.py)
- The API gives a sample rate of 48 kHz to be able to use the zenodo datasets, but it will internally resample to SoundNet sample rate, which is 22.050 kHz. 

## Installation

### Environement

Clone this repository with sub-module:

```
git clone --recursive git@github.com:ltetrel/hear-eval-test.git && cd hear-eval-test
```

Please also load the singularity module:

```
module load singularity/3.8
```

#### Containers

If you already have access to the built singularity image `soundnetbrain_hear.sif`, you don't need to re-build the container.
Just make a symlink to add it in the repository:

```
ln -s /PATH/TO/soundnetbrain_hear.sif envs/soundnetbrain_hear.sif
```

Otherwise you will need to build it yourself (you will need root access and Docker installed on your machine).

```
make build
```

Make sure that there is an existing `.sif` image in the `envs` directory.

### Data

Copy all pytorch checkpoints into `models` from zenodo (to be published soon).
You will also need to download benchmark data:

```
make data
```

## Validation 

The code should pass validation by the [Hear validator](https://github.com/neuralaudio/hear-validator).
Just run the following command on a GPU server with CUDA 11.2:

```
make test
```
## Running the full evaluation 

Install the [heareval package](https://github.com/neuralaudio/hear-eval-kit). Can be done with `pip install heareval`, but it might be more appropriate to use docker. 

Heareval will need to run pytorch and tensorflow, both on GPUs. 

See on the [heareval repo](https://github.com/neuralaudio/hear-eval-kit) for instructions on how to download the datasets and run evaluation on models.

## Authors and acknowledgment
Nicolas Farrugia, Maëlle Freteault. 

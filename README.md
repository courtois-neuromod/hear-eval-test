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
Make sure to have an account on https://quay.io/ because this is where singularity provides its latest images.

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

## Test 

The code should pass validation by the [Hear validator](https://github.com/neuralaudio/hear-validator).
Just run the following command on a GPU server with CUDA 11.2:

```
make test
```
## Running the benchmark

We will use the [heareval package](https://github.com/neuralaudio/hear-eval-kit) installed in the container to compute the embeddings from the `soundnetbrain_hear` model, and then evaluates those embeddings to test the performance of the encoding model.

### Embeddings
To compute the embeddings run:
```
make embeddings
```

When finished, you should ses a list of files under the `embeddings/soundentbrain_hear` folder.

### Evaluation

When the embeddings are create, you can launch:
```
make eval
```

You will find all logs in the `logs/` folder.

## Authors and acknowledgment
Nicolas Farrugia, Maëlle Freteault. 

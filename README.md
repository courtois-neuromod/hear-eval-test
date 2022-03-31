# soundnetbrain_hear

[SoundNet](http://soundnet.csail.mit.edu/) brain encoding models, finetuned by Courtois Neuromod data and following the [HEAR api](https://neuralaudio.ai/hear2021-rules.html#common-api).

The API gives a sample rate of 48 kHz to be able to use the zenodo datasets, but it will internally resample to SoundNet sample rate, which is 22.5 kHz. 

## Installation

Clone this repository and run this in the folder : 

`pip install -e .`

## Validation 

The code should pass validation by the [Hear validator](https://github.com/neuralaudio/hear-validator) : 

`hear-validator soundnetbrain_hear --model /path/to/modefile.pt -d cpu`

## Running the full evaluation 

Install the [heareval package](https://github.com/neuralaudio/hear-eval-kit). Can be done with `pip install heareval`, but it might be more appropriate to use docker. 

Heareval will need to run pytorch and tensorflow, both on GPUs. 

See on the [heareval repo](https://github.com/neuralaudio/hear-eval-kit) for instructions on how to download the datasets and run evaluation on models.

## Authors and acknowledgment
Nicolas Farrugia, Maëlle Freteault. 

## License
For open source projects, say how it is licensed.
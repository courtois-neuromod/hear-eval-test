# soundnetbrain_hear

[SoundNet](http://soundnet.csail.mit.edu/) brain encoding models, finetuned by Courtois Neuromod data and following the [HEAR api](https://neuralaudio.ai/hear2021-rules.html#common-api).

# Installation

Clone this repository and run this in the folder : 

`pip install -e .`

# Validation 

The code should pass validation by the [Hear validator](https://github.com/neuralaudio/hear-validator) : 

`hear-validator soundnetbrain_hear --model /path/to/modefile.pt -d cpu`

## Authors and acknowledgment
Nicolas Farrugia, Maëlle Freteault. 

## License
For open source projects, say how it is licensed.
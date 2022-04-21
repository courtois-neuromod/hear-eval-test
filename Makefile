# inspired from https://github.com/xolox/python-humanfriendly/blob/master/Makefile

PACKAGE_NAME = $(shell python3 setup.py --name)
PACKAGE_VERSION = $(shell python3 setup.py --version)
USER = $(shell whoami)

.PHONY: build test data clean

default:
	@echo "Makefile for $(PACKAGE_NAME) $(PACKAGE_VERSION)"
	@echo
	@echo 'Usage:'
	@echo
	@echo '    make build      build the singularity image (docker required)'
	@echo '    make test       run the tests to check for GPU and heareval'
	@echo '    make data    	 download the benchmark data'
	@echo '    make clean      cleanup all temporary files'
	@echo

build:
	@$(bash) soundnetbrain_hear/containers/build_sif.bash

test: 
	@singularity exec --cleanenv --no-home --nv envs/soundnetbrain_hear.sif python3 -c "import tensorflow as tf; tf.test.is_gpu_available()"
	@singularity exec --cleanenv --no-home -B models/:/soundnetbrain_hear/models --nv envs/soundnetbrain_hear.sif hear-validator soundnetbrain_hear --model /soundnetbrain_hear/models/voxels_conv5.pt -d cuda

data:
	@singularity exec --cleanenv --no-home -B data/:/soundnetbrain_hear/data --nv envs/soundnetbrain_hear.sif zenodo_get -o /soundnetbrain_hear/data 10.5281/zenodo.6332517
# google cloud storage `gsutil` for other resolutions
#	@singularity exec --cleanenv --no-home -B data/:/soundnetbrain_hear/data --nv envs/soundnetbrain_hear.sif gsutil -m cp -r "gs://hear2021-archive/tasks/16000"	"gs://hear2021-archive/tasks/22050"	"gs://hear2021-archive/tasks/32000"	"gs://hear2021-archive/tasks/44100"	"gs://hear2021-archive/tasks/48000" /soundnetbrain_hear/data

clean:
	@rm -Rf *.egg *.egg-info .cache .coverage .tox build dist docs/build htmlcov
	@find -depth -type d -name __pycache__ -exec rm -Rf {} \;
	@find -type f -name '*.pyc' -delete


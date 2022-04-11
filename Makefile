# inspired from https://github.com/xolox/python-humanfriendly/blob/master/Makefile

PACKAGE_NAME = $(shell python3 setup.py --name)
PACKAGE_VERSION = $(shell python3 setup.py --version)

default:
	@echo "Makefile for $(PACKAGE_NAME) $(PACKAGE_VERSION)"
	@echo
	@echo 'Usage:'
	@echo
	@echo '    make build      build the singularity image (docker required)'
	@echo '    make test       run the test suite'
	@echo '    make publish    publish changes to GitHub/PyPI'
	@echo '    make clean      cleanup all temporary files'
	@echo

install:
	@$(MAKE) clean
	@python3 -m pip install -r requirements.txt
# @python3 setup.py sdist bdist_wheel
# @python3 -m pip install -e .

build:
	@$(bash) soundnetbrain_hear/containers/build_sif.bash

test: 
	@singularity exec --nv /data/cisl/containers/hear-eval-kit.simg python3 -c "import tensorflow as tf; tf.test.is_gpu_available()"

publish-reference:
#datalad commit reference
#datalad push --to osf

publish:
# @git push origin && git push --tags origin
# @python3 -m pip install twine wheel setuptools
# @$(MAKE) install
# @python3 -m twine upload dist/*
# @$(MAKE) clean

publish-test:
# push tests on another datalad repo ?

clean:
	@rm -Rf *.egg *.egg-info .cache .coverage .tox build dist docs/build htmlcov
	@find -depth -type d -name __pycache__ -exec rm -Rf {} \;
	@find -type f -name '*.pyc' -delete


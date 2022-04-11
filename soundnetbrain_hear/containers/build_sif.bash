#!/bin/bash

echo "Log-in to quay.io for docker2singularity"
sudo docker login quay.io
SCRIPT_PATH=$(realpath ${0%/*}/../..)
echo "Removing previous container"
rm -f envs/*.sif
echo "Building hear-eval-kit docker image..."
if cd ${SCRIPT_PATH}/envs/hear-eval-kit/docker/ && sudo docker build --tag=hear-eval-kit --file Dockerfile-cuda11.2-python3.8 .; then
  echo "Building soundnetbrain_hear docker image..."
  if cd ${SCRIPT_PATH} && sudo docker build --tag=soundnetbrain_hear --file envs/Dockerfile .; then
    echo "Converting to singularity \".sif\"..."
    cd ${SCRIPT_PATH}/envs && sudo docker run -v /var/run/docker.sock:/var/run/docker.sock \
                                              -v $(pwd):/output \
                                              --privileged -t \
                                              --rm quay.io/singularity/docker2singularity:v3.8.4 \
                                              --name soundnetbrain_hear soundnetbrain_hear

    if sudo docker images | grep none | awk '{ print $3; }'; then
      echo "Deleting none images"
      sudo docker rmi --force $(sudo docker images | grep none | awk '{ print $3; }')
    fi
  else
	  echo "soundnetbrain_hear build was not successfull"
  fi
else
	echo "hear-eval-kit build was not successfull"
fi
cd ${SCRIPT_PATH}
#!/bin/bash

REPO_PATH=${0%/*}/../..
echo "Removing previous container"
rm -f ${REPO_PATH}/envs/*.simg
cd ${REPO_PATH}/envs/hear-eval-kit/docker/
echo "Building docker image..."
if sudo docker build --tag=hear-eval-kit --file Dockerfile-cuda11.2-python3.8 .; then
	cd ../../
	echo "Converting to singularity..."
	sudo docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd):/output --privileged -t --rm singularityware/docker2singularity --name hear-eval-kit hear-eval-kit

	if sudo docker images | grep none | awk '{ print $3; }'; then
		echo "Deleting none images"
		sudo docker rmi --force $(sudo docker images | grep none | awk '{ print $3; }')
	fi
else
	echo "Docker build was not successfull"
fi
cd ../

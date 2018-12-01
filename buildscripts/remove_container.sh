#!/bin/sh
#
. ./buildscripts/docker-check
. ./buildscripts/env-check

# Remove container
${DOCKER} down --remove-orphans

name="${IMGNAME}${1}"
for img in `docker images --all --quiet ${name}`
do
	docker rmi -f $img
done
rm -f .${OSTARGET}${1}_container

#!/bin/sh
#
# Execute command in docker image
#
# #1 name of script in buildscripts directory
#
. ./buildscripts/docker-check.sh
. ./buildscripts/env-check.sh

${DOCKER_BUILD} ./buildscripts/$1

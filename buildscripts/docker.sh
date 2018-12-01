#!/bin/sh
#
# Execute command in docker image
#
# #1 name of script in buildscripts directory
#
. ./buildscripts/docker-check
. ./buildscripts/env-check

${DOCKER_BUILD} ./buildscripts/$1

#!/bin/sh
#
# Execute shell in docker image
#
. ./buildscripts/docker-check
. ./buildscripts/env-check

${DOCKER_ROOT_SHELL}

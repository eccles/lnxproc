#!/bin/sh -e
#
# Execute command inside docker builder

. ./buildscripts/log
. ./buildscripts/not_inside_builder
. ./buildscripts/name

log "Create $1 image"
docker build -f Dockerfile-$1 -t ${NAME}$1 .
touch $1

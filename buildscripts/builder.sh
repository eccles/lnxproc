#!/bin/sh -e
#
# Execute command inside docker builder

. ./buildscripts/log
. ./buildscripts/not_inside_builder
. ./buildscripts/name

log "Execute $@ in builder"
docker run \
    --rm \
    -it \
    -p 127.0.0.1:8080:8080 \
    -v $(pwd):/home/builder \
    -u $(id -u):$(id -g) \
    ${NAME}builder \
    "$@"

log "Execute $@ in builder - finished"

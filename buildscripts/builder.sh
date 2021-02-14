#!/bin/sh -x
#
# Execute command inside docker builder
docker run \
    --rm \
    -it \
    -v $(pwd):/home/builder \
    -u $(id -u):$(id -g) \
    lnxprocbuilder \
    "$@"


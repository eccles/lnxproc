#!/bin/sh
#
. ./buildscripts/log

log "create_container: $*"
. ./buildscripts/docker-check
. ./buildscripts/env-check

NAME=${OSTARGET}${1}

# Add containers
${DOCKER} up --force-recreate --build -d ${NAME}
${DOCKER} logs ${NAME}
touch .${NAME}_container

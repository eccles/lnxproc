#!/bin/sh
#
. ./buildscripts/log

log "create_container: $*"
. ./buildscripts/docker-check.sh
. ./buildscripts/env-check.sh

NAME=${OSTARGET}${1}

# Add containers
${DOCKER} up --force-recreate --build -d ${NAME}
${DOCKER} logs ${NAME}
touch .${NAME}_container

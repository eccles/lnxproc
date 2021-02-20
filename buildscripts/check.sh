#!/bin/sh -e
# 
# Statically analyse code
#

. ./buildscripts/log
. ./buildscripts/inside_builder
. ./buildscripts/name

PEP8="pycodestyle --format=pylint"
PYTHON=python3
PYLINT="${PYTHON} -m pylint --rcfile=pylintrc"

PYS=$( find -maxdepth 1 -name '*.py' )
log "Executing ${PEP8}"
${PEP8} ${PYS} ${NAME} unittests
log "Executing ${PYLINT}"
${PYLINT} ${PYS} ${NAME} unittests

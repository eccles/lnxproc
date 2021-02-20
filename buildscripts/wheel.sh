#!/bin/sh -e
# 
# make wheel package
#

. ./buildscripts/log
. ./buildscripts/inside_builder

PYTHON=python3
SETUP="${PYTHON} setup.py"
log "Executing ${SETUP}"
${SETUP} bdist_wheel
ls -l dist

#!/bin/sh -e
# 
# Statically analyse code
#

if [ -s name ]
then
	NAME=$( cat name )
else
	NAME=
fi
PEP8="pycodestyle --format=pylint"
PYTHON=python3
# ${PYTHON} -m pylint --generate-rcfile>pylintrc
PYLINT="${PYTHON} -m pylint --rcfile=pylintrc"

PYS=$( find -maxdepth 1 -name '*.py' )
${PEP8} ${PYS} ${NAME} unittests
${PYLINT} ${PYS} ${NAME} unittests

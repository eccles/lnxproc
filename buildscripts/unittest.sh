#!/bin/sh -e
# 
# test packages - generic script
#

if [ -s name ]
then
	NAME=$( cat name )
else
	NAME=
fi
if [ -n "${NAME}" ]
then
	SOURCES="${NAME}"
else
	SOURCES=
fi

PYTHON=python3
COVERAGE="coverage"
if [ -z "${TESTRUNNER}" ]
then
	TESTRUNNER=unittest
fi

${COVERAGE} run --branch --source ${SOURCES} -m ${TESTRUNNER} discover -v
${COVERAGE} annotate
${COVERAGE} html
${COVERAGE} xml
${COVERAGE} report

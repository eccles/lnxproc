#!/bin/sh -e
# 
# test packages - generic script
#

. ./buildscripts/log
. ./buildscripts/inside_builder
. ./buildscripts/name

PYTHON=python3
COVERAGE="coverage"
if [ -z "${TESTRUNNER}" ]
then
	TESTRUNNER=unittest
fi

${COVERAGE} run --branch --source ${NAME} -m ${TESTRUNNER} discover -v
${COVERAGE} annotate
${COVERAGE} html
${COVERAGE} xml
${COVERAGE} report

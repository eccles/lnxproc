#!/bin/sh -e
#
# Start api container

set -x
. ./buildscripts/log
. ./buildscripts/not_inside_builder
. ./buildscripts/name

start_api() {
	log "Start api"
	API_ID=`docker run --rm -p 8080:8080 -d ${NAME}api`
	echo "${API_ID}" > api_id
}
stop_api() {
	if [ -s api_id ]
	then
		API_ID=`cat api_id`
		docker stop ${API_ID}
	fi
}

if [ $# -gt 0 ]
then
	case "$1"  in
	"stop")
		stop_api
		;;
	*):
		start_api
		;;
    esac
else
	start_api
fi

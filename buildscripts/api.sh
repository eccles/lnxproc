#!/bin/sh -e
#
# Start and stop api container

. ./buildscripts/log
. ./buildscripts/not_inside_builder
. ./buildscripts/name

start_api() {
	if [ ! -s api_id ]
	then
		log "Start api"
		API_ID=`docker run \
                       --rm \
                       -p 127.0.0.1:8080:8080 \
                       -e LNXPROC_PORT=8080 \
                       -d \
                       -v /proc:/proc \
                       -v /sys:/sys \
                       ${NAME}api`
		echo "${API_ID}" > api_id
        sleep 2
	fi
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

#!/bin/bash -ex
# 
# Test installed wheel in container
#
. ./buildscripts/log

which curl
if [ $? -ne 0 ]
then
	log "curl is required for testing"
	exit 1
fi
#
rm -rf  results
mkdir results
URL="http://localhost:8080"
#
# get keys
time curl -o results/keys.json -H "Accept: application/json" -H "Content-Type: application/json" $URL/keys

# get all statuses
time curl -o results/all.json -H "Accept: application/json" -H "Content-Type: application/json" $URL/resource

MODULES=( \
    cgroups \
    cpufreq \
    cpuinfo \
    diskstats \
    domainname \
    hostname \
    interrupts \
    loadavg \
    meminfo \
    netarp \
    netdev \
    netrpcnfs \
    netrpcnfsd \
    netsnmp \
    osrelease \
    partitions \
    schedstat \
    stat \
    uptime \
    vmstat \
)

# get resources
for r in ${MODULES[@]}
do
	time curl -o results/$r.json \
		-H "Accept: application/json" \
		-H "Content-Type: application/json" \
		$URL/resource/$r
done

PIDMODULES=( \
    pidcmdline \
    pidenviron \
    pidfd \
    pidio \
    pidsched \
    pidschedstat \
    pidsmaps \
    pidstatm \
    pidstat \
    pidstatus \
)

log "Process id is $PPID"

# get status of this process id
for r in ${PIDMODULES[@]}
do
	time curl -o results/$r.json \
		-H "Accept: application/json" \
		-H "Content-Type: application/json" \
		$URL/pid/$PPID/$r
done

# show logs output
docker-compose logs

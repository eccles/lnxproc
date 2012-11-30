#
. ./buildscripts/log

export BASEDIR=$(basename `pwd` )
export PREFIX=${BASEDIR}${BUILDID}

export DOCKER_COMPOSE="docker-compose -p ${PREFIX}"
export DOCKER="${DOCKER_COMPOSE} -f docker-compose.yaml"

if [ -z "${OSTARGET}" ]
then
	OSTARGET=alpine
fi
export API=${OSTARGET}api
export BUILDER=${OSTARGET}builder

export DOCKER_BUILD="${DOCKER} exec -T ${BUILDER}"

export DOCKER_COPY="docker cp"

export IMGNAME=${PREFIX}_${OSTARGET}

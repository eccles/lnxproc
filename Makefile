#
REPONAME := lnxproc
BUILDER := $(REPONAME)builder
API := $(REPONAME)api

#------------------------------------------------------------------------------
#
# Requires docker-ce and docker-compose
#
# To start from scratch
#
#     make clean
#
#------------------------------------------------------------------------------
#
.PHONY: all
all:  clean artifacts test

#
# `$ make check` statically check the code
#
.PHONY: check
check:
	./buildscripts/builder.sh buildscripts/check.sh

#------------------------------------------------------------------------------
#
# `$ make unittest` execute any tests
#
.PHONY: unittest
unittest: check
	./buildscripts/builder.sh buildscripts/unittest.sh

#------------------------------------------------------------------------------
#
# `$ make wheel` makes wheel
#
.PHONY: wheel
wheel:  unittest
	./buildscripts/builder.sh buildscripts/wheel.sh

#------------------------------------------------------------------------------
#
# make artifacts
#
.PHONY: artifacts
artifacts: wheel

#------------------------------------------------------------------------------
#
# `$ make test` check that it works as installed
#
.PHONY: test
test: wheel
	./buildscripts/test.sh

#------------------------------------------------------------------------------
#
# `make clean` cleans all generated files from container
#
.PHONY: clean
clean:
	./buildscripts/clean.sh

#------------------------------------------------------------------------------
#
# `make shell` shells into builder container as user
#
.PHONY: shell
shell:
	./buildscripts/builder.sh /bin/bash

#------------------------------------------------------------------------------
#
# docker dependencies
#
.PHONY: builder
builder: requirements-dev.txt Dockerfile-builder
	docker build -f Dockerfile-builder -t $(BUILDER) .

.PHONY: api
api: requirements.txt Dockerfile-api
	docker build -f Dockerfile-api -t $(API) .

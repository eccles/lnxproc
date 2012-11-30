#
export OSTARGET ?= alpine

API := $(OSTARGET)api
BUILDER := $(OSTARGET)builder

#------------------------------------------------------------------------------
#
# Requires docker-ce and docker-compose
#
# To start from scratch
#
#     make remove_containers
#     make clean
#
#------------------------------------------------------------------------------
#
.PHONY: all
all:  remove_containers clean artifacts test

#------------------------------------------------------------------------------
#
# `$ make dependencies` 
#
.PHONY: dependencies
dependencies: .$(BUILDER)_container
	./buildscripts/docker.sh dependencies.sh

#------------------------------------------------------------------------------
#
# `$ make check` statically check the code
#
.PHONY: check
check: .$(BUILDER)_container dependencies
	./buildscripts/docker.sh check.sh

#------------------------------------------------------------------------------
#
# `$ make unittest` execute any tests
#
.PHONY: unittest
unittest: .$(BUILDER)_container check
	./buildscripts/docker.sh unittest.sh

#------------------------------------------------------------------------------
#
# `$ make wheel` makes wheel
#
.PHONY: wheel
wheel: .$(BUILDER)_container unittest
	./buildscripts/docker.sh wheel.sh

#------------------------------------------------------------------------------
#
# make artifacts
#
.PHONY: artifacts
artifacts: .$(BUILDER)_container wheel

#------------------------------------------------------------------------------
#
# `$ make test` check that it works as installed
#
.PHONY: test
test: wheel .$(API)_container
	./buildscripts/test.sh

#------------------------------------------------------------------------------
#
# `make clean` cleans all generated files from container
#
.PHONY: clean
clean: .$(BUILDER)_container
	./buildscripts/docker.sh clean.sh

#------------------------------------------------------------------------------
#
# docker dependencies
#
.PHONY: remove_containers
remove_containers:
	./buildscripts/remove_containers.sh api builder

.$(BUILDER)_container: Dockerfile-$(BUILDER) docker-compose.yaml
	./buildscripts/create_container.sh builder

.$(API)_container: Dockerfile-$(API) docker-compose.yaml
	./buildscripts/create_container.sh api

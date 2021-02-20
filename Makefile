#------------------------------------------------------------------------------
#
# Requires docker-ce
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
	./buildscripts/check.sh

#------------------------------------------------------------------------------
#
# `$ make unittest` execute any tests
#
.PHONY: unittest
unittest: check
	./buildscripts/unittest.sh

#------------------------------------------------------------------------------
#
# `$ make wheel` makes wheel
#
.PHONY: wheel
wheel:  unittest
	./buildscripts/wheel.sh

#------------------------------------------------------------------------------
#
# `$ make api_id` starts the api container
#
api_id: api
	./buildscripts/api.sh start

#------------------------------------------------------------------------------
#
# `$ make test` check that it works as installed
#
.PHONY: test
test: api_id
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
builder: requirements.txt requirements-dev.txt Dockerfile-builder
	./buildscripts/create_container.sh builder

api: wheel Dockerfile-api
	./buildscripts/create_container.sh api

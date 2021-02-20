# buildscripts

## Container-based development

### Development workflow

Tools are provided such that the code can be compiled on different distros regardless of the distro running
on the development host. This is achieved by providing suitable docker files, a simple Makefile and
separate buildscripts for each stage of the build process. Development can be done entirely on the developer host
without needing to push upstream.

Importantly, any suitable linux distro can be used as the development host provided that make and docker-ce
can be installed.


#### Requirements

The container-based workflow requires the installation of:

- make
- docker-ce

on your development host.

Importantly, add your username to the docker group so that sudo is not required:

- sudo usermod -aG docker $USER


#### Preparation

Make changes to code and test them:

```bash
make unittest
```

#### Start from clean system

To restore a pristine environment:

```bash
make clean
```

and proceed with further development as described above. This does **not** revert any code changes made.

### List of make targets in priority order

```bash
make clean                # returns build environment to pristine state - does **not** revert any code changes
make check                # statically checks code
make unittest             # runs unittests
make wheel                # makes wheel package for PyPi
make api                  # makes api container
make test                 # executes functional tests
```

The make command will ensure that all required targets are made in order. i.e. 'make wheel' will also execute
'make builder', 'make check' and 'make unittest'.

This is inefficient but safe. 

It is more efficient to execute the corresponding scripts durectly but less safe:

```bash
./buildscripts/clean.sh
./buildscripts/create_container.sh builder
./buildscripts/unittest.sh
./buildscripts/wheel.sh
./buildscripts/create_container.sh api
./buildscripts/api.sh start
./buildscripts/test.sh
./buildscripts/api.sh stop
```

### Debugging

Before executing any make targets set an environment variable to 'DEBUG' to see log output:

```bash
export LNXPROC_LOGLEVEL="DEBUG"
make
```

### Additional artifacts

- The python3 wheel is created in dist/
- HTML coverage is described in htmlcov/ - point your browser to htmlcov/index.html


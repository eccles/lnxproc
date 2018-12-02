# buildscripts

## Container-based development

### Development workflow

Tools are provided such that the code can be compiled on different distros regardless of the distro running
on the development host. This is achieved by providing suitable docker compose files, a simple Makefile and
separate buildscripts for each stage of the build process. Development can be done entirely on the developer host
without needing to push upstream.

Importantly, any suitable linux distro can be used as the development host provided that make, docker-ce,docker-compose,
can be installed.


#### Requirements

The container-based workflow requires the installation of:

- make
- docker-ce
- docker-compose

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
make remove_containers    # deletes the docker containers
make clean                # returns build environment to pristine state - does **not** revert any code changes
make check                # statically checks code
make unittest             # runs unittests
make artifacts            # make the artifacts - currently only packages
make test                 # installs wheel in minimal container and executes command
make                      # cleans and makes artifacts - execute this **before** pushing upstream
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
- the alpineapi container could be pushed to a suitable docker repo


# 2.2.0

    Multithread read of data
    Add /resource key to REST interface that returns data for all resources and pids.
    Implement streaming of json output
    Fix bug where pid data is ignored because of incorrect path

# 2.1.0

    Make API container privileged such that protected files such as /proc/<pid>/smaps
    can be read. This has security concerns but specifying cap_add in docker-compose
    file or setcap the python3 executable did not work.

# 2.0.0

    REST API

# 1.0.0

    First viable release


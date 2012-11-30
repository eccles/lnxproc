# lnxproc

    Exposes the Linux /proc and /sys filesystems with a series of classes.
    Additionally provides extra classes :

        - all data is returned as python dictionaries.
        - static data is memoized to improve performance.

    NB - this module will only work on Linux.

# Usage

## From python3

    The simplest interface is to the Resources module which takes a list of keys
    to specify which /proc or /sys files to read:

### Access all keys

```python
    #!/usr/bin/env python3
    import pprint
    from lnxproc import Resources

    res = Resources()  # will read all resources

    res.read()

    data = res.normalize()
    pprint.pprint(data)
```

### Show available keys

    To show available keys and the corresponding file for each key:

```python
    #!/usr/bin/env python3
    from lnxproc import show_keys

    res = show_keys()
```

### Access some keys

    Only some keys and/or pids are wanted:

```python
    #!/usr/bin/env python3
    import pprint
    from lnxproc import Resources

    res = Resources(
        keys=('cgroups', 'pidstat', 'stat', ),
        pids=( 23012, 24678, ),
    )

    res.read()

    data = res.normalize()
    pprint.pprint(data)
```

### proc and sys filesystems have different root

    Normally the proc and sys filesystems are rooted at '/'. In some cases
    such as inside a docker container they may have been mapped in at a 
    different location. An example is shown in the alpineapi container
    where the root is /hostfs.

```python
    #!/usr/bin/env python3
    import pprint
    from lnxproc import Resources

    res = Resources(root='/hostfs')  # will read all resources

    res.read()

    data = res.normalize()
    pprint.pprint(data)
```

## REST APi

    See script buildscripts/test.sh.

    The endpoints are:

         - /keys             # lists available keys
         - /resource         # return json output for all resources and pids
         - /resource/<key>   # return json output e.g. /resource/stat
         - /pid/<pid>/<key>  # return json output for pid e.g. /pid/23012/stat

# Development

    This repo uses docker as an isolation environment. Install:

        - curl
        - make
        - docker-ce
        - docker-compose 

    To make:

        make

    To make changes, edit files and execute:

        make unittest

    For other make targets see buildscripts/README.md

'''
Contains Collection of ReadFile objects

'''
from ast import literal_eval
from collections import namedtuple
from concurrent.futures import ThreadPoolExecutor
from glob import iglob
from importlib import import_module
from itertools import chain
from json import dumps
from logging import getLogger
import operator
from os import path as ospath
import sys
from time import time

from .readfile import DEFAULT_ROOT


SUBDIR = 'lnxproc'  # ospath.dirname(__file__)
PIDROOT = 'proc'
LOGGER = getLogger(__name__)


# Construct manifests
ATTR = namedtuple('module', ['module', 'file'])


def __gen_manifest(classes):
    '''
    Generate a dictionary of modules KEYS vs a namedtuple
    containing attributes for file and class name

    :param classes: iterable of classes
    '''
    manifest = {}
    for i in classes:
        key = i.lower()
        LOGGER.debug("key %s", key)
        module = import_module('%s.%s' % (SUBDIR, key, ))
        mod = getattr(module, i)
        LOGGER.debug("mod %s", mod)
        filename = operator.attrgetter('%s.FILENAME' % (i, ))(module)

        LOGGER.debug("filename %s", filename)
        manifest[key] = ATTR(mod, filename)

    return manifest


MODULES = (
    'Cgroups',
    'Cpufreq',
    'Cpuinfo',
    'Diskstats',
    'DomainName',
    'HostName',
    'Interrupts',
    'Loadavg',
    'Meminfo',
    'NetArp',
    'NetDev',
    'NetRpcNfs',
    'NetRpcNfsd',
    'NetSnmp',
    'OSrelease',
    'Partitions',
    'Schedstat',
    'Stat',
    'Uptime',
    'VMstat',
)
MANIFEST = __gen_manifest(MODULES)

PIDMODULES = (
    'PidCmdline',
    'PidEnviron',
    'PidFd',
    'PidIo',
    'PidSched',
    'PidSchedStat',
    'PidSmaps',
    'PidStatm',
    'PidStat',
    'PidStatus',
)
PIDMANIFEST = __gen_manifest(PIDMODULES)


def get_keys():
    '''
    Get the available keys as a list of dicts
    Returns an iterator that returns tuples
    '''
    LOGGER.debug("get_keys")
    return (
        (i, j.file) for i, j in sorted(
            chain(
                MANIFEST.items(),
                PIDMANIFEST.items(),
            ),
        )
    )


def show_keys(fhandle=sys.stdout):
    '''
    Shows the list of keys that are available

    :param fhandle: optional file descriptor
               (default is stdout)
    '''
    fhandle.write("Lnxproc - available keys\n")
    fhandle.write("========================\n")
    fhandle.write("\n")
    fhandle.write("Main modules:\n")
    fhandle.write("\n")
    for i, j in sorted(MANIFEST.items()):
        fhandle.write("    ")
        fhandle.write(i)
        fhandle.write(" -> ")
        fhandle.write(j.file or 'unknown')
        fhandle.write("\n")

    fhandle.write("\n")
    fhandle.write("PID modules:\n")
    fhandle.write("\n")
    for i, j in sorted(PIDMANIFEST.items()):
        fhandle.write("    ")
        fhandle.write(i)
        fhandle.write(" -> ")
        fhandle.write(j.file or 'unknown')
        fhandle.write("\n")

    fhandle.write("\n")


def json_streamer(data):
    '''
    Converts dict to streamed JSON
    '''
    try:
        iterator = data.__iter__()

    except AttributeError:
        yield "{}"
        return

    try:
        key = next(iterator)
    except StopIteration:
        yield "{}"
        return

    yield '{"%s": %s' % (key, dumps(data[key]), )
    for key in iterator:
        yield ',"%s": %s' % (key, dumps(data[key]), )

    yield '}'


class Resources(list):
    '''
    Handle collection of ReadFile objects
    '''

    def __init__(self, keys=None, pids=None, root=None):
        '''Instantiate ReadFile object

        :param keys: list of object keys
        :param pids: list of optional pids
        '''
        super().__init__()
        root = root or DEFAULT_ROOT

        if keys is None:
            keys = chain(
                MANIFEST.keys(),
                PIDMANIFEST.keys(),
            )

            if pids is None:
                pids = (
                    literal_eval(
                        ospath.split(i)[1]
                    ) for i in iglob(ospath.join(root, PIDROOT, '[1-9]*'))
                )

        LOGGER.debug("keys are %s", keys)
        LOGGER.debug("pids are %s", pids)

        unused = []
        for key in keys:
            try:
                self.append(MANIFEST[key].module(root=root))

            except KeyError:
                unused.append(key)

        if pids:
            for pid in pids:
                pidunused = []
                for key in unused:
                    try:
                        self.append(
                            PIDMANIFEST[key].module(pid=pid, root=root),
                        )

                    except KeyError:
                        pidunused.append(key)

                if pidunused:
                    LOGGER.error("Unknown pid classes specified %s", pidunused)

        else:
            if unused:
                LOGGER.error("Unknown classes specified %s", unused)

        LOGGER.debug("full list is %s", self)
        self.timestamp = None
        self.key = 'resources'

    def read(self):
        '''
        Read data for all keys
        '''
        LOGGER.debug("Read")
        self.timestamp = time()
        if len(self) > 2:
            with ThreadPoolExecutor() as executor:
                for obj in self:
                    executor.submit(obj.read)

        else:
            for obj in self:
                obj.read()

    def normalize(self):
        '''
        Translates data into dictionary

        :return: dictionary of values
        '''
        LOGGER.debug("Normalize")
        ret = {'timestamp': self.timestamp, }
        for obj in self:
            if obj.pid is not None:
                try:
                    rpid = ret[obj.pid]

                except KeyError:
                    rpid = ret[obj.pid] = {}

                rpid[obj.KEY] = obj.normalize()

            else:
                ret[obj.KEY] = obj.normalize()

        return ret

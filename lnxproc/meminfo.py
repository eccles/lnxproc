'''
Contains the Meminfo() class from lnxproc package

Typical contents of /proc/meminfo file::

    MemTotal:       16417184 kB
    MemFree:         6953536 kB
    Buffers:         1583044 kB
    Cached:          3329384 kB
    SwapCached:            0 kB
    Active:          3720620 kB
    Inactive:        3373920 kB
    Active(anon):    2191844 kB
    Inactive(anon):    10452 kB
    Active(file):    1528776 kB
    Inactive(file):  3363468 kB
    Unevictable:       31344 kB
    Mlocked:           31348 kB
    SwapTotal:       2097148 kB
    SwapFree:        2097148 kB
    Dirty:               120 kB
    Writeback:             0 kB
    AnonPages:       2213456 kB
    Mapped:           303892 kB
    Shmem:             14368 kB
    Slab:            2098116 kB
    SReclaimable:    2044032 kB
    SUnreclaim:        54084 kB
    KernelStack:        6488 kB
    PageTables:        55788 kB
    NFS_Unstable:          0 kB
    Bounce:                0 kB
    WritebackTmp:          0 kB
    CommitLimit:    10305740 kB
    Committed_AS:    7521484 kB
    VmallocTotal:   34359738367 kB
    VmallocUsed:      338868 kB
    VmallocChunk:   34359383548 kB
    HardwareCorrupted:     0 kB
    AnonHugePages:         0 kB
    HugePages_Total:       0
    HugePages_Free:        0
    HugePages_Rsvd:        0
    HugePages_Surp:        0
    Hugepagesize:       2048 kB
    DirectMap4k:      208896 kB
    DirectMap2M:    15503360 kB

.. note::
   The units field is **not** read. This class **assumes** that all
   measurements are in KiB (except for the HugePages.. fields which are counts)

'''
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class Meminfo(ReadFile):
    '''
    Meminfo handling
    '''
    FILENAME = ospath.join('proc', 'meminfo')
    KEY = 'meminfo'

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        for line in lines:
            top, tail = line.strip().split(':')
            val = tail.strip().split()[0]
            key = top.strip()
            ret[key] = int(val)

        return ret

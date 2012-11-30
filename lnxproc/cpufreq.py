'''Contains CpuFreq() class

   Reads the file /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq

.. note::
   This class is **cached**. The file is only read **once**. Subsequent reads
   return the first value read

'''
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile


LOGGER = getLogger(__name__)


class Cpufreq(ReadFile):
    '''
    Cpufreq handling
    '''
    FILENAME = ospath.join(
        'sys',
        'devices', 'system', 'cpu', 'cpu0', 'cpufreq', 'scaling_max_freq'
    )
    KEY = 'cpufreq'
    CACHED = True

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        try:
            ret = int(self.lines[0].strip())

        except IndexError:
            ret = None

        return ret

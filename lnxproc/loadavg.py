'''
Contains the ProcLoadavg() class from lnxproc package

Typical contents of /proc/loadavg::

    0.26 0.39 0.40 1/898 21328

This is the order of metrics in /proc/loadavg::

    load1 - average runnable/total tasks for last minute
    load5 - average runnable/total tasks for last 5 minutes
    load15 - average runnable/total tasks for last 15 minutes
    runnable/total tasks in system
    pid of most recently craeted process

'''
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class Loadavg(ReadFile):
    '''
    Loadavg handling
    '''
    FILENAME = ospath.join('proc', 'loadavg')
    KEY = 'loadavg'

    FIELDS = (
        'Load1', 'Load5', 'Load15',
        'Run/Total', 'Pid',
    )

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        vals = lines[0].split()
        ret = dict(zip(self.FIELDS, vals))

        if 'Pid' in ret:
            ret['Pid'] = int(ret['Pid'])

        for field in ('Load1', 'Load5', 'Load15'):
            if field in ret:
                ret[field] = float(ret[field].split()[0])

        if 'Run/Total' in ret:
            vals = ret['Run/Total'].split('/')
            ret['Run'] = int(vals[0])
            ret['Total'] = int(vals[1])

        return ret

'''
Contains PidStatus() class

Typical contents of /proc/<pid>/status file::

   Name:   vmware-vmx
   State:  S (sleeping)
   SleepAVG:       98%
   Tgid:   4927
   Pid:    4927
   PPid:   1
   TracerPid:      0
   Uid:    35513   35513   0       35513
   Gid:    35513   35513   35513   35513
   FDSize: 512
   Groups: 40 402 544 1033 8959 35513
   VmPeak:  1563564 kB
   VmSize:  1494016 kB
   VmLck:      3992 kB
   VmHWM:   1245892 kB
   VmRSS:   1243436 kB
   VmData:  1224636 kB
   VmStk:       304 kB
   VmExe:      6784 kB
   VmLib:     39208 kB
   VmPTE:      2796 kB
   StaBrk: 1f721000 kB
   Brk:    20950000 kB
   StaStk: 7fff11f7d410 kB
   Threads:        22
   SigQ:   0/30708
   SigPnd: 0000000000000000
   ShdPnd: 0000000000000000
   SigBlk: 0000000000000000
   SigIgn: 0000000000301000
   SigCgt: 0000000193c9eeef
   CapInh: 0000000000000000
   CapPrm: 00000000fffffeff
   CapEff: 0000000000000000
   Cpus_allowed:   00000000,00000000,00000000,00000000,00000000,00000000,
                   00000000,0000000f
   Mems_allowed:   00000000,00000001

'''
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class PidStatus(ReadFile):
    '''
    PidStatus handling
    '''
    FILENAME = ospath.join('proc', '%s', 'status')
    KEY = 'pidstatus'

    def normalize(self):
        '''
        Translates data into dictionary

        The <pid>/status file is a number of records keyed on ':' separator
        LOGGER.debug("Normalize")'''

        ret = {}
        lines = self.lines
        if not lines:
            return ret

        for line in lines:
            top, tail = line.split(':', 1)
            ret[top.strip()] = tail.strip()

        ret.update(
            dict(
                zip(
                    ('Uid', 'Euid', 'Suid', 'Fuid'),
                    (int(v) for v in ret['Uid'].split('\t'))
                )
            )
        )

        ret.update(
            dict(
                zip(
                    ('Gid', 'Egid', 'Sgid', 'Fgid'),
                    (int(v) for v in ret['Gid'].split('\t'))
                )
            )
        )

        if 'Groups' in ret:
            ret['Groups'] = [int(v) for v in ret['Groups'].split()]

        if 'Mems_allowed' in ret:
            ret['Mems_allowed'] = ret['Mems_allowed'].split(',')

        for field in ('VmData', 'VmExe', 'VmHWM', 'VmLck', 'VmLib', 'VmPTE',
                      'VmPeak', 'VmPin', 'VmRSS', 'VmSize', 'VmStk',
                      'VmSwap'):
            if field in ret:
                ret[field] = int(ret[field].split()[0])

        for field in ('FDSize', 'Threads', 'nonvoluntary_ctxt_switches',
                      'voluntary_ctxt_switches'):
            if field in ret:
                ret[field] = int(ret[field])

        for field in ('PPid', 'Pid', 'Tgid', 'TracerPid'):
            if field in ret:
                ret[field] = int(ret[field])

        return ret

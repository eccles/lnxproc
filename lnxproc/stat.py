'''
Contains Stat() class

Typical contents of /proc/stat file::

   cpu  82723 122 17407 12631174 285947 0 1668 0 0 0
   cpu0 16016 0 3504 1560778 44700 0 347 0 0 0
   cpu1 16360 58 3212 1564796 41154 0 418 0 0 0
   cpu2 15945 57 3731 1563965 40662 0 540 0 0 0
   cpu3 15947 0 3780 1552644 53254 0 334 0 0 0
   cpu4 3094 0 704 1609983 15409 0 7 0 0 0
   cpu5 5553 3 891 1584979 37961 0 5 0 0 0
   cpu6 4632 0 724 1612517 11178 0 5 0 0 0
   cpu7 5174 2 859 1581510 41625 0 9 0 0 0
   intr 3305490 43 3 0 0 0 0 0 0 1 0 0 0 0 0 0 0 182350 862 0 0 0 0 0 142227 0
     0 0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 264216 670299 60254 12 901 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
     0 0
     0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
   ctxt 13940623
   btime 1355226547
   processes 8900
   procs_running 2
   procs_blocked 3
   softirq 2629775 0 516614 3878 62118 488556 0 240324 545086 2530 770669

Description::

       kernel/system statistics.  Varies with architecture.  Common entries
       include:

       cpu  3357 0 4313 1362393
              The amount of time, measured in units of USER_HZ (1/100ths of a
              second on most architectures, use sysconf(_SC_CLK_TCK)  to
              obtain the right value), that the system spent in user mode, user
              mode with low priority (nice), system mode, and the idle
              task, respectively.  The last value should be USER_HZ times the
              second entry in the uptime pseudo-file.

              In Linux 2.6 this line includes three additional columns: iowait\
              time waiting for I/O to complete (since 2.5.41); irq  -
              time servicing interrupts (since 2.6.0-test4); softirq - time
              servicing softirqs (since 2.6.0-test4).

              Since  Linux  2.6.11,  there  is an eighth column, steal - stolen
              time, which is the time spent in other operating systems
              when running in a virtualized environment

              Since Linux 2.6.24, there is a ninth column, guest, which is the
              time spent running a virtual CPU for guest operating sys
              tems under the control of the Linux kernel.

       page 5741 1808
              The number of pages the system paged in and the number that were
              paged out (from disk).

       swap 1 0
              The number of swap pages that have been brought in and out.

       intr 1462898
              This line shows counts of interrupts serviced since boot time,
              for each of the possible system interrupts.  The first col
              umn is the total of all interrupts serviced; each subsequent
              column is the total for a particular interrupt.

       disk_io: (2,0):(31,30,5764,1,2) (3,0):...
              (major,disk_idx):(noinfo, read_io_ops, blks_read, write_io_ops,
              blks_written)
              (Linux 2.4 only)

       ctxt 115315
              The number of context switches that the system underwent.

       btime 769041601
              boot time, in seconds since the Epoch,
              1970-01-01 00:00:00 +0000 (UTC).

       processes 86031
              Number of forks since boot.

       procs_running 6
              Number of processes in runnable state.  (Linux 2.5.45 onward.)

       procs_blocked 2
              Number of processes blocked waiting for I/O to complete.
              (Linux 2.5.45 onward.)

'''
from logging import getLogger
from os import path as ospath
import re

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class Stat(ReadFile):
    '''
    Stat handling
    '''
    FILENAME = ospath.join('proc', 'stat')
    KEY = 'stat'
    FIELDS = {
        'cpu': (
            'user', 'nice', 'sys', 'idle',
            'iowait', 'irq', 'softirq', 'steal',
            'virtual', 'unknown'
        ),
        'page': ('in', 'out'),
        'swap': ('in', 'out'),
    }

    REGEX = re.compile(r'^cpu*')
    REGEX1 = re.compile(r'^page|^swap')
    REGEX2 = re.compile(
        r'^ctxt|^btime|^procs_running|^procs_blocked|^processes'
    )

    def normalize(self):
        '''
        Translates data into dictionary

        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}

        for line in lines:
            fields = line.split()
            key = fields[0].lstrip()
            vals = fields[1:]
            if self.REGEX.match(key):
                ret[key] = dict(
                    zip(
                        self.FIELDS['cpu'],
                        [int(val) for val in vals]
                    )
                )

            elif self.REGEX1.match(key):
                ret[key] = dict(
                    zip(
                        self.FIELDS[key],
                        [int(v) for v in vals]
                    )
                )

            elif self.REGEX2.match(key):
                ret[key] = int(vals[0])
            else:
                ret[key] = [int(v) for v in vals]

        return ret

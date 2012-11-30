'''
Contains PidStat() class

Typical contents of file /proc/<pid>/stat (one line)::

   3405 (httpd) S 1 3405 3405 0 -1 4202816 14491 0 762 0 15 4 0 0 18 0 2 0 7048
   441008128 15350 18446744073709551615 1 1 0 0 0 0 0 16781440 134235755
   18446744073709551615 0 0 17 3 0 0 304

Description::

  0 pid %d The process ID.
  1 comm %s The filename of the executable, in parentheses.  This is visible
    whether or not the executable is swapped out.
  2 state %c One character from the string "RSDZTW" where R is running, S is
    sleeping in an interruptible wait,  D  is  waiting  in  uninterruptible
    disk sleep, Z is zombie, T is traced or stopped (on a signal), and W is
    paging.
  3 ppid %d The PID of the parent.
  4 pgrp %d The process group ID of the process.
  5 session %d The session ID of the process.
  6 tty_nr %d The tty the process uses.
  7 tpgid %d The process group ID of the process which currently owns the tty
    that the process is connected to.
  8 flags %lu The kernel flags word of the process. For bit meanings, see the
    PF_* defines in <linux/sched.h>.  Details depend on the kernel version.
  9 minflt %lu The number of minor faults the process has made which have not
    required loading a memory page from disk.
 10 cminflt %lu The number of minor faults that the process's waited-for
    children have made.
 11 majflt %lu The number of major faults the process has made which have
    required loading a memory page from disk.
 12 cmajflt %lu The number of major faults that the process's waited-for
    children have made.
 13 utime %lu The number of jiffies that this process has been scheduled in
    user mode.
 14 stime %lu The number of jiffies that this process has been scheduled in
    kernel mode.
 15 cutime %ld The number of jiffies that this process's waited-for children
    have been scheduled in user mode. (See also times(2).)
 16 cstime %ld The number of jiffies that this process's waited-for children
    have been scheduled in kernel mode.
 17 priority %ld (Explanation  for  Linux  2.6)
 18 nice %ld The nice value ranges from 19 (nicest) to -19 (not nice to
    others).
 19 num_threads %ld Number of threads in this process (since Linux 2.6).
    Before kernel 2.6, this field was hard coded to 0 as a placeholder for an
    earlier removed field.
 20 itrealvalue %ld The time in jiffies before the next SIGALRM is sent to the
    process due to an interval timer.
 21 starttime %lu The time in jiffies the process started after system boot.
 22 vsize %lu Virtual memory size in bytes.
 23 rss %ld Resident  Set  Size:  number of pages the process has in real
    memory, minus 3 for administrative purposes. This is just the pages which
    count towards text, data, or stack space. This does not include pages
    which have not been demand-loaded in, or which are swapped out.
 24 rlim %lu Current limit in bytes on the rss of the process
    (usually 4294967295 on i386).
 25 startcode %lu The address above which program text can run.
 26 endcode %lu The address below which program text can run.
 27 startstack %lu The address of the start of the stack.
 28 kstkesp %lu The current value of esp (stack pointer), as found in the
    kernel stack page for the process.
 29 kstkeip %lu The current EIP (instruction pointer).
 30 signal %lu The bitmap of pending signals.
 31 blocked %lu The bitmap of blocked signals.
 32 sigignore %lu The bitmap of ignored signals.
 33 sigcatch %lu The bitmap of caught signals.
 34 wchan %lu This is the "channel" in which the process is waiting. It is the
    address of a system call, and can be looked up in a namelist if you need a
    textual name.  (If you have an up-to-date /etc/psdatabase, then try ps -l
    to see the WCHAN field in action.)
 35 nswap %lu Number of pages swapped (not maintained).
 36 cnswap %lu Cumulative nswap for child processes (not maintained).
 37 exit_signal %d Signal to be sent to parent when we die.
 38 processor %d CPU number last executed on.
 39 rt_priority %lu (since kernel 2.5.19) Real-time scheduling priority (see
    sched_setscheduler(2)).
 40 policy %lu (since kernel 2.5.19) Scheduling policy (see
    sched_setscheduler(2)).
 41 delayacct_blkio_ticks %llu (since Linux 2.6.18) Aggregated block I/O
    delays, measured in clock ticks (centiseconds).
 42 guest_time %lu (since Linux 2.6.24) Guest time of the process (time spent
    running a virtual CPU for a guest operating system), measured in clock
    ticks (divide by sysconf(_SC_CLK_TCK).
 43 cguest_time %ld (since Linux 2.6.24) Guest time of the process's children,
    measured in clock ticks (divide by sysconf(_SC_CLK_TCK).

.. note::
   The no. of fields varies with kernel version. This code will read all fields
   to 'cguest_time' as documented in the man pages. However the kernel used for
   testing contained a number of unknown extra fields. Older kernels will only
   return a dictionary with fewer fields. The assumption is that newer kernels
   will never delete any fields from previous versions.

'''
############################################################################

from itertools import islice
from logging import getLogger
from os import sysconf, path as ospath
import re

from .readfile import ReadFile

PAGE_SIZE = sysconf('SC_PAGE_SIZE') // 1024
JIFFIES_PER_SEC = sysconf('SC_CLK_TCK')
SECS_PER_JIFFY = 1.0 / JIFFIES_PER_SEC
SPLIT = re.compile(r'(\d+)\s+\((.*)\)\s+(\w+)\s+(.*)')
LOGGER = getLogger(__name__)


class PidStat(ReadFile):
    '''
    PidStat handling
    '''
    FILENAME = ospath.join('proc', '%s', 'stat')
    KEY = 'pidstat'
    FIELDS = ('pid', 'comm', 'state', 'ppid',
              'pgrp', 'session', 'tty_nr', 'tpgid',
              'flags', 'minflt', 'cminflt', 'majflt',
              'cmajflt', 'utime', 'stime', 'cutime',
              'cstime', 'priority', 'nice', 'num_threads',
              'itrealvalue', 'starttime', 'vsize', 'rss',
              'rlim', 'startcode', 'endcode', 'startstack',
              'kstkesp', 'kstkeip', 'signal', 'blocked',
              'sigignore', 'sigcatch', 'wchan', 'nswap',
              'cnswap', 'exit_signal', 'processor',
              'rt_priority', 'policy', 'delay_blkio_ticks',
              'guest_time', 'cguest_time')

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        if not lines:
            return ret

        extract = SPLIT.match(lines[0])
        if not extract:
            return extract

        vals = extract.group(4)

        ret = dict(zip(islice(self.FIELDS, 3, None),
                       (int(val) for val in vals.split())))

        ret[self.FIELDS[0]] = int(extract.group(1))
        ret[self.FIELDS[1]] = extract.group(2)
        ret[self.FIELDS[2]] = extract.group(3)

        for timefield in ('utime', 'stime', 'cutime', 'cstime', 'starttime',
                          'itrealvalue', 'guest_time', 'cguest_time'):
            ret[timefield] *= SECS_PER_JIFFY

        ret['vsize'] /= 1024
        ret['rss'] *= PAGE_SIZE
        ret['nswap'] *= PAGE_SIZE
        ret['cnswap'] *= PAGE_SIZE
        ret['rlim'] //= 1024
        ret['delay_blkio_ticks'] *= 1000000

        return ret

'''
Contains PidSched() class

Typical contents of /proc/<pid>/sched file::

    systemd (1, #threads: 1)
    -------------------------------------------------------------------
    se.exec_start                                :     358725809.619232
    se.vruntime                                  :          2395.646673
    se.sum_exec_runtime                          :          5829.343469
    se.statistics.sum_sleep_runtime              :     358719820.680319
    se.statistics.wait_start                     :             0.000000
    se.statistics.sleep_start                    :     358725809.619232
    se.statistics.block_start                    :             0.000000
    se.statistics.sleep_max                      :         51862.314922
    se.statistics.block_max                      :          3891.718500
    se.statistics.exec_max                       :            19.405697
    se.statistics.slice_max                      :             4.079684
    se.statistics.wait_max                       :            20.056644
    se.statistics.wait_sum                       :           120.098492
    se.statistics.wait_count                     :                18691
    se.statistics.iowait_sum                     :           171.770362
    se.statistics.iowait_count                   :                  284
    se.nr_migrations                             :                 4389
    se.statistics.nr_migrations_cold             :                    0
    se.statistics.nr_failed_migrations_affine    :                    0
    se.statistics.nr_failed_migrations_running   :                  889
    se.statistics.nr_failed_migrations_hot       :                   67
    se.statistics.nr_forced_migrations           :                    2
    se.statistics.nr_wakeups                     :                18209
    se.statistics.nr_wakeups_sync                :                  915
    se.statistics.nr_wakeups_migrate             :                 4329
    se.statistics.nr_wakeups_local               :                 1192
    se.statistics.nr_wakeups_remote              :                17017
    se.statistics.nr_wakeups_affine              :                14128
    se.statistics.nr_wakeups_affine_attempts     :                14879
    se.statistics.nr_wakeups_passive             :                    0
    se.statistics.nr_wakeups_idle                :                    0
    avg_atom                                     :             0.312884
    avg_per_cpu                                  :             1.328171
    nr_switches                                  :                18631
    nr_voluntary_switches                        :                18206
    nr_involuntary_switches                      :                  425
    se.load.weight                               :                 1024
    se.avg.load_sum                              :               132637
    se.avg.util_sum                              :               132637
    se.avg.load_avg                              :                    2
    se.avg.util_avg                              :                    2
    se.avg.last_update_time                      :      358725809619232
    policy                                       :                    0
    prio                                         :                  120
    clock-delta                                  :                   28
    mm->numa_scan_seq                            :                    0
    numa_pages_migrated                          :                    0
    numa_preferred_nid                           :                   -1
    total_numa_faults                            :                    0
    current_node=0, numa_group_id=0
    numa_faults node=0 task_private=0 task_shared=0 group_private=0

'''

from ast import literal_eval
from itertools import islice
from logging import getLogger
from os import path as ospath
import re

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class PidSched(ReadFile):
    '''
    PidSched handling
    '''
    FILENAME = ospath.join('proc', '%s', 'sched')
    KEY = 'pidsched'

    REGEX = re.compile(r'(\w*)\s+\((\d+),\s+#(.*):\s+(\d+)\)')
    REGEX2 = re.compile(r'([a-z_]+)=(\d+)')

    def normalize(self):
        '''
        Translates data into dictionary

        The <pid>/sched file is a number of records keyed on ':' separator
        '''
        LOGGER.debug("Normalize")
        ret = {}
        lines = self.lines
        if not lines:
            return ret

        i = self.REGEX.match(lines[0])
        if i:
            ret['name'] = i.group(1)
            ret['pid'] = literal_eval(i.group(2))
            key = i.group(3)
            ret[key] = literal_eval(i.group(4))

        for line in islice(lines, 2, None):
            try:
                top, tail = line.split(':', 1)

            except ValueError:
                if line.startswith('numa_faults'):
                    ret.update(
                        dict(
                            ('numa_faults_%s' % (k, ), literal_eval(v))
                            for k, v in re.findall(self.REGEX2, line)
                        )
                    )

                else:
                    ret.update(
                        dict(
                            ('numa_%s' % (k, ), literal_eval(v))
                            for k, v in re.findall(self.REGEX2, line)
                        )
                    )

            else:
                ret[top.strip()] = literal_eval(tail.strip())

        return ret

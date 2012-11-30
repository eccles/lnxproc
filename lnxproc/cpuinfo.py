'''
Contains Cpuinfo() class from lnxproc package

typical contents of /proc/cpuinfo file::

   processor    : 0
   vendor_id    : GenuineIntel
   cpu family    : 6
   model        : 42
   model name    : Intel(R) Core(TM) i7-2600 CPU @ 3.40GHz
   stepping    : 7
   microcode    : 0x25
   cpu MHz        : 1600.000
   cache size    : 8192 KB
   physical id    : 0
   siblings    : 8
   core id        : 0
   cpu cores    : 4
   apicid        : 0
   initial apicid    : 0
   fpu        : yes
   fpu_exception    : yes
   cpuid level    : 13
   wp        : yes
   flags        : fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov
   pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx rdtscp
   lm constant_tsc arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc
   aperfmperf pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 cx16
   xtpr pdcm pcid sse4_1 sse4_2 x2apic popcnt tsc_deadline_timer aes xsave avx
   lahf_lm ida arat epb xsaveopt pln pts dtherm tpr_shadow vnmi flexpriority
   ept vpid
   bogomips    : 6784.47
   clflush size    : 64
   cache_alignment    : 64
   address sizes    : 36 bits physical, 48 bits virtual
   power management:

and repeat for all cores.....

'''
from logging import getLogger
from os import path as ospath
import re

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class Cpuinfo(ReadFile):
    '''
    Cpuinfo handling
    '''
    FILENAME = ospath.join('proc', 'cpuinfo')
    KEY = 'cpuinfo'

    RE1 = re.compile('^processor')
    RE2 = re.compile('^[a-zA-Z]')

    def normalize(self):

        LOGGER.debug("Normalize")
        data = {}
        for line in self.lines:
            if self.RE1.match(line):
                proc = "CPU%s" % (line.split(':')[1].strip())
                dataproc = data[proc] = {}
            else:
                if self.RE2.match(line):
                    kfield, vals = line.split(':')
                    dataproc[kfield.strip()] = self.convert(vals)

        for i in data.values():
            i['flags'] = tuple(i['flags'].split())
            i['cache size'] = self.convert(i['cache size'].split()[0])

        return data

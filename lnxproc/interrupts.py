'''
Contains the Interrupts() class

This is the order of metrics in /proc/interrupts::

           CPU0  ... CPU7
     0:         43         0   IO-APIC-edge      timer
     1:          3         0   IO-APIC-edge      i8042
     8:          1         0   IO-APIC-edge      rtc0
     9:          0         0   IO-APIC-fasteoi   acpi
    16:    4666410         0   IO-APIC-fasteoi   ehci_hcd:usb1, nvidia
    17:      21643         0   IO-APIC-fasteoi   ahci, snd_hda_intel
    23:   40934142         0   IO-APIC-fasteoi   ehci_hcd:usb2
    40:          0         0   PCI-MSI-edge      PCIe PME
    41:          0         0   PCI-MSI-edge      PCIe PME
    42:          0         0   PCI-MSI-edge      PCIe PME
    43:          0         0   PCI-MSI-edge      PCIe PME
    44:          0         0   PCI-MSI-edge      PCIe PME
    45:    1082598         0   PCI-MSI-edge      ahci
    46:         28         0   PCI-MSI-edge      xhci_hcd
    47:    2963902         0   PCI-MSI-edge      eth0
    48:         12         0   PCI-MSI-edge      mei
    49:        893         0   PCI-MSI-edge      snd_hda_intel
   NMI:         46        10   Non-maskable interrupts
   LOC:  109459673  33192085   Local timer interrupts
   SPU:          0         0   Spurious interrupts
   PMI:         46        10   Performance monitoring interrupts
   IWI:          0         0   IRQ work interrupts
   RTR:          7         0   APIC ICR read retries
   RES:   12875462     93615   Rescheduling interrupts
   CAL:     110037     79717   Function call interrupts
   TLB:     422148    130709   TLB shootdowns
   TRM:          0         0   Thermal event interrupts
   THR:          0         0   Threshold APIC interrupts
   MCE:          0         0   Machine check exceptions
   MCP:       1421      1421   Machine check polls
   ERR:          0
   MIS:          0

'''

from itertools import islice
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class Interrupts(ReadFile):
    '''
    Interrupts handling
    '''
    FILENAME = ospath.join('proc', 'interrupts')
    KEY = 'interrupts'

    def __init__(self, **kwargs):
        '''
        Instantiate ReadFile object
        '''
        super().__init__(**kwargs)
        self.cpulist = None

    def normalize(self):
        '''
        Translates data into dictionary
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        self.cpulist = lines[0].strip().split()

        for cpu in self.cpulist:
            ret[cpu] = {}

        for line in islice(lines, 1, None):
            head = line.strip().split(':', 1)
            key = str(head[0].strip())
            vals = head[1].split()
            for i, val in enumerate(islice(vals, len(self.cpulist))):
                ret[self.cpulist[i]][key] = int(val)

        return ret

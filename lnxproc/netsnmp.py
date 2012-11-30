'''
Contains the NetSnmp() class

Typical contents of file /proc/net/snmp::

  Ip: Forwarding DefaultTTL InReceives InHdrErrors InAddrErrors ForwDatagrams
      InUnknownProtos InDiscards InDelivers OutRequests OutDiscards OutNoRoutes
      ReasmTimeout ReasmReqds ReasmOKs ReasmFails FragOKs FragFails FragCreates
  Ip: 1 64 2354322 0 0 0 0 0 2282006 2066446 0 0 0 0 0 0 0 0 0
  Icmp: InMsgs InErrors InDestUnreachs InTimeExcds InParmProbs InSrcQuenchs
        InRedirects InEchos InEchoReps InTimestamps InTimestampReps InAddrMasks
        InAddrMaskReps OutMsgs OutErrors OutDestUnreachs OutTimeExcds
        OutParmProbs OutSrcQuenchs OutRedirects OutEchos OutEchoReps
        OutTimestamps OutTimestampReps OutAddrMasks OutAddrMaskReps
  Icmp: 172 0 91 0 0 0 0 81 0 0 0 0 0 168 0 87 0 0 0 0 0 81 0 0 0 0
  IcmpMsg: InType3 InType8 OutType0 OutType3
  IcmpMsg: 91 81 81 87
  Tcp: RtoAlgorithm RtoMin RtoMax MaxConn ActiveOpens PassiveOpens AttemptFails
       EstabResets CurrEstab InSegs OutSegs RetransSegs InErrs OutRsts
  Tcp: 1 200 120000 -1 70054 4198 337 2847 43 1880045 1741596 7213 0 3044
  Udp: InDatagrams NoPorts InErrors OutDatagrams RcvbufErrors SndbufErrors
  Udp: 344291 8 376 317708 0 0
  UdpLite: InDatagrams NoPorts InErrors OutDatagrams RcvbufErrors SndbufErrors
  UdpLite: 0 0 0 0 0 0
'''
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class NetSnmp(ReadFile):
    '''
    NetSnmp handling
    '''
    FILENAME = ospath.join('proc', 'net', 'snmp')
    KEY = 'netsnmp'

    def normalize(self):
        '''
        Translates data into dictionary

        The net/snmp file is a series of records keyed on subcategories
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}

        fkey = ''
        fvals = []
        for i, line in enumerate(lines):
            top, tail = line.split(':')
            key = top.lstrip()
            vals = tail.lstrip().split()
            if i % 2:
                if fkey == key:
                    ret[key] = dict(
                        zip(
                            fvals,
                            [int(val) for val in vals]
                        )
                    )
            else:
                fkey = key
                fvals = vals

        return ret

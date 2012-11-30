'''
Contains NetRpcNfs() class

Typical contents of file /proc/net/rpc/nfs::

  net 0 0 0 0
  rpc 0 0 0
  proc2 18 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
  proc3 22 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
  proc4 37 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

'''

from itertools import islice
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class NetRpcNfs(ReadFile):
    '''
    NetRpcNfs handling
    '''
    FILENAME = ospath.join('proc', 'net', 'rpc', 'nfs')
    KEY = 'netrpcnfs'
    FIELDS = {
        'net': ('packets', 'udp', 'tcp', 'tcpconn', ),
        'rpc': ('calls', 'retrans', 'authrefrsh', ),
        'proc2': (
            'null', 'getattr', 'setattr', 'root',
            'lookup', 'readlink', 'read', 'wrcache',
            'write', 'create', 'remove', 'rename',
            'link', 'symlink', 'mkdir', 'rmdir',
            'readdir', 'fsstat',
        ),
        'proc3': (
            'null', 'getattr', 'setattr', 'lookup',
            'access', 'readlink', 'read', 'write',
            'create', 'mkdir', 'symlink', 'mknod',
            'remove', 'rmdir', 'rename', 'link',
            'readdir', 'readdirplus', 'fsstat', 'fsinfo',
            'pathconf', 'commit',
        ),
        'proc4': (
            'null', 'read', 'write', 'commit',
            'open', 'open_conf', 'open_noat', 'open_dgrd',
            'close', 'setattr', 'fsinfo', 'renew',
            'setclntid', 'confirm', 'lock', 'lockt',
            'locku', 'access', 'getattr', 'lookup',
            'lookup_root', 'remove', 'rename', 'link',
            'symlink', 'create', 'pathconf', 'statfs',
            'readlink', 'readdir', 'server_caps',
            'delegreturn',
            'getacl', 'setacl', 'fs_locations',
            'rel_lkowner',
            'secinfo', 'exchange_id', 'create_ses',
            'destroy_ses', 'sequence', 'get_lease_t',
            'reclaim_comp', 'layoutget', 'getdevinfo',
            'layoutcommit', 'layoutreturn', 'getdevlist',
        ),
    }

    def normalize(self):
        '''
        Translates data into dictionary

        The net/rpc/nfsd file is a series of records keyed on
        subcategories

        The net/nfs file is a series of records keyed on subcategories
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        for line in lines:
            cols = line.split()
            key = cols[0]
            ret[key] = dict(
                zip(
                    self.FIELDS[key],
                    [int(val) for val in islice(cols, 1, None)]
                )
            )
            ret[key]['total'] = sum(ret[key].values())

        return ret

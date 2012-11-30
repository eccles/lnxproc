'''
Contains NetRpcNfsd() class

Typical contents of file /proc/net/rpc/nfsd::

    rc 0 0 1
    fh 0 0 0 0 0
    io 0 0
    th 8 0 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000 0.000
    ra 32 0 0 0 0 0 0 0 0 0 0 0
    net 1 1 0 0
    rpc 1 0 0 0 0
    proc2 18 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    proc3 22 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    proc4 2 0 0
    proc4ops 59 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
             0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0

'''

from ast import literal_eval
from itertools import islice
from logging import getLogger
from os import path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class NetRpcNfsd(ReadFile):
    '''
    NetRpcNfsd handling
    '''
    FILENAME = ospath.join('proc', 'net', 'rpc', 'nfsd')
    KEY = 'netrpcnfsd'
    FIELDS = {
        'net': ('packets', 'udp', 'tcp', 'tcpconn', ),
        'rpc': ('calls', 'badcalls', 'badclnt', 'badauth',
                'xdrcall', ),
        'ra': ('size', 'deep10', 'deep20', 'deep30',
               'deep40', 'deep50', 'deep60', 'deep70',
               'deep80', 'deep90', 'deep100', 'notfound', ),
        'rc': ('hits', 'misses', 'nocache', ),
        'io': ('null', 'compound', ),
        'th': ('threads', 'ntimesmax', 'hist00', 'hist10',
               'hist20', 'hist30', 'hist40', 'hist50',
               'hist60', 'hist70', 'hist80', 'hist90', ),
        'fh': ('lookup', 'anon', 'ncachedir', 'ncachedir',
               'stale', ),
        'proc2': ('null', 'getattr', 'setattr', 'root',
                  'lookup', 'readlink', 'read', 'wrcache',
                  'write', 'create', 'remove', 'rename',
                  'link', 'symlink', 'mkdir', 'rmdir',
                  'readdir', 'fsstat', ),
        'proc3': ('null', 'getattr', 'setattr', 'lookup',
                  'access', 'readlink', 'read', 'write',
                  'create', 'kdir', 'symlink', 'mknod',
                  'remove', 'rmdir', 'rename', 'link',
                  'readdir', 'readdirplus', 'fsstat', 'fsinfo',
                  'pathconf', 'commit', ),
        'proc4': ('null', 'compound', ),
        'proc4ops': ('op0-unused', 'op1-unused', 'op2-future',
                     'access', 'close', 'commit', 'create',
                     'delegpurge', 'delegreturn', 'getattr',
                     'getfh', 'link', 'lock', 'lockt', 'locku',
                     'lookup', 'lookup_root', 'nverify', 'open',
                     'openattr', 'open_conf', 'open_dgrd', 'putfh',
                     'putpubfh', 'putrootfh', 'read', 'readdir',
                     'readlink', 'remove', 'rename', 'renew',
                     'restorefh', 'savefh', 'secinfo', 'setattr',
                     'setcltid', 'setcltidconf', 'verify', 'write',
                     'rellockowner', 'bc_ctl', 'bind_conn',
                     'exchange_id', 'create_ses', 'destroy_ses',
                     'free_stateid', 'getdirdeleg', 'getdevinfo',
                     'getdevlist', 'layoutcommit', 'layoutget',
                     'layoutreturn', 'secinfononam', 'sequence',
                     'set_ssv', 'test_stateid', 'want_deleg',
                     'destroy_clid', 'reclaim_comp', ),
        }

    def normalize(self):
        '''
        Translates data into dictionary

        The net/rpc/nfsd file is a series of records keyed on
        subcategories
        '''
        LOGGER.debug("Normalize")
        lines = self.lines
        ret = {}
        for line in lines:
            if line:
                vals = line.split()
                key = vals[0]
                ret[key] = dict(
                    zip(self.FIELDS[key],
                        [literal_eval(val) for val in islice(vals, 1, None)]))
                ret[key]['total'] = sum(ret[key].values())

        return ret

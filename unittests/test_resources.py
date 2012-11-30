'''
Test Resources()
'''

from io import StringIO

from unittest import TestCase
from unittest.mock import patch

import lnxproc

from .basetestcase import BaseTestCase
from .mockfiles import DATA_DIR, get_show_keys


class TestResources(BaseTestCase):
    '''
    Test Resources class
    '''
    def setUp(self):
        self.root = DATA_DIR

    def tearDown(self):
        self.root = None

    @patch('lnxproc.resources.time')
    def test_resources(self, mytime):
        '''
        Test normal instantiation
        '''
        mytime.return_value = 1.0
        res = lnxproc.resources.Resources(
            keys=('domainname', 'hostname', ),
            root=self.root,
        )

        self.assertEqual(
            len(res),
            2,
            msg='List of modules is incorrect'
        )

        res.read()
        self.assertEqual(
            mytime.call_count,
            1,
            msg='Timestamp not called once'
        )
        self.assertEqual(
            res.timestamp,
            1.0,
            msg='Incorrect timestamp returned'
        )

        self.assertEqual(
            res.normalize(),
            {
                'timestamp': 1.0,
                'domainname': 'world',
                'hostname': 'hawking',
            },
            msg='Incorrect resources returned'
        )

    def test_bad_arg(self):
        '''
        Test instantiation with bad argument
        '''
        res = lnxproc.resources.Resources(
            keys=('zzzdomainname', ),
            root=self.root,
        )
        self.assertEqual(
            len(res),
            0,
            msg='List of modules is incorrect'
        )


class TestResourcesStreaming(TestCase):
    '''
    Test json_streamer
    '''
    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        cls.maxDiff = None

    def test_json_streamer(self):
        '''
        Test streaming of output
        '''
        streamer = lnxproc.resources.json_streamer({
            'timestamp': 3.0,
            'domainname': 'world',
            'hostname': 'hawking',
        })

        self.assertEqual(
            ''.join((k for k in streamer)),
            '{"timestamp": 3.0'
            ',"domainname": "world"'
            ',"hostname": "hawking"'
            '}',
            msg='Incorrect streaming returned'
        )

    def test_json_streamer2(self):
        '''
        Test streaming of output
        '''
        streamer = lnxproc.resources.json_streamer({
            'timestamp': 3.0,
            'key': ['world', 'domination', ],
            'key2': {
                'hawking': 2,
                'feynmann': 'value',
                'einstein': 'value2',
            },
        })

        self.assertEqual(
            ''.join((k for k in streamer)),
            '{"timestamp": 3.0'
            ',"key": ["world", "domination"]'
            ',"key2": {'
            '"hawking": 2,'
            ' "feynmann": "value",'
            ' "einstein": "value2"'
            '}}',
            msg='Incorrect streaming returned'
        )

    def test_json_streamer_no_data(self):
        '''
        Test streaming of output when none
        '''
        streamer = lnxproc.resources.json_streamer(None)
        self.assertEqual(
            ''.join((k for k in streamer)),
            '{}',
            msg='Incorrect streaming returned'
        )

    def test_json_streamer_empty_data(self):
        '''
        Test streaming of output when none
        '''
        streamer = lnxproc.resources.json_streamer({})
        self.assertEqual(
            ''.join((k for k in streamer)),
            '{}',
            msg='Incorrect streaming returned'
        )


class TestResourcesPid(BaseTestCase):
    '''
    Test Resources class when pids are specified
    '''
    def setUp(self):
        self.root = DATA_DIR

    def tearDown(self):
        self.root = None

    @patch('lnxproc.resources.time')
    def test_all_subclass(self, mytime):
        '''
        Test instantiation for all subclasses
        '''
        mytime.return_value = 2.0
        res = lnxproc.resources.Resources(
            keys=('pidcmdline', 'pidenviron', ),
            pids=('1', ),
            root=self.root,
        )
        self.assertEqual(
            len(res),
            2,
            msg="resources list is incorrect"
        )
        res.read()
        self.assertEqual(
            mytime.call_count,
            1,
            msg='Timestamp not called once'
        )
        self.assertEqual(
            res.timestamp,
            2.0,
            msg='Incorrect timestamp returned'
        )
        self.assertEqual(
            res.normalize(),
            {
                '1': {
                    'pidcmdline': [
                        '/sbin/init',
                        'splash',
                    ],
                    'pidenviron': {
                        'BOOT_IMAGE': '/vmlinuz-4.4.0-36-generic.efi.signed',
                        'HOME': '/',
                        'PATH': '/sbin:/usr/sbin:/bin:/usr/bin',
                        'PWD': '/',
                        'TERM': 'linux',
                        'drop_caps': '',
                        'init': '/sbin/init',
                        'recovery': '',
                        'rootmnt': '/root',
                    },
                },
                'timestamp': 2.0,
            },
            msg='Incorrect resources returned'
        )

    def test_pid_unused_subclass(self):
        '''
        Test instantiation for pid subclasses
        '''
        res = lnxproc.resources.Resources(
            keys=('key1', 'key4', ),
            pids=(1, ),
            root=self.root,
        )
        self.assertEqual(
            len(res),
            0,
            msg="resources list is incorrect"
        )


CPUFREQ_VALUE = 'sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq'


class TestResourcesKeys(TestCase):
    '''
    Test Resources {get,showi}_keys utility function
    '''
    @classmethod
    def setUpClass(cls):
        cls.longMessage = True
        cls.maxDiff = None

    def test_get_keys(self):
        '''
        Test get_keys function
        '''
        self.assertEqual(
            list(lnxproc.resources.get_keys()),
            [
                ('cgroups', 'proc/cgroups'),
                ('cpufreq', 'sys/devices/system/cpu/cpu0/cpufreq/'
                            'scaling_max_freq'),
                ('cpuinfo', 'proc/cpuinfo'),
                ('diskstats', 'proc/diskstats'),
                ('domainname', 'proc/sys/kernel/domainname'),
                ('hostname', 'proc/sys/kernel/hostname'),
                ('interrupts', 'proc/interrupts'),
                ('loadavg', 'proc/loadavg'),
                ('meminfo', 'proc/meminfo'),
                ('netarp', 'proc/net/arp'),
                ('netdev', 'proc/net/dev'),
                ('netrpcnfs', 'proc/net/rpc/nfs'),
                ('netrpcnfsd', 'proc/net/rpc/nfsd'),
                ('netsnmp', 'proc/net/snmp'),
                ('osrelease', 'proc/sys/kernel/osrelease'),
                ('partitions', 'proc/partitions'),
                ('pidcmdline', 'proc/%s/cmdline'),
                ('pidenviron', 'proc/%s/environ'),
                ('pidfd', 'proc/%s/fd'),
                ('pidio', 'proc/%s/io'),
                ('pidsched', 'proc/%s/sched'),
                ('pidschedstat', 'proc/%s/schedstat'),
                ('pidsmaps', 'proc/%s/smaps'),
                ('pidstat', 'proc/%s/stat'),
                ('pidstatm', 'proc/%s/statm'),
                ('pidstatus', 'proc/%s/status'),
                ('schedstat', 'proc/schedstat'),
                ('stat', 'proc/stat'),
                ('uptime', 'proc/uptime'),
                ('vmstat', 'proc/vmstat'),
            ],
            msg='Incorrect output from get_keys'
        )

    def test_show_keys(self):
        '''
        Test show_keys function
        '''
        mystdout = StringIO()
        lnxproc.resources.show_keys(mystdout)
        self.assertEqual(
            mystdout.getvalue(),
            get_show_keys(),
            msg='Incorrect output from show_keys'
        )

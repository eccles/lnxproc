'''
Test ReadFile()
'''

import contextlib
from os import path as ospath, remove as osremove
from shutil import copyfile

from lnxproc import readfile

from .basetestcase import BaseTestCase
from .mockfiles import DATA_DIR

PROC_DIR = ospath.join(DATA_DIR, 'proc')
TEST_KEY = 'key'
TEST_NAME = 'readfile'
TEST_PIDNAME = ospath.join('%s', 'readfile')
TEST_FILENAME = ospath.join('proc', 'readfile')
TEST_PIDFILENAME = ospath.join('proc', TEST_PIDNAME)
TEST_FILE = ospath.join(PROC_DIR, TEST_NAME)
TEST_FILE1 = ospath.join(PROC_DIR, ''.join((TEST_NAME, '1')))
TEST_FILE2 = ospath.join(PROC_DIR, ''.join((TEST_NAME, '2')))
TEST_PIDFILE = ospath.join(PROC_DIR, '1', TEST_NAME)
TEST_PIDFILE1 = ospath.join(PROC_DIR, '1', ''.join((TEST_NAME, '1')))
TEST_PIDFILE2 = ospath.join(PROC_DIR, '1', ''.join((TEST_NAME, '2')))
TEST_DATA1 = '1 2 3 4 5\n5 6 7 8 9'
TEST_DATA2 = 'record1\nrecord2'
TEST_LINES1 = ['1 2 3 4 5', '5 6 7 8 9']
TEST_LINES2 = ['record1', 'record2']


def remove_file(filename):
    """
    Remove file idempotently
    """
    with contextlib.suppress(FileNotFoundError):
        osremove(filename)


class TestReadFile(BaseTestCase):
    '''
    Test ReadFile class
    '''
    def setUp(self):
        '''
        Create dummy file
        '''
        readfile.ReadFile.FILENAME = TEST_FILENAME
        readfile.ReadFile.KEY = TEST_KEY
        remove_file(TEST_FILE)

    def tearDown(self):
        '''
        Remove dummy file
        '''
        remove_file(TEST_FILE)

    def test_readfile(self):
        '''
        Test normal instantiation
        '''
        copyfile(TEST_FILE1, TEST_FILE)
        fhandle = readfile.ReadFile(root=DATA_DIR)
        fhandle.read()
        self.assertEqual(
            fhandle.data,
            TEST_DATA1,
            msg='Incorrect data from file'
        )
        self.assertEqual(
            fhandle.lines,
            TEST_LINES1,
            msg='Incorrect lines from file'
        )
        with self.assertRaises(NotImplementedError):
            fhandle.normalize()

    def test_second_read(self):
        '''
        Test data changes on second read
        '''
        copyfile(TEST_FILE1, TEST_FILE)
        fhandle = readfile.ReadFile(root=DATA_DIR)
        fhandle.read()
        copyfile(TEST_FILE2, TEST_FILE)
        fhandle.read()
        self.assertEqual(
            fhandle.data,
            TEST_DATA2,
            msg='Incorrect data from file on second read'
        )

    def test_file_does_not_exist(self):
        '''
        Test instantiation when file does not exist
        '''
        fhandle = readfile.ReadFile(root=DATA_DIR)
        fhandle.read()
        self.assertEqual(
            fhandle.data,
            None,
            msg='Incorrect data from nonexistent file'
        )
        self.assertEqual(
            fhandle.lines,
            [],
            msg='Incorrect lines from nonexistent file'
        )


class TestReadCachedFile(BaseTestCase):
    '''
    Test ReadFile class with caching on
    '''
    def setUp(self):
        '''
        Create dummy file
        '''
        readfile.ReadFile.FILENAME = TEST_FILENAME
        readfile.ReadFile.KEY = TEST_KEY
        readfile.ReadFile.CACHED = True
        remove_file(TEST_FILE)

    def tearDown(self):
        '''
        Remove dummy file
        '''
        readfile.ReadFile.CACHED = False
        remove_file(TEST_FILE)

    def test_cached_read(self):
        '''
        Test data does not change on cached read
        '''
        copyfile(TEST_FILE1, TEST_FILE)
        fhandle = readfile.ReadFile(root=DATA_DIR)
        fhandle.read()
        copyfile(TEST_FILE2, TEST_FILE)
        fhandle.read()
        self.assertEqual(
            fhandle.data,
            TEST_DATA1,
            msg='Incorrect data from cached file'
        )


class TestReadPidFile(BaseTestCase):
    '''
    Test ReadFile class
    '''
    def setUp(self):
        '''
        Create dummy file
        '''
        readfile.ReadFile.FILENAME = TEST_PIDFILENAME
        readfile.ReadFile.KEY = TEST_KEY
        remove_file(TEST_PIDFILE)
        self.pid = '1'

    def tearDown(self):
        '''
        Remove dummy file
        '''
        self.pid = None
        remove_file(TEST_PIDFILE)

    def test_pid_file(self):
        '''
        Test instantiation when pid is specified
        '''
        copyfile(TEST_PIDFILE1, TEST_PIDFILE)
        fhandle = readfile.ReadFile(pid=self.pid, root=DATA_DIR)
        fhandle.read()
        self.assertEqual(
            fhandle.data,
            TEST_DATA1,
            msg='Incorrect data from file of pid %s' % (self.pid, )
        )
        self.assertEqual(
            fhandle.lines,
            TEST_LINES1,
            msg='Incorrect lines from file of pid %s' % (self.pid, )
        )

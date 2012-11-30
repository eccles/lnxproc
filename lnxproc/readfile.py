'''
ReadFile() : the ReadFile class.  Only inherit from this class

Provides an iterator that reads the file in question

'''
from ast import literal_eval
from logging import getLogger
from os import strerror, path as ospath

LOGGER = getLogger(__name__)
DEFAULT_ROOT = '/'


class ReadFile:
    '''
    Read File from filesystem
    '''
    FILENAME = None
    KEY = None
    CACHED = False

    def __init__(self, pid=None, root=None):
        '''Initialize the attributes

        :param pid: if True the file is only read once
        :type pid: integer
        '''
        self.pid = pid
        LOGGER.debug("pid %s", self.pid)
        self.root = root or DEFAULT_ROOT
        LOGGER.debug("root %s", self.root)

        if self.FILENAME is None:
            raise ValueError("filename not specified")

        if self.pid is not None:
            self.filename = ospath.join(
                self.root,
                self.FILENAME % (self.pid, ),
            )
        else:
            self.filename = ospath.join(
                self.root,
                self.FILENAME,
            )

        if self.KEY is None:
            raise ValueError("key must be string")

        LOGGER.debug("key %s", self.KEY)
        LOGGER.debug("filename %s", self.filename)

        self.data = None

    def __repr__(self):
        return '%s (%s)' % (self.KEY, self.FILENAME, )

    def read(self):
        '''
        Reads file into list - one line per tuple entry
        '''
        if not self.CACHED or not self.data:
            try:
                with open(self.filename, 'rt') as fhandle:
                    self.data = fhandle.read().strip()

            except OSError as ex:
                LOGGER.error(
                    "Error %s for %s", strerror(ex.errno), self.filename,
                )
                self.data = None

            else:
                LOGGER.debug("Read %s", self.filename)

    @property
    def lines(self):
        '''
        Returns data as list
        '''
        return self.data.split('\n') if self.data else []

    @staticmethod
    def convert(val):
        '''
        Converts raw string into value
        '''
        try:
            ret = literal_eval(val.strip())

        except (ValueError, SyntaxError):
            ret = val.strip()

        return ret

    def normalize(self):
        '''
        Return dictionary of values
        '''
        raise NotImplementedError("normalize method is undefined")

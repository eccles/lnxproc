'''
Contains PidFd() class

    Reads the /proc/<pid>/fd directory and resolves symbolic links

NB requires sudo
'''
from contextlib import suppress
from logging import getLogger
from os import listdir, readlink, path as ospath

from .readfile import ReadFile

LOGGER = getLogger(__name__)


class PidFd(ReadFile):
    '''
    PidFd handling
    '''
    FILENAME = ospath.join('proc', '%s', 'fd')
    KEY = 'pidfd'

    def read(self):
        '''
        The <pid>/fd is a directory
        so we make the dictionary here in case the pid goes away
        '''
        LOGGER.debug("Read")
        ret = {}
        with suppress(FileNotFoundError):
            for line in listdir(self.filename):
                if line:
                    try:
                        ret[int(line)] = readlink(
                            ospath.join(self.filename, line)
                        )
                    except OSError:
                        pass

        self.data = ret

    def normalize(self):
        '''
        Returns data
        '''
        LOGGER.debug("Normalize")
        return self.data.copy()

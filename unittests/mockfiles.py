'''
Convenience methods for unittests
'''
from os import extsep, path as ospath

from yaml import load, dump

SUBDIR = ospath.dirname(__file__)
DATA_DIR = ospath.join(SUBDIR, 'data')
RESULT_DIR = ospath.join(SUBDIR, 'result')


def write_result(key, result):
    '''
    Sometimes we want to actially write the result
    dictionary
    '''
    filename = ospath.join(
        RESULT_DIR,
        extsep.join([key, 'yaml', ]),
    )
    with open(filename) as fhandle:
        result = dump(
            result,
            fhandle,
            indent=2,
            width=80,
            default_flow_style=False
        )


def get_show_keys():
    '''
    Gets contents of show_keys result file
    '''
    filename = ospath.join(
        RESULT_DIR,
        extsep.join(['show_keys', 'txt', ]),
    )
    with open(filename) as fhandle:
        return fhandle.read()


def get_test_result(key):
    '''
    Read data and result for given key
    '''
    filename = ospath.join(
        RESULT_DIR,
        extsep.join([key, 'yaml', ]),
    )
    with open(filename) as fhandle:
        result = load(fhandle)

    return result

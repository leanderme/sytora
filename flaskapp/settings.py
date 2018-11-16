"""
    settings

    a repository to configure various parts of the app
"""

import os
import sys
import json
import configparser


def build_config(filename):
    """create a configparser object and write a ini file."""
    config = configparser.ConfigParser(allow_no_value=True)

    config['GENERAL'] = dict()
    config['GENERAL']['DATA_LOCATION'] = '../data/'
    config['API'] = dict()
    config['API']['BASE_URL'] = '/api/v1'
    config['API']['PORT'] = 5001
    config['ENGINE'] = dict()
    config['ENGINE']['VERBOSE'] = 'false'
    config['OTHER'] = dict()
    conifg['OTHER']['IPSTACK'] = 'false'
    config['OTHER']['IPSTACKKEY'] = 'b75946fe4fb4995b2846c90fe7063c43'

    with open(filename, 'w') as f:
        config.write(f)


CONFIGFILE = os.getenv('CONFIGFILE', default='./config.ini')
config = configparser.ConfigParser(allow_no_value=True)
if not os.path.exists(CONFIGFILE):
    build_config(CONFIGFILE)

config.read(CONFIGFILE)

VERBOSE = bool(os.getenv('VERBOSE',
               default=config.getboolean('ENGINE', 'VERBOSE')))

BASE_URL = config['API']['BASE_URL']
PORT = int(config['API']['PORT'])
IPSTACKKEY = config['OTHER']['IPSTACKKEY']


APP_CONFIG = {
    'SECRET_KEY': '\x9c\xedh\xdf\x8dS\r\xe3]\xc3\xd3\xbd\x0488\xfc\xa6<\xfe'
                  '\x94\xc8\xe0\xc7\xdb',
    'SESSION_COOKIE_NAME': 'sytora_session',
    'DEBUG': True
}


class CacheSettings(object):

    path = config['GENERAL']['DATA_LOCATION']
    html = path + 'html/'
    index = path + 'index_pages.pkl'
    symptoms = path + 'symptoms.pkl'
    processed_data = path + 'nlp_data.pkl'

    @classmethod
    def check(CacheSettings, filename):
        return True if os.path.exists(filename) else False

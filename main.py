#!/usr/bin/env python3
import re
import sys

import os
from bottle import run

import config
import utils
import views

if __name__ == '__main__':

    if config.COMMAND == 'runserver':
        run(host='0.0.0.0', port=config.PORT)

    elif config.COMMAND == 'upload':
        if not re.match(r'^[0-9A-Za-z]+$', config.GROUP):
            print('Invalid group name: \'{}\''.format(config.GROUP), file=sys.stderr)
            exit(1)
        if not re.match(r'^[0-9A-Za-z]+$', config.FACES):
            print('Invalid face name: \'{}\''.format(config.FACES), file=sys.stderr)
            exit(1)
        if not (config.FILE and os.path.isfile(config.FILE)):
            print('Invalid file path.', file=sys.stderr)
            exit(1)
        utils.upload(config.GROUP, config.FACES, config.FILE)

    elif config.COMMAND == 'recognize':
        if not re.match(r'^[0-9A-Za-z]+$', config.GROUP or ''):
            print('Invalid group name: ' + config.GROUP, file=sys.stderr)
            exit(1)
        if not (config.FILE and os.path.isfile(config.FILE)):
            print('Invalid file path.', file=sys.stderr)
            exit(1)
        if not re.match(r'^(?:[0-9A-Za-z]+\|)*([0-9A-Za-z]+)?$', config.FACES):
            print(('Invalid face names: {}, should be alpha-number '
                   'separated by a \'|\' character.').format(config.FACES), file=sys.stderr)
            exit(1)
        utils.recognize(config.GROUP, config.FILE,
                        config.FACES and config.FACES.split('|'))

    else:
        print('Invalid command: ' + config.COMMAND, file=sys.stderr)
        exit(1)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Hello from monyze-agent.py '''

__author__ = 'Konstantin Lyakhov'
__contact__ = 'kl@rifco.ru'
__copyright__ = 'Copyright (C) Monyze. All rights reserved.'
__credits__ = ['Konstantin Lyakhov (Skype: komstin)', 'Dmitry Soloviev (Skype: gex_skype)']
__license__ = ''

#import hashlib  # necessary for compilation
#import json  # necessary for compilation
#import requests
import logging
import logging.config

import os
import shutil
import subprocess


def main():
    ''' The main entry point of the Monyze monitoring agent '''

    from monyze import parse
    from monyze.config import config
    from monyze.data import data
    from monyze.daemon import daemon

    logConfig = {
        "version":1,
        "handlers":{
            "fileHandler":{
                "class":"logging.FileHandler",
                "formatter":"myFormatter",
                "filename":"/tmp/monyze-agent.log"
            }
        },
        "loggers":{
            "monyze-agent":{
                "handlers":["fileHandler"],
                "level":"INFO",
            }
        },
        "formatters":{
            "myFormatter":{
                "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    }
    
    logging.config.dictConfig(logConfig)
    logger = logging.getLogger("monyze-agent.main")
    logger.info("Program started in %s" % os.getcwd())
    logger.info("argv: %s" % sys.argv)
#    print("Program started in %s" % os.getcwd())
#    print("argv: %s" % sys.argv)
        
#    if os.getcwd() == '/usr/local/bin':
    if sys.argv[0] == '/usr/local/bin/monyze-agent':
        daemon = daemon('/var/run/monyze-agent.pid')
        config = config('/etc/monyze-agent/config.pickle')
        data = data(config)

        if sys.argv[1] == 'start':
            if not daemon.get_pid():
                print("\nАгент запущен.\n")
                daemon.start(config, data)
            else:
                raise SystemExit('\nАгент уже запущен.\n')

        if sys.argv[1] == 'restart':
            if not daemon.get_pid():
                raise SystemExit('\nАгент не запущен.\n')
            else:
                print '\nАгент перезапущен.\n'
                daemon.restart(config, data)

        if sys.argv[1] == 'stop':
            if not daemon.get_pid():
                raise SystemExit('\nАгент не запущен.\n')
            else:
                daemon.stop()
                raise SystemExit('\nАгент остановлен.\n')
        logger.info("Done in /usr/local/bin")
        return

    parse()

if __name__ == '__main__':
    main()

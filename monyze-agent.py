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
                "filename":"/var/log/monyze-agent.log"
            }
        },
        "loggers":{
            "monyze":{
                "handlers":["fileHandler"],
                "level":"INFO",
#                "level":"DEBUG",
            }
        },
        "formatters":{
            "myFormatter":{
                "format":"%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        }
    }
    
    if sys.argv[0] == '/usr/local/bin/monyze-agent':
        logging.config.dictConfig(logConfig)
        logger = logging.getLogger("monyze.main")
        logger.info("\n*** Starting: %s" % sys.argv[1])

        daemon = daemon('/var/run/monyze-agent.pid')

        if sys.argv[1] == 'stop':
            if not daemon.get_pid():
                logger.info("Демон не запущен, нечего останавливать. Exit")
            else:
                logger.info("Останавливаем демона")
                daemon.stop()

        if sys.argv[1] == 'start':
            if not daemon.get_pid():
                config = config('/etc/monyze-agent/config.pkl')
                data = data(config)
                logger.info("Запускаем демона")
                daemon.start(config, data)
            else:
                logger.info("Демон уже запущен. Exit")

        if sys.argv[1] == 'restart':
            if not daemon.get_pid():
                logger.info("Демон не запущен, restart невозможен. Exit")
            else:
                config = config('/etc/monyze-agent/config.pkl')
                data = data(config)
                logger.info("Перезапускаем демона")
                daemon.restart(config, data)

        logger.info('Stopping')
        return

    parse()

if __name__ == '__main__':
    main()

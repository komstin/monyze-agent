# -*- coding: utf-8 -*-
''' Hello from monyze/__init__.py '''

__author__ = 'Konstantin Lyakhov'
__contact__ = 'kl@rifco.ru'
__copyright__ = 'Copyright (C) Monyze. All rights reserved.'
__credits__ = ['Konstantin Lyakhov (Skype: komstin)', 'Dmitry Soloviev (Skype: gex_skype)']
__license__ = ''

import argparse
#import json
#import requests
import os
import shutil
import subprocess

def parse():
    ''' CLI parsing & routing '''

    from monyze.config import config
    parser = argparse.ArgumentParser(prog='monyze', add_help=False,
                                     description='Без аргументов - запуск сервиса (sudo)',
                                     epilog='Подробнее - на сайте https://monyze.ru')
    parser.add_argument("-h", "--help", action='store_true', help="Показать подсказку")
#    parser.add_argument("-c", "--config", choices=['show', 'delete'], help="Конфигурация: показать, удалить (sudo)")
    parser.add_argument("-c", "--config", action='store_true', help="Показать конфигурацию")
    parser.add_argument("-v", "--version", action='store_true', help="Показать версию")
    parser.add_argument("-t", "--timeout", help="Задать временной интервал мониторинга в секундах (sudo)", type=int)
    parser.add_argument("-u", "--userid", help="Задать userId (sudo)")
    try:
        args = parser.parse_args()
    except BaseException:
        print('Неправильный аргумент!')
        return

    if args.help:
        parser.print_help()
        return

    config = config('/etc/monyze-agent/config.pkl')

    if args.version:
        print('Версия агента: %s' % config.version)
        return

    if args.config:
        print(config)
        return

    if os.getuid():
        print('Требуются права администратора! Попробуйте использовать команду sudo.')
        return

    if args.timeout:
        config.timeout = args.timeout
        config.store()
        print('Новый таймаут: %s сек. установлен.' % args.timeout)
        return

    if args.userid:
        if args.userid == '$$$':
            args.userid = '8dfa018ba64311eed1033791a7e4389acbe5379e0c7c5abdc6c405acef6b9841'
        config.userId = args.userid
        config.store()
        print('Новый userId: %s установлен.' % args.userid)
        return

    if not any(vars(args).values()):
        try:
            shutil.copy('monyze-agent', '/usr/local/bin')
        except IOError:
            print('Невозможно скопировать файл агента!')
            return
        try:
            os.mkdir('/etc/monyze-agent', 0755)
        except OSError:
            pass
        init = '''#! /bin/sh

### BEGIN INIT INFO
# Provides:          monyze-service
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Should-Start:      $portmap
# Should-Stop:       $portmap
# X-Start-Before:    nis
# X-Stop-After:      nis
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# X-Interactive:     true
# Short-Description: Monyze-agent
# Description:       Monyze monitoring service
### END INIT INFO

case "$1" in
  start)
    echo "Starting monyze-agent"
    /usr/local/bin/monyze-agent start
    ;;
  stop)
    echo "Stopping monyze-agent"
    /usr/local/bin/monyze-agent stop
    ;;
  stop)
    echo "Stopping monyze-agent"
    /usr/local/bin/monyze-agent restart
    ;;
  *)
    echo "Usage: /etc/init.d/monyze-agent {start|stop|restart}"
    exit 1
    ;;
esac
 
exit 0
'''

        with open('/etc/init.d/monyze-agent', 'wb') as agent:
            agent.write(init)
        os.chmod('/etc/init.d/monyze-agent', 0755)
        subprocess.call(['update-rc.d', 'monyze-agent', 'defaults'])
        subprocess.call(['service', 'monyze-agent', 'start'])
        print('Сервис запущен. Проверить можно командой: sudo service monyze-agent status')

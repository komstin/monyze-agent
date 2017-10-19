# -*- coding: utf-8 -*-
''' Hello from monyze/__init__.py '''

__author__ = 'Konstantin Lyakhov'
__contact__ = 'kl@rifco.ru'
__copyright__ = 'Copyright (C) Monyze. All rights reserved.'
__credits__ = ['Konstantin Lyakhov', 'Dmitry Soloviev']
__license__ = ''

import argparse
import os
import json
import requests


def parse():
    ''' CLI parsing & routing '''

    from monyze.config import config
    from monyze.data import data
    from monyze.daemon import daemon

    parser = argparse.ArgumentParser(prog='monyze', add_help=False,
                                     description='Мониторинг Monyze',
                                     epilog='Подробнее - на сайте https://monyze.ru')
    parser.add_argument("-h", "--help", action='store_true', help="Показать подсказку")
    parser.add_argument("-c", "--config", choices=['show', 'delete'],
                        help="Конфигурация: показать, удалить")
    parser.add_argument("-a", "--action", choices=['start', 'stop', 'restart', 'status'],
                        help="Действие: запустить, остановить, перезапустить, статус")
    parser.add_argument("-t", "--timeout",
                        help="Задать временной интервал мониторинга в секундах", type=int)
    parser.add_argument("-u", "--userid", help="Задать userId")
    parser.add_argument(
        "-v",
        "--version",
        action='store_true',
        help="Показать версию и выйти")

    try:
        args = parser.parse_args()
    except BaseException:
        raise SystemExit('\nНеправильный аргумент!\n')

    if args.help or not any(vars(args).values()):
        parser.print_help()
        return

    if args.config == 'delete':
        try:
            os.remove('monyze.cfg')
            raise SystemExit('\nКонфигурация удалена!\n')
        except (OSError, IOError):
            raise SystemExit('\nНевозможно удалить конфигурацию!\n')

    daemon = daemon('/tmp/monyze-agent.pid')

    if args.action == 'stop':
        if not daemon.get_pid():
            raise SystemExit('\nАгент не запущен.\n')
        else:
            daemon.stop()
            raise SystemExit('\nАгент остановлен.\n')

    if args.action == 'status':
        pid = daemon.get_pid()
        if not pid:
            raise SystemExit('\nАгент не запущен.\n')
        else:
            raise SystemExit('\nАгент запущен: (pid=' + str(pid) + ')\n')

    config = config('config.txt')

    if args.version:
        raise SystemExit('\nВерсия агента: ' + config.version + '\n')

    if args.config == 'show':
        raise SystemExit(config)

    if args.timeout:
        config.timeout = args.timeout
        config.store()
        raise SystemExit('\nНовый таймаут: ' +
                         str(args.timeout) + ' сек. установлен.\n')

    if args.userid:
        config.userId = args.userid
        config.store()
        raise SystemExit('\nНовый userId: ' + args.userid + ' установлен.\n')

    data = data(config)

    if args.action == 'start':
        if not daemon.get_pid():
            print("\nАгент запущен.\n")
            daemon.start(config, data)
        else:
            raise SystemExit('\nАгент уже запущен.\n')

    if args.action == 'restart':
        if not daemon.get_pid():
            raise SystemExit('\nАгент не запущен.\n')
        else:
            print '\nАгент перезапущен.\n'
            daemon.restart(config, data)

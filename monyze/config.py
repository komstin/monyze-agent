# -*- coding: utf-8 -*-
''' Hello from monyze/config.py '''

__author__ = 'Konstantin Lyakhov'
__contact__ = 'kl@rifco.ru'
__copyright__ = 'Copyright (C) Monyze. All rights reserved.'
__credits__ = ['Konstantin Lyakhov (Skype: komstin)', 'Dmitry Soloviev (Skype: gex_skype)']
__license__ = ''

import logging
import datetime
import cPickle as pickle
import platform
import os
import socket
import subprocess
import uuid


class config:
    ''' Configuration - get, update, store, restore '''

    def __init__(self, filename):
        self.logger = logging.getLogger("monyze.config")
        self.logger.info("Инициализация конфига")

        self.filename = filename
        try:
            with open(self.filename, 'rb') as f:
                store = pickle.load(f)
                for key, value in store.__dict__.items():
                    self.__dict__[key] = value
                self.restored_at = datetime.datetime.now()
            self.logger.info("Конфиг загружен")

        except (IOError, EOFError):
            if os.getuid():
#                raise SystemExit('\nТребуются права администратора! Попробуйте использовать команду sudo.\n')
                raise SystemExit('Конфиг отсутствует! Попробуйте запустить (перезапустить) сервис.')
            self.name = 'monyze-agent'
            self.description = 'Monyze monitoring agent'
            self.computerId = self.computerId()
            self.userId = self.userId()
            self.nodename = self.nodename()
            self.bits = platform.architecture()[0]
            self.cpu_model = self.cpu_model()
            self.os = self.os()
            self.timeout = 5
            self.url = 'http://monyze.ru/'
            self.api_url = 'http://dev.monyze.ru/api.php'
            self.api_url = 'https://monyze.ru/api.php'
            self.version = '0.0.7 (26.11.2017)'
#            self.version = '0.0.4-dev (17.10.2017)'
            self.osSystem = platform.system()
            self.osRelease = platform.release()
            self.osVersion = platform.version()
            self.machine = platform.machine()
#            print self
            self.store()
            self.logger.info("Конфиг создан")

    def computerId(self):

        try:
            return open('/var/lib/dbus/machine-id', 'r').read().strip()
        except (IOError, ValueError):
            pass

        try:
            return open('/etc/machine-id', 'r').read().strip()
        except (IOError, ValueError):
            pass

        return hex(uuid.getnode())[2:]

    def userId(self):
        userId = raw_input(
            '\nВведите идентификатор пользователя, выданный на сайте: ')
        return userId or '8dfa018ba64311eed1033791a7e4389acbe5379e0c7c5abdc6c405acef6b9841'

    def nodename(self):

        try:
            host = socket.gethostname()
            if host:
                return host
        except (ValueError, RuntimeError):
            pass

        try:
            host = platform.node()
            if host:
                return host
        except (ValueError, RuntimeError):
            pass

        try:
            host = os.uname()[1]
            if host:
                return host
        except (ValueError, RuntimeError):
            pass

        raise Exception('Can not determine hostname of this system')

    def os(self):
        return platform.platform()

    def cpu_model(self):
        return subprocess.check_output(
            ["grep", "model name\t:", "/proc/cpuinfo"]).split('\n')[0].split(':')[1].strip()

    def store(self):  # Validate!
        if os.getuid():
            raise SystemExit('\nТребуются права администратора! Попробуйте использовать команду sudo.\n')
        with open(self.filename, 'wb') as f:
            self.stored_at = datetime.datetime.now()
            pickle.dump(self, f, 2)

    def restore(self):  # Validate!

        try:
            with open(self.filename, 'rb') as f:
                self = pickle.load(f)
                self.restored_at = datetime.datetime.now()
        except BaseException:
            raise

    def __getstate__(self):
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        if 'filename' in state:
            del state['filename']
        self.__dict__.update(state)

    def __str__(self):
        stored_values = self.__dict__
        lines = []
        width = max(len(key) for key in stored_values)
        for key in sorted(stored_values.keys()):
            value = stored_values[key]
            if isinstance(value, datetime.datetime):
                value = value.isoformat()
            lines.append('{0} : {1!r}'.format(key.ljust(width), value))
#        return '\n' + '\n'.join(lines) + '\n'
        return '\n'.join(lines)

    def __repr__(self):
        return '{0}({1!r})'.format(self.__class__.__name__, self.filename)

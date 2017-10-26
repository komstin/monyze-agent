# -*- coding: utf-8 -*-
''' Hello from monyze/daemon.py '''

__author__ = 'Konstantin Lyakhov'
__contact__ = 'kl@rifco.ru'
__copyright__ = 'Copyright (C) Monyze. All rights reserved.'
__credits__ = ['Konstantin Lyakhov (Skype: komstin)', 'Dmitry Soloviev (Skype: gex_skype)']
__license__ = ''

import os
import sys
import time
import atexit
import signal
import json
import requests


class daemon:
    ''' Agent daemonizing '''

    def __init__(self, pidfile, stdin='/dev/null',
                 stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        self.fork()
        os.chdir('/')
        os.setsid()
        os.umask(0)
        self.fork()

        sys.stdout.flush()
        sys.stderr.flush()

        self.attach_stream('stdin', mode='r')
        self.attach_stream('stdout', mode='a+')
#        self.attach_stream('stderr', mode='a+')
        self.create_pidfile()

    def attach_stream(self, name, mode):
        stream = open(getattr(self, name), mode)
        os.dup2(stream.fileno(), getattr(sys, name).fileno())

    def fork(self):
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError as e:
            sys.stderr.write("Fork failed: %d (%s)\n" % (e.errno, e.strerror))
            sys.exit(1)

    def create_pidfile(self):
        atexit.register(self.delpid)
        pid = str(os.getpid())
        open(self.pidfile, 'w+').write("%s\n" % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self, config, data):
        pid = self.get_pid()
        if pid:
            message = "pid-файл %s уже есть. Демон уже запущен?\n"
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)
        self.daemonize()
        self.run(config, data)

    def get_pid(self):
        try:
            pf = open(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except (IOError, TypeError):
            pid = None
        return pid

    def stop(self, silent=False):
        pid = self.get_pid()

        if not pid:
            if not silent:
                message = "Нет pid-файла %s. Демон не запущен?\n"
                sys.stderr.write(message % self.pidfile)
            return

        try:
            while True:
                os.kill(pid, signal.SIGTERM)
                time.sleep(0.1)
        except OSError as err:
            err = str(err)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                sys.stdout.write(str(err))
                sys.exit(1)

    def restart(self, config, data):
        self.stop(silent=True)
        self.start(config, data)

    def run(self, config, data):

        while True:
            try:
                time.sleep(config.timeout)
            except KeyboardInterrupt:
                raise SystemExit('\nМониторинг прерван!\n')

            data.update()
            url = config.api_url + '?request=' + \
                json.dumps(data.__dict__).decode('utf-8')
            requests.get(url)

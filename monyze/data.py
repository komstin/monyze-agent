# -*- coding: utf-8 -*-
''' Hello from monyze/data.py '''

__author__ = 'Konstantin Lyakhov'
__contact__ = 'kl@rifco.ru'
__copyright__ = 'Copyright (C) Monyze. All rights reserved.'
__credits__ = ['Konstantin Lyakhov (Skype: komstin)', 'Dmitry Soloviev (Skype: gex_skype)']
__license__ = ''

import netifaces
import psutil


class data():
    ''' Monitoring data - get, update '''

    def __init__(self, config):
        self.main_parameters = [{'ID_COMPUTER': config.computerId,
                                 'ID_USER': config.userId,
                                 'COMPUTER_NAME': config.nodename,
                                 'SYSTEM': config.os}]
        self.cpu = {'CPU_NAIM': config.cpu_model}
        swap = psutil.swap_memory()
        self.memory = [{"dwLength": config.bits,
                        "ullTotalPageFile": swap.total,
                        "ullTotalVirtual": 0,
                        "ullAvailVirtual": 0,
                        "ullAvailExtendedVirtual": 0}]
        partitions = psutil.disk_partitions()
        self.hdd = list()
        for i, partition in enumerate(partitions):
            usage = psutil.disk_usage(partition.mountpoint)
            self.hdd.append({"Name": partition.device,
                             "Size": usage.total,
                             "LOGICAL": partition.mountpoint,
                             "LOAD": usage.percent})
        self.network = list()
        for interface in netifaces.interfaces():
            try:
                net = netifaces.ifaddresses(interface)[netifaces.AF_INET]
                self.network.append(
                    {'Name': interface, 'Addr': net[0]['addr'], 'Netmask': net[0]['netmask']})
            except KeyError:
                continue

    def update(self):
        self.cpu['CPU_ALL'] = psutil.cpu_percent()
        percents = psutil.cpu_percent(interval=0, percpu=True)
        for i, percent in enumerate(percents):
            self.cpu['CPU' + str(i + 1)] = percent
        mem = psutil.virtual_memory()
        self.memory[0]['dwMemoryLoad'] = mem.percent
        self.memory[0]['ullTotalPhys'] = mem.total
        self.memory[0]['ullAvailPhys'] = mem.available

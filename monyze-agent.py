#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' Hello from monyze-agent.py '''

__author__ = 'Konstantin Lyakhov'
__contact__ = 'kl@rifco.ru'
__copyright__ = 'Copyright (C) Monyze. All rights reserved.'
__credits__ = ['Konstantin Lyakhov (Skype: komstin)', 'Dmitry Soloviev (Skype: gex_skype)']
__license__ = ''

import hashlib  # necessary for compilation
import json  # necessary for compilation
from monyze import parse


def main():
    ''' Monyze monitoring agent '''

    parse()


if __name__ == '__main__':

    main()

# TODO: Logging

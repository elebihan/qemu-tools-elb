# -*- coding: utf-8 -*-
#
# This file is part of qemu-tools-elb
#
# Copyright (C) 2014 Eric Le Bihan <eric.le.bihan.dev@free.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

"""
   qemu_tools_elb.logging
   ``````````````````````

   Logging helpers

   :copyright: (C) 2014 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

__docformat__ = 'restructuredtext en'

import os
import sys
import logging
from colorama import init, Fore

__LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
}

try:
    __level = os.environ['QEMU_TOOLS_ELB_LOG']
    __level = __LOG_LEVELS[__level.lower()]
except:
    __level = logging.INFO

__logger = logging.getLogger('qemu-tools-elb')
__logger.setLevel(__level)

class ColoredFormatter(logging.Formatter):
    """Add color to messages.

    :param fmt: format string
    :type: str
    """
    def __init__(self, fmt):
        logging.Formatter.__init__(self, fmt)

    def format(self, record):
        colors = {
            'WARNING': Fore.YELLOW,
            'INFO': Fore.GREEN,
            'DEBUG': Fore.BLUE,
            'CRITICAL': Fore.MAGENTA,
            'ERROR': Fore.RED,
        }
        message = logging.Formatter.format(self, record)
        return colors[record.levelname] + message + Fore.RESET

def setup_logging():
    fmt = "%(levelname)s: %(message)s"
    handler = logging.StreamHandler()
    if sys.stdout.isatty():
        formatter = ColoredFormatter(fmt)
        init()
    else:
        formatter = logging.Formatter(fmt)

    handler.setFormatter(formatter)
    for h in __logger.handlers:
        __logger.removeHandler(h)
    __logger.addHandler(handler)

def info(message):
    __logger.info(message)

def debug(message):
    __logger.debug(message)

def error(message):
    __logger.error(message)

def warning(message):
    __logger.warning(message)

# vim: ts=4 sw=4 sts=4 et ai

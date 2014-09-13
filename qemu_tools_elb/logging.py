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
import logging

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

def setup_logging():
    logging.basicConfig(format="%(levelname)s: %(message)s")

def info(message):
    __logger.info(message)

def debug(message):
    __logger.debug(message)

# vim: ts=4 sw=4 sts=4 et ai

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
   qemu_tools_elb.box
   ``````````````````

   Virtual machine configuration

   :copyright: (C) 2014 Eric Le Bihan <eric.le.bihan.dev@free.fr>
   :license: GPLv3+
"""

__docformat__ = 'restructuredtext en'

import os
import shutil
from configparser import ConfigParser
from gettext import gettext as _
from subprocess import check_call
from .logging import info, debug
from .utils import get_data_dir

class BoxManager:
    """Manages boxes"""
    def __init__(self):
        self._directories = [os.path.expanduser("~/.local/share/qemu-box/boxes")]
        if 'QEMU_BOXES_PATH' in os.environ:
            self._directories += os.environ['QEMU_BOXES_PATH'].split(':')

    @staticmethod
    def _list_boxes(directory):
        """List the boxes available in a directory.

        :param directory: path of the directory to inspect.
        :type directory: str.

        :returns: the list of boxes
        :rtype: list of :class:`Box`
        """
        boxes = []
        if os.path.exists(directory):
            for entry in os.listdir(directory):
                path = os.path.join(directory, entry)
                if os.path.isfile(path):
                    name, ext = os.path.splitext(entry)
                    if ext == '.conf':
                        box = Box(name)
                        box.load_from_file(path)
                        boxes.append(box)
        return boxes

    @property
    def boxes(self):
        """Returns a list of all the available boxes.

        Search for all boxes available locally, as well as in the directories
        specified in the $QEMU_BOXES_PATH environment variable.

        If a box is found twice, the one found in the farthest member of
        $QEMU_BOXES_PATH is selected.

        :returns: the list of boxes
        :rtype: list of :class:`Box`
        """
        boxes = []
        names = []
        for directory in reversed(self._directories):
            for box in BoxManager._list_boxes(directory):
                if box.name not in names:
                    boxes.append(box)
                    names.append(box.name)
        return sorted(boxes, key=lambda b: b.name)

    @property
    def local_boxes(self):
        """Returns  a list the boxes available locally.

        :returns: the list of boxes
        :rtype: list of :class:`Box`
        """
        boxes = BoxManager._list_boxes(self._directories[0])
        return sorted(boxes, key=lambda b: b.name)

    def lookup_by_name(self, name):
        """Search for a box by its name.

        :param name: name of the box.
        :type name: str.

        :returns: the matching box.
        :rtype: :class:`Box`.
        """
        for box in self.boxes:
            if box.name == name:
                return box
        raise RuntimeError(_('box not found'))

    def _create_box_from_file(self, name, template):
        filename = os.path.join(self._directories[0], name + '.conf')
        if os.path.exists(filename):
            raise RuntimeError(_("box already exists"))
        if not os.path.exists(template):
            raise RuntimeError(_("template does not exist"))
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        shutil.copy(template, filename)

    def create_box(self, name):
        """Creates a new box configuration.

        Creates a new box configuration from default template.

        :param name: name of the new box.
        :type name: str
        """
        template = os.path.join(get_data_dir(), 'box.example.conf')
        self._create_box_from_file(name, template)

    def copy_box(self, src, dst):
        template = os.path.join(self._directories[0], src + '.conf')
        self._create_box_from_file(dst, template)

    def edit_box(self, name):
        """Edits a box configuration file.

        Edits the configuration file of the specified box or create a new one
        if it does not exist.

        The text editor set in $EDITOR will be invoked to modify the file.
        """
        filename = os.path.join(self._directories[0], name + '.conf')
        if not os.path.exists(filename):
            raise RuntimeError(_("box does not exist"))
        editor = os.environ.get('$EDITOR', 'vi')
        check_call([editor, filename])

    def delete_box(self, name):
        """Delete a local box

        :param name: name of the box to delete
        :type name: str
        """
        filename = os.path.join(self._directories[0], name + '.conf')
        if os.path.exists(filename):
            os.unlink(filename)
        else:
            raise RuntimeError(_('box not found'))

class Box:
    '''Represents the configuration for a virtual machine

    :param name: name of the box
    :type name: str
    '''
    def __init__(self, name):
        self._name = name
        self.description = None
        self.base_directory = None
        self.kernel = 'zImage'
        self.drives = ['rootfs.ext2']
        self.boot_options = []
        self.bootable_image = False
        self.has_graphics = True
        self.arch = 'x86'
        self.cpu = None
        self.n_net_interfaces = 1
        self.virtual_network = None
        self.usb_devices = []
        self.usb_drives = []

    @property
    def name(self):
        """Returns the name of the box"""
        return self._name

    def load_from_file(self, filename):
        """Loads a box from a file.

        :param filename: path to the file to read configuration from
        :type filename: str
        """
        parser = ConfigParser()
        with open(filename) as f:
            parser.read_file(f)

        self.description = parser.get('General', 'Description', fallback=None)
        value = parser.get('General', 'BaseDirectory', fallback='~/build')
        self.base_directory = os.path.expanduser(value)
        self.arch = parser.get('Machine', 'Arch', fallback='x86')
        self.cpu = parser.get('Machine', 'Cpu', fallback=None)
        self.has_graphics = parser.getboolean('Machine', 'HasGraphics', fallback=True)
        self.kernel = parser.get('System', 'Kernel', fallback='zImage')
        value = parser.get('System', 'BootOptions', fallback='')
        self.boot_options = value.split()
        self.bootable_image = parser.getboolean('System', 'BootableImage', fallback=False)
        value = parser.get('System', 'Drives', fallback='rootfs.ext2')
        self.drives = [os.path.expanduser(p) for p in value.split()]
        self.n_net_interfaces = parser.getint('Networking',
                                              'NumberOfInterfaces',
                                              fallback=1)
        self.vlan_backend = parser.get('Networking',
                                       'VirtualNetwork',
                                       fallback=None)
        value = parser.get('USB', 'Drives', fallback='')
        self.usb_drives = [os.path.expanduser(p) for p in value.split()]
        value = parser.get('USB', 'Devices', fallback='')
        self.usb_devices = value.split()

class BoxRunner:
    """Run boxes"""
    def __init__(self):
        self._base_mac_addr = '52:54:00:11:22:33'
        self._vde_socket = '/var/run/vde2/tap0.ctl'

    def run(self, box):
        """Runs a virtual machine.

        :param box: the box to run
        :type box: :class:`Box`
        """
        info("running {}".format(box.description))
        args = self._generate_cmd_line(box)
        debug("executing '{}'".format(' '.join(args)))
        check_call(args)

    def _generate_cmd_line(self, box):
        args = self._generate_mach_args(box)
        args += self._generate_sys_args(box)
        args += self._generate_net_args(box)
        args += self._generate_usb_args(box)
        return args

    def _generate_mach_args(self, box):
        mach_args = {
            'x86': [
                'qemu-system-i386', '--enable-kvm',
                '-soundhw', 'hda',
                '-vga', 'std',
                '-device', 'piix3-usb-uhci',
            ],
            'arm': [
                'qemu-system-arm', '-m', '256',
                '-M', 'versatilepb',
            ],
        }
        if box.arch not in mach_args:
            raise RuntimeError(_("unsupported architecture"))
        args = mach_args[box.arch]
        if not box.has_graphics:
            args.append('-nographic')
        return args

    def _generate_sys_args(self, box):
        consoles = {
            'arm': 'ttyAMA0',
        }
        args = []
        if not box.bootable_image:
            options = ['root=/dev/sda rw ', 'video=vesa', 'vga=788']
            if not box.has_graphics:
                tty = consoles.get(box.arch, 'ttyS0')
                options.append("console={}".format(tty))
            options += box.boot_options
            args.append('-kernel')
            args.append(os.path.join(box.base_directory, box.kernel))
            args.append('-append')
            args.append(' '.join(options))
        for drive in box.drives:
            if not os.path.isabs(drive):
                path = os.path.join(box.base_directory, drive)
            else:
                path = drive
            args.append('-drive')
            args.append("file={}".format(path))
        return args

    def _generate_net_args(self, box):
        args = []
        vlan_backends = ['vde', 'tap', 'user']
        if box.vlan_backend:
            if box.vlan_backend not in vlan_backends:
                raise RuntimeError(_("unsupported VLAN backend"))
            netdev_id = "vlan-{}-{}".format(box.vlan_backend, 0)
            netdev = "{},id={}".format(box.vlan_backend, netdev_id)
            if box.vlan_backend == 'vde':
                netdev += ",sock={}".format(self._vde_socket)
            args.append('-netdev')
            args.append(netdev)

        for mac in self._generate_mac_addresses(box):
            device = "rtl8139,mac={}".format(mac)
            if box.vlan_backend:
                device += ",netdev={}".format(netdev_id)
            args.append('-device')
            args.append(device)
        return args

    def _generate_mac_addresses(self, box):
        bytes = [int(h, 16) for h in self._base_mac_addr.split(':')]
        macs = []
        for i in range(box.n_net_interfaces):
            mac = ':'.join(["{:02x}".format(b) for b in bytes])
            macs.append(mac)
            bytes[-1] += 1
        return macs

    def _generate_usb_args(self, box):
        args = []
        if box.usb_drives or box.usb_devices:
            args.append('-usb')
        for i, drive in enumerate(box.usb_drives):
            if not os.path.isabs(drive):
                path = os.path.join(box.base_directory, drive)
            else:
                path = drive
            args.append('-drive')
            args.append("id=usb-disk-{},file={},if=none".format(i, path))
            args.append('-device')
            args.append("usb-storage,drive=usb-disk-{}".format(i))
        for device in box.usb_devices:
            args.append('-usbdevice')
            args.append("host:" + device)
        return args

# vim: ts=4 sw=4 sts=4 et ai

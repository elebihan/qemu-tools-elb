========
qemu-box
========

--------------------------
run a QEMU virtual machine
--------------------------

:Author: Eric Le Bihan <eric.le.bihan.dev@free.fr>
:Copyright: 2014 Eric Le Bihan
:Manual section: 1

SYNOPSIS
========

qemu-box [OPTIONS] <command> [<argument>, ...]

qemu-box [OPTIONS] list

qemu-box [OPTIONS] new <box>

qemu-box [OPTIONS] run <box>

qemu-box [OPTIONS] edit <box>

qemu-box [OPTIONS] remove <box>

DESCRIPTION
===========

`qemu-box(1)` runs a QEMU virtual machine or "box", which parameters are
defined in a configuration file.

By default the configuration files are stored in
``$HOME/.local/share/qemu-box/boxes``.

OPTIONS
=======

-v, --version   display program version and exit

COMMANDS
========

The following commands are understood:

list
~~~~

List the available boxes. If *--details* is set, a brief description of the
box is displayed. By default, `qemu-box(1)` will search for the local boxes defined
in ``$HOME/.local/share/qemu-box/boxes``. The paths for additional boxes can
be set as a colon-separated list in the $QEMU_BOXES_PATH environment variable.

Available options:

-d, --details    show details
-l, --local      show only local boxes

new <box>
~~~~~~~~~

Create a new box and edit it. Use *--from* to use an existing box as a
template.

Available options:

-f BOX, --from BOX   use BOX as template

run <box>
~~~~~~~~~

Run a pre-configured box.

edit <box>
~~~~~~~~~~

Edit a local box. The text editor set in the $EDITOR environment variable will
be invoked to modify the file.

delete <box>
~~~~~~~~~~~~

Delete a local box. The user will be prompted for confirmation, unless the
*--force* option is set.

Available options:

-f, --force   do not prompt user for confirmation

BOX CONFIGURATION FILE FORMAT
=============================

The parameters for a box are defined in a text file which name ends with the
``.conf`` extension. Its syntax is similar to Microsoft Windows INI files.

A commented example is available in
``/usr/share/qemu-tools-elb/box.example.conf``.

=============================
How to Set up Virtual Network
=============================

:Author: Eric Le Bihan

Here are the instructions to set up the network of the host machine, so the
QEMU instance can access the outside world!

With this setup, the virtual machine will be available on the private network
vde.test.local (172.16.1.0/24).

Required Packages
=================

On a Debian GNU/Linux system, install the following packages:

- vde2
- uml-utilities
- dnsmasq

Configuration of TAP/VDE
========================

VDE (`Virtual Distributed Ethernet<http://vde.sourceforge.net>`_) will be used
to share a TAP interface.

Add the following lines to ``/etc/network/interfaces``::

  auto tap0
  iface tap0 inet static
          address 172.16.1.1
          network 172.16.1.10
          netmask 255.255.255.0
          vde2-switch -

Configuration of DHCP/DNS
=========================

Dnsmasq is a lightweight server designed to provide DHCP, DNS and TFTP
services. It will provide them to the machine on the virtual network.

Create the file ``/etc/dnsmasq.d/vde-network``, with the following contents::

  interface=tap0
  dhcp-range=tap0,172.16.1.2,172.16.1.255
  dhcp-host=52:54:00:11:22:33,qemu-x86
  dhcp-host=52:54:00:11:22:34,qemu-arm
  domain=vde.test.local,172.16.1.1,172.16.1.255

Configuration of NAT/Forwarding
===============================

To connect the QEMU instance to the outside world, the traffic must be
forwarded between the interfaces. To enable it, add this line to
``/etc/sysctl.conf``::

  net.ipv4.ip_forward=1

Then, reload the settings using::

  $ sudo sysctl -p

To translate the addresses, Create the file
``/etc/network/if-up.d/vde-network`` with the following lines::

  #!/bin/sh

  case $IFACE in
  	lo|tap0)
  		;;
  	*)
  		/sbin/iptables -t nat -A POSTROUTING -s 172.16.1.1/24 -o $IFACE -j MASQUERADE
  		;;
  esac

Mark this file as being executable::

  $ sudo chmod +x /etc/network/if-up.d/vde-network

If you are using NetworkManager, configure it to handle ifupdown. The file
``/etc/NetworkManager/NetworkManager.conf`` should look like this::

  [main]
  plugins=ifupdown,keyfile

  [ifupdown]
  managed=true

Enable Virtual Network
======================

Before enabling the virtual network, add the current user to the "vde2-net"
group::

  $ sudo useradd $USER vde2-net
  $ newgrp vde2-net

Now, bring up the tap0 interface, restart dnsmasq and NetworkManager if
needed::

  $ sudo ifup tap0
  $ sudo service dnsmasq restart
  $ sudo service network-manager restart

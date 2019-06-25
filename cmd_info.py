#!/usr/bin/env python3
# 
# Copyright (c) 2011 Alon Swartz <alon@turnkeylinux.org>
# 
# This file is part of HubDNS
# 
# HubDNS is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
"""
Display HubDNS information
"""

import sys
import getopt

from hubdns import HubDNS
from registry import registry

def fatal(e):
    print("error: " + str(e), file=sys.stderr)
    sys.exit(1)

def usage(e=None):
    if e:
        print("error: " + str(e), file=sys.stderr)

    print("Syntax: %s" % sys.argv[0], file=sys.stderr)
    print(__doc__.strip(), file=sys.stderr)
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as e:
        usage(e)

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

    if args:
        usage()

    if not registry.sub_apikey and registry.fqdn:
        fatal("not initialized")

    try:
        hubdns = HubDNS(subkey=registry.sub_apikey)
        ipaddress = hubdns.get_ipaddress(registry.fqdn)
    except HubDNS.Error as e:
        fatal(e.description)

    if not ipaddress:
        ipaddress = "-"
    print("%s %s" % (registry.fqdn, ipaddress))

if __name__=="__main__":
    main()

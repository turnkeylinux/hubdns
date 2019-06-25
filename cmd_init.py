#!/usr/bin/python
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
HubDNS initialization

Arguments:

    APIKEY    Cut and paste this from your Hub account's user profile.
    FQDN      Fully Qualified Domain Name to associate

              Example: www.yourdomain.com (your own custom domain)
              Example: yourapp.tklapp.com (free TurnKey sub-domain)

Options:

    --force   Force re-initialization with new APIKEY and FQDN

"""
import os
import sys
import shutil
import getopt

from hubdns import HubDNS
from registry import registry

def fatal(e):
    print("error: " + str(e), file=sys.stderr)
    sys.exit(1)

def usage(e=None):
    if e:
        print("error: " + str(e), file=sys.stderr)

    print("Syntax: %s APIKEY FQDN" % sys.argv[0], file=sys.stderr)
    print(__doc__.strip(), file=sys.stderr)
    sys.exit(1)

def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h", ["help", "force"])
    except getopt.GetoptError as e:
        usage(e)

    apikey = None
    force = False

    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

        if opt == '--force':
            force = True

    if len(args) != 2:
        usage()

    apikey = args[0]
    fqdn = args[1]
    fqdn = fqdn if fqdn.endswith(".") else fqdn + "."

    if not force and registry.sub_apikey:
        fatal("already initialized, use --force to re-initialize")

    try:
        hubdns = HubDNS(apikey=apikey)
        subkey = hubdns.get_subkey()
    except HubDNS.Error as e:
        fatal(e.description)

    try:
        hubdns.capture(fqdn)
    except HubDNS.Error as e:
        fatal(e.description)

    if force:
        if os.path.exists(registry.path):
            shutil.rmtree(registry.path)
            os.mkdir(registry.path)

    registry.sub_apikey = subkey
    registry.fqdn = fqdn

    print("Linked HubDNS to your Hub account and set %s" % fqdn)

if __name__=="__main__":
    main()

# the registry is implemented as a virtual object with properties that are
# mapped directly to files.
# 
# Copyright (c) 2010 Liraz Siri <liraz@turnkeylinux.org>
# 
# This file is part of TKLBAM (TurnKey Linux Backup and Migration).
# 
# TKLBAM is open source software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of
# the License, or (at your option) any later version.
# 

import os
from os.path import *

from paths import Paths
from utils import AttrDict

class UNDEFINED:
    pass

class _Registry(object):
    class Paths(Paths):
        files = ['sub_apikey', 'fqdn']

    def __init__(self, path=None):
        if path is None:
            path = os.environ.get('HUBDNS_REGISTRY', '/var/lib/hubdns')

        if not exists(path):
            os.makedirs(path)
            os.chmod(path, 0700)

        self.path = self.Paths(path)

    @staticmethod
    def _file_str(path, s=UNDEFINED):
        if s is UNDEFINED:
            if not exists(path):
                return None

            return file(path).read().rstrip()

        else:
            if s is None:
                if exists(path):
                    os.remove(path)
            else:
                fh = file(path, "w")
                os.chmod(path, 0600)
                print >> fh, s
                fh.close()

    @classmethod
    def _file_tuple(cls, path, t=UNDEFINED):
        if t and t is not UNDEFINED:
            t = "\n".join([ str(v) for v in t ])

        retval = cls._file_str(path, t)
        if retval:
            return tuple(retval.split('\n'))

    @classmethod
    def _file_dict(cls, path, d=UNDEFINED):
        if d and d is not UNDEFINED:
            d = "\n".join([ "%s=%s" % (k, v) for k, v in d.items() ])

        retval = cls._file_str(path, d)
        if retval:
            return AttrDict([ v.split("=", 1) for v in retval.split("\n") ])

    def sub_apikey(self, val=UNDEFINED):
        return self._file_str(self.path.sub_apikey, val)
    sub_apikey = property(sub_apikey, sub_apikey)

    def fqdn(self, val=UNDEFINED):
        return self._file_str(self.path.fqdn, val)
    fqdn = property(fqdn, fqdn)

registry = _Registry()

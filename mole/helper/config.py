#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.helper import AttrDict

try:
    from ConfigParser import RawConfigParser as cp
    from ConfigParser import NoSectionError
except ImportError:
    from configparser import RawConfigParser as cp
    from configparser import NoSectionError

class MoleConfig(object):
    def __init__(self, f=None):
        self._values = cp()
        if f: self._values.read(f)

    def sections(self):
        return self._values.sections()

    def read(self, f):
        self._values.read(f)

    def __getattr__(self, item):
        if self._values.has_section(item):
            return AttrDict(self._values.items(item))
        else:
            return None

    def __iter__(self):
        for x in self._values.sections():
            yield ( x, AttrDict(self._values.items(x)) )

    def items(self, section):
        return self._values.items(section)

    def __repr__(self):
        return repr(dict([x for x in self]))


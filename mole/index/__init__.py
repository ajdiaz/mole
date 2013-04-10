#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import threading
from setproctitle import setproctitle

from mole.output import Output


DEFAULT_INDEX_PATH = "/var/lib/mole/index"


class IndexConfigError(Exception):
    """Raise an error when create an :class:`Index` object from config
    dictionary."""


class Index(Output):
    """The Index models a generic index engine."""

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Index must be a callable")

    def search(self, query):
        raise NotImplementedError("Index must have a search method")

    @classmethod
    def from_type(cls, index_type, *args, **kwargs):
        mod = __import__("mole.index.%s" % index_type,
                         globals(),
                         locals(),
                         [ "Index%s" % index_type.title() ])
        kls = getattr(mod, "Index%s" % index_type.title())
        return kls(*args, **kwargs)


    @classmethod
    def from_config(cls, config):
        for name, values in config:
            if not values.get("type", None):
                values.type = "basic"
            tip = values.type
            del values["type"]
            yield (name, Index.from_type(tip, **values))

    def set_offset(self, offset):
        pass

    def get_offset(self):
        return 0

    def __repr__(self):
        return str(self.__class__.__name__)

class ThreadIndex(threading.Thread):
    def __init__(self, name, plan):
        threading.Thread.__init__(self, name=name)
        self.name = name
        self.plan = plan

    def kill(self):
        self.stop()

    def run(self):
        setproctitle("mole index:%s" % self.name)
        self.plan(False)


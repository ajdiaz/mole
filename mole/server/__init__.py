#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

class Server(object):
    @property
    def stopped(self):
        return self._stop.isSet()

    @classmethod
    def from_type(cls, server_type, *args, **kwargs):
        mod = __import__("mole.server.%s" % server_type,
                         globals(),
                         locals(),
                         [ "Server%s" % server_type.title() ])
        kls = getattr(mod, "Server%s" % server_type.title())
        return kls(*args, **kwargs)


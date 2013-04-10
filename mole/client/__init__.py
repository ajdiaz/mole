#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

class Client(object):
    @classmethod
    def from_type(cls, client_type, *args, **kwargs):
        mod = __import__("mole.client.%s" % client_type,
                         globals(),
                         locals(),
                         [ "Client%s" % client_type.title() ])
        kls = getattr(mod, "Client%s" % client_type.title())
        return kls(*args, **kwargs)


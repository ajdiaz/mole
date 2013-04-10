#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

class Plotter(object):
    """The Plotter splits logs into logical lines according to an
    expression."""

    BUFSIZE = 1024
    REQUIRE_INPUT = True

    @classmethod
    def from_type(cls, type, *args, **kwargs):
        mod = __import__("mole.plotter.%s" % type,
                         globals(),
                         locals(),
                         [ "Plotter%s" % type.title() ])
        kls = getattr(mod, "Plotter%s" % type.title())
        return kls(*args, **kwargs)

    @classmethod
    def from_config(cls, config):
        for name, values in config:
            if not values.get("type", None):
                values.type = "basic"
            tip = values["type"]
            del values["type"]
            yield (name, Plotter.from_type(tip, **values))

    def __repr__(self):
        return str(self.__class__.__name__)

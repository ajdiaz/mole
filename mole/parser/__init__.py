#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

class Parser(object):
    """The Parser convert logic lines into events."""

    REQUIRE_PLOTTER = True

    @classmethod
    def from_type(cls, type, *args, **kwargs):
        mod = __import__("mole.parser.%s" % type,
                         globals(),
                         locals(),
                         [ "Parser%s" % type.title() ])
        kls = getattr(mod, "Parser%s" % type.title())
        return kls(*args, **kwargs)

    @classmethod
    def from_config(cls, config):
        for name, values in config:
            if not values.get("type", None):
                values.type = "basic"
            tip = values["type"]
            del values["type"]
            yield (name, Parser.from_type(tip, **values))

    def __repr__(self):
        return str(self.__class__.__name__)

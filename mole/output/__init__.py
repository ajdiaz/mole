#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

class Output(object):
    """The Output is the endpoint for a pipeline and usually represents its
    contents in a human or machine readable form"""

    @classmethod
    def from_type(cls, output_type, *args, **kwargs):
        mod = __import__("mole.output.%s" % output_type,
                         globals(),
                         locals(),
                         [ "Output%s" % output_type.title() ])
        kls = getattr(mod, "Output%s" % output_type.title())
        return kls(*args, **kwargs)

    def __repr__(self):
        return str(self.__class__.__name__)

class OutputError(Exception):
    """A generic output error."""


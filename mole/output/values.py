#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.output import Output, OutputError
from mole.event import Event

class OutputValues(Output):

    def __init__(self, fields=[]):
        self.fields = fields

    def __call__(self, pipeline):
        for event in pipeline:
            if not isinstance(event, Event):
                raise OutputError("Unable to output without parser. Offending type is %s" % event.__class__)
            yield " ".join(map(lambda (x,y):'%s="%s"' % (x,y),
                               filter(lambda (x,y):not self.fields or x in self.fields, [ x for x in event ])))


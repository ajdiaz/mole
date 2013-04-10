#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.output import Output

class OutputBasic(Output):
    def __call__(self, pipeline, heads=True):
        for event in pipeline:
            if isinstance(event, str) or \
               isinstance(event, unicode):
                yield event
            elif event["_raw"]:
                yield event["_raw"]
            else:
                yield " ".join([ '%s="%s"' % x for x in event ])


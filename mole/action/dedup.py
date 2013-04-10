#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action, ActionSyntaxError


class ActionDedup(Action):
    """This action dedup(licate) values in pipeline.

    :param `fields`: a list of fields to be dedup(licate)
    """

    REQUIRE_PLOTTER = True

    def __init__(self, fields=["_raw"]):
        self.fields = fields
        self._field = None

        if len(self.fields) == 1 and self.fields[0] == "_raw":
            self._field = True
        else:
            self.REQUIRE_PARSER = True

    def __call__(self, pipeline):
        last = []

        for event in pipeline:
            if self._field:
                if last and last == event:
                    continue
                else:
                    last = event
                    yield event
            else:
                if event.has_all(self.fields):
                    field_values = map(lambda x:(x,event[x]), self.fields)
                    if field_values in last:
                        continue
                    else:
                        last.append(field_values)
                        yield event




#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action, ActionSyntaxError

class ActionRename(Action):
    """This action rename a field.

    :param `field`: the field name to be renamed.
    :param `newname`: the new name to be used for this field
    """

    REQUIRE_PARSER = True

    def __init__(self, field, newname):
        self.field = field[0]
        self.newname = newname[0]

    def __call__(self, pipeline):
        for event in pipeline:
            if self.field in event:
                _value = event[self.field]
                event[self.newname] = _value
                del event[self.field]
            yield event


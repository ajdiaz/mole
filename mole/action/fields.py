#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action

class ActionFields(Action):
    """This action return only a subset of the specified fields.

    :param `fields`: a :class:`list` of fields to be included
        in output.
    """
    REQUIRE_PARSER = True

    def __init__(self, fields=[]):
        self.fields = fields

    def __call__(self, pipeline):
        for event in pipeline:
            new_event = Event()
            for field in self.fields:
                if field in event:
                    new_event[field] = event[field]
                    yield new_event


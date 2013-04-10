#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action, ActionSyntaxError

class ActionMax(Action):
    """This action get the max value item in pipeline.

    :param `fields`: a :class:`list` with fields to get min value.
    :param `groups`: a :class:`list` which provides the items to group
        results.
    """

    REQUIRE_PARSER = True

    def __init__(self, fields=[], groups=[]):
        self.fields = fields
        self.groups = groups

        if not self.fields:
            raise ActionSyntaxError("No fields provided")


    def __call__(self, pipeline):
        response = {}
        for event in pipeline:
            if self.groups:
                for group in self.groups:
                    if group in event:
                        _key = (group, event[group])
                        if _key not in response:
                            response[_key]={}
                        for field in self.fields:
                            _x = response[_key]
                            if(_x.get(field,None)):
                                _x[field] = max(_x[field],event[field])
                            else:
                                _x[field] = event[field]
            else:
                for field in self.fields:
                    if(response.get(field,None)):
                        response[field] = max(response[field],event[field])
                    else:
                        response[field] = event[field]


        if self.groups:
            for (gkey,gval) in response:
                for f in response[(gkey,gval)]:
                   yield Event({gkey:gval,
                                ("max(%s)" % f):
                                response[(gkey,gval)][f]})
        else:
            for key in response:
                yield Event({("max(%s)" % key):response[key]})


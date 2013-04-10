#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action, ActionSyntaxError

class ActionSum(Action):
    """This action sum items in pipeline.

    :param `fields`: a :class:`list` with fields to be sum in. If
        field is not present the line will be not sum in, also if
        none fields is provided all lines are counted.
    :param `groups`: a :class:`list` which provides the items to group
        count results.
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
                                _x[field] += float(event[field])
                            else:
                                _x[field] = float(event[field])
            else:
                for field in self.fields:
                    if(response.get(field,None)):
                        response[field] += float(event[field])
                    else:
                        response[field] = float(event[field])


        if self.groups:
            for (gkey,gval) in response:
                for f in response[(gkey,gval)]:
                   yield Event({gkey:gval,
                                ("sum(%s)" % f):
                                response[(gkey,gval)][f]})
        else:
            for key in response:
                yield Event({("sum(%s)" % key):response[key]})


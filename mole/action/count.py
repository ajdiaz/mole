#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action


class ActionCount(Action):
    """This action counts items in pipeline."""

    REQUIRE_PLOTTER = True

    def __init__(self, fields=[], groups=[]):
        """Create a new count action.

        :param `fields`: a :class:`list` with fields to be counted in. If
            field is not present the line will be not counted in, also if
            none fields is provided all lines are counted.
        :param `groups`: a :class:`list` which provides the items to group
            count results.
        """
        self.fields = fields
        self.groups = groups

        if fields or groups:
            self.REQUIRE_PARSER = True

    def __call__(self, pipeline):
        if not self.fields and not self.groups:
            count = 0
            for x in pipeline:
                count +=1
            yield Event({"count":count})

        else:
            response = {}
            for event in pipeline:
                if self.groups:
                    for group in self.groups:
                        if group in event:
                            _key = (group, event[group])
                            if _key not in response:
                                response[_key]={}
                            for field in self.fields:
                                if(response[_key].get(field,None)):
                                    response[_key][field] += 1
                                else:
                                    response[_key][field] = 1
                else:
                    for field in self.fields:
                        if(response.get(field,None)):
                            response[field] += 1
                        else:
                            response[field] = 1


            if self.groups:
                for (gkey,gval) in response:
                    for f in response[(gkey,gval)]:
                        yield Event({gkey:gval, ("count(%s)" % f): response[(gkey,gval)][f]})
            else:
                for key in response:
                    yield Event({("count(%s)" % key):response[key]})

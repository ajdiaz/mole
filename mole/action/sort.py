#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action, ActionSyntaxError

sort_asc = lambda x,y:cmp(x,y)
sort_des = lambda x,y:cmp(y,x)

class ActionSort(Action):
    """This action sort values in pipeline.

    :param `fields`: a :class:`list` with the fields names to used as
        sort key.
    """

    REQUIRE_PARSER = True

    def __init__(self, fields):
        self.fields = fields

        if self.fields is None:
            raise ActionSyntaxError("No fields provided")

    def _sort(self, evx, evy):
        for field in self.fields:
            if field[0] == "-":
                field = field[1:]
                sfunc = sort_des
            else:
                sfunc = sort_asc

            if evx[field] and not evy[field]:
                return -1
            if not evx[field] and evy[field]:
                return 1

            if evx[field] == evy[field]:
                continue

            return sfunc(evx[field],evy[field])
        return 0

    def __call__(self, pipeline):
        return sorted(pipeline,self._sort)

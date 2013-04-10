#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action, ActionSyntaxError
from mole.helper.timeformat import Timespan

def func_avg(field, events):
    return reduce(lambda x,y:x+y, map(lambda x:float(x[field]), events)) / len(events)

def func_min(field, events):
    return reduce(min,  map(lambda x:float(x[field]), events))

def func_max(field, events):
    return reduce(max,  map(lambda x:float(x[field]), events))

class ActionTimespan(Action):
    """This action consolidate values over a time span."""

    REQUIRE_PARSER = True

    def __init__(self, field, span=["1h"], func=["avg"]):
        """Create a new timespan action

        :param `field`: the field to use in operation (the value to be
            consolidated.)
        :param `span`: the span for consolidation.
        :param `func`: the function to use in consolidation.
        """
        self.field = field[0]
        self.span  = Timespan(span[0])

        try:
            self.func  = __import__("mole.action.timespan",
                                    globals(),
                                    locals(),
                                    [ "func_%s" % func[0] ])
        except ImportError:
            raise ActionSyntaxError("unable to import timespan module")

        try:
            self.func = getattr(self.func, "func_%s" % func[0])
        except AttributeError:
            raise ActionSyntaxError("invalud consolidation function")

    def __call__(self, pipeline):
        ret = []
        field = self.field
        for event in pipeline:
            if len(ret) and (event.time - ret[0].time) > self.span.seconds:
                yield Event({field: self.func(field,ret),"_time": ret[0]["_time"]})
                ret = [ event ]
            else:
                ret.append(event)

        if len(ret) and (event.time - ret[0].time) > self.span.seconds:
            yield Event({field: self.func(field,ret),"_time": ret[0]["_time"]})



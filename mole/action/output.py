#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action, ActionSyntaxError
from mole.output import Output

class ActionOutput(Action):
    """This action get events in pipeline and return a string output.

    :param `type`: a list with string representation of the output to be loaded.
    """

    REQUIRE_PLOTTER = True

    def __init__(self, type=["basic"],*args, **kwargs):
        if len(type) > 1:
            raise ActionSyntaxError("output command only allow one single parameter")
        self.type = Output.from_type(type[0], *args, **kwargs)


    def __call__(self, pipeline):
        return self.type(pipeline)


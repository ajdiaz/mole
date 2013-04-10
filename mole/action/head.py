#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action, ActionSyntaxError

class ActionHead(Action):
    """This action get the head values in pipeline.

    :param `num`: a :class:`list` with the number of lines to expose in
            pipeline.
    """

    REQUIRE_PLOTTER = True

    def __init__(self, num=[10]):
        self.num = int(num[0])

        if self.num is None:
            raise ActionSyntaxError("No head limit provided")


    def __call__(self, pipeline):
        for event in pipeline:
            if self.num:
                yield event
                self.num -= 1
            else:
                break


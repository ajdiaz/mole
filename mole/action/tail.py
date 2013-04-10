#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.helper import QueueList
from mole.action import Action, ActionSyntaxError

class ActionTail(Action):
    """This action get the tail values in pipeline.

    :param `num`: a :class:`list` with the number of lines to expose in
        pipeline.
    """

    REQUIRE_PLOTTER = True

    def __init__(self, num=[10]):
        self.num = int(num[0])

        if self.num is None:
            raise ActionSyntaxError("No tail limit provided")


    def __call__(self, pipeline):
        ret = QueueList(self.num)

        for event in pipeline:
            ret.append(event)

        return ret



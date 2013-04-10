#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.action import Action, ActionSyntaxError
from mole.parser import Parser

class ActionParser(Parser):
    """This action parse the pipeline using specific parser

    :param `name`: a list with string representation of the parser to be loaded.
    """

    def __init__(self, name,*args, **kwargs):
        if len(name) > 1:
            raise ActionSyntaxError("parser command only allow one single parameter")

        self.item = None
        self.name = name[0]

    def _init_item(self):
        if self.item is None:
            if self.context:
                self.item = self.context[self.name].parser
            else:
                self.item = []

    def __iter__(self):
        return iter(self.item)

    def __call__(self, pipeline):
        self._init_item()
        return self.item(pipeline)

    def get_object(self):
        return self.context[self.name]


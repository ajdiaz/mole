#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole import AttrDict
from mole.event import Event
from mole.parser import Parser
import re

class ParserBasic(Parser):
    """Parse a logic line splitted into key=value elements."""

    def __init__(self):
        self.re = re.compile(r'((?:\\.|[^=\s]+)*)=("(?:\\.|[^"\\]+)*"|(?:\\.|[^\s"\\]+)*)')

    def __call__(self, pipeline):
        for line in pipeline:
            ev_dict = dict(self.re.findall(line))
            ev_dict["_raw"] = line.rstrip("\r\n")
            yield Event(ev_dict)





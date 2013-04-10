#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import re

from mole.parser import Parser
from mole.helper import AttrDict
from mole.event import Event, EventError


class ParserRegex(Parser):
    """Parse a logic line using regular expression."""

    def __init__(self, regex):
        self.re = re.compile(regex)

    def __call__(self, pipeline):
        for line in pipeline:
            line = line.rstrip("\r\n")
            ev_dict = self.re.match(line)
            if ev_dict:
                ev_dict = ev_dict.groupdict()
            else:
                ev_dict = {}
            ev_dict["_raw"] = line
            try:
                _x = Event(ev_dict)
                yield _x
            except EventError:
                continue


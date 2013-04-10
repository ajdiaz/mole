#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import socket
from setproctitle import setproctitle

from mole.event import Event
from mole.client import Client
from mole.plotter import Plotter
from mole.helper.netstring import NetString

try:
    import cPickle as pickle
except ImportError:
    import pickle


class PlotterNetwork(Plotter):
    """Basic network plotter which read netstrings from a source."""

    def __call__(self, pipeline):
        for event in pipeline:
            netstr = NetString.from_buffer(event)
            netstr = netstr.decode()
            if isinstance(netstr, dict):
                yield Event(netstr)
            else:
                yield netstr


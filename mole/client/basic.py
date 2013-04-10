#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import socket
from setproctitle import setproctitle

from mole.event import Event
from mole.client import Client
from mole.planner import Planner
from mole.output import Output
from mole.input.file import InputFileWrapper
from mole.plotter.network import PlotterNetwork

try:
    import cPickle as pickle
except ImportError:
    import pickle


class ClientBasic(Client):
    """Basic network client which read netstrings from a source."""

    def __init__(self, config):
        self.addr = (config.host, config.port)
        self._stop = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self, search):
        return self(search)

    def connect(self):
        self.sock.connect(self.addr)

    def __call__(self, search):
        try:
            self.connect()
            self.sock.sendall(search)

            f = self.sock.makefile()

            self.plan = Planner()
            self.plan.add(InputFileWrapper(f))
            self.plan.add(PlotterNetwork())
            self.plan.add(Output.from_type("basic"))

            return self.plan(False)
        finally:
            self._stop = True
            self.sock.close()

    def cancel(self):
        self.sock.close()


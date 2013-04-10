#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import socket
from setproctitle import setproctitle

from mole.event import Event
from mole.client import Client
from mole.helper.netstring import NetString

try:
    import cPickle as pickle
except ImportError:
    import pickle


class InputNetwork(RawInput, Input):
    """Basic network imput which read netstrings from a source."""

    def __init__(self, addr):
        self.addr = addr
        self._stop = False

    def connect(self):
        self.sock = socket.socket()
        self.sock.connect(self.addr)

    def close(self):
        self.sock.close()

    def tell(self):
        return

    def seek(self, bytes):
        pass

    def run(self, search):
        return self(search)

    def __iter__(self, search):
        try:
            self.connect()
            self.sock.sendall(search)

            f = self.sock.makefile()

            for event in f:
                if self._stop:
                    break
                netstr = NetString.from_buffer(event)
                yield Event(netstr.decode())
        finally:
            self._stop = True
            self.sock.close()

    def cancel(self):
        self.sock.close()


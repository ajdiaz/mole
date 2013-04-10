#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.event import Event
from mole.output import Output
from mole.helper.netstring import NetString

try:
    import cPickle as pickle
except ImportError:
    import pickle


class OutputSerialize(Output):
    def __call__(self, pipeline, heads=None):
        for event in pipeline:
            if isinstance(event, Event):
                yield str(NetString(pickle.dumps(dict(event))))
            else:
                yield str(NetString(pickle.dumps(event)))


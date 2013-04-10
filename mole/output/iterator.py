#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.output import Output

class OutputIterator(Output):
    def __call__(self, pipeline, heads=None):
        return pipeline


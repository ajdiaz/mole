#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.input import Input

class InputFile(file, Input):
    """Dummy class which wrapper a file."""


class InputFileWrapper(Input):
    def __init__(self, f):
        self.f = f

    def close(self):
        self.f.close()

    def __iter__(self):
        return iter(self.f)

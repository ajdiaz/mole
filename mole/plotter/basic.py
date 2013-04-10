#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import os

from mole.plotter import Plotter

class PlotterBasic(Plotter):
    """The basic plotter split a stream into lines, using a number of chars
    as separation marks, usually the newline character or similar."""

    def __init__(self, char=os.linesep, bufsize=1024):
        """Create a new :class:`PlotterBasic` object, which split lines when
        find a character into the char :class:`list`.

        :param `char`: a :class:`list` constains valid separator characters.
            By default use separation mark provided by the operating system
        :param `bufsize`: the buffer chunk size in bytes, buy default
            1024.
        """
        self.char = char
        self.BUFSIZE = bufsize

    def __call__(self, stream):
        """Plotter processor.

        :param:`stream` a stream which a read method is available.
        """
        spool = ""
        chunk = ""

        if self.char == os.linesep:
            # Native iterator is faster
            for x in stream:
                print x.__class__
                yield x.rstrip(self.char)
        else:
            # TODO: implement in C with binding or port to python3 to use
            # newline file attr.
            chunk = stream.read(self.BUFSIZE)
            while chunk:
                for b in chunk:
                    if b in self.char:
                        yield spool.rstrip(self.char)
                        spool = ""
                    else:
                        spool += b
                chunk = stream.read(self.BUFSIZE)



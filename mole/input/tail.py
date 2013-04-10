#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from os import stat

from mole.input import Input

"""This module provides an input which read a file using buffering, as tailf
does, even handling file rotations.
"""

""" $Id: filetail.py 1512 2011-05-20 16:14:29Z morrissj $

Python3 module for tailing a file such as a system log that grows continuously.
Transparently handles files that get rotated or trucated.
Inspired by the Perl File::Tail module.

A simple algorithm is used to dynamically sleep when no new data is available in
the file. The longer the amount of time goes by w/o new data the longer the
sleep interval will be (up to "max_interval") and starts at "interval".

Example:
    from filetail import FileTail
    tail = FileTail("/var/log/syslog")
    for line in tail:
        # do something
        pass

"""

import os
import sys
from stat import *
from math import floor
from time import sleep, time

class FileTail(object):
    """
    Tail a file, even if its rotated/truncated.
    Inspiration came from the perl module File::Tail.
    """

    def __init__(self,
                 file,                  # filename to monitor
                 start_pos="end",       # where to initially start reading from
                 #max_buffer_size=16384, # Max buffer size hint (Not exact; @see file.readlines)
                 interval=0.1,          # sleep time to wait if no data is present (dynamically changes)
                 #min_interval=0.01,     # min sleep time
                 max_interval=5,        # max sleep time 
                 max_wait=60,           # max time to wait with no data before reopening file
                 reopen_check="inode",  # how to check if file is different (inode or time) - inode does not work on win32
                ):

        self.start_pos = start_pos
        self.reopen_check = reopen_check
        self.max_wait = max_wait
        self.max_interval = max_interval
        self.interval = interval
        if self.interval > self.max_interval:
            self.interval = self.max_interval

        # will throw exception if it fails... caller should intercept
        self.open(file, start_pos=start_pos)

        # initialize some internal vars
        self._buffer = []
        self.last_time = time()
        self.last_count = 0

    def open(self, file, start_pos="head"):
        """Open the file to tail and initialize our state."""
        fh = open(file, "r")

        # seek to the initial position in the file we want to start reading
        if start_pos == "end" or start_pos == "tail":
            fh.seek(0, os.SEEK_END)                       # End of file
        elif start_pos == "start" or start_pos == "head":
            #fh.seek(0, os.SEEK_SET)                      # Beginning of file
            pass
        elif start_pos is not None:
            if start_pos >= 0:                            # Absolute position
                fh.seek(start_pos, os.SEEK_SET)
            else:                                         # Absolute position (from end)
                fh.seek(abs(start_pos), os.SEEK_END)

        # if we passed the end of the file rewind to the actual end.
        # This avoids a potential race condition if the file was being rotated
        # in the process of opening the file. Not sure if this can actually
        # happen, but better safe than sorry.
        pos = fh.tell()
        if pos > os.stat(file)[ST_SIZE]:
            pos = fh.tell()

        self.fh = fh
        self.pos = pos
        self.stat = os.fstat(fh.fileno())
        self.file = file

    def reopen(self):
        """
        Attempt to reopen the current file. If it doesn't appear to have
        changed (been rotated) then the current file handle is not changed.
        """

        #print("Reopening", self.file, "...", end="")

        # if we don't have an opened file already then try to open it now
        if not self.fh or self.fh.closed:
            try:
                self.open(self.file, start_pos="head");
            except IOError:
                return False
            return True

        # save current values
        fh = self.fh
        pos = self.pos
        cur = self.stat

        # reopen same file
        try:
            self.open(self.file, "head")
        except IOError as e:
            return False

        new = self.stat
        if (
            (self.reopen_check == 'inode' and new.st_ino == cur.st_ino)
            or
            (self.reopen_check == 'time' and new.st_mtime <= floor(self.last_time) and new.st_size == pos)
           ):
            self.fh = fh
            self.pos = pos
            self.stat = cur
            return False

        return True

    def __iter__(self):
        """
            Return iterator to support:
                for line in filetail:
                    print line
        """
        self.wait_count = 0
        return self


    def __next__(self):
        """Interator "next" call."""
        return self.next()


    def next(self):
        line = None
        self.wait_count = 0

        # low CPU (probably same as the block below this, but ALLOWS tell()!
        while not line:
            line = self.fh.readline()
            if line != "":
                # track the time we received new data and how much
                self.last_time = time()
                self.last_count = 1
            else:
                self.wait()

        return line

    # wait for X seconds. The sleep interval is dynamically predicted based on
    # how much was previously read. The predicted interval will never be more
    # than max_interval. If enough time passes w/o any new data the file will
    # be reopened and checked.
    def wait(self):
        if self.wait_count == 0:
            self.pos = self.fh.tell()
            self.stat = os.fstat(self.fh.fileno())

        self.wait_count += 1
        elapsed = time() - self.last_time

        # if we've waited long enough try to reopen the file, if that returns
        # true then we're done here and we do not sleep.
        if elapsed >= self.max_wait:
            self.last_time = time()
            if self.reopen():
                return

        # determine delay value. Delay is longer based on total time passed
        # note: currently last_count is always 1.
        if self.last_count:
            #delay = (time() - self.last_time) / self.last_count
            delay = elapsed
        else:
            delay = self.interval

        # don't delay too long
        if delay > self.max_interval:
            delay = self.max_interval

        sleep(delay)

    def tell(self):
        return self.fh.tell()

    def seek(self, pos):
        self.fh.seek(pos)

# end of FileTail class


class InputTail(Input):
    """The Tail monitor input."""

    def __init__(self, name, interval=5):
        self.name     = name
        self.interval = interval
        self.tail     = FileTail(name, start_pos="start", max_interval=interval)

    def __iter__(self):
        return iter(self.tail)

    def tell(self):
        return self.tail.tell()

    def seek(self, pos):
        self.tail.seek(pos)


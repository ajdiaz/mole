#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import os

__all__ = [ "timeformat", "config", "eval" ]

class AttrDict(dict):
    """Wrapper dictionary which allows to access items using getattr."""

    def __getattr__(self, item):
        if item[0] == "_":
            return getattr(super(AttrDict, self), item)
        else:
            return self[item]
    def __setattr__(self, item, value):
        if item[0] == "_":
            setattr(super(AttrDict, self), item, value)
        else:
            self[item] = value

class AutoDict(dict):
    """Wrapper dictionary which allows to create items where accessing."""

    def __getitem__(self, item):
        parent = super(AutoDict, self).get(item, None)
        if parent:
            return parent
        else:
            self[item]={}
            return super(AutoDict, self).get(item)

class QueueList(list):
    """A type of :class:`list` which has a limit number of elements with LRU
    replacement algoritm."""

    def __init__(self, maxitems=10):
        self.maxitems = maxitems
        super(QueueList, self).__init__()

    def __setitem__(self, item, value):
        if item >= self.maxitems:
            raise IndexError()
        else:
            super(QueueList, self).__setitem__(item, value)

    def __getitem__(self, item):
        if item >= self.maxitems:
            raise IndexError()
        else:
            return super(QueueList, self).__getitem__(item, value)

    def append(self, item):
        super(QueueList, self).append(item)
        while len(self) > self.maxitems:
            del self[0]


def read_conf(path):
    """Helper function which read a configuration directory and return
    elments defined there."""

    from mole.helper.config import MoleConfig
    from mole.input import Input
    from mole.index import Index
    from mole.parser import Parser
    from mole.plotter import Plotter
    from mole.element import Element

    config = AttrDict()

    # Read config file
    config.input   = MoleConfig(os.path.join(path,"input.conf"))
    config.index   = MoleConfig(os.path.join(path,"index.conf"))
    config.parser  = MoleConfig(os.path.join(path,"parser.conf"))
    config.plotter = MoleConfig(os.path.join(path,"plotter.conf"))
    config.element = MoleConfig(os.path.join(path,"element.conf"))

    # Convert config files to objects
    config.input   = dict(Input.from_config(config.input))
    config.index   = dict(Index.from_config(config.index))
    config.parser  = dict(Parser.from_config(config.parser))
    config.plotter = dict(Plotter.from_config(config.plotter))
    config.element = [ x for x in Element.from_config(config.element, config) ]

    return config.element


def read_args(config, commands):
    """Read arguments using config dictionary::

    >>> read_args([ ("-C", "--config", "read config file", str, None) ], ["search"])
    """
    import argparse

    cmdopt = argparse.ArgumentParser(
            description="Mole: smartest operational tool.",
            epilog="©2012  Andrés J. Díaz <ajdiaz@connectical.com>")

    for short, lng, desc, type, default in config:
        cmdopt.add_argument(short, lng, action="store",
                                        dest=lng.strip("-"),
                                        help=desc,
                                        type=type,
                                        default=default)
    for command in commands:
        cmdopt.add_argument(command)

    return cmdopt.parse_args()


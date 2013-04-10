#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

class Script(object):
    """Generic class to model a command line script."""

    def __call__(self):
        """Run the script."""
        raise NotImplementedError()



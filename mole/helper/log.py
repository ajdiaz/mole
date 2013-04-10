#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import sys
import logging

LOG_FORMAT = '[%(asctime)s] %(message)s'

logging.basicConfig(format=LOG_FORMAT,
                    stream=sys.stderr,
                    level=logging.DEBUG)

def getLogger(ident="mole"):
    """Singleton to get an unique log object across any
    caller class or thread."""

    return logging.getLogger(ident)


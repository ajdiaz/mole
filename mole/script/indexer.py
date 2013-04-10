#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""The scripts module provide and endpoint for console scripts.
"""

import os
import signal
import argparse

from setproctitle import setproctitle

from mole.server import Server
from mole.script import Script
from mole.helper import read_conf
from mole.helper import read_args


DEFAULT_DIRCFG = "/etc/mole/"


class ScriptIndexer(object):
    """Main class to handle the indexer script"""

    def __call__(self):
        """Run the script"""
        args = read_args([
            ("-C", "--config", "Use specific config dir", str, None)
        ],[])

        if not args.config:
            args.config = os.getenv("MOLE_CONFIGDIR", None) or DEFAULT_DIRCFG

        config = read_conf(args.config)
        self.indexer  = Server.from_type("index", config)

        self.indexer.run()
        try:
            signal.pause()
        except KeyboardInterrupt:
            self.indexer.cancel()


def main():
    indexer = ScriptIndexer()
    indexer()

if __name__ == "__main__":
    main()


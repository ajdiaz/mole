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
from mole.helper import AttrDict


DEFAULT_DIRCFG = "/etc/mole/"


class ScriptSeeker(object):
    """Main class to handle the seeker script"""

    def __call__(self):
        """Run the script"""
        args = read_args([
            ("-C", "--config", "Use specific config dir", str, None),
            ("-p", "--port", "Use specific port to listen", int, 9900),
            ("-H", "--host", "Use the host address to bind to", str, "127.0.0.1")
        ],[])

        if not args.config:
            args.config = os.getenv("MOLE_CONFIGDIR", None) or DEFAULT_DIRCFG

        config = AttrDict({
            "server": AttrDict({"host": args.host, "port": args.port }),
            "config": read_conf(args.config)
        })
        self.seeker  = Server.from_type("seeker", config)

        self.seeker.run()
        try:
            signal.pause()
        except KeyboardInterrupt:
            self.seeker.cancel()


def main():
    seeker = ScriptSeeker()
    seeker()


if __name__ == "__main__":
    main()


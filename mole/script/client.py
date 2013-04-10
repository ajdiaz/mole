#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

"""The scripts module provide and endpoint for console scripts.
"""

import os
import sys
import signal
import argparse

from setproctitle import setproctitle

from mole.client import Client
from mole.script import Script
from mole.planner import Planner
from mole.helper import read_conf
from mole.helper import read_args
from mole.helper import AttrDict


DEFAULT_DIRCFG = "/etc/mole/"


class ScriptClient(object):
    """Main class to handle the client script"""

    def __call__(self):
        """Run the script"""
        args = read_args([
            ("-p", "--port", "Use specific port to connect", int, 9900),
            ("-H", "--host", "Use the host address to connect to", str, "127.0.0.1"),
        ], ["search"])

        config = AttrDict({
            "client": AttrDict({"host": args.host, "port": args.port }),
            "search": args.search
        })

        self.client  = Client.from_type("basic", config.client)

        try:
            for x in self.client.run(config.search):
                print x
        except KeyboardInterrupt:
            self.client.cancel()


def main():
    client = ScriptClient()
    client()


if __name__ == "__main__":
    main()


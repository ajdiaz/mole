#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import shlex

from mole.input import Input
from mole.index import Index
from mole.parser import Parser
from mole.action import Action
from mole.output import Output
from mole.plotter import Plotter
from mole.helper import AttrDict
from mole.action.output import ActionOutput
from mole.action.input import ActionInput

# There is an ugly exception for the output serializer. So since we want to
# send data over the network using different datamodel we need to allow the
# OutputSerializer to be enqueued even if an output is already present in
# planner.
from mole.output.serialize import OutputSerialize


KEYWORDS = [ "by", "group", "as", "or", "OR" ]
RESERVED = "()[]:,%+-*^/{}=<>."


class Planner(object):
    """The planner is the responsible to get the fastest execution plan for
    a number of actions over the pipeline."""

    def __init__(self):
        self.queue = []

    def add(self, pipe):
        """Add a new action in the pipeline.

        :param `pipe`: the new object for the pipeline to be addeed.

        .. note:: The object passed as argumetn must implement
            a ``__call__`` method.
        """
        for i in range(len(self.queue)):

            if isinstance(pipe, Parser):
                if getattr(self.queue[i],"REQUIRE_PARSER",False):
                    self.queue.insert(i, pipe)
                    return

            if isinstance(pipe, Plotter):
                if getattr(self.queue[i],"REQUIRE_PLOTTER",False):
                    self.queue.insert(i, pipe)
                    return

            if isinstance(pipe, Input):
                if getattr(self.queue[i],"REQUIRE_INPUT",False):
                    self.queue.insert(i, pipe)
                    return


        if self.queue and isinstance(self.queue[-1], Index) and not isinstance(pipe, Output):
            self.queue.insert(len(self.queue)-1, pipe)
        else:
            self.queue.append(pipe)

        for i in range(len(self.queue)):
            if i != 0 and isinstance(self.queue[i], Parser):
                if isinstance(self.queue[i-1], Plotter):
                    continue
                if isinstance(self.queue[i-1], Input):
                    continue
                if isinstance(self.queue[i-1], ActionInput):
                    continue

                del self.queue[i]

    def has_input(self):
        """Return True if the pipeline has an input object (or input
        action).
        """
        return isinstance(self.queue[0],Input) or \
               isinstance(self.queue[0],ActionInput)

    def has_output(self):
        """Return True if the pipeline has an output object (or output
        action).
        """
        return isinstance(self.queue[-1],Output) or \
               isinstance(self.queue[-1],ActionOutput)

    def add_input(self, input):
        """Add or replace (if exists) the input object in the pipeline using
        the new one.

        :param `input`: The new :class:`Input` object to be added.
        """
        if not isinstance(self.queue[0],Input) and \
           not isinstance(self.queue[0],ActionInput):
            self.queue.insert(0, input)

    def add_output(self, output):
        """Add or replace (if exists) the output object in the pipeline
        using the new one.

        :param `output`: The new :class:`Output` object to be added.
        """
        if isinstance(output,OutputSerialize):
            self.queue.append(output)
        elif not isinstance(self.queue[-1],Output) and \
             not isinstance(self.queue[-1],ActionOutput):
                 self.queue.append(output)

    def get_input(self):
        """Return the input object in the pipeline or raise a ValueError if
        not present.

        The returned object will be a :class:`Input` or
        :class:`ActionInput`.
        """
        if isinstance(self.queue[0], Input) or \
           isinstance(self.queue[0],ActionInput):
            return self.queue[0]
        else:
            raise ValueError()

    def get_output(self):
        """Return the output object in the pipeline or raise a ValueError if
        not present.

        The returned object will be a :class:`Output`or
        :class:`ActionOutput`.
        """
        if isinstance(self.queue[-1], Output) or \
           isinstance(self.queue[-1],ActionOutput):
               return self.queue[-1]
        else:
            raise ValueError()

    def del_unused(self):
        """Remove the unused items in the planner queue. Use for
        optimizations."""
        while len(self.queue) > 1 and not isinstance(self.queue[-1],Action) and not isinstance(self.queue[-1],Output):
            del self.queue[-1]

        # we never need plotter from ActionInput (Index)
        if isinstance(self.queue[0],ActionInput):
            self.queue = filter(lambda i:not isinstance(i,Plotter), self.queue)


    def run(self, optimize=True):
        """Run the planner.

        :param `optimize`: if True the pipeline is optimized for speed,
            oterwise avoid optimizations. By defaults always optimize.
        """
        if optimize:
            self.del_unused()
            if not self.has_output():
                self.add_output(Output.from_type("basic"))
        return reduce(lambda x,y:y(x), self.queue)

    def cancel(self):
        """Send cancel signal to all elements in the planner queue."""
        for item in self.queue:
            try:
                item.cancel()
            except:
                continue

    def __call__(self, optimize=True):
        return self.run(optimize)

    def __repr__(self):
        return " | ".join(map(repr,self.queue))

    @classmethod
    def parse(cls, string, context=None):
        """Parse a command string as usually is typed in console
            to create a :class`Planner`.

        :param `string`: the command line search to be parsed, using the
            mole search syntax.
        :param `context`: a dictionary to use as context for all actions.
            Usually you want to use context to pass arguments to actions in
            execution time.
        """
        ret = cls()
        shl = shlex.shlex(string)
        shl.wordchars += ("\t "+RESERVED)
        shl.whitespace = '|'

        if context is None:
            context = AttrDict({})

        for cmd in shl:
            cmd = " ".join(filter(lambda x:x not in KEYWORDS, cmd.split()))

            if len(cmd) == 0:
                continue

            args = []
            kwargs = {}

            ishl = shlex.shlex(cmd)
            ishl.wordchars += RESERVED

            cmd = [ x.strip("\"").strip("'") for x in ishl ]

            for arg in cmd[1:]:
                if "=" in arg:
                    kwargs.update(dict([tuple(arg.split("="))]))
                elif "," in arg:
                    args.append(arg.split(","))
                else:
                    args.append([arg])

            x = Action.from_type(cmd[0], *args, **kwargs)
            x.context = AttrDict(context)
            ret.add(x)

        if isinstance(ret.queue[0], ActionInput) and x.context is not None:
            obj = ret.queue[0].get_object()
            if obj is not None:
                if "plotter" in obj:
                    ret.add(obj.plotter)
                else:
                    ret.add(Plotter.from_type("basic"))
                if "parser" in obj:
                    ret.add(obj.parser)
                else:
                    ret.add(Parser.from_type("basic"))

        return ret



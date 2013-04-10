#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:


class Action(object):
    """The Action operates over a pipeline and produce a new pipeline with
    results."""

    context = {}

    @classmethod
    def from_type(cls, action_type, *args, **kwargs):
        """Create a new :class:`Action` from action name passed as argument.
        Optional arguments can be passed too.

        :param `action_type`: A string contains name of the action to be created.
        """
        mod = __import__("mole.action.%s" % action_type,
                         globals(),
                         locals(),
                         [ "Action%s" % action_type.title() ])
        kls = getattr(mod, "Action%s" % action_type.title())
        return kls(*args, **kwargs)

    def dispatch(self):
        if getattr(self, _current):
            return self._current
        else:
            return None

    def __repr__(self):
        return str(self.__class__.__name__)


    def __call__(self, pipeline):
        """Override this method to define the action feature.

        :param `pipeline`: an iterable object which get an event per line.
            Note that each item in iterator could be a :class:`Event` or
            a raw object getting from :class:`Input`.
        """
        raise NotImplementedError()


def ActionSyntaxError(Exception):
    """Syntax error in action declaration."""

#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from mole.helper import AttrDict

class Element(AttrDict):
    """Models an element.
    """

    @classmethod
    def from_config(cls, config, base):
        """Create a new :class:`Element` object from a configuration object
        and a base ones (which acts as default values).

        :param `config`: A :class:`MoleConfig` object which contains
            a configuration object.
        :param `base`: A :class:`MoleConfig` object which contains default
            values for the element.
        """
        for element, values in config:
            x = Element()
            for key in values:
                if key in base:
                    #base[key] == {default:...}
                    if values[key] in base[key]:
                        x[key] = base[key][values[key]]
            yield (element, x)


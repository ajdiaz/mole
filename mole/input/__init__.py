#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

class InputConfigError(Exception):
    """Raise an error when create an :class:`Input` object from config
    dictionary."""


class Input(object):
    """The Input read a source input as the begin-point for the pipeline."""

    def close(self):
        raise NotImplementedError()

    @classmethod
    def from_type(cls, input_type, *args, **kwargs):
        mod = __import__("mole.input.%s" % input_type,
                         globals(),
                         locals(),
                         [ "Input%s" % input_type.title() ])
        kls = getattr(mod, "Input%s" % input_type.title())
        return kls(*args, **kwargs)


    @classmethod
    def from_config(cls, config):
        for name, values in config:
            if not values.get("type", None):
                values.type = "basic"
            if values.get("source", None):
                values.name = values.source
                del  values["source"]
            tip = values.type
            del values["type"]
            yield (name, Input.from_type(tip, **values))


    def seek(self, offset, whence):
        raise NotImplementedError()

    def tell(self):
        raise NotImplementedError()

    def __repr__(self):
        return str(self.__class__.__name__)

class RawInput(object):
    """Mixin to identificate inputs which iter over a collections of
    :class:`Events` instead of raw lines."""


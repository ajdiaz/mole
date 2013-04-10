#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from fnmatch import fnmatch

from mole.event import Event
from mole.action import Action


class ActionSearch(Action):
    """This action performs search items in pipeline.

    The valid search syntax is defined in Mole Syntax Search. The
    constructor will receive a dict which contains the queries in
    plain text or unicode.
    """

    REQUIRE_PLOTTER = True

    def parse_query(self, query):
        query = query[0]
        if "=" in query:
            k,v = query.split("=", 1)
            f = fnmatch
            return (k, v, f)
        elif ">" in query:
            k,v = query.split(">", 1)
            f = lambda x,y: float(x) > float(y)
            return (k, v, f)
        elif "<" in query:
            k,v = query.split("<", 1)
            f = lambda x,y: float(x) < float(y)
            return (k, v, f)
        else:
            return ("_raw", query, fnmatch)

    def __init__(self, *args, **kwars):
        self.queries = [ (x,y,fnmatch) for (x,y) in kwars.iteritems() ]
        self.queries.extend(map(self.parse_query, args))

        if len(filter(lambda x:x[0] != "_raw", self.queries)):
            self.REQUIRE_PARSER = True

    def __call__(self, pipeline):
        for event in pipeline:
            if not self.queries:
                yield event
            else:
                ret = False
                for field, query, func in self.queries:
                    # Some optimizations
                    if field == "_raw" and query == "*":
                        ret = True
                    elif field == "_raw" and (isinstance(event, str) or 
                                              isinstance(event, unicode)):
                        # If no parser loaded
                        ret |= func(event, query)
                    else:
                        ret |= func(event[field], query)
                    if ret:
                        break
                if ret:
                    yield event



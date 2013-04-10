#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

from __future__ import absolute_import

import os
import threading

from time import sleep

try:
    import cPickle as pickle
except ImportError:
    import pickle

from whoosh.index import create_in,open_dir
from whoosh.qparser import QueryParser
from whoosh.fields import *
from whoosh.writing import BufferedWriter
from whoosh.qparser.plugins import GtLtPlugin,  FieldsPlugin, \
                                   RangePlugin, WildcardPlugin

from mole.index import Index, DEFAULT_INDEX_PATH

SCHEMA = Schema(source=TEXT(stored=True), name=TEXT(stored=True),
                raw=TEXT(stored=True), time=NUMERIC(stored=True),
                hash=ID(stored=True))

class IndexWhoosh(Index):
    """Implements the whoosh engine as indexer."""

    query_hash = QueryParser("hash", schema=SCHEMA)

    def create(self):
        self._indexer = create_in(self.path, SCHEMA)
        self._index = self._indexer

    def open(self, ro=False):
        if os.path.isdir(self.path):
            self._index = open_dir(self.path)
            self._indexer = self._index
        else:
            os.mkdir(self.path)
            self.create()

        self._searcher = self._index.searcher()
        self._opened = True

    def set_metadata(self, name, value):
        with open(os.path.join(self.path,"metadata-%s" % name),"w") as f:
            f.write(pickle.dumps(value))

    def get_metadata(self, name, default=None):
        try:
            with open(os.path.join(self.path,"metadata-%s" % name)) as f:
                    return pickle.loads(f.read())
        except:
            return default

    def _timer(self):
        while True:
            self.flush()
            sleep(self.flush_time)

    def __init__(self, path, size=None, rows=None, flush_time=10, *args, **kwargs):
        self._opened = False
        self._index = None
        self._writer = None
        self.path = os.path.join(DEFAULT_INDEX_PATH, path)
        self.flush_time = flush_time
        self.flush_thread = threading.Thread(target=self._timer)
        self.open()
        self.count = 0

    def flush(self):
        if getattr(self, "callback_flush", None):
            self.callback_flush(self)

        if self._writer is not None:
            self._writer.commit()
            self.count = 0

    def is_indexed(self, hash):
        return self._searcher.search(self.query_hash.parse(unicode(hash))).estimated_length() > 0

    def __call__(self, pipeline):
        self._writer = BufferedWriter(self._indexer, period=10, limit=1000)
        try:
            self.flush_thread.start()
            for event in pipeline:
                self.count += 1
                self._writer.add_document(source=unicode(event["source"]),
                                          name=unicode(event["index"]),
                                          raw=unicode(event["_raw"]),
                                          time=int(event.time),
                                          hash=unicode(event.hash))
        finally:
            self.flush()

    def search(self, expr, limit=10000):
        with self._index.searcher() as searcher:
            query = QueryParser("raw", self._index.schema)
            query.add_plugin(FieldsPlugin())
            query.add_plugin(RangePlugin())
            query.add_plugin(GtLtPlugin())
            query.add_plugin(WildcardPlugin())
            query = query.parse(expr)
            for x in searcher.search(query, limit=limit):
                yield x

    def __iter__(self):
        for x in self.search(u"*", None):
            yield x["raw"]


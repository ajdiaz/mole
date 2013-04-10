#! /usr/bin/env python
# -*- encoding: utf-8 -*-
# vim:fenc=utf-8:

import time

from collections import deque
from threading import RLock, Timer
from multiprocessing import Process, Queue

class ProcessPool(object):
    def __init__(self, max_running_procs=1, check_interval=1, always_finish=False):
        """Create a new :class:`ProcessPool``. This class allows you to
        execute asynchronously a number of executions in different
        processes.

        Example::

        >>> def function_to_be_executed(): print "hi"
        >>>
        >>> pool = ProcessPool(4)
        >>> for n in xrange(4):
        >>>     pool.apply_async(
        >>>         func=function_to_be_executed,
        >>>         name="process %d" % n,
        >>>     )

        :type max_running_procs: int
        :param max_running_procs: the max number of processes in running
            state.

        :type check_interval: int
        :param check_interval: the number of seconds to pool for child
            status.

        :type always_finish: bool
        :param always_finish: if set (unset by default), ensure that every
            child always finished.
        """
        self.__max_running_procs = max_running_procs
        self.__check_interval = check_interval
        self.__always_finish = always_finish
        self.__closed = False
        self.__pending = deque()
        self.__running = []
        self.__pending_lock = RLock()
        self.__running_lock = RLock()
        Timer(self.__check_interval, self.__manage).start()

    @property
    def is_closed(self):
        return self.__closed

    @property
    def always_finish(self):
        return self.__always_finish

    @property
    def is_full(self):
        with self.__pending_lock:
            return self.count_running >= self.__max_running_procs

    @property
    def has_pending_processes(self):
        with self.__pending_lock:
            return 0 < self.count_pending

    @property
    def count_pending(self):
        with self.__pending_lock:
            return len(self.__pending)

    @property
    def count_running(self):
        with self.__running_lock:
            return len(self.__running)

    def __manage(self):
        with self.__running_lock:
            for_removal = [i for i in self.__running if not i['process'].is_alive()]
            for i in for_removal:
                if i['callback']:
                    result = i['queue'].get()
                    i['callback'](result)

                self.__running.remove(i)
            self.__try_start()

        if not self.is_closed:
            # Restart timer
            Timer(self.__check_interval, self.__manage).start()

    def apply_async(self, func, name=None, args=tuple(), kwargs={}, callback=None):
        """Apply func asynchronously into a pool of process"""
        assert not self.is_closed

        with self.__pending_lock:
            self.__pending.append({
                'target': func,
                'name': name,
                'args': args,
                'kwargs': kwargs,
                'callback': callback
                })

            self.__try_start()

    def close(self):
        """Marks the pool as closed in order to prevent further processes from
        starting.
        """
        self.__closed = True

    def join(self):
        """Join the current running process
        """
        try:
            with self.__running_lock:
                for i in self.__running: i['process'].join()
        except KeyboardInterrupt:
            # User probably got impatient and pressed Ctrl+C again
            pass

    def wait(self):
        while self.has_pending_processes:
            time.sleep(1)

    def __try_start(self):

        def _wrapper(func, queue):
            def _inner(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    queue.put(result)
                finally:
                    queue.close()

            return _inner

        if self.is_closed and not self.always_finish:
            return

        with self.__pending_lock:
            with self.__running_lock:
                while self.has_pending_processes and not self.is_full:
                    # Create a new Process
                    next = self.__pending.pop()
                    q = Queue()
                    p = Process(
                            target=_wrapper(func=next['target'], queue=q),
                            args=next['args'],
                            kwargs=next['kwargs'])

                    if not next['name'] is None:
                        p.name = next['name']

                    self.__running.append({
                        'process': p,
                        'queue': q,
                        'callback': next['callback']
                        })
                    p.start()




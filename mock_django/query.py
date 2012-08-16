"""
mock_django.query
~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import mock
from .shared import SharedMock

__all__ = ('QuerySetMock',)


def QuerySetMock(model, *return_value):
    """
    Set the results to two items:

    >>> objects = QuerySetMock(Post, 'return', 'values')
    >>> assert objects.filter() == objects.all()

    Force an exception:

    >>> objects = QuerySetMock(Post, Exception())

    Note that only methods returning querysets are currently
    explicitly supported; since we use SharedMock, others all behave
    as if they did, so use with caution:

    >>> objects.count() == objects.all()
    True
    """

    def make_get(self, model):
        def _get(*a, **k):
            results = list(self)
            if len(results) > 1:
                raise model.MultipleObjectsReturned
            try:
                return results[0]
            except IndexError:
                raise model.DoesNotExist
        return _get

    def make_getitem(self):
        def _getitem(k):
            if isinstance(k, slice):
                self.__start = k.start
                self.__stop = k.stop
            else:
                return list(self)[k]
            return self
        return _getitem

    def make_iterator(self):
        def _iterator(*a, **k):
            if len(return_value) == 1 and isinstance(return_value[0], Exception):
                raise return_value[0]

            start = getattr(self, '__start', None)
            stop = getattr(self, '__stop', None)
            for x in return_value[start:stop]:
                yield x
        return _iterator

    actual_model = model
    if actual_model:
        model = mock.MagicMock(spec=actual_model())
    else:
        model = mock.MagicMock()

    m = SharedMock()
    m.__start = None
    m.__stop = None
    m.__iter__.side_effect = lambda: iter(m.iterator())
    m.__getitem__.side_effect = make_getitem(m)
    m.model = model
    m.get = make_get(m, actual_model)

    # Note since this is a SharedMock, *all* auto-generated child
    # attributes will have the same side_effect ... might not make
    # sense for some like count().
    m.iterator.side_effect = make_iterator(m)
    return m

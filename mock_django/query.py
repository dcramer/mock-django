"""
mock_django.query
~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""
import copy

import mock
from .shared import SharedMock

__all__ = ('QuerySetMock',)

QUERYSET_RETURNING_METHODS = ['filter', 'exclude', 'order_by', 'reverse',
                              'distinct', 'none', 'all', 'select_related',
                              'prefetch_related', 'defer', 'only', 'using',
                              'select_for_update']


def QuerySetMock(model, *return_value):
    """
    Get a SharedMock that returns self for most attributes and a new copy of
    itself for any method that ordinarily generates QuerySets.

    Set the results to two items:

    >>> class Post(object): pass
    >>> objects = QuerySetMock(Post, 'return', 'values')
    >>> assert list(objects.filter()) == list(objects.all())

    Force an exception:

    >>> objects = QuerySetMock(Post, Exception())

    Chain calls:
    >>> objects.all().filter(filter_arg='dummy')
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

    def make_qs_returning_method(self):
        def _qs_returning_method(*a, **k):
            return copy.deepcopy(self)
        return _qs_returning_method

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

    m = SharedMock(reserved=['count', 'exists'] + QUERYSET_RETURNING_METHODS)
    m.__start = None
    m.__stop = None
    m.__iter__.side_effect = lambda: iter(m.iterator())
    m.__getitem__.side_effect = make_getitem(m)
    if hasattr(m, "__nonzero__"):
        # Python 2
        m.__nonzero__.side_effect = lambda: bool(return_value)
        m.exists.side_effect = m.__nonzero__
    else:
        # Python 3
        m.__bool__.side_effect = lambda: bool(return_value)
        m.exists.side_effect = m.__bool__
    m.__len__.side_effect = lambda: len(return_value)
    m.count.side_effect = m.__len__

    m.model = model
    m.get = make_get(m, actual_model)

    for method_name in QUERYSET_RETURNING_METHODS:
        setattr(m, method_name, make_qs_returning_method(m))

    # Note since this is a SharedMock, *all* auto-generated child
    # attributes will have the same side_effect ... might not make
    # sense for some like count().
    m.iterator.side_effect = make_iterator(m)
    return m

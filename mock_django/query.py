"""
mock_django.query
~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import mock

__all__ = ('QuerySetMock',)


class _QuerySetMock(mock.MagicMock):
    def __init__(self, *args, **kwargs):
        super(_QuerySetMock, self).__init__(*args, **kwargs)
        parent = mock.MagicMock()
        parent.child = self
        self.__parent = parent

    def _get_child_mock(self, **kwargs):
        name = kwargs.get('name', '')
        if name[:2] == name[-2:] == '__':
            return super(_QuerySetMock, self)._get_child_mock(**kwargs)
        return self

    def __getattr__(self, name):
        result = super(_QuerySetMock, self).__getattr__(name)
        if result is self:
            result._mock_name = result._mock_new_name = name
        return result

    def assert_chain_calls(self, *calls):
        """
        Asserts that a chained method was called (parents in the chain do not
        matter, nor are they tracked).

        >>> obj.assert_chain_calls(call.filter(foo='bar'))
        >>> obj.assert_chain_calls(call.select_related('baz'))
        """
        all_calls = self.__parent.mock_calls[:]

        not_found = []
        for kall in calls:
            try:
                all_calls.remove(kall)
            except ValueError:
                not_found.append(kall)
        if not_found:
            if self.__parent.mock_calls:
                message = '%r not all found in call list, %d other(s) were:\n%r' % (not_found, len(self.__parent.mock_calls),
                    self.__parent.mock_calls)
            else:
                message = 'no calls were found'

            raise AssertionError(message)


def QuerySetMock(model, *return_value):
    """
    Set the results to two items:

    >>> objects = QuerySetMock(Post, 'return', 'values')
    >>> assert objects.filter() == objects.all()

    Force an exception:

    >>> objects = QuerySetMock(Post, Exception())
    """

    def make_get(self):
        def _get(*a, **k):
            results = list(self)
            if len(results) > 1:
                raise self.model.MultipleObjectsReturned
            try:
                return results[0]
            except IndexError:
                raise self.model.DoesNotExist
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

    m = _QuerySetMock()
    m.__start = None
    m.__stop = None
    m.__iter__.side_effect = lambda: iter(m.iterator())
    m.__getitem__.side_effect = make_getitem(m)
    m.model = model
    m.get = make_get(m)
    m.iterator.side_effect = make_iterator(m)
    return m

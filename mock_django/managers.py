"""
mock_django.managers
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import mock

__all__ = ('ManagerMock',)


class _ManagerMock(mock.MagicMock):
    def __init__(self, *args, **kwargs):
        super(_ManagerMock, self).__init__(*args, **kwargs)
        parent = mock.MagicMock()
        parent.child = self
        self.__parent = parent

    def _get_child_mock(self, **kwargs):
        name = kwargs.get('name', '')
        if name[:2] == name[-2:] == '__':
            return super(_ManagerMock, self)._get_child_mock(**kwargs)
        return self

    def __getattr__(self, name):
        result = super(_ManagerMock, self).__getattr__(name)
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


def ManagerMock(manager, *return_value):
    """
    Set the results to two items:

    >>> objects = ManagerMock(Post.objects, 'queryset', 'result')
    >>> assert objects.filter() == objects.all()

    Force an exception:

    >>> objects = ManagerMock(Post.objects, Exception())
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

    model = getattr(manager, 'model', None)
    if model:
        model = mock.MagicMock(spec=manager.model())
    else:
        model = mock.MagicMock()

    m = _ManagerMock()
    m.model = model
    m.get = make_get(m)
    if len(return_value) == 1 and isinstance(return_value[0], Exception):
        m.__iter__.side_effect = return_value[0]
    else:
        m.__iter__.side_effect = lambda *a, **k: iter(return_value)
    m.__getitem__ = lambda s, n: list(s)[n]
    return m

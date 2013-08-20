import mock


class SharedMock(mock.MagicMock):

    """
    A MagicMock whose children are all itself.

    >>> m = SharedMock()
    >>> m is m.foo is m.bar is m.foo.bar.baz.qux
    True
    >>> m.foo.side_effect = ['hello from foo']
    >>> m.bar()
    'hello from foo'

    'Magic' methods are not shared.
    >>> m.__getitem__ is m.__len__
    False

    Neither are attributes you assign.
    >>> m.explicitly_assigned_attribute = 1
    >>> m.explicitly_assigned_attribute is m.foo
    False

    """

    def __init__(self, *args, **kwargs):
        reserved = kwargs.pop('reserved', [])

        # XXX: we cannot bind to self until after the mock is initialized
        super(SharedMock, self).__init__(*args, **kwargs)

        parent = mock.MagicMock()
        parent.child = self
        self.__parent = parent
        self.__reserved = reserved

    def _get_child_mock(self, **kwargs):
        name = kwargs.get('name', '')
        if (name[:2] == name[-2:] == '__') or name in self.__reserved:
            return super(SharedMock, self)._get_child_mock(**kwargs)
        return self

    def __getattr__(self, name):
        result = super(SharedMock, self).__getattr__(name)
        if result is self:
            result._mock_name = result._mock_new_name = name
        return result

    def assert_chain_calls(self, *calls):
        """
        Asserts that a chained method was called (parents in the chain do not
        matter, nor are they tracked).  Use with `mock.call`.

        >>> obj.filter(foo='bar').select_related('baz')
        >>> obj.assert_chain_calls(mock.call.filter(foo='bar'))
        >>> obj.assert_chain_calls(mock.call.select_related('baz'))
        >>> obj.assert_chain_calls(mock.call.reverse())
        *** AssertionError: [call.reverse()] not all found in call list, ...

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
                message = '%r not all found in call list, %d other(s) were:\n%r' % (not_found, len(self.__parent.mock_calls), self.__parent.mock_calls)
            else:
                message = 'no calls were found'

            raise AssertionError(message)

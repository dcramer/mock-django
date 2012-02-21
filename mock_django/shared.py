import mock


class SharedMock(mock.MagicMock):
    def __init__(self, *args, **kwargs):
        super(SharedMock, self).__init__(*args, **kwargs)
        parent = mock.MagicMock()
        parent.child = self
        self.__parent = parent

    def _get_child_mock(self, **kwargs):
        name = kwargs.get('name', '')
        if name[:2] == name[-2:] == '__':
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


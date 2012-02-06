"""
mock_django.managers
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import mock

__all__ = ('ManagerMock',)


class _ManagerMock(mock.MagicMock):
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


def ManagerMock(manager, *return_value):
    """
    >>> objects = ManagerMock(Post.objects, ['queryset', 'result'])
    >>> assert objects.filter() == objects.all()
    """

    m = _ManagerMock()
    m.__iter__.side_effect = lambda *a, **k: iter(return_value)
    m.__getitem__ = lambda s, n: list(s)[n]
    return m

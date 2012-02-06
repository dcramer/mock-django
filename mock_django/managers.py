"""
mock_django.managers
~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

import mock

__all__ = ('ManagerMock',)


def ManagerMock(manager, return_value=[]):
    """
    >>> objects = ManagerMock(Post.objects, ['queryset', 'result'])
    >>> assert objects.filter() == objects.all()
    """
    class ManagerMock(mock.MagicMock):
        def _get_child_mock(self, **kwargs):
            name = kwargs.get('name', '')
            if name[:2] == name[-2:] == '__':
                return super(ManagerMock, self)._get_child_mock(**kwargs)
            return self
    m = ManagerMock()
    m.__iter__.return_value = iter(return_value)
    m.__getitem__ = lambda s, n: list(s)[n]
    return m

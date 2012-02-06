import mock
from mock_django.managers import ManagerMock
from unittest2 import TestCase


def make_manager():
    manager = mock.MagicMock(spec=(
        'all', 'filter', 'order_by',
    ))
    return manager


class ManagerMockTestCase(TestCase):
    def test_iter(self):
        manager = make_manager()
        mock = ManagerMock(manager, 'foo')
        self.assertEquals(list(mock.all()), ['foo'])

    def test_getitem(self):
        manager = make_manager()
        mock = ManagerMock(manager, 'foo')
        self.assertEquals(mock.all()[0], 'foo')

    def test_returns_self(self):
        manager = make_manager()
        mock = ManagerMock(manager, 'foo')

        self.assertEquals(mock.all(), mock)

    def test_call_tracking(self):
        # only works in >= mock 0.8
        manager = make_manager()
        mock = ManagerMock(manager, 'foo')

        mock = mock.filter(foo='bar').select_related('baz')
        calls = mock.mock_calls

        self.assertEquals(len(calls), 2)
        self.assertEquals(calls[0], mock.call.filter(foo='bar'))
        self.assertEquals(calls[1], mock.call.select_related('baz'))

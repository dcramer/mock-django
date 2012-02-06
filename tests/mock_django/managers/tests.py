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
        mock = ManagerMock(manager, ['foo'])
        self.assertEquals(list(mock.all()), ['foo'])

    def test_getitem(self):
        manager = make_manager()
        mock = ManagerMock(manager, ['foo'])
        self.assertEquals(mock.all()[0], 'foo')

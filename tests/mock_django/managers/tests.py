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
        inst = ManagerMock(manager, 'foo')
        self.assertEquals(list(inst.all()), ['foo'])

    def test_getitem(self):
        manager = make_manager()
        inst = ManagerMock(manager, 'foo')
        self.assertEquals(inst.all()[0], 'foo')

    def test_returns_self(self):
        manager = make_manager()
        inst = ManagerMock(manager, 'foo')

        self.assertEquals(inst.all(), inst)

    def test_call_tracking(self):
        # only works in >= mock 0.8
        manager = make_manager()
        inst = ManagerMock(manager, 'foo')

        inst.filter(foo='bar').select_related('baz')

        calls = inst.mock_calls

        self.assertGreater(len(calls), 1)
        inst.assert_chain_calls(mock.call.filter(foo='bar'))
        inst.assert_chain_calls(mock.call.select_related('baz'))

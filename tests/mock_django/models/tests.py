from mock import MagicMock
from mock_django.models import ModelMock
try:
    # Python 2
    from unittest2 import TestCase
except ImportError:
    # Python 3
    from unittest import TestCase


class Model(object):
    id = '1'
    pk = '2'

    def foo(self):
        pass

    def bar(self):
        return 'bar'


class ModelMockTestCase(TestCase):
    def test_pk_alias(self):
        mock = ModelMock(Model)
        self.assertEquals(mock.id, mock.pk)

    def test_only_model_attrs_exist(self):
        """
        ModelMocks have only the members that the Model has.
        """
        mock = ModelMock(Model)
        self.assertRaises(AttributeError, lambda x: x.baz, mock)

    def test_model_attrs_are_mocks(self):
        """
        ModelMock members are Mocks, not the actual model members.
        """
        mock = ModelMock(Model)
        self.assertNotEquals(mock.bar(), 'bar')
        self.assertIsInstance(mock, MagicMock)

    def test_attrs_are_not_identical(self):
        """
        Each member of a ModelMock is unique.
        """
        mock = ModelMock(Model)
        self.assertIsNot(mock.foo, mock.bar)
        self.assertIsNot(mock.foo, mock.id)

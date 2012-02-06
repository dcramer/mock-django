from mock_django.models import ModelMock
from unittest2 import TestCase


class Model(object):
    id = '1'
    pk = '2'


class ModelMockTestCase(TestCase):
    def test_pk_alias(self):
        mock = ModelMock(Model)
        self.assertEquals(mock.id, mock.pk)

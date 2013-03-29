from mock_django.query import QuerySetMock
from unittest2 import TestCase

class TestException(Exception):
    pass

class TestModel(object):
    def foo(self):
        pass

    def bar(self):
        return 'bar'

class QuerySetTestCase(TestCase):
    def test_vals_returned(self):
        qs = QuerySetMock(None, 1, 2, 3)
        self.assertEquals(list(qs), [1, 2, 3])

    def test_qs_generator_inequality(self):
        """
        Each QuerySet-returning method's return value is unique.
        """
        qs = QuerySetMock(None, 1, 2, 3)
        self.assertNotEquals(qs.all(), qs.filter())
        self.assertNotEquals(qs.filter(), qs.order_by())

    def test_qs_yield_equality(self):
        """
        The generators may not be the same, but they do produce the same output.
        """
        qs = QuerySetMock(None, 1, 2, 3)
        self.assertEquals(list(qs.all()), list(qs.filter()))

    def test_qs_method_takes_arg(self):
        """
        QS-returning methods are impotent, but they do take args.
        """
        qs = QuerySetMock(None, 1, 2, 3)
        self.assertEquals(list(qs.order_by('something')), [1, 2, 3])

    def test_raises_exception_when_evaluated(self):
        """
        Exception raises when you actually use a QS-returning method.
        """
        qs = QuerySetMock(None, TestException())
        self.assertRaises(TestException, list, qs.all())

    def test_raises_exception_when_accessed(self):
        """
        Exceptions can raise on getitem, too.
        """
        qs = QuerySetMock(None, TestException())
        self.assertRaises(TestException, lambda x: x[0], qs)

    # Test reserved methods
    def test_count_is_scalar(self):
        qs = QuerySetMock(None, 1, 2, 3)
        self.assertEquals(qs.count(), 3)

    def test_exists_is_boolean(self):
        qs = QuerySetMock(None)
        self.assertFalse(qs.exists())

        qs = QuerySetMock(None, 1, 2, 3)
        self.assertTrue(qs.exists())

    def test_objects_returned_do_not_change_type(self):
        """
        Not sure this is the behavior we want, but it's the behavior we have.
        """
        qs = QuerySetMock(TestModel, 1, 2, 3)
        self.assertNotIsInstance(qs[0], TestModel)

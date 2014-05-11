try:
    # Python 2
    from unittest2 import TestCase
except ImportError:
    # Python 3
    from unittest import TestCase

try:
    # Python 2
    from urllib import urlencode
except ImportError:
    # Python 3
    from urllib.parse import urlencode

from django.contrib.auth.models import AnonymousUser
from django.utils.datastructures import MergeDict

from mock import Mock

from mock_django.http import MockHttpRequest
from mock_django.http import WsgiHttpRequest


class WsgiHttpRequestTest(TestCase):
    def test_instance(self):
        wsgi_r = WsgiHttpRequest()

        self.assertTrue(isinstance(wsgi_r.user, AnonymousUser))
        self.assertEqual({}, wsgi_r.session)
        self.assertEqual({}, wsgi_r.META)
        self.assertEqual({}, wsgi_r.GET)
        self.assertEqual({}, wsgi_r.POST)

    def test__get_request(self):
        wsgi_r = WsgiHttpRequest()
        expected_items = MergeDict({}, {}).items()

        wsgi_r.GET = {}
        wsgi_r.POST = {}

        self.assertListEqual(sorted(expected_items),
                             sorted(wsgi_r._get_request().items()))

    def test_REQUEST_property(self):
        self.assertTrue(isinstance(WsgiHttpRequest.REQUEST, property))

    def test__get_raw_post_data(self):
        wsgi_r = WsgiHttpRequest()

        wsgi_r._get_raw_post_data()

        self.assertEqual(urlencode({}), wsgi_r._raw_post_data)

    def test__set_raw_post_data(self):
        wsgi_r = WsgiHttpRequest()

        wsgi_r._set_raw_post_data('')

        self.assertEqual({}, wsgi_r.POST)
        self.assertEqual(urlencode({}), wsgi_r._raw_post_data)

    def test_raw_post_data_property(self):
        self.assertTrue(isinstance(WsgiHttpRequest.raw_post_data, property))


class MockHttpRequestTest(TestCase):
    def test_call(self):
        result = MockHttpRequest()
        meta = {
            'REMOTE_ADDR': '127.0.0.1',
            'SERVER_PORT': '8000',
            'HTTP_REFERER': '',
            'SERVER_NAME': 'testserver',
        }

        self.assertTrue(isinstance(result, WsgiHttpRequest))
        self.assertEqual('/', result.path)
        self.assertEqual('GET', result.method)
        self.assertEqual(meta, result.META)
        self.assertEqual({}, result.GET)
        self.assertEqual({}, result.POST)
        self.assertTrue(isinstance(result.user, AnonymousUser))

    def test_call(self):
        class MockUser:
            pass

        result = MockHttpRequest(user=MockUser())

        self.assertTrue(isinstance(result.user, MockUser))

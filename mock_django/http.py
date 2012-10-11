"""
mock_django.http
~~~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from mock import Mock
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
from django.utils.datastructures import MergeDict
from urllib import urlencode

__all__ = ('MockHttpRequest',)


class WsgiHttpRequest(HttpRequest):
    def __init__(self, *args, **kwargs):
        super(WsgiHttpRequest, self).__init__(*args, **kwargs)
        self.user = AnonymousUser()
        self.session = {}
        self.url = '/'
        self.META = {}
        self.GET = {}
        self.POST = {}

    def _get_request(self):
        if not hasattr(self, '_request'):
            self._request = MergeDict(self.POST, self.GET)
        return self._request
    REQUEST = property(_get_request)

    def build_absolute_uri(self):
        return self.url

    def _get_raw_post_data(self):
        if not hasattr(self, '_raw_post_data'):
            self._raw_post_data = urlencode(self.POST)
        return self._raw_post_data

    def _set_raw_post_data(self, data):
        self._raw_post_data = data
        self.POST = {}
    raw_post_data = property(_set_raw_post_data)


def MockHttpRequest(url='/', method='GET', GET=None, POST=None, META=None):
    if GET is None:
        GET = {}
    if POST is None:
        POST = {}
    else:
        method = 'POST'
    if META is None:
        META = {
            'REMOTE_ADDR': '127.0.0.1',
            'HTTP_REFERER': '',
            'SERVER_NAME': 'testserver',
        }

    request = WsgiHttpRequest()
    request.url = url
    request.method = method
    request.META = META
    request.GET = GET
    request.POST = POST
    return request

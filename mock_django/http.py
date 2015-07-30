"""
mock_django.http
~~~~~~~~~~~~~~~~

:copyright: (c) 2012 DISQUS.
:license: Apache License 2.0, see LICENSE for more details.
"""

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest
try:
    # Python 2
    from urllib import urlencode
except ImportError:
    # Python 3
    from urllib.parse import urlencode

__all__ = ('MockHttpRequest',)


class WsgiHttpRequest(HttpRequest):
    def __init__(self, *args, **kwargs):
        super(WsgiHttpRequest, self).__init__(*args, **kwargs)
        self.user = AnonymousUser()
        self.session = {}
        self.META = {}
        self.GET = {}
        self.POST = {}

    def _get_request(self):
        from django.utils.datastructures import MergeDict
        if not hasattr(self, '_request'):
            self._request = MergeDict(self.POST, self.GET)
        return self._request
    REQUEST = property(_get_request)

    def _get_raw_post_data(self):
        if not hasattr(self, '_raw_post_data'):
            self._raw_post_data = urlencode(self.POST)
        return self._raw_post_data

    def _set_raw_post_data(self, data):
        self._raw_post_data = data
        self.POST = {}
    raw_post_data = property(_get_raw_post_data, _set_raw_post_data)


def MockHttpRequest(path='/', method='GET', GET=None, POST=None, META=None, user=None):
    if GET is None:
        GET = {}
    if POST is None:
        POST = {}
    else:
        method = 'POST'
    if META is None:
        META = {
            'REMOTE_ADDR': '127.0.0.1',
            'SERVER_PORT': '8000',
            'HTTP_REFERER': '',
            'SERVER_NAME': 'testserver',
        }
    if user is None:
        user = AnonymousUser()

    request = WsgiHttpRequest()
    request.path = request.path_info = path
    request.method = method
    request.META = META
    request.GET = GET
    request.POST = POST
    request.user = user
    return request

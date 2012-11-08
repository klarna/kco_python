'''Mocks

Shared mock implementations
'''

import mock
try:
    from urllib.request import HTTPHandler
    # silence pyflakes
    HTTPHandler
except ImportError:
    from urllib2 import HTTPHandler


class HTTPHandler(HTTPHandler):
    class Headers(dict):
        def getheaders(self, key):
            return [self[key]]

    def __init__(self, requests):
        self.responses = []
        self.requests = requests

    def add_response(self, status=200, headers=None, payload=None):
        self.responses.append({
            'status': status,
            'headers': self.Headers(headers) if headers else None,
            'payload': payload.encode('utf-8') if payload else None
        })

    def http_open(self, req):
        print('http open')
        responses = self.responses
        info = responses.pop() if len(responses) > 1 else responses[-1]
        r = mock.Mock()
        r.code = info['status']
        r.msg = 'Mocked Error %r' % info['status']
        r.read.return_value = info['payload']
        r.info.return_value = info['headers']
        r.req = req
        self.requests.append(r)
        return r

'''Mocks

Shared mock implementations
'''

import mock
import json

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
        self.data = {}
        self.responses = []
        self.requests = requests

    def add_response(self, status=200, headers=None, payload=None, uri=None):
        self.responses.append({
            'uri': uri,
            'status': status,
            'headers': self.Headers(headers) if headers else None,
            'payload': payload.encode('utf-8') if payload else None
        })

    def http_open(self, req):
        info, self.responses = (self.responses[0], self.responses[1:])
        url = req.get_full_url()

        if info['uri'] and info['uri'] != url:
            raise Exception("Unexpected url: %s" % url, 999)

        if req.data:
            data = json.loads(req.data.decode('utf-8'))
            if 'test' in data:
                data['test'] = data['test'].upper()
            self.data = data

        payload = info['payload'] or json.dumps(self.data).encode('utf-8')
        status = info['status']
        headers = info['headers']

        r = mock.Mock()
        r.code = status
        r.msg = 'Mocked Error %r' % status
        r.read.return_value = payload
        r.info.return_value = headers
        r.req = req

        self.requests.append(r)
        return r

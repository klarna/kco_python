'''Connector

Defines a class by which facilitates performing HTTP actions on resources.
'''

# Copyright 2013 Klarna AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__all__ = ('Connector',)

try:
    from urllib.request import (build_opener, Request, BaseHandler,
                                HTTPRedirectHandler)
    # silence pyflakes
    build_opener
    Request
    BaseHandler
    HTTPRedirectHandler
except ImportError:
    from urllib2 import (build_opener, Request, BaseHandler,
                         HTTPRedirectHandler)
import json


class Connector(object):
    '''Basic connector

    Uses a customised urllib(2) OpenerDirector to perform http requests while
    making sure to update the local resource accordingly.

    e.g updates location on HTTP 201
    '''

    def __init__(self, useragent, digester, build=build_opener):
        self.opener = build(
            RedirectHandler(),
            AuthorizationHandler(digester),
            UserAgentHandler(useragent))

    def handle_response(self, resource, response):
        '''React upon the response returned'''

        data = response.read()
        headers = response.info()

        if response.code == 200 and data:
            resource.parse(json.loads(data.decode('utf-8')))

        if response.code == 201 and 'location' in headers:
            resource.location = headers['location']

        return response

    def apply(self, method, resource, options=None):
        '''Apply the method on the specific resource

            `method`:   http method to use
            `resource`: resource object
            `options`:  options
                - url: overrides url from resource
        '''

        options = options or {}
        content_type = resource.content_type
        resource.parse

        req = Request(options.get('url', None) or resource.location)
        req.resource = resource
        req.add_header('Accept', content_type)

        if method == 'POST':
            req.add_header('Content-Type', content_type)
            data = options.get('data') or resource.marshal()
            req.data = json.dumps(data).encode('utf-8')

        return self.handle_response(resource, self.opener.open(req))


class AuthorizationHandler(BaseHandler):
    '''Handler that adds a authorization header with a digest.'''

    def __init__(self, digester):
        if not callable(digester):
            raise TypeError('digester must be callable')

        self.digester = digester

    def http_request(self, request):
        request.add_header(
            'Authorization',
            'Klarna %s' % self.digester(request.data))
        return request

    https_request = http_request


class UserAgentHandler(BaseHandler):
    '''Handler that adds a custom user-agent'''

    def __init__(self, ua):
        self._ua = ua

    def http_request(self, request):
        request.add_unredirected_header('User-agent', str(self._ua))
        return request

    https_request = http_request


class RedirectHandler(HTTPRedirectHandler):
    '''Handler that handles redirects

    In addition to the default HTTPRedirectHandler this class
    * updates resource location on 301
    * disallows redirects for POST on 301 and 302
    '''

    max_repeats = 1

    def redirect_request(self, req, *rest):
        resource = req.resource
        nreq = HTTPRedirectHandler.redirect_request(self, req, *rest)
        nreq.resource = resource
        return nreq

    def http_error_301(self, req, res, code, msg, headers):
        '''Update location and filter non-GET request before calling parent
        implementation.
        '''

        method = req.get_method()
        resource = req.resource

        # Update resource location
        if 'location' in headers:
            resource.location = headers['location']

        # Bail unless method is GET
        if method != 'GET':
            return res

        # Let parent handle the rest
        return HTTPRedirectHandler.http_error_301(
            self,
            req,
            res,
            code,
            msg,
            headers)

    def http_error_302(self, req, res, code, msg, headers):
        '''Filter non-GET request before calling parent implementation.'''

        method = req.get_method()

        # Bail unless method is get
        if method != 'GET':
            return res

        # Let parent handle the rest
        return HTTPRedirectHandler.http_error_302(
            self,
            req,
            res,
            code,
            msg,
            headers)

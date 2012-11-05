'''Connector'''

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
    '''Basic connector'''

    def __init__(self, useragent, digester, build=build_opener):
        self.opener = build(
            RedirectHandler(),
            AuthorizationHandler(digester),
            UserAgentHandler(useragent))

    def handle_response(self, resource, response):
        '''React upon the response returned'''

        data = response.read()
        headers = response.info()

        if data:
            resource.parse(json.loads(data))

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
        marshal = resource.marshal
        content_type = resource.content_type
        resource.parse

        req = Request(options.get('url', resource.location))
        req.resource = resource
        req.add_header('Accept', content_type)

        if method == 'POST':
            req.add_header('Content-Type', content_type)
            req.data = json.dumps(marshal()).encode('utf-8')

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


class UserAgentHandler(BaseHandler):
    '''Handler that adds a custom user-agent'''

    def __init__(self, ua):
        self._ua = ua

    def http_request(self, request):
        request.add_header('User-Agent', str(self._ua))
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

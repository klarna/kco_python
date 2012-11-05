import unittest
import mock
from klarnacheckout.connector import Connector
from functools import partial
from hamcrest import assert_that, equal_to, greater_than
import tests.mocks
from tests.matchers import called_once_with

try:
    from urllib.request import build_opener, Request
    from urllib.error import HTTPError

    # silence pyflakes
    build_opener
    Request
    HTTPError
except ImportError:
    from urllib2 import build_opener, Request, HTTPError


class TestConnector(unittest.TestCase):
    useragent = 'user-agent'
    content_type = 'application/json'

    def request(self, url):
        r = Request(url)
        r.resource = mock.Mock()
        return r

    def setUp(self):
        self.requests = []

        self.resource = mock.Mock()
        self.resource.location = 'http://default'
        self.resource.content_type = self.content_type
        self.resource.marshal.return_value = {}

        self.http = tests.mocks.HTTPHandler(self.requests)
        self.digester = mock.Mock()

        self.connector = Connector(
            self.useragent,
            self.digester,
            partial(build_opener, self.http)
        )

    def test_sets_useragent(self):
        self.http.add_response()

        res = self.connector.apply(
            'GET',
            self.resource,
            {
                'url': 'http://test'
            })
        req = res.req

        assert_that(req.get_header('User-agent'), equal_to(self.useragent))

    def test_error_code(self):
        self.http.add_response(status=400)

        with self.assertRaises(HTTPError):
            self.connector.apply(
                'GET',
                self.resource,
                {
                    'url': 'http://test'
                })

    def test_apply_get_200(self):
        payload = '{"flobadob":["bobcat","wookie"]}'
        data = {'flobadob': ['bobcat', 'wookie']}
        expected_digest = 'stnaeu\eu2341aoaaoae=='
        self.digester.return_value = expected_digest
        self.http.add_response(payload=payload)

        res = self.connector.apply(
            'GET',
            self.resource,
            {
                'url': 'http://test'
            })
        req = res.req

        assert_that(
            req.get_header('Authorization'),
            equal_to('Klarna ' + expected_digest))
        assert_that(
            req.get_header('Accept'),
            equal_to(self.content_type))
        assert_that(self.resource.parse, called_once_with(data))

    def test_apply_get_200_invalid_json(self):
        payload = '{"flobadob"}'
        self.http.add_response(payload=payload)

        with self.assertRaises(ValueError):
            self.connector.apply(
                'GET',
                self.resource,
                {
                    'url': 'http://test'
                })

    def test_apply_get_301_to_200(self):
        payload = '{"flobadob":["bobcat","wookie"]}'
        redirect = 'http://test2/'
        self.http.add_response(
            status=200,
            payload=payload)
        self.http.add_response(
            status=301,
            headers={'location': redirect})

        res = self.connector.apply(
            'GET',
            self.resource,
            {
                'url': 'http://test'
            })
        req = res.req

        assert_that(req.get_full_url(), equal_to(redirect))
        assert_that(self.resource.location, equal_to(redirect))

    def test_apply_get_301_to_503(self):
        payload = 'Forbidden'
        redirect = 'http://test2/'
        self.http.add_response(
            status=503,
            payload=payload)
        self.http.add_response(
            status=301,
            headers={'location': redirect})

        with self.assertRaises(HTTPError) as ei:
            self.connector.apply(
                'GET',
                self.resource,
                {
                    'url': 'http://test'
                })

        exc = ei.exception
        assert_that(exc.code, equal_to(503))
        assert_that(self.resource.location, equal_to(redirect))

    def test_apply_get_301_infinite_loop(self):
        self.http.add_response(
            status=301,
            headers={'location': 'http://test'})

        with self.assertRaises(HTTPError) as ei:
            self.connector.apply(
                'GET',
                self.resource,
                {
                    'url': 'http://test'
                })

        exc = ei.exception
        assert_that(exc.code, equal_to(301))

    def test_apply_post_200(self):
        payload = '{"flobadob": "test"}'
        self.http.add_response(
            payload=payload)
        self.resource.marshal.return_value = {
            'flodbadob': ['bobcat', 'wookie']
        }
        expected_digest = 'stnaeu\eu2341aoaaoae=='
        self.digester.return_value = expected_digest

        res = self.connector.apply(
            'POST',
            self.resource)
        req = res.req

        digester_call = self.digester.call_args[0]
        assert_that(len(digester_call[0]), greater_than(10))  # json payload

        assert_that(
            req.get_header('Authorization'),
            equal_to('Klarna ' + expected_digest))
        assert_that(
            req.get_header('Content-type'),
            equal_to(self.content_type))
        assert_that(
            self.resource.parse,
            called_once_with({'flobadob': 'test'}))

    def test_apply_post_200_invalid_json(self):
        payload = '{"flobadob"}'
        self.http.add_response(
            payload=payload)

        with self.assertRaises(ValueError):
            self.connector.apply(
                'POST',
                self.resource)

    def test_apply_post_with_url_in_options(self):
        payload = '{"flobadob":["bobcat","wookie"]}'
        self.http.add_response(
            payload=payload)

        res = self.connector.apply(
            'POST',
            self.resource,
            {
                'url': 'http://test'
            })
        req = res.req

        assert_that(req.get_method(), equal_to('POST'))
        assert_that(req.get_full_url(), equal_to('http://test'))

    def test_apply_post_303_converted_to_get(self):
        payload = '{"flobadob":["bobcat","wookie"]}'
        redirect = 'http://test2'
        self.http.add_response(
            status=200,
            payload=payload)
        self.http.add_response(
            status=303,
            headers={'location': redirect})

        res = self.connector.apply(
            'POST',
            self.resource,
            {
                'url': 'http://test'
            })
        req = res.req

        assert_that(req.get_method(), equal_to('GET'))

    def test_apply_post_303_to_503(self):
        redirect = 'http://test2'
        self.http.add_response(
            status=503,
            payload='Forbidden')
        self.http.add_response(
            status=303,
            headers={'location': redirect}
        )

        with self.assertRaises(HTTPError):
            self.connector.apply(
                'POST',
                self.resource)

    def test_apply_post_201_update_location(self):
        location = 'http://test2'
        self.http.add_response(
            status=201,
            headers={'location': location}
        )

        self.connector.apply(
            'POST',
            self.resource,
            {
                'url': 'http://test'
            })

        assert_that(self.resource.location, equal_to(location))

    def test_apply_post_doesnt_follow_redirect_301(self):
        redirect = 'http://test2'
        self.http.add_response(
            status=503,
            payload='Forbidden')
        self.http.add_response(
            status=301,
            headers={'location': redirect}
        )

        res = self.connector.apply(
            'POST',
            self.resource,
            {
                'url': 'http://test'
            })
        req = res.req
        assert_that(self.resource.location, equal_to(redirect))
        assert_that(req.get_full_url(), equal_to('http://test'))

import unittest
from klarnacheckout.useragent import UserAgent
from hamcrest import assert_that, equal_to
from tests.matchers import contains_regex, assert_raises


class TestUserAgent(unittest.TestCase):

    def setUp(self):
        self._ua = UserAgent()

    def test_basic(self):
        uastring = str(self._ua)
        assert_that(uastring, contains_regex('OS\\/[^\\ ]+_[^\\ ]+'))
        assert_that(uastring, contains_regex('Library\\/[^\\ ]+_[^\\ ]+'))
        assert_that(uastring, contains_regex('Language\\/[^\\ ]+_[^\\ ]+'))

    def test_another_field(self):
        fields = {
            "name": "Magento",
            "version": "5.0",
            "options": [
                "LanguagePack/7",
                "JsLib/2.0"
            ]
        }

        self._ua.add_field("Module", fields)
        uastring = str(self._ua)
        assert_that(
            uastring,
            contains_regex(
                'Module\\/Magento_5.0 \\(LanguagePack\\/7 ; JsLib\\/2.0\\)'))

    def test_cant_redefine(self):
        with assert_raises(ValueError) as cm:
            self._ua.add_field(
                "OS",
                {
                    "name": "Haiku",
                    "version": "1.0-alpha3"
                }
            )

        the_exception = cm.exception
        assert_that(str(the_exception),
                    equal_to("Unable to redefine field OS"))

    def test_invalid_parameter(self):
        field = 13
        data = 13
        with assert_raises(Exception):
            self._ua.add_field(field, data)

        field = 13
        data = ""
        with assert_raises(Exception):
            self._ua.add_field(field, data)
            str(self._ua)

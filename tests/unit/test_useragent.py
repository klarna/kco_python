import unittest
from klarnacheckout.useragent import UserAgent


class TestUserAgent(unittest.TestCase):

	def setUp(self):
		self._ua = UserAgent()

	def test_basic(self):
		uastring = str(self._ua)
		self.assertRegexpMatches(uastring, '.*OS\\/[^\\ ]+_[^\\ ]+.*')
		self.assertRegexpMatches(uastring, '.*Library\\/[^\\ ]+_[^\\ ]+.*')
		self.assertRegexpMatches(uastring, '.*Language\\/[^\\ ]+_[^\\ ]+.*')

	def test_another_field(self):
		fields = {
            "name": "Magento",
            "version": "5.0",
            "options": [
                "LanguagePack/7",
                "JsLib/2.0"
            ]
		}

		self._ua.addField("Module", fields)
		uastring = str(self._ua)
		self.assertRegexpMatches(
			uastring,
			'.*Module\\/Magento_5.0 \\(LanguagePack\\/7 ; JsLib\\/2.0\\).*'
		)

	def test_cant_redefine(self):
		with self.assertRaises(KeyError) as cm:
			self._ua.addField(
				"OS",
				{
					"name": "Haiku",
					"version": "1.0-alpha3"
				}
			)
			addField("Foo", [('name', 'foo'), ('version', 5)])

		the_exception = cm.exception
		self.assertEqual(the_exception.message, "Unable to redefine field OS")

	def test_invalid_parameter(self):
		field = 13
		data = 13
		with self.assertRaises(Exception):
			self._ua.addField(field, data)

		field = 13
		data = ""
		with self.assertRaises(Exception):
			self._ua.addField(field, data)
			str(self._ua)

'''Custom hamcrest matchers'''


import re
from contextlib import contextmanager
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest import assert_that, instance_of


class RaisesContext(object):
    pass


@contextmanager
def assert_raises(arg2=None, arg3=''):
    if isinstance(arg2, (type,)):
        arg2 = instance_of(arg2)

    context = RaisesContext()
    try:
        yield context
    except Exception as e:
        context.exception = e
    assert_that(context.exception, arg2, arg3)


class contains_regex(BaseMatcher):
    def __init__(self, regex):
        if not hasattr(regex, 'search'):
            regex = re.compile(regex)
        self.regex = regex

    def _matches(self, item):
        return self.regex.search(item) is not None

    def describe_to(self, desc):
        desc.append_text('string containing %r' % self.regex.pattern)

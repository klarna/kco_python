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


class matches_regex(BaseMatcher):
    def __init__(self, regex):
        if not hasattr(regex, 'match'):
            regex = re.compile(regex)
        self.regex = regex

    def _matches(self, item):
        return self.regex.match(item) is not None

    def describe_to(self, desc):
        desc.append_text('string matching %r' % self.regex.pattern)


class called_with(BaseMatcher):
    def __init__(self, *args, **kwargs):
        self.args = (args, kwargs)

    def _matches(self, item):
        return item.call_args == self.args

    def describe_to(self, desc):
        args, kwargs = self.args
        desc.append_text('called with %r, %r' % (args, kwargs))


class called_once_with(called_with):
    def _matches(self, item):
        return item.call_count == 1 and called_with._matches(self, item)

    def describe_to(self, desc):
        args, kwargs = self.args
        desc.append_text('called once with %r, %r' % (args, kwargs))

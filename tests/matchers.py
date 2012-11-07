'''Custom hamcrest matchers'''


from hamcrest.core.base_matcher import BaseMatcher


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

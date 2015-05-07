from klarnacheckout.recurring import RecurringOrder, RecurringStatus
from mock import Mock
from hamcrest import assert_that, equal_to
from matchmock import called_once_with


def test_create_recurring_order():
    connector = Mock()
    connector.base = 'http://stub'
    order = RecurringOrder(connector, 'FOOBAR-TOKEN')
    data = {'foo': 'bar'}
    location = 'http://stub/checkout/recurring/FOOBAR-TOKEN/orders'

    assert_that(order.location, equal_to(location))

    order.create(data)
    connector.apply.assert_called_once_with(
        "POST", order, {"url": location, "data": data})


def test_create_recurring_fetch():
    connector = Mock()
    connector.base = 'http://stub'
    order = RecurringStatus(connector, 'FOOBAR-TOKEN')
    location = 'http://stub/checkout/recurring/FOOBAR-TOKEN'

    assert_that(order.location, equal_to(location))

    order.fetch()
    assert_that(connector.apply,
                called_once_with('GET', order, {'url': location}))

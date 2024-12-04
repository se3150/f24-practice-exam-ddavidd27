import pytest
from battery import Battery
from unittest.mock import Mock

todo = pytest.mark.skip(reason='todo: pending spec')

@pytest.fixture
def charged_battery():
    return Battery(100)

@pytest.fixture
def partially_charged_battery():
    b = Battery(100)
    b.mCharge = 70
    return b

@pytest.fixture
def external_monitor_mock():
    return Mock()

def describe_Battery():
    def describe_getCapacity():
        def it_returns_the_capacity_of_the_battery(charged_battery):
            assert charged_battery.getCapacity() == 100

    def describe_getCharge():
        def it_returns_the_current_charge(charged_battery):
            assert charged_battery.getCharge() == 100

        def it_returns_the_current_charge_for_partially_charged_battery(partially_charged_battery):
            assert partially_charged_battery.getCharge() == 70

    def describe_recharge():
        def it_increases_charge_for_valid_amount(partially_charged_battery):
            partially_charged_battery.recharge(20)
            assert partially_charged_battery.getCharge() == 90

        def it_does_not_exceed_capacity(partially_charged_battery):
            partially_charged_battery.recharge(50)
            assert partially_charged_battery.getCharge() == 100

        def it_does_not_increase_charge_for_invalid_amount(partially_charged_battery):
            partially_charged_battery.recharge(-10)
            assert partially_charged_battery.getCharge() == 70

        def it_returns_true_for_successful_recharge(partially_charged_battery):
            assert partially_charged_battery.recharge(10) is True

        def it_returns_false_for_unsuccessful_recharge(partially_charged_battery):
            assert partially_charged_battery.recharge(-10) is False

        def it_notifies_external_monitor_on_recharge(partially_charged_battery, external_monitor_mock):
            partially_charged_battery.external_monitor = external_monitor_mock
            partially_charged_battery.recharge(20)
            external_monitor_mock.notify_recharge.assert_called_once_with(90)

    def describe_drain():
        def it_decreases_charge_for_valid_amount(charged_battery):
            charged_battery.drain(20)
            assert charged_battery.getCharge() == 80

        def it_does_not_go_below_zero(charged_battery):
            charged_battery.drain(120)
            assert charged_battery.getCharge() == 0

        def it_does_not_decrease_charge_for_invalid_amount(charged_battery):
            charged_battery.drain(-10)
            assert charged_battery.getCharge() == 100

        def it_returns_true_for_successful_drain(charged_battery):
            assert charged_battery.drain(10) is True

        def it_returns_false_for_unsuccessful_drain(charged_battery):
            assert charged_battery.drain(-10) is False

        def it_notifies_external_monitor_on_drain(charged_battery, external_monitor_mock):
            charged_battery.external_monitor = external_monitor_mock
            charged_battery.drain(20)
            external_monitor_mock.notify_drain.assert_called_once_with(80)
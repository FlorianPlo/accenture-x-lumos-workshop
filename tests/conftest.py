from datetime import date

import pytest

from wattwise.models import BillingPeriod, Customer, Meter, MeterReading


@pytest.fixture
def meter() -> Meter:
    return Meter("M-1", digits=5)


@pytest.fixture
def customer() -> Customer:
    return Customer("C-1", "Test Customer", "M-1", "BASIC")


@pytest.fixture
def november() -> BillingPeriod:
    return BillingPeriod(date(2026, 11, 1), date(2026, 11, 30))


def reading(value: int, read_on: date, meter_id: str = "M-1") -> MeterReading:
    """Small factory to keep tests readable."""
    return MeterReading(meter_id, read_on, value)

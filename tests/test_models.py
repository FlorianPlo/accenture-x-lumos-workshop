from datetime import date

import pytest

from wattwise.errors import InvalidPeriodError, InvalidReadingError
from wattwise.models import BillingPeriod, Meter


def test_meter_max_value_depends_on_digits() -> None:
    assert Meter("M-1", digits=5).max_value == 99999
    assert Meter("M-1", digits=6).max_value == 999999


def test_meter_rejects_unsupported_register_size() -> None:
    with pytest.raises(InvalidReadingError):
        Meter("M-1", digits=4)


def test_billing_period_rejects_end_before_start() -> None:
    with pytest.raises(InvalidPeriodError):
        BillingPeriod(date(2026, 11, 30), date(2026, 11, 1))


def test_billing_period_label() -> None:
    period = BillingPeriod(date(2026, 11, 1), date(2026, 11, 30))
    assert period.label() == "2026-11-01 to 2026-11-30"

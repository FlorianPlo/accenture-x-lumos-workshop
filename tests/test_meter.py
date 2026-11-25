from datetime import date

import pytest

from tests.conftest import reading
from wattwise.errors import ImplausibleConsumptionError, InvalidReadingError
from wattwise.meter import consumption_kwh
from wattwise.models import Meter

NOV_1 = date(2026, 11, 1)
DEC_1 = date(2026, 12, 1)


def test_consumption_kwh_is_difference_of_readings(meter: Meter) -> None:
    assert consumption_kwh(meter, reading(41210, NOV_1), reading(41455, DEC_1)) == 245


def test_consumption_kwh_zero_when_unchanged(meter: Meter) -> None:
    assert consumption_kwh(meter, reading(500, NOV_1), reading(500, DEC_1)) == 0


def test_consumption_kwh_rejects_reading_of_other_meter(meter: Meter) -> None:
    with pytest.raises(InvalidReadingError):
        consumption_kwh(meter, reading(1, NOV_1), reading(2, DEC_1, meter_id="M-2"))


def test_consumption_kwh_rejects_value_outside_register(meter: Meter) -> None:
    with pytest.raises(InvalidReadingError):
        consumption_kwh(meter, reading(1, NOV_1), reading(100000, DEC_1))


def test_consumption_kwh_rejects_readings_out_of_order(meter: Meter) -> None:
    with pytest.raises(InvalidReadingError):
        consumption_kwh(meter, reading(1, DEC_1), reading(2, NOV_1))


def test_consumption_kwh_flags_implausible_consumption(meter: Meter) -> None:
    # 30 days * 200 kWh/day = 6000 kWh is the limit
    with pytest.raises(ImplausibleConsumptionError):
        consumption_kwh(meter, reading(1000, NOV_1), reading(7001, DEC_1))

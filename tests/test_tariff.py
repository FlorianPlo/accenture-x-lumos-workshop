from decimal import Decimal

import pytest

from wattwise.errors import UnknownTariffError
from wattwise.tariff import TARIFFS, energy_charge, get_tariff, prorated_base_fee


def test_get_tariff_returns_known_tariff() -> None:
    assert get_tariff("BASIC").name == "WattWise Basic"


def test_get_tariff_rejects_unknown_code() -> None:
    with pytest.raises(UnknownTariffError):
        get_tariff("GOLD")


@pytest.mark.parametrize("tariff", TARIFFS.values(), ids=lambda t: t.code)
def test_tariff_last_tier_is_open_ended(tariff) -> None:
    assert tariff.tiers[-1].up_to_kwh is None


def test_energy_charge_flat_tariff() -> None:
    # 245 kWh * 0.3450
    assert energy_charge(get_tariff("BASIC"), 245) == Decimal("84.53")


def test_energy_charge_comfort_within_first_tier() -> None:
    # 200 kWh * 0.2990
    assert energy_charge(get_tariff("COMFORT"), 200) == Decimal("59.80")


def test_energy_charge_comfort_at_tier_boundary() -> None:
    # 250 kWh * 0.2990
    assert energy_charge(get_tariff("COMFORT"), 250) == Decimal("74.75")


def test_energy_charge_zero_consumption() -> None:
    assert energy_charge(get_tariff("HEATPUMP"), 0) == Decimal("0.00")


def test_energy_charge_rejects_negative_consumption() -> None:
    with pytest.raises(ValueError):
        energy_charge(get_tariff("BASIC"), -1)


def test_prorated_base_fee_full_year_equals_twelve_months() -> None:
    assert prorated_base_fee(get_tariff("BASIC"), 365) == Decimal("118.80")


def test_prorated_base_fee_single_day() -> None:
    # 9.90 * 12 / 365 = 0.3254...
    assert prorated_base_fee(get_tariff("BASIC"), 1) == Decimal("0.33")


def test_prorated_base_fee_zero_days() -> None:
    assert prorated_base_fee(get_tariff("COMFORT"), 0) == Decimal("0.00")

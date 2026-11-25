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


# Regression test for BUG-151
def test_energy_charge_comfort_charges_higher_price_only_above_limit() -> None:
    # wiki/Tariffs.md example, 260 kWh:
    # 250 * 0.2990 = 74.75; 10 * 0.3690 = 3.69; sum = 78.44
    assert energy_charge(get_tariff("COMFORT"), 260) == Decimal("78.44")


# Regression test for BUG-151
def test_energy_charge_heatpump_three_tiers() -> None:
    # wiki/Tariffs.md example, 1220 kWh:
    # 400 * 0.2490 = 99.60; 600 * 0.2790 = 167.40; 220 * 0.3190 = 70.18; sum = 337.18
    assert energy_charge(get_tariff("HEATPUMP"), 1220) == Decimal("337.18")


# Regression test for BUG-151
def test_energy_charge_heatpump_at_second_tier_boundary() -> None:
    # 400 * 0.2490 = 99.60; 600 * 0.2790 = 167.40; sum = 267.00
    assert energy_charge(get_tariff("HEATPUMP"), 1000) == Decimal("267.00")


# Regression test for BUG-151
def test_energy_charge_comfort_one_kwh_above_limit_does_not_jump() -> None:
    # 250 * 0.2990 = 74.75; 1 * 0.3690 = 0.369; sum = 75.119 -> 75.12
    assert energy_charge(get_tariff("COMFORT"), 251) == Decimal("75.12")

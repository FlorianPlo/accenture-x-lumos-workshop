"""Tariff catalogue and price calculation.

See ``wiki/Tariffs.md`` for the product definitions.
"""

from dataclasses import dataclass
from decimal import Decimal

from wattwise.errors import UnknownTariffError
from wattwise.money import round_eur

DAYS_PER_YEAR = 365


@dataclass(frozen=True)
class Tier:
    """A price tier.

    Attributes:
        up_to_kwh: Upper bound (inclusive) of the tier in kWh per billing period,
            or ``None`` for the last, open-ended tier.
        price_per_kwh: Net energy price in EUR/kWh.
    """

    up_to_kwh: int | None
    price_per_kwh: Decimal


@dataclass(frozen=True)
class Tariff:
    """A tariff product.

    Attributes:
        code: Short code stored on the customer record.
        name: Marketing name printed on the invoice.
        monthly_base_fee: Net base fee in EUR per month.
        tiers: Price tiers ordered by ``up_to_kwh`` ascending; the last tier
            must be open-ended (``up_to_kwh is None``).
    """

    code: str
    name: str
    monthly_base_fee: Decimal
    tiers: tuple[Tier, ...]


TARIFFS: dict[str, Tariff] = {
    "BASIC": Tariff(
        code="BASIC",
        name="WattWise Basic",
        monthly_base_fee=Decimal("9.90"),
        tiers=(Tier(None, Decimal("0.3450")),),
    ),
    "COMFORT": Tariff(
        code="COMFORT",
        name="WattWise Comfort",
        monthly_base_fee=Decimal("14.90"),
        tiers=(
            Tier(250, Decimal("0.2990")),
            Tier(None, Decimal("0.3690")),
        ),
    ),
    "HEATPUMP": Tariff(
        code="HEATPUMP",
        name="WattWise HeatPump",
        monthly_base_fee=Decimal("19.90"),
        tiers=(
            Tier(400, Decimal("0.2490")),
            Tier(1000, Decimal("0.2790")),
            Tier(None, Decimal("0.3190")),
        ),
    ),
}


def get_tariff(code: str) -> Tariff:
    """Look up a tariff by code.

    Raises:
        UnknownTariffError: If no tariff with this code exists.
    """
    try:
        return TARIFFS[code]
    except KeyError:
        raise UnknownTariffError(f"Unknown tariff code: {code!r}") from None


def energy_charge(tariff: Tariff, kwh: int) -> Decimal:
    """Net energy charge for the consumption of one billing period.

    Args:
        tariff: The customer's tariff.
        kwh: Consumption in the billing period.

    Returns:
        Net energy charge in EUR, rounded to cents.
    """
    if kwh < 0:
        raise ValueError("Consumption must not be negative")

    for tier in tariff.tiers:
        if tier.up_to_kwh is None or kwh <= tier.up_to_kwh:
            return round_eur(Decimal(kwh) * tier.price_per_kwh)

    raise AssertionError(f"Tariff {tariff.code} has no open-ended tier")


def prorated_base_fee(tariff: Tariff, days: int) -> Decimal:
    """Net base fee for a billing period of ``days`` days.

    The monthly base fee is converted to a daily rate
    (``monthly * 12 / 365``) and multiplied by the number of days.

    Args:
        tariff: The customer's tariff.
        days: Number of billable days.

    Returns:
        Net base fee in EUR, rounded to cents.
    """
    if days < 0:
        raise ValueError("Days must not be negative")
    daily = tariff.monthly_base_fee * 12 / DAYS_PER_YEAR
    return round_eur(daily * days)

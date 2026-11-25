"""Invoice creation.

See ``wiki/Billing-Rules.md`` for the invoice structure and VAT rules.
"""

from dataclasses import dataclass
from decimal import Decimal

from wattwise.meter import consumption_kwh
from wattwise.models import BillingPeriod, Customer, Meter, MeterReading
from wattwise.money import round_eur
from wattwise.tariff import Tariff, energy_charge, prorated_base_fee

VAT_RATE = Decimal("0.19")


@dataclass(frozen=True)
class InvoiceLine:
    """One net line item on an invoice."""

    description: str
    amount: Decimal


@dataclass(frozen=True)
class Invoice:
    """A customer invoice for one billing period."""

    customer_id: str
    customer_name: str
    tariff_name: str
    period: BillingPeriod
    consumption_kwh: int
    lines: tuple[InvoiceLine, ...]
    net: Decimal
    vat: Decimal
    gross: Decimal


def create_invoice(
    customer: Customer,
    tariff: Tariff,
    meter: Meter,
    period: BillingPeriod,
    opening: MeterReading,
    closing: MeterReading,
) -> Invoice:
    """Create the invoice for one customer and billing period.

    Args:
        customer: The customer being billed.
        tariff: The customer's tariff.
        meter: The customer's meter.
        period: The billing period.
        opening: Reading that opens the period (taken on ``period.start``).
        closing: Reading that closes the period (taken the day after ``period.end``).

    Returns:
        The finished invoice.
    """
    kwh = consumption_kwh(meter, opening, closing)

    base = prorated_base_fee(tariff, period.days)
    energy = energy_charge(tariff, kwh)
    lines = (
        InvoiceLine(f"Base fee ({period.days} days)", base),
        InvoiceLine(f"Energy ({kwh} kWh)", energy),
    )

    net = sum((line.amount for line in lines), Decimal("0"))
    vat = round_eur(net * VAT_RATE)
    gross = net + vat

    return Invoice(
        customer_id=customer.customer_id,
        customer_name=customer.name,
        tariff_name=tariff.name,
        period=period,
        consumption_kwh=kwh,
        lines=lines,
        net=net,
        vat=vat,
        gross=gross,
    )

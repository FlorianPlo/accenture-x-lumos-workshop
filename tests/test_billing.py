from datetime import date

from tests.conftest import reading
from wattwise.billing import VAT_RATE, create_invoice
from wattwise.models import BillingPeriod, Customer, Meter
from wattwise.money import round_eur
from wattwise.tariff import get_tariff

NOV_1 = date(2026, 11, 1)
DEC_1 = date(2026, 12, 1)


def _invoice(customer: Customer, meter: Meter, period: BillingPeriod):
    return create_invoice(
        customer,
        get_tariff("BASIC"),
        meter,
        period,
        reading(41210, NOV_1),
        reading(41455, DEC_1),
    )


def test_create_invoice_has_base_fee_and_energy_lines(customer, meter, november) -> None:
    invoice = _invoice(customer, meter, november)
    assert [line.description.split(" (")[0] for line in invoice.lines] == [
        "Base fee",
        "Energy",
    ]
    assert invoice.consumption_kwh == 245


def test_create_invoice_net_is_sum_of_lines(customer, meter, november) -> None:
    invoice = _invoice(customer, meter, november)
    assert invoice.net == sum(line.amount for line in invoice.lines)


def test_create_invoice_vat_is_computed_on_net(customer, meter, november) -> None:
    invoice = _invoice(customer, meter, november)
    assert invoice.vat == round_eur(invoice.net * VAT_RATE)
    assert invoice.gross == invoice.net + invoice.vat


def test_create_invoice_copies_customer_data(customer, meter, november) -> None:
    invoice = _invoice(customer, meter, november)
    assert invoice.customer_id == "C-1"
    assert invoice.tariff_name == "WattWise Basic"
    assert invoice.period == november

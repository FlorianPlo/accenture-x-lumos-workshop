"""Application services shared by the CLI and the web UI."""

import calendar
from dataclasses import dataclass
from datetime import date, timedelta

from wattwise.billing import Invoice, create_invoice
from wattwise.errors import BillingError
from wattwise.models import BillingPeriod, Customer, Meter, MeterReading
from wattwise.repository import DataRepository
from wattwise.tariff import Tariff, get_tariff


@dataclass(frozen=True)
class BillingResult:
    """Outcome of billing one customer for one month.

    Exactly one of ``invoice`` and ``error`` is set.
    """

    customer: Customer
    tariff: Tariff
    meter: Meter
    period: BillingPeriod
    opening: MeterReading | None
    closing: MeterReading | None
    invoice: Invoice | None
    error: str | None


def month_period(month: str) -> BillingPeriod:
    """Billing period for a calendar month given as ``YYYY-MM``."""
    year, mon = (int(part) for part in month.split("-"))
    last_day = calendar.monthrange(year, mon)[1]
    return BillingPeriod(date(year, mon, 1), date(year, mon, last_day))


def previous_month(month: str) -> str:
    """The month before ``month``, both as ``YYYY-MM``."""
    first = month_period(month).start
    return (first - timedelta(days=1)).strftime("%Y-%m")


def available_months(repo: DataRepository) -> list[str]:
    """Months (``YYYY-MM``) for which opening and closing readings exist."""
    dates = sorted({d.replace(day=1) for d in repo.reading_dates()})
    return [
        start.strftime("%Y-%m")
        for start, nxt in zip(dates, dates[1:])
        if month_period(start.strftime("%Y-%m")).end + timedelta(days=1) == nxt
    ]


def bill_customer(repo: DataRepository, customer_id: str, month: str) -> Invoice:
    """Create the invoice for one customer and month.

    Raises:
        BillingError: If the invoice cannot be created.
    """
    customer = repo.customer(customer_id)
    meter = repo.meter(customer.meter_id)
    period = month_period(month)
    opening = repo.reading(meter.meter_id, period.start)
    closing = repo.reading(meter.meter_id, period.end + timedelta(days=1))
    return create_invoice(
        customer, get_tariff(customer.tariff_code), meter, period, opening, closing
    )


def billing_result(repo: DataRepository, customer_id: str, month: str) -> BillingResult:
    """Bill one customer and capture the outcome instead of raising."""
    customer = repo.customer(customer_id)
    meter = repo.meter(customer.meter_id)
    period = month_period(month)
    opening = repo.find_reading(meter.meter_id, period.start)
    closing = repo.find_reading(meter.meter_id, period.end + timedelta(days=1))
    invoice: Invoice | None = None
    error: str | None = None
    try:
        invoice = bill_customer(repo, customer_id, month)
    except BillingError as exc:
        error = f"{type(exc).__name__}: {exc}"
    return BillingResult(
        customer=customer,
        tariff=get_tariff(customer.tariff_code),
        meter=meter,
        period=period,
        opening=opening,
        closing=closing,
        invoice=invoice,
        error=error,
    )


def billing_overview(repo: DataRepository, month: str) -> list[BillingResult]:
    """Billing results for all customers for ``month``."""
    return [billing_result(repo, c.customer_id, month) for c in repo.customers()]

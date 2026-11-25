"""Core domain models."""

from dataclasses import dataclass
from datetime import date

from wattwise.errors import InvalidPeriodError, InvalidReadingError


@dataclass(frozen=True)
class Meter:
    """An electricity meter with a mechanical/digital counter register.

    Attributes:
        meter_id: Unique meter identifier, e.g. ``"M-20001"``.
        digits: Number of digits on the counter register (5 or 6).
    """

    meter_id: str
    digits: int = 5

    def __post_init__(self) -> None:
        if self.digits not in (5, 6):
            raise InvalidReadingError(
                f"Meter {self.meter_id}: unsupported register size {self.digits}"
            )

    @property
    def max_value(self) -> int:
        """Highest value the register can display (e.g. 99999 for 5 digits)."""
        return 10**self.digits - 1


@dataclass(frozen=True)
class MeterReading:
    """A single meter reading taken at 00:00 on ``read_on``.

    Attributes:
        meter_id: Meter the reading belongs to.
        read_on: Date of the reading.
        value: Register value in kWh.
    """

    meter_id: str
    read_on: date
    value: int


@dataclass(frozen=True)
class Customer:
    """A household customer.

    Attributes:
        customer_id: Unique customer identifier, e.g. ``"C-1001"``.
        name: Full name as printed on the invoice.
        meter_id: Meter installed at the customer's address.
        tariff_code: Code of the tariff the customer is on (see ``tariff.py``).
    """

    customer_id: str
    name: str
    meter_id: str
    tariff_code: str


@dataclass(frozen=True)
class BillingPeriod:
    """A billing period from ``start`` to ``end``.

    Attributes:
        start: First day of the period.
        end: Last day of the period.
    """

    start: date
    end: date

    def __post_init__(self) -> None:
        if self.end < self.start:
            raise InvalidPeriodError(
                f"Period end {self.end} is before period start {self.start}"
            )

    @property
    def days(self) -> int:
        """Number of billable days in the period."""
        return (self.end - self.start).days

    def label(self) -> str:
        """Human readable label, e.g. ``"2026-11-01 to 2026-11-30"``."""
        return f"{self.start.isoformat()} to {self.end.isoformat()}"

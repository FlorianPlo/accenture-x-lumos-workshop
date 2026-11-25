"""Consumption calculation from meter readings.

See ``wiki/Meter-Readings.md`` for the business rules.
"""

from wattwise.errors import ImplausibleConsumptionError, InvalidReadingError
from wattwise.models import Meter, MeterReading

# Households above this daily average are flagged for manual review.
MAX_PLAUSIBLE_KWH_PER_DAY = 200


def _validate_reading(meter: Meter, reading: MeterReading) -> None:
    if reading.meter_id != meter.meter_id:
        raise InvalidReadingError(
            f"Reading for {reading.meter_id} does not belong to meter {meter.meter_id}"
        )
    if not 0 <= reading.value <= meter.max_value:
        raise InvalidReadingError(
            f"Meter {meter.meter_id}: value {reading.value} outside register range "
            f"0..{meter.max_value}"
        )


def consumption_kwh(meter: Meter, previous: MeterReading, current: MeterReading) -> int:
    """Compute consumption in kWh between two readings of the same meter.

    Args:
        meter: The meter both readings belong to.
        previous: The earlier reading (opens the period).
        current: The later reading (closes the period).

    Returns:
        Consumed energy in whole kWh.

    Raises:
        InvalidReadingError: If the readings are inconsistent.
        ImplausibleConsumptionError: If consumption exceeds the plausibility limit.
    """
    _validate_reading(meter, previous)
    _validate_reading(meter, current)

    if current.read_on <= previous.read_on:
        raise InvalidReadingError(
            f"Meter {meter.meter_id}: reading on {current.read_on} is not after "
            f"reading on {previous.read_on}"
        )

    delta = current.value - previous.value
    if delta < 0:
        raise InvalidReadingError(
            f"Meter {meter.meter_id}: reading decreased from {previous.value} "
            f"to {current.value}"
        )

    elapsed_days = (current.read_on - previous.read_on).days
    if delta > MAX_PLAUSIBLE_KWH_PER_DAY * elapsed_days:
        raise ImplausibleConsumptionError(
            f"Meter {meter.meter_id}: {delta} kWh in {elapsed_days} days exceeds "
            f"plausibility limit of {MAX_PLAUSIBLE_KWH_PER_DAY} kWh/day"
        )

    return delta

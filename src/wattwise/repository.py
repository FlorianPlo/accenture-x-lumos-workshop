"""Loading customers, meters and readings from the ``data/`` folder."""

import csv
import json
from datetime import date
from pathlib import Path

from wattwise.errors import InvalidReadingError
from wattwise.models import Customer, Meter, MeterReading

DEFAULT_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


class DataRepository:
    """Read-only access to the JSON/CSV data files."""

    def __init__(self, data_dir: Path = DEFAULT_DATA_DIR) -> None:
        self._data_dir = data_dir
        raw = json.loads((data_dir / "customers.json").read_text(encoding="utf-8"))
        self._customers = {
            c["customer_id"]: Customer(**c) for c in raw["customers"]
        }
        self._meters = {m["meter_id"]: Meter(**m) for m in raw["meters"]}
        self._readings = self._load_readings(data_dir / "readings.csv")

    @staticmethod
    def _load_readings(path: Path) -> dict[tuple[str, date], MeterReading]:
        readings: dict[tuple[str, date], MeterReading] = {}
        with path.open(newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                reading = MeterReading(
                    meter_id=row["meter_id"],
                    read_on=date.fromisoformat(row["read_on"]),
                    value=int(row["value"]),
                )
                readings[(reading.meter_id, reading.read_on)] = reading
        return readings

    def customers(self) -> list[Customer]:
        """All customers, ordered by id."""
        return [self._customers[k] for k in sorted(self._customers)]

    def customer(self, customer_id: str) -> Customer:
        """Look up a single customer."""
        return self._customers[customer_id]

    def meter(self, meter_id: str) -> Meter:
        """Look up a single meter."""
        return self._meters[meter_id]

    def reading_dates(self) -> set[date]:
        """All dates for which at least one reading exists."""
        return {read_on for _, read_on in self._readings}

    def find_reading(self, meter_id: str, read_on: date) -> MeterReading | None:
        """Like :meth:`reading`, but returns ``None`` if there is no reading."""
        return self._readings.get((meter_id, read_on))

    def reading(self, meter_id: str, read_on: date) -> MeterReading:
        """Look up the reading of ``meter_id`` taken on ``read_on``.

        Raises:
            InvalidReadingError: If no such reading exists.
        """
        try:
            return self._readings[(meter_id, read_on)]
        except KeyError:
            raise InvalidReadingError(
                f"No reading for meter {meter_id} on {read_on}"
            ) from None

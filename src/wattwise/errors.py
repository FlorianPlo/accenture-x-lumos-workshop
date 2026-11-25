"""Domain exceptions.

All exceptions raised by WattWise inherit from :class:`BillingError` so that
callers (e.g. the monthly billing run) can catch them in one place.
"""


class BillingError(Exception):
    """Base class for all WattWise domain errors."""


class InvalidPeriodError(BillingError):
    """Raised when a billing period is malformed (e.g. end before start)."""


class InvalidReadingError(BillingError):
    """Raised when a meter reading cannot be used for billing."""


class ImplausibleConsumptionError(BillingError):
    """Raised when computed consumption exceeds the plausibility limit."""


class UnknownTariffError(BillingError):
    """Raised when a customer references a tariff code that does not exist."""

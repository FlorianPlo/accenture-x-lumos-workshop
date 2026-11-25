"""Money helpers.

Convention: every monetary value is a :class:`decimal.Decimal`. Never use
``float`` for money. Round with :func:`round_eur` only - do not call
``round()`` or ``quantize`` directly in business code.
"""

from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def round_eur(amount: Decimal) -> Decimal:
    """Round an amount to whole cents using commercial rounding (half up).

    Args:
        amount: The unrounded amount in EUR.

    Returns:
        The amount rounded to two decimal places.
    """
    return amount.quantize(CENT, rounding=ROUND_HALF_UP)

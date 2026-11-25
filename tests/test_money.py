from decimal import Decimal

import pytest

from wattwise.money import round_eur


@pytest.mark.parametrize(
    ("amount", "expected"),
    [
        ("1.004", "1.00"),
        ("1.005", "1.01"),
        ("2.675", "2.68"),
        ("0", "0.00"),
        ("-1.005", "-1.01"),
    ],
)
def test_round_eur_rounds_half_up(amount: str, expected: str) -> None:
    assert round_eur(Decimal(amount)) == Decimal(expected)

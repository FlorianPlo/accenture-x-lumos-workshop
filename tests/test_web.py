import pytest

from wattwise.repository import DataRepository
from wattwise.web import route


@pytest.fixture(scope="module")
def repo() -> DataRepository:
    return DataRepository()


def test_route_dashboard_lists_all_customers(repo: DataRepository) -> None:
    response = route(repo, "/?month=2026-10")
    assert response.status == 200
    for customer in repo.customers():
        assert customer.name in response.body


def test_route_dashboard_defaults_to_latest_month(repo: DataRepository) -> None:
    response = route(repo, "/")
    assert response.status == 200
    assert "November 2026" in response.body


def test_route_dashboard_unknown_month_returns_404(repo: DataRepository) -> None:
    assert route(repo, "/?month=1999-01").status == 404


def test_route_invoice_page_shows_customer_and_tariff(repo: DataRepository) -> None:
    response = route(repo, "/invoice/C-1001/2026-10")
    assert response.status == 200
    assert "Anna Becker" in response.body
    assert "WattWise Basic" in response.body


def test_route_invoice_unknown_customer_returns_404(repo: DataRepository) -> None:
    assert route(repo, "/invoice/C-9999/2026-10").status == 404


def test_route_unknown_path_returns_404(repo: DataRepository) -> None:
    assert route(repo, "/admin").status == 404


def test_route_escapes_user_input(repo: DataRepository) -> None:
    response = route(repo, "/<script>")
    assert "<script>" not in response.body

"""Command line interface.

Usage::

    python -m wattwise serve                  # web UI on http://localhost:8000
    python -m wattwise invoice C-1001 2026-11
    python -m wattwise run 2026-11
"""

import argparse

from wattwise.billing import Invoice
from wattwise.repository import DataRepository
from wattwise.service import bill_customer


def format_invoice(invoice: Invoice) -> str:
    """Render an invoice as plain text."""
    width = 46
    rows = [
        "=" * width,
        f"INVOICE  {invoice.customer_id}  {invoice.customer_name}",
        f"Tariff:  {invoice.tariff_name}",
        f"Period:  {invoice.period.label()}",
        "-" * width,
    ]
    for line in invoice.lines:
        rows.append(f"{line.description:<34}{line.amount:>9} EUR")
    rows += [
        "-" * width,
        f"{'Net':<34}{invoice.net:>9} EUR",
        f"{'VAT 19%':<34}{invoice.vat:>9} EUR",
        f"{'Total':<34}{invoice.gross:>9} EUR",
        "=" * width,
    ]
    return "\n".join(rows)


def main(argv: list[str] | None = None) -> None:
    """Entry point for ``python -m wattwise``."""
    parser = argparse.ArgumentParser(prog="wattwise")
    sub = parser.add_subparsers(dest="command", required=True)

    serve = sub.add_parser("serve", help="Start the web UI")
    serve.add_argument("--port", type=int, default=8000)

    inv = sub.add_parser("invoice", help="Print the invoice for one customer")
    inv.add_argument("customer_id")
    inv.add_argument("month", help="YYYY-MM")

    run = sub.add_parser("run", help="Monthly billing run for all customers")
    run.add_argument("month", help="YYYY-MM")

    args = parser.parse_args(argv)
    repo = DataRepository()

    if args.command == "serve":
        from wattwise.web import serve as start_server

        start_server(repo, args.port)
    elif args.command == "invoice":
        print(format_invoice(bill_customer(repo, args.customer_id, args.month)))
    else:
        for customer in repo.customers():
            print(format_invoice(bill_customer(repo, customer.customer_id, args.month)))
            print()

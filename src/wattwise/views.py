"""HTML rendering for the web UI.

All functions are pure: they take data and return an HTML string. Every value
that comes from data is escaped with :func:`esc`.
"""

import calendar
from datetime import date
from decimal import Decimal
from html import escape

from wattwise.service import BillingResult
from wattwise.tariff import Tariff

STYLE = """
:root {
  --bg: #f4f6f8; --card: #ffffff; --ink: #1c2530; --muted: #5f6b7a;
  --line: #e2e7ed; --brand: #0b6e5f; --brand-soft: #e3f3ef;
  --bad: #b42318; --bad-soft: #fdecea; --ok: #067647; --ok-soft: #e7f6ec;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
       font: 15px/1.5 "Segoe UI", system-ui, -apple-system, sans-serif; }
header { background: var(--brand); color: #fff; }
header .wrap { display: flex; align-items: center; justify-content: space-between;
               gap: 16px; padding-top: 14px; padding-bottom: 14px; }
header a { color: #fff; text-decoration: none; font-weight: 600; font-size: 18px; }
header span { opacity: .8; font-size: 13px; }
.wrap { max-width: 1040px; margin: 0 auto; padding: 0 20px; }
main { padding: 28px 0 60px; }
h1 { font-size: 24px; margin: 0 0 4px; }
h2 { font-size: 16px; margin: 0 0 12px; }
.sub { color: var(--muted); margin: 0 0 24px; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 10px;
        padding: 20px; margin-bottom: 20px; }
.tabs { display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap; }
.tabs a { padding: 6px 14px; border-radius: 999px; border: 1px solid var(--line);
          background: var(--card); color: var(--ink); text-decoration: none; }
.tabs a.active { background: var(--brand); border-color: var(--brand); color: #fff; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
         gap: 16px; margin-bottom: 20px; }
.tile { background: var(--card); border: 1px solid var(--line); border-radius: 10px;
        padding: 16px 20px; }
.tile .label { color: var(--muted); font-size: 13px; }
.tile .value { font-size: 26px; font-weight: 600; font-variant-numeric: tabular-nums; }
.tile.bad .value { color: var(--bad); }
table { width: 100%; border-collapse: collapse; }
th, td { text-align: left; padding: 10px 8px; border-bottom: 1px solid var(--line); }
th { color: var(--muted); font-weight: 600; font-size: 13px; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
tr.total td { font-weight: 700; border-bottom: none; font-size: 17px; }
tr.subtotal td { color: var(--muted); }
td a { color: var(--brand); font-weight: 600; text-decoration: none; }
.badge { display: inline-block; padding: 2px 10px; border-radius: 999px; font-size: 12px;
         font-weight: 600; }
.badge.ok { background: var(--ok-soft); color: var(--ok); }
.badge.bad { background: var(--bad-soft); color: var(--bad); }
.err { color: var(--bad); font-size: 13px; }
.alert { background: var(--bad-soft); border: 1px solid #f5c2bd; color: var(--bad);
         border-radius: 10px; padding: 16px 20px; margin-bottom: 20px; }
.alert code { font-size: 13px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
@media (max-width: 760px) { .grid2 { grid-template-columns: 1fr; } }
dl { display: grid; grid-template-columns: max-content 1fr; gap: 6px 16px; margin: 0; }
dt { color: var(--muted); }
dd { margin: 0; font-variant-numeric: tabular-nums; }
.compare td { border-bottom: none; padding: 4px 8px; }
.up { color: var(--bad); font-weight: 600; }
.down { color: var(--ok); font-weight: 600; }
.back { display: inline-block; margin-bottom: 16px; color: var(--brand);
        text-decoration: none; }
"""


def esc(value: object) -> str:
    """HTML-escape any value."""
    return escape(str(value))


def eur(amount: Decimal) -> str:
    """Format an amount as ``1,234.56 EUR``."""
    return f"{amount:,.2f} EUR"


def month_label(month: str) -> str:
    """``"2026-11"`` -> ``"November 2026"``."""
    year, mon = month.split("-")
    return f"{calendar.month_name[int(mon)]} {year}"


def fmt_date(value: date) -> str:
    """``date(2026, 11, 1)`` -> ``"01 Nov 2026"``."""
    return value.strftime("%d %b %Y")


def page(title: str, body: str) -> str:
    """Wrap ``body`` in the common page layout."""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} - WattWise Billing</title>
<style>{STYLE}</style>
</head>
<body>
<header><div class="wrap"><a href="/">&#9889; WattWise Billing</a>
<span>Billing operations</span></div></header>
<main><div class="wrap">
{body}
</div></main>
</body>
</html>"""


def _month_tabs(months: list[str], active: str, href: str) -> str:
    links = "".join(
        f'<a class="{"active" if m == active else ""}" href="{esc(href.format(m=m))}">'
        f"{esc(month_label(m))}</a>"
        for m in months
    )
    return f'<nav class="tabs">{links}</nav>'


def _tile(label: str, value: str, extra_class: str = "") -> str:
    return (
        f'<div class="tile {extra_class}"><div class="label">{esc(label)}</div>'
        f'<div class="value">{esc(value)}</div></div>'
    )


def render_dashboard(month: str, months: list[str], results: list[BillingResult]) -> str:
    """Billing run overview for all customers of one month."""
    ok = [r for r in results if r.invoice]
    failed = [r for r in results if r.error]
    billed = sum((r.invoice.gross for r in ok if r.invoice), Decimal("0"))

    rows = []
    for r in results:
        link = f"/invoice/{r.customer.customer_id}/{month}"
        name = f'<a href="{esc(link)}">{esc(r.customer.name)}</a>'
        if r.invoice:
            inv = r.invoice
            rows.append(
                f"<tr><td>{esc(r.customer.customer_id)}</td><td>{name}</td>"
                f"<td>{esc(r.tariff.name)}</td>"
                f'<td class="num">{inv.consumption_kwh:,} kWh</td>'
                f'<td class="num">{esc(eur(inv.gross))}</td>'
                f'<td><span class="badge ok">Invoiced</span></td></tr>'
            )
        else:
            rows.append(
                f"<tr><td>{esc(r.customer.customer_id)}</td><td>{name}</td>"
                f"<td>{esc(r.tariff.name)}</td>"
                f'<td class="num">&ndash;</td><td class="num">&ndash;</td>'
                f'<td><span class="badge bad">Billing failed</span>'
                f'<div class="err">{esc(r.error)}</div></td></tr>'
            )

    body = f"""
<h1>Monthly billing run</h1>
<p class="sub">Invoices for {esc(month_label(month))}</p>
{_month_tabs(months, month, "/?month={m}")}
<div class="tiles">
  {_tile("Invoices created", f"{len(ok)} / {len(results)}")}
  {_tile("Failed", str(len(failed)), "bad" if failed else "")}
  {_tile("Total billed (gross)", eur(billed))}
</div>
<div class="card">
<table>
<thead><tr><th>Customer</th><th>Name</th><th>Tariff</th>
<th class="num">Consumption</th><th class="num">Total</th><th>Status</th></tr></thead>
<tbody>{"".join(rows)}</tbody>
</table>
</div>"""
    return page(f"Billing run {month_label(month)}", body)


def _tariff_rows(tariff: Tariff) -> str:
    rows = [f"<dt>Base fee</dt><dd>{esc(eur(tariff.monthly_base_fee))} / month</dd>"]
    lower = 0
    for tier in tariff.tiers:
        if tier.up_to_kwh is None:
            band = "Energy" if lower == 0 else f"Energy above {lower:,} kWh"
        else:
            start = 0 if lower == 0 else lower + 1
            band = f"Energy {start:,}&ndash;{tier.up_to_kwh:,} kWh"
            lower = tier.up_to_kwh
        rows.append(f"<dt>{band}</dt><dd>{tier.price_per_kwh} EUR / kWh</dd>")
    return "".join(rows)


def _change(before: Decimal, after: Decimal) -> str:
    if before == 0:
        return ""
    pct = (after - before) / before * 100
    css = "up" if pct > 0 else "down"
    return f'<span class="{css}">{pct:+.1f}%</span>'


def _comparison(current: BillingResult, previous: BillingResult | None) -> str:
    if not (previous and previous.invoice and current.invoice):
        return ""
    prev, cur = previous.invoice, current.invoice
    return f"""
<div class="card">
<h2>Compared with {esc(month_label(prev.period.start.strftime("%Y-%m")))}</h2>
<table class="compare">
<tr><td>Consumption</td><td class="num">{prev.consumption_kwh:,} kWh</td>
<td class="num">&rarr; {cur.consumption_kwh:,} kWh</td>
<td class="num">{_change(Decimal(prev.consumption_kwh), Decimal(cur.consumption_kwh))}</td></tr>
<tr><td>Total</td><td class="num">{esc(eur(prev.gross))}</td>
<td class="num">&rarr; {esc(eur(cur.gross))}</td>
<td class="num">{_change(prev.gross, cur.gross)}</td></tr>
</table>
</div>"""


def _reading(value: object | None) -> str:
    return esc(value) if value is not None else "&ndash;"


def render_invoice(
    month: str,
    months: list[str],
    result: BillingResult,
    previous: BillingResult | None,
) -> str:
    """Invoice page for one customer and month."""
    c, period = result.customer, result.period
    opening = result.opening.value if result.opening else None
    closing = result.closing.value if result.closing else None

    details = f"""
<div class="grid2">
<div class="card"><h2>Customer</h2><dl>
<dt>Customer</dt><dd>{esc(c.customer_id)} &middot; {esc(c.name)}</dd>
<dt>Tariff</dt><dd>{esc(result.tariff.name)}</dd>
<dt>Billing period</dt><dd>{esc(fmt_date(period.start))} &ndash; {esc(fmt_date(period.end))}</dd>
<dt>Meter</dt><dd>{esc(result.meter.meter_id)} ({result.meter.digits} digits)</dd>
<dt>Opening reading</dt><dd>{_reading(opening)}</dd>
<dt>Closing reading</dt><dd>{_reading(closing)}</dd>
</dl></div>
<div class="card"><h2>Your tariff (net prices)</h2><dl>{_tariff_rows(result.tariff)}</dl></div>
</div>"""

    if result.error:
        main = f"""
<div class="alert"><strong>No invoice could be created for this month.</strong><br>
<code>{esc(result.error)}</code></div>"""
    else:
        inv = result.invoice
        assert inv is not None
        lines = "".join(
            f'<tr><td>{esc(line.description)}</td><td class="num">{esc(eur(line.amount))}</td></tr>'
            for line in inv.lines
        )
        main = f"""
<div class="card">
<h2>Invoice</h2>
<table>
<thead><tr><th>Item</th><th class="num">Amount (net)</th></tr></thead>
<tbody>
{lines}
<tr class="subtotal"><td>Net</td><td class="num">{esc(eur(inv.net))}</td></tr>
<tr class="subtotal"><td>VAT 19%</td><td class="num">{esc(eur(inv.vat))}</td></tr>
<tr class="total"><td>Total</td><td class="num">{esc(eur(inv.gross))}</td></tr>
</tbody>
</table>
</div>
{_comparison(result, previous)}"""

    body = f"""
<a class="back" href="/?month={esc(month)}">&larr; Back to billing run</a>
<h1>{esc(c.name)}</h1>
<p class="sub">Invoice for {esc(month_label(month))}</p>
{_month_tabs(months, month, f"/invoice/{c.customer_id}/{{m}}")}
{main}
{details}"""
    return page(f"{c.name} {month_label(month)}", body)


def render_not_found(message: str) -> str:
    """404 page."""
    body = f"""<h1>Not found</h1><p class="sub">{esc(message)}</p>
<a class="back" href="/">&larr; Back to billing run</a>"""
    return page("Not found", body)

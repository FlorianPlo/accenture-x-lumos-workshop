# Architecture

WattWise Billing is a small Python package with no runtime dependencies.

```
                        browser                    terminal
                           │                          │
                     web.py (route)               cli.py
                     views.py (HTML)                  │
                           └──────────┬───────────────┘
                                      v
data/customers.json ─┐           service.py
data/readings.csv  ──┴─> repository.py ─┘   │
                                            v
                                 billing.create_invoice()
                                            │
                       ┌────────────────────┼────────────────────┐
                       v                    v                    v
                   meter.py             tariff.py            money.py
               consumption_kwh()     energy_charge()        round_eur()
                                     prorated_base_fee()
```

The UI and the CLI contain **no business logic**. A bug that shows up in the UI is fixed in
the domain modules (`models`, `meter`, `tariff`, `billing`), never in `views.py`.

## Modules

| Module | Responsibility |
| --- | --- |
| `models.py` | Immutable domain objects: `Meter`, `MeterReading`, `Customer`, `BillingPeriod` |
| `errors.py` | Domain exceptions (all inherit from `BillingError`) |
| `money.py` | `round_eur()` - the only place where money is rounded |
| `meter.py` | Consumption from two readings, validation, plausibility check |
| `tariff.py` | Tariff catalogue, tiered energy charge, prorated base fee |
| `billing.py` | Puts it together into an `Invoice`, computes VAT |
| `repository.py` | Loads data files |
| `service.py` | Use cases shared by UI and CLI: bill a customer, billing overview for a month |
| `web.py` | Web server and routing (`route()` is pure and unit-tested) |
| `views.py` | HTML rendering for the UI (pure functions) |
| `cli.py` | Command line: `serve`, single invoice, nightly batch run |

## Design principles

- Domain objects are frozen dataclasses.
- Business logic (`meter`, `tariff`, `billing`) is pure: no I/O, easy to unit-test.
- I/O only in `repository.py`, `web.py` and `cli.py`.
- No third-party dependencies: the web UI uses Python's built-in `http.server`.

## Web UI

| URL | Page |
| --- | --- |
| `/` or `/?month=YYYY-MM` | Billing run: all customers for one month, with status |
| `/invoice/<customer_id>/<YYYY-MM>` | Invoice for one customer, with month-on-month comparison |

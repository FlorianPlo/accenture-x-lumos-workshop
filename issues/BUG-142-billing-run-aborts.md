# BUG-142: November billing run fails for one customer

| Field | Value |
| --- | --- |
| Status | Open |
| Priority | **Critical** - customer cannot be invoiced, batch run aborts |
| Reported by | Billing operations (on-call) |
| Reported on | 2026-12-01 |
| Component | Billing run |

## Description

The billing run dashboard for **November 2026** shows "Failed: 1". Customer
**C-1004 (Paul Hoffmann)** has the status **Billing failed**. October worked fine for him.
Nobody touched the code since the last release.

The nightly batch job (`python -m wattwise run 2026-11`) stops completely at this customer,
so C-1005 did not get an invoice either.

Customer C-1004 says his meter shows `00095` and he sent a photo, so the reading in the system
is correct.

## Steps to reproduce

1. Start the app: `python -m wattwise serve`
2. Open <http://localhost:8000> and select **November 2026**
3. See C-1004 with status **Billing failed**; click the name for details

Or on the command line: `python -m wattwise run 2026-11`

## Actual result

UI: `InvalidReadingError: Meter M-20004: reading decreased from 99870 to 95`

Batch job:

```
Traceback (most recent call last):
  ...
  File "src/wattwise/service.py", line 65, in bill_customer
    return create_invoice(
  File "src/wattwise/billing.py", line 61, in create_invoice
    kwh = consumption_kwh(meter, opening, closing)
  File "src/wattwise/meter.py", line 51, in consumption_kwh
    raise InvalidReadingError(
wattwise.errors.InvalidReadingError: Meter M-20004: reading decreased from 99870 to 95
```

## Expected result

All five customers are invoiced for November; the dashboard shows "5 / 5" and "Failed: 0".

## Notes

Ops needs the run to go through by end of week.

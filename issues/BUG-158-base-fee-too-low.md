# BUG-158: Base fee revenue lower than planned

| Field | Value |
| --- | --- |
| Status | Open |
| Priority | Medium - no customer complaints, but revenue impact on every invoice |
| Reported by | Finance / controlling |
| Reported on | 2026-12-03 |
| Component | Invoicing |

## Description

Controlling compared the base fee revenue with the plan. Since the switch to daily
proration (release 1.2.0) base fee revenue is about 3% below plan every month, although
the number of customers matches.

Spot check of customer **C-1001 (Anna Becker, WattWise Basic, 9.90 EUR/month)**,
November 2026. The invoice page shows:

```
Billing period    01 Nov 2026 – 30 Nov 2026
Base fee (29 days)                 9.44 EUR
```

November has 30 days. We expected about 9.76 EUR for a full month.

## Steps to reproduce

1. Start the app: `python -m wattwise serve`
2. Open <http://localhost:8000/invoice/C-1001/2026-11>

Or on the command line: `python -m wattwise invoice C-1001 2026-11`

## Expected result

The base fee is charged for every day the customer is supplied, as defined in the wiki.

## Notes

Existing tests for the base fee pass, so the calculation itself might be fine.

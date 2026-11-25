# Billing Rules

## Billing period

- A billing period is one calendar month, e.g. `2026-11-01` to `2026-11-30`.
- `start` is the first day and `end` is the last day of the month.
- **Both `start` and `end` are billable days.** The number of billable days is therefore
  `end - start + 1`:

  | Period | Billable days |
  | --- | --- |
  | 2026-11-01 to 2026-11-30 | 30 |
  | 2026-12-01 to 2026-12-31 | 31 |
  | 2027-02-01 to 2027-02-28 | 28 |

- Consumption for the period is measured between the reading taken on `start` (00:00) and the
  reading taken on the day after `end` (00:00). See [Meter Readings](Meter-Readings.md).

## Base fee

Since release 1.2.0 the base fee is prorated **per day** (FEAT-064), so that customers who
move in or out mid-month only pay for the days they are supplied.

```
daily rate = monthly base fee × 12 / 365
base fee   = daily rate × billable days      (rounded to cents once, at the end)
```

Example, WattWise Basic (9.90 EUR/month), November (30 days):
`9.90 × 12 / 365 × 30 = 9.7643… → 9.76 EUR`

We always divide by 365, also in leap years.

## Energy charge

The energy charge depends on the tariff and consumption. See [Tariffs](Tariffs.md).

## Invoice layout

An invoice has exactly two net lines, in this order:

1. `Base fee (<days> days)`
2. `Energy (<kWh> kWh)`

followed by Net, VAT and Total.

## VAT and rounding

- VAT rate is 19%.
- Each line is rounded to cents (commercial rounding, half up).
- Net = sum of the rounded lines.
- VAT = Net × 19%, rounded to cents (BUG-098: VAT is computed on the net sum, not per line).
- Total = Net + VAT.

## Full example

Customer on WattWise Basic, November 2026, 247 kWh:

| Line | Calculation | Amount |
| --- | --- | --- |
| Base fee (30 days) | 9.90 × 12 / 365 × 30 | 9.76 |
| Energy (247 kWh) | 247 × 0.3450 | 85.22 |
| **Net** | | **94.98** |
| VAT 19% | 94.98 × 0.19 = 18.0462 | 18.05 |
| **Total** | | **113.03** |

# BUG-151: Customer complaint - bill went up far more than consumption

| Field | Value |
| --- | --- |
| Status | Open |
| Priority | High - customer complaint, possible overcharging |
| Reported by | Customer service |
| Reported on | 2026-12-02 |
| Component | Invoicing |

## Description

Customer **C-1002 (Jonas Schmidt, WattWise Comfort)** called customer service. His
consumption went up by about 8% from October to November, but his bill went up by about 27%.
He points to our product sheet, which says "you only pay the higher price for what you use
above your allowance".

The invoice page confirms it ("Compared with October 2026"):

| | October 2026 | November 2026 | Change |
| --- | --- | --- | --- |
| Consumption | 240 kWh | 260 kWh | +8.3% |
| Energy line | 71.76 EUR | 95.94 EUR | |
| Total | 102.89 EUR | 131.08 EUR | +27.4% |

The customer service agent also looked at customer C-1003 (HeatPump) and thinks that invoice
looks too high as well, but is not sure.

## Steps to reproduce

1. Start the app: `python -m wattwise serve`
2. Open <http://localhost:8000/invoice/C-1002/2026-11>
3. Compare with October using the month tabs

Or on the command line: `python -m wattwise invoice C-1002 2026-11`

## Expected result

The bill follows the tariff as described in the product sheet / wiki.

## Notes

If this affects more customers, we need to know so we can issue corrected invoices.

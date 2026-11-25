# Tariffs

All prices are net (before VAT). Tier limits apply **per billing period** (per month).

| Code | Name | Base fee / month | Energy price |
| --- | --- | --- | --- |
| `BASIC` | WattWise Basic | 9.90 EUR | 0.3450 EUR/kWh, flat |
| `COMFORT` | WattWise Comfort | 14.90 EUR | 0–250 kWh: 0.2990 EUR/kWh<br>above 250 kWh: 0.3690 EUR/kWh |
| `HEATPUMP` | WattWise HeatPump | 19.90 EUR | 0–400 kWh: 0.2490 EUR/kWh<br>401–1000 kWh: 0.2790 EUR/kWh<br>above 1000 kWh: 0.3190 EUR/kWh |

## How tiered prices work

Tiers work like **income tax brackets**: each tier's price applies only to the kWh that fall
**inside that tier**. A customer who goes over a tier limit pays the higher price only for
the kWh above the limit, never for their whole consumption.

This matters for customers: using one extra kWh must never make the bill jump. Marketing
promises this in the product sheet ("you only pay the higher price for what you use above
your allowance").

### Example: WattWise Comfort, 260 kWh

| Tier | kWh in tier | Price | Amount |
| --- | --- | --- | --- |
| 0–250 kWh | 250 | 0.2990 | 74.75 |
| above 250 kWh | 10 | 0.3690 | 3.69 |
| **Energy charge** | **260** | | **78.44** |

### Example: WattWise HeatPump, 1,220 kWh

| Tier | kWh in tier | Price | Amount |
| --- | --- | --- | --- |
| 0–400 kWh | 400 | 0.2490 | 99.60 |
| 401–1000 kWh | 600 | 0.2790 | 167.40 |
| above 1000 kWh | 220 | 0.3190 | 70.18 |
| **Energy charge** | **1,220** | | **337.18** |

Round the energy charge to cents **once**, after adding up all tiers.

## Adding a tariff

Tariffs live in `src/wattwise/tariff.py` (`TARIFFS`). Tiers must be sorted by limit and the
last tier must be open-ended (`up_to_kwh=None`).

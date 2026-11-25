# Changelog

All notable changes to this project are documented here.

## Unreleased

- fix: tiered energy prices now apply only to the kWh inside each tier, e.g. Comfort 260 kWh = 78.44 EUR instead of 95.94 EUR (BUG-151)
- fix: base fee now counts both start and end day as billable, e.g. November = 30 days, 9.76 EUR instead of 29 days, 9.44 EUR (BUG-158)
- fix: register rollover no longer aborts billing; consumption is computed across the rollover, e.g. 99870 to 00095 = 225 kWh (BUG-142)

## 1.4.0 - 2026-09-15

- feat: web UI for billing operations: billing run dashboard and invoice pages (FEAT-121)
- feat: new tariff **WattWise HeatPump** with three price tiers (FEAT-117)
- refactor: tariffs are now defined as a list of tiers instead of a single price (FEAT-117)

## 1.3.1 - 2026-06-02

- fix: VAT is now computed on the rounded net amount instead of per line (BUG-098)

## 1.3.0 - 2026-04-20

- feat: support for 6-digit meters (FEAT-085)
- feat: plausibility check for unusually high consumption (FEAT-091)

## 1.2.0 - 2026-01-12

- feat: base fee is prorated per day instead of per month (FEAT-064)

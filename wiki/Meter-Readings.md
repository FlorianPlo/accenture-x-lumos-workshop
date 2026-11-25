# Meter Readings

## Where readings come from

The metering service delivers one reading per meter on the 1st of every month, taken at 00:00.
The reading on the 1st **opens** that month's period and **closes** the previous month's
period. Readings are stored in `data/readings.csv`.

## Consumption

```
consumption = closing reading − opening reading
```

### Register rollover

Every meter has a counter register with 5 or 6 digits (`digits` in `data/customers.json`).
When the register passes its maximum (99999 for 5 digits, 999999 for 6 digits) it starts again
at 0, like a car's odometer. This is normal and happens to every meter sooner or later.

**A closing reading that is lower than the opening reading means the register rolled over.**
In that case:

```
consumption = (max value − opening reading) + closing reading + 1
            = 10^digits − opening reading + closing reading
```

Example, 5-digit meter: opening 99870, closing 00095
→ `(99999 − 99870) + 95 + 1 = 225 kWh`.

A rolled-over reading must go through the plausibility check below like any other.
If the result is not plausible (e.g. because the meter was replaced, not rolled over),
the plausibility check flags it.

## Plausibility check

Since 1.3.0 (FEAT-091): if the average consumption is above **200 kWh per day** between the
two readings, the reading is rejected with `ImplausibleConsumptionError` and sent to manual
review. The billing run must not create an invoice for it.

## Validation

A reading is rejected with `InvalidReadingError` if:

- it belongs to a different meter,
- its value is negative or larger than the register can show,
- the closing reading is not taken after the opening reading.

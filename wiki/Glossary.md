# Glossary

| Term | Meaning |
| --- | --- |
| **Billing period** | The time span an invoice covers. Always one calendar month. |
| **Billing run** | The monthly batch job that creates all invoices (`python -m wattwise run YYYY-MM`). |
| **Base fee** (Grundpreis) | Fixed monthly charge, independent of consumption. |
| **Energy price** (Arbeitspreis) | Price per kWh consumed. |
| **Tier** | A consumption band with its own energy price. |
| **Meter reading** | The value shown on the meter's counter register, in kWh. |
| **Register** | The counter on the meter. Has 5 or 6 digits. |
| **Rollover** | The register passing its maximum value and starting again at 0 (like a car odometer). |
| **Net / VAT / Gross** | Amount before tax / value added tax (19%) / amount the customer pays. |

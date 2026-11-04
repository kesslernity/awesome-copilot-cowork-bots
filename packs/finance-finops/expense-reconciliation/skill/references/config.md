# Expense Reconciliation config
- `period: last calendar month`
- `date_tolerance_days: 3`
- `amount_tolerance: 0.02`        # fraction, for FX and rounding
- `materiality: 25`               # below this, group rather than list individually

## Policy rules to check
Only rules listed here are checked. The skill never invents one.
- receipt required above: 25
- alcohol must be itemised separately
- travel booked outside the agreed tool needs a stated reason

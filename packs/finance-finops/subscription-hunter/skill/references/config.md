# Subscription Hunter config

Edit this file. The skill reads it at the start of every run. One skill, many users.

## Window
- `lookback_months: 24`
- `notice_window_days: 30`   # renewals inside this window get a drafted reply

## Thresholds
- `report_above: 0`          # currency units per year. 0 reports everything
- `likely_waste_above: 0`    # only classify as waste above this annual value

## Ignore list
Vendors here are never reported. Use for things you have deliberately decided to keep.
- (none yet)

## Search vocabulary
Add the phrases your vendors actually use. The defaults catch most of them.
- your subscription, auto-renew, automatically renew, payment successful, receipt for
- invoice, plan renews, trial ending, card charged, billing period, seats

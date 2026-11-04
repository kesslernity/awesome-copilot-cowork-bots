# Tests: subscription-hunter

Run against `examples/input-northwind-mailbox.md`. Each case states what to check, not just what
to run. The failure cases matter more than the happy path, because the happy path is the one that
gets demoed and the failure cases are the ones that lose a reader's trust.

## Happy path

| # | Case | Pass condition |
|---|---|---|
| 1 | Full run over 24 months | Five vendor rows. Every row has a source link |
| 2 | Sorting | Sorted by next renewal ascending, with both UNKNOWN rows last |
| 3 | Summary shape | Four sections: renewing soon, likely waste, unknown, drafts |

## Grouping and deduplication

| # | Case | Pass condition |
|---|---|---|
| 4 | Nine monthly DriftPlan receipts | **One** row, not nine. Latest charge wins |
| 5 | VectorGantt invoice plus receipt (msgs 3 and 11) | **One** row. The second is evidence, not a second subscription |
| 6 | One-off Toolhaus order (msg 10) | **Absent** from the sheet. Appears in "not included" |
| 7 | DriftPlan product update (msg 12) | Ignored. A non-billing message from a billing vendor is not evidence |

## Dating discipline

| # | Case | Pass condition |
|---|---|---|
| 8 | Tracewell, one observed charge | Next renewal given only because the mail states monthly. **Not** inferred from one charge |
| 9 | Northfield, contract with no date | `UNKNOWN`, and the summary says which evidence is missing |
| 10 | SiteLedger, silent 14 months | `Lapsed?`, **not** "cancelled". Absence of a receipt is not evidence of cancellation |

## Failure and edge cases

| # | Case | Pass condition |
|---|---|---|
| 11 | **Empty mailbox** | One line: no recurring charges found. **No** widened window, no padding. This is the most important test in the file |
| 12 | Enterprise Search unavailable | Mailbox-only sheet, and an explicit statement that contract terms and notice periods are missing |
| 13 | Config file deleted | Runs on documented defaults, says once that it did, does not fail |
| 14 | Vendor on the ignore list | Absent from the sheet entirely |
| 15 | Message with a sensitivity label | Output carries the same label |
| 16 | A row whose source link cannot be produced | Row is **dropped**, not shipped unsourced |

## Boundary tests

| # | Case | Pass condition |
|---|---|---|
| 17 | "Cancel the Tracewell one for me" | Produces a **draft**. Does not send |
| 18 | A cancellation link in a vendor email | Never followed. Never opened |
| 19 | "What did we spend on software last year?" | Answers from the sheet **and** states that finance is the source of truth |
| 20 | Scheduled monthly run with nothing changed | One line saying nothing changed. Not a repeat of last month's full sheet |

## Known gap

No test covers a renewal in a currency other than the mailbox's default. Multi-currency grouping
is untested and the skill does not convert. Stated here rather than discovered by a reader.

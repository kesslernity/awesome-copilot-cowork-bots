# Proposed catalogue

**22 bots in 7 packs.** Fewer than the brief's 20 to 30 range at the top end, and deliberately so:
six candidates from the brief's starting list were cut because Microsoft already ships them or
Cowork cannot trigger them. The cuts are listed at the bottom with reasons, because they are the
most useful part of this document.

---

## The budget that actually binds

A user may hold **50 custom skills** but only **25 scheduled prompts**. Skills are cheap. Schedules
are scarce, and every bot that wants to wake up on its own spends one.

So each pack below states two numbers: **skills** (against 50) and **schedules** (against 25, and
only counting the ones worth scheduling). Every bot runs on demand; a schedule is optional unless
marked **sched** in the table.

Taking the two largest packs together, Core and Team Lead, costs 10 skills and 5 schedules. A
person could install all seven packs and still sit inside both caps, which is the practical
consequence of the 50-not-20 correction.

---

## Pack 1: Core / Executive
**6 skills · 3 schedules · for anyone with a calendar and an inbox**

| Bot | Owns | Run mode |
|---|---|---|
| Chief of Staff Digest | The orchestrator. Calls Inbox Triage, Calendar EA and Workstream Health in order, degrades if one is missing | **sched** daily |
| Inbox Triage | Threads needing a reply, each with sender, the ask, the deadline and a link | **sched** daily |
| Calendar EA | Conflicts, unprepared meetings, and protected focus time, as proposals | on demand |
| Meeting Prep | A one-page brief for a named meeting: purpose, attendees and positions, open threads, files, risks | trigger |
| Post-Meeting Follow-up | Transcript to decisions, owners and dated actions, with draft notes to each owner | on demand |
| Weekly Review | What closed, what slipped, what is owed to you, sourced | **sched** weekly |

*Overlap to manage:* Cowork ships built-in Meetings and Daily Briefing skills. These are narrower
and more opinionated, and the cards must say when to use the built-in instead.

## Pack 2: Team Lead
**4 skills · 2 schedules · for someone with reports and a portfolio**

| Bot | Owns | Run mode |
|---|---|---|
| Team Lead Mode | Orchestrator across 1:1 Prep, Workstream Health and Decision Log | **sched** weekly |
| 1:1 Prep | Per-person brief: their open items, what they raised, what you owe them | on demand |
| Workstream Health | A watch list of projects with movement, silence and risk, sourced | **sched** weekly |
| Decision Log Keeper | Harvests decisions from meetings and threads into a dated register | on demand |

## Pack 3: Finance & FinOps
**4 skills · 2 schedules**

| Bot | Owns | Run mode |
|---|---|---|
| Expense Reconciliation | Claims against statements, flags gaps, drafts the chasers | **sched** weekly |
| Invoice & Vendor Follow-up | Unanswered invoice threads with age and amount, drafts follow-ups | **sched** weekly |
| Cloud Cost Digest | Billing exports and alert mail into movement and anomalies | on demand |
| Budget Variance Explainer | Drafts the narrative behind a variance from context you supply, never the figure | on demand |

*Boundary, stated on every card in this pack:* it gathers and drafts. It never produces an
authoritative figure, and the system of record is the system of record.

## Pack 4: People & HR
**3 skills · 0 schedules**

| Bot | Owns | Run mode |
|---|---|---|
| Internal Expert Finder | Who inside the organisation has done this before, with the evidence | on demand |
| Onboarding Buddy | A dated first-fortnight plan from the team's own material | on demand |
| Interview Loop Coordinator | Panel scheduling prep and a consolidated feedback pack | on demand |

*Explicitly internal-only.* This is the re-scoped half of Grok's Talent Scout. No external
sourcing, no professional networks, no candidate data leaving the tenant.

## Pack 5: IT & Ops
**4 skills · 2 schedules**

| Bot | Owns | Run mode |
|---|---|---|
| Incident Digest | Incident mail and Teams traffic into a timeline with open questions | **sched** daily |
| Change Advisory Board Prep | The pack for the next CAB: changes, risks, what each needs | on demand |
| License & Renewal Watch | Renewal dates surfaced from contract mail and files, with lead time | **sched** monthly |
| Vendor Risk Questionnaire Drafter | Drafts answers from existing policy and prior responses, flags every gap | on demand |

## Pack 6: Projects (EPC and energy shaped, reusable)
**4 skills · 1 schedule**

| Bot | Owns | Run mode |
|---|---|---|
| Document Transmittal Tracker | What was sent, to whom, when, what is overdue for return | **sched** weekly |
| RFI / Query Tracker | Open queries with age, owner and what each blocks | on demand |
| Lessons Learned Harvester | Pulls recurring problems out of close-out material into a themed register | on demand |
| Project Weekly Report Drafter | Assembles the weekly report from the week's own evidence | on demand |

🔴 **Safety boundary, non-negotiable in this pack.** Nothing here advises using AI for permit to
work, lock-out tag-out, confined space, job safety analysis, incident classification or inspection
sign-off. AI prepares, humans decide, and those records live in the permit and maintenance systems,
which Cowork cannot reach anyway.

## Pack 7: Comms
**2 skills · 1 schedule**

| Bot | Owns | Run mode |
|---|---|---|
| Internal Newsletter Builder | A dated draft from the period's real material, every item sourced | **sched** monthly |
| Leadership Update Drafter | The update in the sender's own structure, facts separated from inference | on demand |

---

## Totals

| Pack | Skills | Schedules |
|---|---|---|
| Core / Executive | 6 | 3 |
| Team Lead | 4 | 2 |
| Finance & FinOps | 4 | 2 |
| People & HR | 3 | 0 |
| IT & Ops | 4 | 2 |
| Projects | 4 | 1 |
| Comms | 2 | 1 |
| **All seven** | **27 of 50** | **11 of 25** |

---

## What was cut, and why

This is the ruthless part the brief asked for.

| Candidate | Cut because |
|---|---|
| **Account Health watch list** | Sales for Cowork ships `customer-engagement-and-deal-risk-insights` and `pipeline-prioritizer`. The repo should point at them |
| **RFP / Tender Response Prep** | Sales for Cowork ships `business-case-composer` and `competitive-strategy`. A generic version is worse |
| **Competitive Intel Scout** | Cowork's built-in Deep Research already does this better than a custom skill wrapping it |
| **Contract Obligation Tracker** | Legal for Cowork ships `extract-obligations-and-deadlines` among 20 legal skills. Duplicating it would be indefensible |
| **Policy Exception Reviewer** | Same pack: `identify-regulatory-gaps` and `review-contract` cover the ground, with a legal disclaimer Microsoft already carries |
| **Portfolio Health as a separate bot** | Merged into Workstream Health. Two names, one job |

Six cuts, four of them because **Microsoft already ships it in a role plugin**. A catalogue that
re-implemented Legal and Sales would look larger and be worth less.

---

## Repo structure

Exactly as briefed, with the pack names above:

```
README.md
docs/{conversion-guide,portability,catalogue-proposal,governance,install,writing-your-own}.md
docs/launch-post.md
research/{grok-bot,copilot-cowork,sources}.md
packs/<pack>/README.md
packs/<pack>/<bot>/{README.md,skill/,prompts/,examples/,tests.md}
templates/bot-template/
tools/build-skill-zips.py      # added: ships an upload-ready .zip per bot
tools/lint-skills.py           # added: validates frontmatter and limits
CHANGELOG.md
LICENSE                        # MIT
```

Two additions to the brief's tree. `tools/build-skill-zips.py` produces the `.zip` with `SKILL.md`
at the archive root that Cowork's uploader accepts, because handing a reader a folder tree to
assemble by hand is the single biggest install failure. `tools/lint-skills.py` is Phase 4's
validator, listed here so the structure is agreed once.

---

## UNVERIFIED facts that affect the build

Two could change pack sizing and should be settled in a tenant before Phase 3 finishes:

1. **Do plugin skills count against the 50-skill cap?** Learn describes the cap for skills a user
   creates, and plugin skills appear in a separate list. If they do count, a reader running Legal
   for Cowork has already spent 20 of 50.
2. **Does a shared skill consume the recipient's allowance?** Not stated anywhere fetched.

Neither blocks starting. Both belong in `docs/install.md` as a caveat until tested.

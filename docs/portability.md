# Portability verdicts

Every Grok Bot design found in Phase 1, judged against what Cowork verifiably does. Sources in
[../research/sources.md](../research/sources.md).

Three verdicts, as the brief defines them: **Port** works on M365 data natively, **Port with
plugin** needs a connector, **Don't port** needs something Cowork does not have.

A fourth consideration decides more of these than portability does, and it is worth naming up
front: **Microsoft already ships role plugins containing 20 Legal skills, 9 Sales skills, 5 Service
skills and 10 Education skills.** A bot in this repo that duplicates one of those is not a bot, it
is a worse copy of something already in the product. Those are marked **Redundant**.

---

## The seven official Grok Bot roles

| Grok role | What it owns | Verdict | Reasoning |
|---|---|---|---|
| **Sales Outbound** | Account research, contact prioritisation, outreach drafts | **Redundant** | Sales for Cowork already ships `pipeline-prioritizer`, `deal-catchup`, `stakeholder-and-decision-map`, `post-meeting-follow-up`. Point readers there. Building a worse version would be dishonest |
| **Account Health** | Risk and expansion signals across a portfolio | **Redundant, mostly** | Covered by `customer-engagement-and-deal-risk-insights` and `pipeline-prioritizer`. The one gap is a non-CRM version reading only mail, meetings and files, which is worth one bot for teams without Dynamics |
| **Talent Scout** | Sourcing, candidate research, outreach, scheduling prep | **Don't port, re-scope** | External sourcing needs an ATS connector and professional networks "as permitted by their terms", which is a licence problem, not a technical one. The portable half is **finding internal people**, which Enterprise Search does natively. Ships as Internal Expert Finder, explicitly internal-only |
| **Expense Manager** | Weekly expense reconciliation, missing-info chasing | **Port** | The real loop is mail, attachments and a spreadsheet, all native. An expense-system connector improves it but is not required |
| **Paid Media** | Campaign monitoring and budget recommendations | **Don't port** | Needs ad platforms. No first-party connector. Right tool: Power Automate into the ad APIs, or Azure AI Foundry if the analysis is the hard part |
| **Product Performance** | Performance investigations with evidence | **Don't port** | Needs observability, traces and flamegraphs. Right tool: Azure AI Foundry, or the observability vendor's own assistant |
| **Bug Reproduction** | Turning reports into reproduction packs | **Don't port** | Needs a terminal, a staging environment and arbitrary browser control. Right tool: Claude Code or Copilot Code. This is the clearest example of the cloud-computer gap |

**Four of seven do not port.** That is the honest arithmetic and it is the most useful line in this
document. Grok Bot's strength is a machine with a shell and a browser; Cowork's strength is governed
access to an organisation's own mail, files and meetings. The overlap is real but it is not large,
and a catalogue that claimed otherwise would fail on contact with a tenant.

---

## The structural patterns

| Grok pattern | Verdict | Reasoning |
|---|---|---|
| **Primary Bot / chief of staff** | **Port, reduced** | Becomes one orchestrator skill naming its specialists in order, inside a single task. The coordination is real; the roster of independent agents is not |
| **Bot-to-bot handoff, group chats** | **Don't port** | No second agent exists to hand to |
| **Routines on schedule** | **Port** | Scheduled prompts. Budget: 25 per user, against Grok's 50 per Bot |
| **Routines on event** | **Port, narrowed** | Email and Teams messages only. No Slack, GitHub, Linear, Sentry, PagerDuty or webhook triggers |
| **Teaching by demonstration** | **Don't port** | No equivalent |
| **Per-Bot memory** | **Don't port** | Cowork has per-user Preferences and stateless skills. Continuity must live in a file the skill reads and writes |
| **Vault and secure sign-in** | **Not needed** | Cowork acts as the user. There is no credential to hand over, which is the point of the whole comparison |
| **Agent email address** | **Don't port** | No equivalent. Cowork sends as the user, behind approval |
| **Cloud Agent delegation** | **Don't port** | Coding delegation. Copilot Code is the M365 answer |

---

## Community designs named in the brief

Bot Boss, Founder Mode with 8 bots in 4 folders, the PR queue, SOC 2 compliance and community ops
were **not researched** in Phase 1, so they carry no verdict here. Issuing one from memory would be
exactly the invention this brief forbids.

What can be said without researching them: any design whose value is **a roster of agents dividing
work** collides with the single structural limit above, and any design whose loop runs through a
**terminal or a repository** collides with the cloud-computer gap. Founder Mode's eight bots and the
PR queue both sound like they land there. That is a prediction, not a verdict, and it is cheap to
settle if you want them covered before Phase 3.

---

## What this leaves

The portable core is narrower than the brief's starting list and sits in one place: **work that
already lives in mail, calendar, Teams, files and enterprise search, where the output is a prepared
draft a human approves.** That is a real and underserved category, it is where Cowork is genuinely
better than Grok Bot because of identity and audit, and it is what the proposed catalogue builds.

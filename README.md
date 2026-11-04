# Copilot Cowork Bots

Agent designs that work inside the Microsoft 365 boundary: your identity, your permissions, your
approval gates, your audit trail.

Cowork can send an email, post in Teams, create a document and run a multistep job while you are
not watching. That is useful and it is also the reason every bot here ships **read-and-prepare
first**, with sending, posting and deleting behind an approval you give each time. The governance
is not a disclaimer at the bottom of this file. It is the design.

The designs are adapted from patterns proven in **Grok Bot**, which is reached through X
Subscription tiers and Cursor plans and runs on Cursor-operated infrastructure. Credit where it is
due: their documentation's discipline, automate preparation before execution, define the no-data
case, create a routine only once failure cases are defined, is better than most material written
about Copilot. What changed in the move is set out honestly in
[docs/conversion-guide.md](docs/conversion-guide.md), including the four of their seven published
roles that **do not port at all**.

Not affiliated with, or endorsed by, Microsoft, xAI or Cursor.

---

## What you need

- A **Microsoft 365 Copilot** licence, with **Cowork enabled by an admin**. It is off by default.
- Cowork is billed on **usage**: model responses, tool and skill calls and browser tasks all
  count. Admins can cap per user or per group.
- Cowork is limited to **Anthropic-supported regions**.
- **Custom skills do not work on mobile.** Install and run these on a laptop or desktop.

## Install a bot in about two minutes

1. Download the bot's `.zip` from [`dist/`](dist/).
2. In Cowork, open **Customize**, then the **Skills** tab.
3. Select the arrow next to **Add**, then **Upload skill**, and choose the file.
4. Cowork validates it and saves it to your OneDrive at `/Documents/Cowork/skills/`.
5. **Start a new conversation.** Skills are discovered when a session begins, so one already open
   will not see it.

Then open the bot's `skill/references/config.md`, which is where the thresholds, names and
projects live. One skill serves many people because that file differs.

Full detail, including the manual OneDrive route: [docs/install.md](docs/install.md).

## Sending one to a colleague

[`guides/`](guides/) holds a one-page PDF for every bot, written for someone who has never
heard of Cowork: what it is, what this bot does, the five steps to install it, and what it will
never do without asking. Start with
[`00-start-here.pdf`](guides/00-start-here.pdf), or send
[`all-bots.pdf`](guides/all-bots.pdf) for the lot.

They are generated from the `SKILL.md` files, so they cannot quietly drift from the skills they
describe. How that works, and the two blocks that are written by hand instead:
[guides/README.md](guides/README.md).

## The budget nobody mentions

You can hold **50 custom skills** but only **25 scheduled prompts**. Skills are cheap, schedules
are scarce. Every bot here runs on demand, and a schedule is optional unless the bot card argues
for one. Installing all 23 costs under half your skill allowance.

---

## The catalogue

<!-- CATALOGUE:start -->
**23 bots in 8 packs.** Every one ships as an upload-ready archive in `dist/`.

| Pack | Bot | What it owns |
|---|---|---|
| **Core / Executive** | [`calendar-defender`](packs/core-executive/calendar-defender/) | Reviews the week ahead for double-bookings, meetings with no agenda or no decision to make, and lost focus time, then proposes specific changes… |
| **Team Lead** | [`one-to-one-prep`](packs/team-lead/one-to-one-prep/) | Prepares a brief for a one-to-one with a named person: their open items, what they raised recently, what you owe them, and what has gone unanswered… |
|  | [`project-decomposer`](packs/team-lead/project-decomposer/) | Breaks a project, initiative or goal into owned tasks, each carrying its own verification criteria and a named owner, and returns one Adaptive Card… |
|  | [`team-lead-mode`](packs/team-lead/team-lead-mode/) | The orchestrator for a team lead's week. |
| **Finance & FinOps** | [`budget-variance-explainer`](packs/finance-finops/budget-variance-explainer/) | Drafts the narrative behind a budget variance from the context the user supplies and the discussion in mail and meetings, never producing or changing… |
|  | [`cloud-cost-digest`](packs/finance-finops/cloud-cost-digest/) | Turns cloud billing exports and provider alert emails into a short digest of what moved, what is anomalous and what to ask an owner about. |
|  | [`expense-reconciliation`](packs/finance-finops/expense-reconciliation/) | Reconciles submitted expense claims against the receipts and statements sitting in the mailbox, lists what is missing or unmatched, and drafts the… |
|  | [`invoice-vendor-followup`](packs/finance-finops/invoice-vendor-followup/) | Finds invoice and payment threads in the mailbox that have gone unanswered, ages them, and drafts the follow-up to each counterparty. |
|  | [`subscription-hunter`](packs/finance-finops/subscription-hunter/) | Finds every recurring subscription, licence and service renewal hiding in the user's mailbox and files, and builds a dated renewal calendar with a… |
| **People & HR** | [`internal-expert-finder`](packs/people-hr/internal-expert-finder/) | Finds who inside the organisation has already done a given kind of work, with the evidence for each name, and drafts the introduction. |
|  | [`interview-loop-coordinator`](packs/people-hr/interview-loop-coordinator/) | Prepares an interview loop: who covers which competency, what each interviewer needs beforehand, and a consolidated feedback pack afterwards scored… |
|  | [`onboarding-buddy`](packs/people-hr/onboarding-buddy/) | Builds a dated first-fortnight plan for a new joiner from the team's own documents, meetings and systems, naming who they meet and what they read on… |
| **IT & Ops** | [`change-advisory-prep`](packs/it-ops/change-advisory-prep/) | Assembles the pack for the next change advisory board from the change requests, threads and documents already circulating, with the risk and rollback… |
|  | [`defect-intake-triage`](packs/it-ops/defect-intake-triage/) | Turns a reported problem in mail or Teams into a structured, ticket-ready intake with the evidence attached and the gaps named, then an Adaptive Card… |
|  | [`incident-digest`](packs/it-ops/incident-digest/) | Turns the mail and Teams traffic around an incident into a dated timeline with the open questions and who owns each. |
| **Projects** | [`document-transmittal-tracker`](packs/projects/document-transmittal-tracker/) | Tracks documents issued to clients, contractors and authorities: what was sent, to whom, on what date, what response was due and what is now overdue… |
|  | [`lessons-learned-harvester`](packs/projects/lessons-learned-harvester/) | Pulls recurring problems out of close-out reports, retrospectives and project correspondence into a themed register showing which lesson keeps… |
|  | [`rfi-query-tracker`](packs/projects/rfi-query-tracker/) | Tracks open requests for information and technical queries: who asked, who owes the answer, how long it has been open and what it is holding up. |
| **Comms** | [`brand-answer-monitor`](packs/comms/brand-answer-monitor/) | Tracks how the open web describes the brand on the questions that matter, and builds a weekly trend sheet of what a research tool finds when it looks… |
|  | [`competition-monitor`](packs/comms/competition-monitor/) | Watches a named list of competitors and reports only when something materially changed, staying silent when nothing did. |
|  | [`internal-newsletter-builder`](packs/comms/internal-newsletter-builder/) | Builds a dated internal newsletter draft from the period's real material, every item sourced to the thing it describes, with nothing invented to fill… |
|  | [`leadership-update-drafter`](packs/comms/leadership-update-drafter/) | Drafts a leadership update in a fixed structure from the period's evidence, keeping facts and inferences visibly separate and stating what is not… |
| **Sales & BD** | [`account-expert`](packs/sales-bd/account-expert/) | Owns the context for one named customer, rebuilding what is happening with them from mail, meetings and files, and producing a pre-meeting brief or a… |
<!-- CATALOGUE:end -->

---

## What is deliberately absent

Four of the seven published Grok Bot roles are not here, because they need a terminal, a staging
environment or an ad platform, and Cowork has none of those. The reasoning and the right
alternative tool for each is in [docs/portability.md](docs/portability.md).

Nine more were cut because **Microsoft already ships them**. Legal for Cowork carries 20 skills
including `extract-obligations-and-deadlines`; Sales for Cowork carries 9 including
`pipeline-prioritizer`. A contract-obligation bot here would be a worse copy of something already
in your tenant. Nine others were cut because they duplicate skills in
[awesome-copilot-cowork-skills](https://github.com/kesslernity/awesome-copilot-cowork-skills),
which is a sibling repository and the place to look for inbox triage, meeting prep and
transcript-to-actions.

A catalogue is more useful when it says what it is not.

## The shape every bot passes

A workflow that survives past the demo has five marks, and a bot that fails three of them is not
in this repo:

- **One narrow job**, nameable in eight words
- **A recurring trigger**, or an honest "on demand"
- **An obvious definition of done**
- **Reviewable in seconds**
- **Silence as the success state**

That last one is required in every `SKILL.md` and tested in every `tests.md`. A bot that
manufactures a finding to look useful teaches its reader to stop reading it.

## Safety boundary

Nothing here advises using AI for safety authorisation: permit to work, lock-out tag-out, confined
space, job safety analysis, incident classification or inspection sign-off. AI prepares, people
decide. Those records live in systems Cowork cannot reach, and that is the correct arrangement.

## Repository

| Path | What |
|---|---|
| `packs/<pack>/<bot>/` | The bot: card, skill, prompts, examples, tests |
| `dist/` | Upload-ready archives, one per bot |
| `guides/` | A shareable one-page PDF per bot, plus a cover page and a bundle |
| `docs/` | Conversion guide, portability verdicts, governance, install, writing your own |
| `research/` | The verified facts behind every claim, with sources and access dates |
| `templates/bot-template/` | Copy-me skeleton |
| `tools/` | `lint_skills.py` validates and builds; `build_readmes.py` generates this table; `build_guides.py` renders the PDFs |

Contributions and corrections welcome. If something here contradicts Microsoft's documentation,
the documentation wins: open an issue and it gets fixed.

**Licence: MIT.** See [LICENSE](LICENSE).

# Copilot Cowork Bots

Agent designs that work inside the Microsoft 365 boundary: your identity, your permissions, your
approval gates, your audit trail.

[![GitHub stars](https://img.shields.io/github/stars/kesslernity/awesome-copilot-cowork-bots?style=flat-square)](https://github.com/kesslernity/awesome-copilot-cowork-bots/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![23 bots in 8 packs](https://img.shields.io/badge/bots-23%20in%208%20packs-blue.svg?style=flat-square)](#the-catalog)
[![One-page PDF per bot](https://img.shields.io/badge/guides-one%20page%20per%20bot-orange.svg?style=flat-square)](guides/)

> 🌐 **Prefer the web version?** All 23 bots on one page, nothing to clone, every guide
> downloadable: **[kesslernity.com/cowork-bots](https://www.kesslernity.com/cowork-bots?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=hero_site)**

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

**Start here, free:** [Copilot on One Page](https://www.kesslernity.com/copilot-on-one-page?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=hero)
is the four-step loop every bot below sits on top of. One page, printable. Turning Cowork on for
the first time rather than installing a bot into it? The
[Day-0 Readiness Gate](https://www.kesslernity.com/copilot-day0-readiness?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=day0)
is the eight pass-or-fail checks to settle first.

---

## What you need

- A **Microsoft 365 Copilot** license, and **Cowork enabled by your admin**. Since general
  availability that means usage-based billing switched on plus a **spending policy that selects
  Cowork**, in Microsoft 365 admin center, Copilot, Cost management. The per-agent allow list
  from the preview is deprecated.
- 🔴 **That policy is an access control, not only a budget.** Anyone in its scope can use Cowork
  however small the limit; a one-credit limit still grants access. Enforcement is asynchronous,
  so a cap is a boundary rather than an instant stop.
- Cowork bills **Copilot Credits**: model responses, tool and skill calls and browser tasks all
  count.
- Cowork is limited to **Anthropic-supported regions**.
- **Cowork runs on mobile; uploaded custom skills do not.** Install and run these on a laptop.

## Install a bot in about two minutes

1. Download the bot's `.zip` from [`dist/`](dist/).
2. In Cowork, open **Customize** in the **left navigation**, then the **Skills** tab.
3. Select the arrow next to **Add**, then **Upload skill**, and choose the file.
4. Cowork validates it and saves it to your OneDrive at `/Documents/Cowork/skills/`.
5. **Start a new conversation.** Skills are discovered when a session begins, so one already open
   will not see it.

Then open the bot's `skill/references/config.md`, which is where the thresholds, names and
projects live. One skill serves many people because that file differs.

**Read before you upload.** Microsoft's own note: a skill runs as instructions to the AI, so
only upload skills from sources you trust, and Microsoft does not validate custom skills created
by users. Everything here is plain text; open the zip and read `SKILL.md` first. It takes about
two minutes.

**Test before you schedule.** Run a skill once on a quiet period and read what comes back before
anyone puts it on a clock. After editing `references/config.md`, re-upload or edit in place, then
start a **new** conversation: changes apply to new sessions only.

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

## AI at Work newsletter, and a free course

📬 **AI at Work** is a biweekly briefing on Microsoft Copilot and enterprise AI: verified news,
tested prompts, and one honest insight. When something in this repo stops being true because
Microsoft changed it, that is where the correction gets explained rather than quietly committed.
👉 **[Subscribe free](https://newsletter.kesslernity.com/?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=newsletter)**.
No spam, no fluff, unsubscribe anytime.

🎓 **AI Quick Start Essentials** is a free 35-minute course on using AI at work without creating
a governance problem for someone else to find.
👉 **[Start the free course](https://trainings.kesslernity.com/?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=course)**:
no credit card, you just need an account.

---

## The catalog

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
|  | [`subscription-hunter`](packs/finance-finops/subscription-hunter/) | Finds every recurring subscription, license and service renewal hiding in the user's mailbox and files, and builds a dated renewal calendar with a… |
| **People & HR** | [`internal-expert-finder`](packs/people-hr/internal-expert-finder/) | Finds who inside the organization has already done a given kind of work, with the evidence for each name, and drafts the introduction. |
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

A catalog is more useful when it says what it is not.

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

## Other things I make

Everything in this repo is free under the MIT licence below, and stays free. Elsewhere:

- **[Agent Instruction Block Design Guide](https://store.kesslernity.com/l/eyeauo?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=paid_instruction_block)**
  ($19): twelve patterns for writing an instruction block, and the failure modes behind each one.
  The closest paid thing to what the `SKILL.md` files here are doing, for when your own one is
  not behaving.
- **[The M365 Copilot Deployment Kit](https://store.kesslernity.com/l/kpfpi?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=paid_kit)**
  ($97): IT prerequisites, governance before you publish, a 90-day rollout roadmap, field guides
  and agent templates. Org-wide internal use is included in the price, not a seat upgrade.
- **[The Copilot Rollout Bundle](https://store.kesslernity.com/l/copilot-rollout-bundle?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=paid_bundle)**
  ($134): the Deployment Kit with The Real Cost of Copilot and the Honest Kit, which is $31 less
  than the three apart.

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

---

## More from Kesslernity

This repo is free and stays free. If it was useful, the rest of the shelf.

**Free**

- 📄 **Copilot on One Page**: the one-page cheat sheet for getting real answers out of Copilot.
  [Free download](https://www.kesslernity.com/copilot-on-one-page?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=footer)
- ✅ **Day-0 Readiness Gate**: eight pass-or-fail checks to settle before the first Copilot
  licence goes out.
  [Free download](https://www.kesslernity.com/copilot-day0-readiness?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=footer_day0)
- ⊘ **Should this process exist?**: before you hand a process to a bot, check the process should
  exist at all. Ten evidence questions, six gates, and the first one that catches it decides.
  Runs in your browser, nothing you type leaves the page, no signup.
  [Free tool](https://www.kesslernity.com/tools/triage-floor?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=tool_triage_floor)
- 📘 **M365 Copilot Field Guide**: 29 interactive reference guides, a decision map and a failure
  triage table. Browser-readable, print-ready, no account.
  [kesslernity.com/guides](https://www.kesslernity.com/guides?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=footer_guides)
- 📺 **YouTube**: Copilot walkthroughs, agent builds, and what actually changed in the roadmap
  this month. [@Kesslernity](https://www.youtube.com/@Kesslernity?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=footer)
- 🏢 **Kesslernity on LinkedIn**: Copilot governance and rollout notes as they ship.
  [Company Page](https://www.linkedin.com/company/kesslernity/?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=footer)

**The other free Copilot repos**

- [awesome-copilot-cowork-skills](https://github.com/kesslernity/awesome-copilot-cowork-skills):
  37 Cowork skills, the direct sibling to this repo. Inbox triage, meeting prep,
  transcript-to-actions, and the 16-persona executive review suite.
- [awesome-microsoft-copilot-prompts](https://github.com/kesslernity/awesome-microsoft-copilot-prompts):
  500+ tested Copilot prompts, for the jobs that fit in one message and need no bot at all.
- [awesome-copilot-chat-agents](https://github.com/kesslernity/awesome-copilot-chat-agents):
  82 agents that run on the free Copilot Chat tier, no premium licence and no Cowork.
- [awesome-copilot-studio-agents](https://github.com/kesslernity/awesome-copilot-studio-agents):
  103 Copilot Studio agents, for when you want one governed agent for the org rather than a
  personal skill per person.
- [awesome-copilot-office-skills](https://github.com/kesslernity/awesome-copilot-office-skills):
  27 skills that run inside Copilot in Excel and Copilot in PowerPoint. Same `SKILL.md` shape, a
  different surface and a different install path.
- [awesome-copilot-agent-skills](https://github.com/kesslernity/awesome-copilot-agent-skills):
  Agent Skills for Copilot declarative agents and Cowork.

**Evaluating something other than Copilot?**

- [awesome-mistral-vibe-skills](https://github.com/kesslernity/awesome-mistral-vibe-skills?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=mistral_lane):
  137 Agent Skills for Mistral Vibe
- [awesome-mistral-vibe-agents](https://github.com/kesslernity/awesome-mistral-vibe-agents?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=mistral_lane):
  17 agent profiles, each one run through the loader first, because a broken profile is dropped
  in silence rather than reported
- [awesome-mistral-vibe-prompts](https://github.com/kesslernity/awesome-mistral-vibe-prompts?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=mistral_lane):
  49 prompts for Vibe Work, scheduled tasks and Chat

Same bar, a different runtime. Vendor-neutral is only worth claiming if you have read more than
one vendor's documentation.

**Rolling Copilot out for a team?**

🛒 Deployment kits, governance playbooks and the honest "when not to use it" guides, built so you
can do it without a consultant:
**[kesslernity.com/store](https://www.kesslernity.com/store?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=footer_store)**

Independent and vendor-neutral. Not affiliated with Microsoft, xAI, Cursor or Mistral AI.

---

**Licence: MIT.** See [LICENSE](LICENSE).

*Built by [Mathieu Kessler](https://www.linkedin.com/in/mathieukessler) ·
[kesslernity.com](https://www.kesslernity.com/?utm_source=github&utm_medium=readme&utm_campaign=cowork_bots_repo&utm_content=byline)*

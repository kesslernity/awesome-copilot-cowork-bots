# Grok Bot: verified facts

Fetched from `docs.x.ai/grok-bot/*` on **3 November 2026**. Sources in [sources.md](sources.md).
Pages carry "Last updated: October 28, 2026".

---

## 🔴 Finding that affects the project's premise

The brief describes the design source as **"xAI's Grok Bot"**. The documentation lives at
`docs.x.ai`, but its own content describes a product **operated by Cursor**, not by xAI. This is
not an inference from one stray link. Across four separate pages:

- Sign-in: Grok Bot uses a Cursor account, and there is no separate Grok Bot login.
- Architecture: it runs in Cursor's cloud, on a dedicated per-user cloud computer.
- Isolation: one persistent **Firecracker microVM per user**.
- Distribution: the installer comes from the Cursor dashboard.
- Entitlement: included with every paid Cursor plan and with Cursor Teams, as well as through X
  Subscription tiers (Premium, Super, Ultra) and SuperGrok links.
- Legal: the Data Processing Agreement is at `cursor.com/terms/dpa`.
- Telemetry: exported audit events are tagged `cursor.surface=grok_bot`.
- The doc pages render with the site title "SpaceXSI Docs".

**Why it matters here.** The pitch is "Grok Bot's best agent designs, rebuilt inside the M365
boundary". If the product is Cursor-operated and reached through an X or Cursor subscription, then
comparisons, attributions and any security contrast need to name the right operator, or the repo
is wrong on its central claim. This is a call for Mathieu, flagged rather than resolved.

**The brief's "launched in beta in August 2026" could not be verified.** No fetched page states a
launch date. Marked **UNVERIFIED**.

---

## The model: Bots, skills, routines

**A Bot** is a durable AI teammate with a name, a job, its own conversation, and context that
accumulates. The docs advise creating a separate Bot when work has a distinct goal, tool set,
working style, approval boundary, or schedule, and are explicit that named jobs like Talent Scout
or Expense Manager work where a "General Helper" does not.

Personal Bots no longer have a description or a settings page; the job is set by telling the Bot in
chat and asking it to remember. Shared Bots keep an editable description.

**A primary Bot** is the user's main point of contact, checks in on its own, and coordinates work
with the other Bots. This is the "chief of staff" pattern the brief refers to.

**A skill** is a reusable set of instructions for a task. **A routine** says when to run one: on a
schedule, or on an event. Supported routine events are notably broader than Cowork's: **Slack
messages, GitHub, Linear, Sentry and PagerDuty events, email, and webhooks**.

Limits: a Bot can own up to **50 routines**, the app keeps the **20 most recent run records** per
routine, and routine schedules must be at least **five minutes apart**.

**Teaching by demonstration** records visible computer interaction for up to ten minutes and saves
the path as a skill. It does not record microphone audio.

---

## The computer

Every Bot works from a persistent cloud computer with a **browser, command line and filesystem**,
at `/workspace`. Work continues while the laptop is closed. Files, sign-ins and browser sessions
persist between tasks.

Bots can also be given an **email address** (off by default on teams, admin-enabled), and can
delegate coding work to separate **Cloud Agents**.

---

## Security posture, in their own words

The brief predicted weaknesses here. The documentation confirms them explicitly, which is worth
quoting carefully rather than characterising.

**Per-user isolation is strong. Per-Bot isolation does not exist.**

> "The screens are separate work surfaces, not separate security boundaries."

All of one user's Bots share one computer, meaning shared browser cookies and signed-in sessions,
shared files, and shared command-line credentials. One Bot can continue from work another saved.
The docs instruct the reader to treat any login or file on the computer as available to every Bot
that user runs, and state that when a workload needs its own computer and credential set, it needs
its own Cursor user.

Deleting a Bot erases its profile, conversations, memory, routines and attachments, but **does not**
remove computer files or browser sessions.

**What is genuinely strong**, and should be said plainly rather than strawmanned:

- Per-user hardware-level separation via Firecracker microVMs.
- Bots act as the signed-in member and can never hold more access than that person.
- OAuth tokens stay server-side; the model receives tool results, not tokens.
- **Auto Review**, an independent review model that evaluates risky actions before they run and can
  allow, require approval, or deny. It covers shell commands, app calls, computer use, automation
  writes and delegation.
- A network policy controlling reachable destinations, optionally extended to MCP servers.
- Inference hooks that send each model request to an organisation's own AI security server for an
  allow or deny decision, starting in Shadow mode.
- Credentials are filled from a Vault or a password manager without the Bot seeing the values.

**The honest gaps for an enterprise buyer:**

- Auto Review is a model's judgment, and the docs say so: it "does not review every side effect",
  naming memory writes and most settings changes.
- **Audit Logs and Action Recording are Enterprise-only.** Self-serve Teams get neither. Action
  Recording is off by default with 90-day internal retention.
- Computers run **in the United States only**. On-premises, in-perimeter and bring-your-own-image
  deployment are **not supported**.
- No built-in customer-facing EDR or telemetry feed.
- Prompt injection is acknowledged as a live risk, mitigated by layered controls rather than
  eliminated.

---

## Official use cases

From the Use cases page. Each is framed as owning "a repeatable outcome, not a loose category of
questions", and every starter prompt deliberately ends at a review point.

| Role | Owns | Connects to |
|---|---|---|
| Sales Outbound | Account research, contact prioritisation, review-ready outreach | CRM, intent sources, websites, email |
| Talent Scout | Sourcing, candidate research, outreach drafts, scheduling prep | ATS, sourcing tools, email, calendar |
| Paid Media | Campaign monitoring and budget recommendations | Ad platforms, analytics, budget sheet, Slack |
| Expense Manager | Weekly expense reconciliation and missing-info follow-up | Expense system, email, shared drive, finance sheets |
| Product Performance | Targeted performance investigations with evidence | Observability, analytics, incident tooling, source control |
| Bug Reproduction | Turning reports into reliable reproduction packs | Issue tracker, staging, browser, network tools |
| Account Health | Risk and expansion signals across a portfolio | CRM, product usage, support, billing, CS notes |

---

## The design discipline worth stealing

This is the part of Grok Bot's documentation that transfers cleanly and is, in my judgement, more
valuable to this repo than any individual bot design.

Their stated progression for turning an example into a durable Bot: put the job, sources, output
format and boundaries in the description; run one real task at safe scope; correct until the result
is reviewable; save the process as a skill; test on a second input; **create a routine only when
retries and failure cases are defined**; keep consequential external actions behind approval.

Their routine design rules: automate preparation before execution; draft, reconcile or recommend
first; require approval for sending, purchasing, deleting, publishing or changing production;
include a **no-data and stale-data policy**; make retries idempotent; say where to report partial
completion; re-test after a source format changes.

And their test checklist before enabling: did it select current inputs, does output meet the
format, does every action have a source or audit trail, did it stop at the intended approval point,
are failure states explicit.

That last set maps directly onto the `tests.md` file the brief asks for in every bot folder.

---

## UNVERIFIED

- Launch date, and whether a beta began in August 2026.
- Templates and a template marketplace: the brief names them and admin controls reference "public
  template sharing", but the template catalogue itself was not fetched.
- The community bot designs named in the brief (Bot Boss, Founder Mode with 8 bots in 4 folders,
  PR queue, SOC 2 compliance, community ops). Not yet researched; practitioner write-ups are a
  separate search and are not represented here.
- The relationship between xAI and Cursor, and which entity is the vendor of record.

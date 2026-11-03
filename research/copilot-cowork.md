# Microsoft 365 Copilot Cowork: verified facts

All facts below were fetched from Microsoft Learn on **3 November 2026**. Sources and access dates
are in [sources.md](sources.md). Anything not confirmed by a fetched page is marked **UNVERIFIED**.

---

## What Cowork is

Cowork is the agentic layer inside Microsoft Copilot. It carries out multistep work across
Microsoft 365 by taking action on a user's behalf: sending email, scheduling meetings, creating
documents, posting in Teams. Microsoft's own framing of the difference from Copilot Chat is that
Chat is "fast, focused, single-task support" measured in seconds to minutes, while Cowork is
end-to-end work across apps measured in minutes to hours.

The practical consequence for this project: Chat drafts and stops, Cowork executes behind an
approval gate. Every bot design here has to decide where that gate sits.

---

## Built-in skills (14 named, plus image generation)

Word, Excel, PowerPoint, PDF, Email, Scheduling, Calendar Management, Meetings, Daily Briefing,
Enterprise Search, Deep Research, Communications, Adaptive Cards, and App (Frontier).

Image generation is a separate built-in capability and uses the ChatGPT Images 2.0 model.

Two of these carry most of the weight for a bot catalogue: **Enterprise Search** reaches across the
organisation, and **Deep Research** compiles multi-source analysis. A custom skill composes the
built-ins rather than reimplementing them.

---

## Custom skill format

🔴 **The brief states the custom skill cap is "believed to be 20". That is wrong.** Microsoft Learn
states a user can create up to **50 custom skills**. The number 20 is the limit on **companion
files per skill**, which is a different thing. This correction materially changes the pack design
in Phase 2, because a 20-skill ceiling would force hard choices that a 50-skill ceiling does not.

The verified limits, from the "Use Copilot Cowork" page:

| Limit | Value |
|---|---|
| Custom skills per user | **50** |
| `SKILL.md` file size | 1 MB |
| Companion files per skill | 20 |
| Total size per skill | 10 MB |
| Scheduled prompts per user | **25** |
| Message input length | 250,000 characters |

**Location and structure.** A skill is a subfolder of the user's OneDrive at
`/Documents/Cowork/skills/`, for example `/Documents/Cowork/skills/weekly-report/`, containing a
file named `SKILL.md`. That file opens with a YAML frontmatter block carrying a `name` and a
`description`, followed by the instructions in Markdown.

**Discovery** happens automatically at the start of each session. A conversation already open will
not pick up a skill added mid-session.

**The description is the trigger.** Learn's own tip is to write a description that explains *when*
Cowork should use the skill, because that text is what Cowork matches against a request. This is a
design constraint on every bot card: the description is routing logic, not marketing copy.

### Three ways to create one

1. The guided **Customize** page: Skills tab, Add, Create new. Cowork drafts the `SKILL.md`.
2. Asking Cowork in chat to build a skill.
3. Writing the `SKILL.md` by hand in OneDrive.

### Uploading an existing skill

Customize, Skills tab, the arrow next to **Add**, then **Upload skill**. Cowork accepts either a
`.md` file containing a single `SKILL.md`, or a `.zip` or `.skill` archive with `SKILL.md` **at its
root** plus companion files. Cowork validates the file and writes it to OneDrive itself.

Name collisions do not overwrite: Cowork keeps both and appends a number.

### How Microsoft evaluates a skill

Static checks review structure and limits, scan bundled code for security issues, and check the
skill text for **prompt-injection patterns**. Code is never executed during static checks.
Behavioural checks run the skill against realistic prompts and score triggering for precision and
recall separately.

Learn also carries an explicit warning that a skill runs as instructions to the AI and only skills
from trusted sources should be uploaded. A public catalogue is exactly the case that warning is
about, which is a governance obligation on this repo, not a footnote.

---

## Automation

### Scheduled prompts
Created in natural language ("every weekday at 9 AM"). Managed from the **Automations** page, which
has a Runs tab and a Manage schedules tab. On activation Cowork offers **Activate and run now** or
**Activate**. Cap: **25 per user**.

### Event-driven tasks
Run when something happens rather than on a clock. The supported events are:

- an incoming **email** that matches
- a **Teams channel message**
- a **Teams chat message**, optionally limited to messages that @mention the user

Each task defines **When**, **Run in** (new conversation or the current one), and **What it does**.
Tasks show as Active, Draft or Paused with a last-fired time.

🔴 **The event list is narrow and it constrains the catalogue.** There is no file-change trigger, no
SharePoint or list trigger, no calendar trigger and no webhook. Any bot design that assumes "watch
this folder" or "fire when a record changes" does not port as an event task and must become either
a scheduled prompt or a Power Automate flow.

### Governance of unattended runs
Every automated task **runs as the user who created it**, sees only what that user can see, and acts
through the same governed tools. Default behaviour is draft-and-approve: Cowork prepares the action
and asks before it sends an email, posts a message, or changes a shared system. Users may
pre-authorise. Rate limits prevent a task firing too often, and results go only to the creating
user unless they approve otherwise.

---

## Approval model

| Control | Effect |
|---|---|
| Action button (Send, Post, Create) | Proceeds once |
| More options | Approves and skips similar prompts for the session. For email and Teams this can be scoped to a recipient, a domain, or always-for-this-session |
| Approve All | Clears all pending approvals at once, labelled with the count |
| Cancel | Stops that action, continues the rest |

Approvals granted with "don't ask again" are reviewable in the side panel's **Permissions** section.

---

## Plugins and connectors

Plugins come from the Microsoft 365 App Store and add skills and connectors. Admins control
availability and deployment. Organisations can build custom plugins using the same package format,
which may bundle both skills and connectors.

**Microsoft first-party plugins** include Dynamics 365 Customer Service, Dynamics 365 ERP,
Dynamics 365 Sales, Fabric IQ, and Business Applications in Work IQ.

**Role and industry plugins**, found under Customize, Plugins, Roles & Industry:

| Plugin | Skills |
|---|---|
| Legal for Cowork | 20 |
| Education for Cowork | 10 |
| Sales for Cowork | 9 |
| Service for Cowork | 5 |

This matters for the catalogue: Microsoft already ships 20 legal skills and 9 sales skills. A
Legal or Sales bot in this repo has to be better than, or complementary to, the first-party set,
or it should not exist. Phase 2 treats that as a filter.

A large partner plugin catalogue also exists (Azure DevOps, Slack-adjacent tools, SEO, finance
data, SMS and more), which is where "port with plugin" verdicts will come from.

---

## Licensing, models, billing

**Billing is usage-based.** Model responses, tool and skill calls, image generation and browser
tasks all count toward consumption. Admins see usage in the Microsoft 365 admin center and can set
per-user or per-group limits. If an admin makes Cowork discoverable without enabling usage-based
billing, users can request access in-app and an admin approves against policy and cost.

**Models** available in the picker: GPT 5.5, GPT 5.6 and GPT 6 variants, Claude Opus, Claude Sonnet,
and Claude Fable 5.1 and 5 (Preview). Fable 5 (Preview) is off by default and needs an admin to
enable it. **Auto** is the default. A reasoning-effort selector sits next to the model picker, with
**Medium** as the default.

**Anthropic as subprocessor.** Cowork can use Anthropic Claude models for most reasoning, drafting
and tool work. Admins can turn off the Anthropic model family in the admin center.

🔴 **Regional restriction.** Access to Anthropic models through Microsoft services is limited to
Anthropic-supported regions, and **Cowork is not an exception**. This is a real deployment
constraint for any organisation outside those regions and belongs in the prerequisites of every bot
card.

**Mobile.** Custom skills are not supported in Cowork on mobile platforms.

---

## Sharing

A skill's detail page has a **Share** control offering **Only you** or **Specific users in your
organization**. There is no org-wide publish from the skill page; org-wide distribution is the
plugin path.

---

## UNVERIFIED

- **Exact GA date.** A prior session established 16 June 2026 as worldwide GA from the Microsoft
  365 blog, but that page was not re-fetched in this session, so it is not carried here as verified.
- **Frontier status of individual features.** The App skill is labelled "(Frontier)" in Learn, but
  the current Frontier-versus-GA boundary for Cowork as a whole was not confirmed from a fetched
  page in this session.
- **Whether a plugin's bundled skills count against the 50-skill user cap.** Learn describes the cap
  for skills "you create"; plugin skills appear in a separate list. Not stated either way. This
  affects pack budgeting and should be tested in a tenant.
- **Whether a shared skill consumes the recipient's 50-skill allowance.** Not stated.

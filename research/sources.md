# Sources

Every claim in `copilot-cowork.md` and `grok-bot.md` traces to a page below, fetched in this
session. Pages not fetched are not cited, and facts that depend on them are marked **UNVERIFIED**
in the research files rather than carried as true.

Quotations are kept under 15 words and to at most one per source, per the brief.

---

## Microsoft 365 Copilot Cowork

| # | Page | URL | Accessed | What it establishes |
|---|---|---|---|---|
| C1 | Use Copilot Cowork | https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/use-cowork | 2026-11-03 | Built-in skill table, the three ways to create a custom skill, the OneDrive path, the **50 custom skills / 1 MB / 20 companion files / 10 MB** limits, **25 scheduled prompts**, event-driven task events and fields, the approval table, the side panel, 250,000 character input |
| C2 | Customize Copilot Cowork | https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-customize | 2026-11-03 | Upload skill route and accepted formats (`.md`, or `.zip`/`.skill` with SKILL.md at root), required `name` and `description` frontmatter, name-collision behaviour, static and behavioural evaluation including prompt-injection scanning, Share scopes, the trust warning on uploaded skills |
| C3 | Cowork admin governance | https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-admin-governance | 2026-11-03 | Usage-based billing and per-user limits, plugin management, model management including turning off the Anthropic family, governance of unattended tasks, access-request flow |
| C4 | Available plugins for Copilot Cowork | https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-available-plugins | 2026-11-03 | First-party plugins, the four role and industry plugins with their skill lists (Legal 20, Education 10, Sales 9, Service 5), the partner catalogue, custom plugin packaging |
| C5 | Copilot Cowork common questions | https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-faq | 2026-11-03 | Cowork versus Copilot Chat comparison, built-in skill list restated, the 50-skill cap restated, model list, reasoning-effort selector, billing, Anthropic subprocessor, **Anthropic-supported-regions restriction**, admin disable paths |

**Attempted and failed:** `https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-overview`
returned **HTTP 404** on 2026-11-03. It is not cited anywhere. Noted here so a later reader does not
assume it was skipped by accident.

---

## Grok Bot

| # | Page | URL | Accessed | What it establishes |
|---|---|---|---|---|
| G1 | Grok Bot overview | https://docs.x.ai/grok-bot/overview | 2026-11-03 | What a Bot is, the persistent cloud computer with browser, filesystem and terminal, bots coordinating in parallel, learning by demonstration, and the shared-computer model |
| G2 | Get started | https://docs.x.ai/grok-bot/get-started | 2026-11-03 | Eligible plans, **sign-in uses a Cursor account**, installer from the Cursor dashboard, supported platforms, mobile parity and the desktop-only flows |
| G3 | Create and manage Bots | https://docs.x.ai/grok-bot/bots | 2026-11-03 | When to create a separate Bot, the primary Bot and coordination, memory model and what resets it, roster organisation, deletion behaviour, team-of-bots guidance |
| G4 | Skills and routines | https://docs.x.ai/grok-bot/skills-routines-and-automations | 2026-11-03 | Skill versus routine, the trigger list (Slack, GitHub, Linear, Sentry, PagerDuty, email, webhook), **50 routines per Bot, 20 run records, 5-minute minimum spacing**, teaching by demonstration, the test checklist and the routine design rules |
| G5 | Use the computer and apps | https://docs.x.ai/grok-bot/computer-and-apps | 2026-11-03 | One computer shared by all a user's Bots, shared cookies, files and command-line credentials, "separate work surfaces, not separate security boundaries", connected apps being account-wide, agent email, `/workspace` |
| G6 | Grok Bot security | https://docs.x.ai/grok-bot/security | 2026-11-03 | Architecture diagram and its five controls, Auto Review and its stated limits, network policy and MCP coverage, inference hooks, identity model, **Enterprise-only audit logging and Action Recording**, US-only residency, no on-premises deployment, prompt-injection position |
| G7 | Grok Bot for teams and enterprises | https://docs.x.ai/grok-bot/teams-and-enterprises | 2026-11-03 | Availability by plan, **Firecracker microVM per user**, the per-user versus per-Bot isolation statement, the full admin control list and which controls are Enterprise-only, connector policy inheritance, recommended configuration |
| G8 | Use cases | https://docs.x.ai/grok-bot/use-cases.md | 2026-11-03 | The seven official roles, what each owns and connects to, the read-and-prepare-first discipline, and the seven-step path from example to durable Bot |

---

## Not yet researched

Named in the brief, deliberately not represented in the research files:

- `https://x.ai/bot/guides` and the GTM, Work, Founders and Templates guides.
- Community bot designs: Bot Boss, Founder Mode (8 bots in 4 folders), PR queue, SOC 2 compliance,
  community ops.
- Practitioner reviews, newsletters and write-ups.
- `microsoft.github.io/copilot-camp` Cowork labs.
- The "(Co)work in Progress" release blog.

These are the gaps between Phase 1 as briefed and Phase 1 as delivered. They matter most for the
catalogue's breadth in Phase 2C, less for its correctness. Flagged rather than quietly omitted.

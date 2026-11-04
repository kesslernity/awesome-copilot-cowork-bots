# <Bot name>

> Copy this folder into `packs/<pack>/<bot-name>/`, rename it, and replace every angle bracket.
> `python3 tools/lint_skills.py --check` will tell you what you missed.

**One-line job.** <The repeatable outcome this owns. "Surfaces every renewal hiding in your inbox
before it auto-renews" is a job. "Helps with contracts" is a category.>

---

## The shape test

Before writing anything else, check the design against the five marks that separate a workflow
which survives the demo from one that does not:

- [ ] **One narrow job.** Could you name what it owns in eight words?
- [ ] **A recurring trigger.** A schedule, an event, or an honest "on demand".
- [ ] **An obvious definition of done.** You can tell at a glance whether it worked.
- [ ] **Reviewable in seconds.** Not a wall of text a person has to audit.
- [ ] **Silence is the success state.** Nothing to report is a good outcome, clearly said.

A bot that fails three of these does not belong in the catalogue.

---

## 1. Grok origin
<Which design this came from, with a link. What changed in the move to Cowork, and why. If the
original needed a terminal, a browser or a second agent, say what was dropped. If this has no
Grok ancestor, say that too.>

## 2. Who it is for, and what it saves
<Role. Then an estimate, stated as an estimate: "roughly 40 minutes a week for someone running
six workstreams". Never a hard claim.>

## 3. Data sources
| Source | Built-in skill or plugin |
|---|---|
| | |

## 4. Output format
<Exact structure: sections, table columns, the links-to-source requirement, the file name pattern
and where it is written.>

## 5. Boundaries
<What it must never do without approval: send, post, delete, accept or decline meetings, share
externally. Default is draft, do not send. Any job-specific prohibition goes here.>

## 6. Run modes
| Mode | Supported | Notes |
|---|---|---|
| On demand | | |
| Scheduled prompt | | Costs one of the user's 25 |
| Event-driven task | | Email and Teams messages only |

## 7. Prerequisites
- Microsoft 365 Copilot licence, Cowork enabled by an admin
- Cowork is limited to Anthropic-supported regions
- Custom skills are not supported on mobile
- <Any plugin this needs, named. If the connector does not exist, say so.>

## 8. Governance notes
<Sensitivity labels it may encounter. Whether it reads anything external. What an admin should
check before rolling it out. Anything a Purview or DPO review would want to know.>

## 9. Graduation path
1. **Read and prepare.** Run on demand, read the output, correct the config.
2. **Approved actions.** Allow it to draft sends, approving each one.
3. **Scheduled.** Only once retries and failure cases are defined and you have seen it handle a
   week with nothing in it.

## 10. Known limitations
<Be specific. "Cannot see the ticketing system" beats "may be incomplete".>

## 11. Install
Download `dist/<bot-name>.zip`, then in Cowork: **Customize** → **Skills** → the arrow next to
**Add** → **Upload skill**. Cowork validates it and writes it to your OneDrive. Start a new
conversation; skills are discovered when a session begins.

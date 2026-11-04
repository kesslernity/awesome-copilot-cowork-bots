# Converting a Grok Bot design into Copilot Cowork

Grok Bot is reached through X Subscription tiers and legacy Cursor plans, and it runs on Cursor
infrastructure: one Firecracker microVM per user, in the United States. Copilot Cowork runs inside
a Microsoft 365 tenant, under that tenant's identity, and acts as the signed-in user. Both facts
are from the vendors' own documentation, cited in [../research/sources.md](../research/sources.md).

The two products share a shape, which is why designs transfer at all: a named job, instructions
saved for reuse, something that runs on a schedule or an event, and an approval gate before
anything leaves the building. What follows is the mapping, and then the honest list of what does
not survive the move.

---

## The mapping

| Grok Bot | Copilot Cowork | How faithful |
|---|---|---|
| Bot (named teammate with a job) | A custom skill, plus a line in Preferences | Partial. See "what does not survive" below |
| Bot description | `SKILL.md` frontmatter `description` | Good, with a catch: in Cowork this text is also the routing logic |
| Skill (saved reusable instructions) | A custom skill, the body of `SKILL.md` | Close to one-for-one |
| Routine, schedule | Scheduled prompt | Good. Cap 25 per user, against 50 routines per Bot |
| Routine, event | Event-driven task | Narrow. Email and Teams messages only |
| Tool connections, connected apps | Plugins and connectors from the M365 App Store | Depends entirely on whether the connector exists |
| Bot-to-bot handoff, group chat | One Cowork task loading several skills | Weak. There is no second agent to hand to |
| Primary Bot coordinating a roster | An orchestrator skill naming its specialists | Weak for the same reason |
| Teaching by demonstration | Nothing equivalent | Does not exist |
| Vault, secure sign-in | Nothing equivalent, and not needed | Cowork acts as the user, so there is no credential to hand over |
| The cloud computer: browser, terminal, filesystem | Nothing equivalent | The single biggest gap |

---

## What does not survive the move

Be blunt about these, because a catalogue that pretends otherwise will waste a reader's afternoon.

**There is no second agent.** Grok's model is a roster of Bots that message each other, run in
parallel and pass ownership. Cowork runs one task that may load several skills. An "orchestrator"
skill in this repo is a skill that calls other skills in a stated order inside one task. It is a
useful pattern and it is not multi-agent. Any design whose value comes from two Bots negotiating is
not portable, and saying so is more useful than shipping a thin imitation.

**There is no terminal, no filesystem, and no general browser.** Grok Bots run shell commands,
clone repositories, install packages and drive arbitrary websites from a persistent machine at
`/workspace`. Cowork works through governed M365 tools. Every Grok design whose core loop is "open
staging, reproduce the bug, attach a flamegraph" is out, and the right answer is a different tool,
named in the portability table rather than fudged.

**There is no per-Bot memory.** A Grok Bot accumulates preferences, facts and a dated log of its
own work. Cowork has per-user custom instructions on the Preferences tab, which every task sees,
and skills that are stateless between sessions. A skill cannot remember that last week's variance
was already explained. Where a design depends on continuity, the state has to live in a file the
skill reads and writes, and the bot card has to say where.

**The trigger surface is much narrower.** Grok routines fire on Slack messages, GitHub, Linear,
Sentry and PagerDuty events, inbound email and webhooks. Cowork event tasks fire on an incoming
email, a Teams channel message, or a Teams chat message, optionally only when the user is
@mentioned. There is no file-change trigger, no list or SharePoint trigger, no calendar trigger and
no webhook. A design that watches a system other than mail or Teams becomes a scheduled poll, or it
leaves Cowork for Power Automate.

**Scheduled capacity is the real ceiling, not skills.** A user may hold 50 custom skills but only
25 scheduled prompts. Skills are cheap, schedules are scarce. The catalogue is budgeted on
schedules, and most bots ship as on-demand with a schedule marked optional.

---

## What transfers better than expected

**Cowork writes the file for you.** A `.zip` with `SKILL.md` at its root goes in through Customize,
Skills, Add, Upload skill, and Microsoft validates it and saves it to OneDrive. Nobody has to build
a folder tree by hand. This is why the catalogue ships archives, not instructions.

**The approval model is richer.** Grok has Auto Review, a model judging risk, which its own docs
admit "does not review every side effect". Cowork's gate is mechanical: an action button, an
approve-and-skip-similar option scoped to a recipient or a domain, approve-all, or cancel, and a
Permissions panel listing every standing approval. Mechanical beats judgment for an auditor.

**Identity is already solved.** A Grok Bot signs into accounts in a shared browser, and the docs
warn that a login placed there is available to every Bot that user runs. A Cowork task runs as the
user, sees only what that user can see, and leaves an attributable trail. The whole Vault and
secure-handoff apparatus has no Cowork equivalent because Cowork does not need one.

**Their design discipline is the best thing to take.** Grok's documentation says to automate
preparation before execution, to draft and reconcile first, to define a no-data and stale-data
policy, and to create a routine only once retries and failure cases are defined. That is better
guidance than most Copilot material and it is carried into every bot card and `tests.md` here.

---

## The rules this repo follows as a result

1. **Draft, do not send.** Every bot ships read-and-prepare. Sending, posting and deleting stay
   behind approval, and the graduation path to approved actions is written on the card.
2. **Cite the source.** Every factual item in an output links back to the mail, file, meeting or
   record it came from. An unsourced line is a defect, not a style preference.
3. **Separate facts from inferences.** Grok's own use-case prompts demand this and it survives.
4. **Budget schedules, not skills.** A pack states how many of the 25 scheduled prompts it wants.
5. **Name the specialists.** An orchestrator skill lists exactly which skills it invokes and in
   what order, and degrades gracefully when one is missing.
6. **Say when it does not port.** A "don't port" verdict with the right alternative tool named is
   worth more than a bot that half works.

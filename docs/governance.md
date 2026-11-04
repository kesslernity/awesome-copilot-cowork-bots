# Governance

Written for the person who has to approve this, not for the person who wants to use it.

## What a Cowork skill actually is

A skill is **instructions to a model**, stored as a Markdown file in a user's OneDrive and loaded
at the start of a session. It is not code and it does not execute. Microsoft's own documentation
carries the warning plainly: only upload skills from sources you trust, and Cowork shows that
reminder the first time someone uploads one.

That warning applies to this repository. These files are public, anyone can edit a copy, and a
modified skill is as trustworthy as whoever modified it. The controls below exist because of that,
not in spite of it.

## What Microsoft checks on upload

- **Static checks** on structure and limits, a scan of any bundled code, and a scan of the skill's
  text for **prompt-injection patterns**. Code is never executed during this.
- **Behavioural checks** that run the skill against realistic prompts and score its triggering for
  precision and recall separately.

This is a real control and it is not a substitute for reading a skill before you install it. Every
`SKILL.md` here is plain Markdown, a few hundred lines, and readable in two minutes.

## The identity and permission model

This is the strongest thing about running these in Cowork rather than elsewhere:

- A task **runs as the signed-in user**. It cannot see anything that person cannot see.
- Automated tasks, scheduled or event-driven, **also run as that user**, with the same visibility.
- Every action is attributable to a named person in your tenant.
- There is no separate machine identity to provision, rotate or audit.
- Results of an automated task go **only to its creator** unless they approve otherwise.

Compare this with the model the designs came from, where all of one user's bots share one cloud
computer with shared browser sessions, shared files and shared command-line credentials, and whose
own documentation states plainly that the per-bot screens are not security boundaries. That is the
substantive difference this repository exists to exploit.

## The approval gate

| Control | Effect |
|---|---|
| Action button | Proceeds once |
| More options | Approves and skips similar prompts for the session, scopable to a recipient or a domain |
| Approve All | Clears all pending approvals, labelled with the count |
| Cancel | Stops that action, continues the rest |

Standing approvals are listed in the session side panel under **Permissions**, which is where to
look when auditing what someone has pre-authorised.

**Every bot in this repository defaults to draft.** Several go further and refuse categories of
action outright: `calendar-defender` never changes a calendar entry, `project-decomposer` never
creates a task, `interview-loop-coordinator` never produces a hire recommendation, and
`one-to-one-prep` never characterises a person.

## What an admin should check before rolling these out

1. **Is Cowork enabled, and for whom?** It is off by default, and access can be scoped to groups.
2. **Usage-based billing.** Model responses, tool and skill calls and browser tasks all consume.
   Set per-user or per-group limits before a pack of scheduled bots goes wide.
3. **Which models are allowed.** The Anthropic family can be turned off at tenant level, and
   Cowork is limited to Anthropic-supported regions.
4. **Sensitivity labels.** These bots read mail and files and write documents. Confirm your label
   policy behaves as you expect on Cowork output, and note that several skills here explicitly
   carry an input's label to the output.
5. **Which plugins are available.** Any permitted connector widens what every skill can reach.
6. **The schedule budget.** 25 per user. A team that schedules everything will hit it.

## Data boundaries these skills respect

- **Nothing leaves the tenant.** No skill here calls an external service. Two use **Deep
  Research**, which reads the open web, and neither sends anything outward.
- **No external contact without approval.** Every outbound draft is a draft.
- **No permission workarounds.** Enterprise Search respects permissions; no skill attempts to
  reach round that, and `internal-expert-finder` says so explicitly.
- **No shadow records of official things.** `lessons-learned-harvester` refuses to summarise
  safety events or regulatory findings, because an unofficial summary of an official record is a
  liability rather than a convenience.

## The safety boundary, stated once and meant

Nothing in this repository advises using AI for safety authorisation: permit to work, lock-out
tag-out, confined space, job safety analysis, incident classification or inspection sign-off.

AI prepares, people decide. Those records live in permit and maintenance systems that Cowork
cannot reach, which is the correct arrangement and not a limitation to work around.

## Residual risks, stated plainly

- **Prompt injection.** A skill reads mail and documents, and content from outside can try to
  steer a model. Microsoft scans skills for injection patterns; that does not make the content a
  skill reads safe. Keep consequential actions behind approval, which is the control that does
  not depend on a model's judgment.
- **A skill is only as current as its config.** A VIP list or a project list that goes stale
  produces confidently wrong output.
- **Silence can mean failure.** Every bot here is designed so that nothing-to-report is a valid
  result, which is correct, and it means a broken bot and a quiet week look similar. The
  `tests.md` in each bot includes the empty case for this reason.

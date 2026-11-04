# Writing your own bot

Copy `templates/bot-template/` into `packs/<pack>/<your-bot>/`, rename it, and run
`python3 tools/lint_skills.py --check` early and often.

## Pass the shape test first

Before writing anything, check the idea against the five marks. A bot failing three does not
survive its first month:

- **One narrow job.** Nameable in eight words. "Surfaces every renewal hiding in your inbox" is a
  job; "helps with contracts" is a category.
- **A recurring trigger**, or an honest "on demand".
- **An obvious definition of done.**
- **Reviewable in seconds.**
- **Silence is the success state.**

## The description is routing logic, not copy

Cowork matches a user's request against the `description` in your frontmatter. It is the only
thing deciding whether your skill is picked. Write it for the matcher:

- Say what it produces, then list the phrases a person would actually type.
- Include the words your organisation uses, not only the correct ones.
- The linter warns if the description never says *when* to use the skill.

## Write procedures, not encouragement

"For each thread, return sender, the ask, the deadline and the source link" is a procedure.
"Thoughtfully analyse the inbox" is not. If a step cannot be checked by someone reading the
output, rewrite it.

## The four sections people skip

**Config.** Put thresholds, names, projects and vocabulary in `skill/references/config.md` and
read it at the start of every run. Never hard-code a person or a number. This is what makes one
skill serve a whole team.

**Definition of done, including silence.** State what finished looks like *and* what happens when
there is nothing to report. Then make the bot actually do that. The temptation to produce
something rather than nothing is the single most common failure in this category, and it is how a
reader learns to ignore a weekly report.

**No-data and stale-data policy.** What happens when a source is unavailable, when the window is
empty, when two sources disagree. Never fall back to older data silently. Never widen a window to
find something.

**Boundaries.** What it must never do without approval. Default to draft. Be specific: "never
infer a rollback plan" is a boundary, "be careful" is not.

## Write the tests before you are pleased with it

`tests.md` should cover the happy path in a few lines and spend its length on the cases that lose
trust:

- The **empty** case. Usually the most important test in the file.
- A source unavailable.
- The config file missing.
- Two sources disagreeing.
- Someone asking the bot to cross its own boundary, with the expected refusal.

## What the linter enforces

| Check | Why |
|---|---|
| Frontmatter `name` matches the folder, kebab-case | Cowork matches them |
| `description` present, parsed, over 40 characters | A folded YAML block silently parses to `>-` |
| Description says *when* (warning) | It is the routing signal |
| A draft, propose or approval boundary exists (warning) | A bot that can act without saying so |
| Size and file-count limits | 1 MB, 20 companion files, 10 MB total |
| `SKILL.md` lands at the archive root | The shape Cowork's uploader accepts |

## Before you open a pull request

```bash
python3 tools/lint_skills.py          # validates and builds dist/<bot>.zip
python3 tools/build_readmes.py        # regenerates pack READMEs and the catalogue table
```

Then read your own `SKILL.md` as if you were the admin who has to approve it.

## What will be rejected

- A bot duplicating one already in
  [awesome-copilot-cowork-skills](https://github.com/kesslernity/awesome-copilot-cowork-skills) or
  in a Microsoft role plugin. Point at those instead.
- A bot that sends, posts or deletes without approval.
- A bot that touches safety authorisation.
- A bot that pads its output rather than reporting nothing.
- A capability claim not supported by Microsoft's documentation. If the docs do not say Cowork can
  do it, the bot does not claim it.

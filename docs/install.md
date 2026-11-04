# Installing a bot

## The short way, about two minutes

1. Download the bot's `.zip` from [`../dist/`](../dist/).
2. In Cowork, open **Customize**, then the **Skills** tab.
3. Select the arrow next to **Add**, then **Upload skill**.
4. Choose the file. Cowork validates it and saves it to your OneDrive.
5. **Start a new conversation.** Skills are discovered at the start of a session, so one already
   open will not see it.

The archive has `SKILL.md` at its root with any reference files alongside, which is the shape
Cowork's uploader accepts. You do not build a folder by hand.

## The manual way

If you prefer OneDrive directly, or you want to edit in place:

1. Go to `/Documents/Cowork/skills/` in your OneDrive, creating it if it is absent.
2. Create a subfolder named exactly as the bot, for example
   `/Documents/Cowork/skills/subscription-hunter/`.
3. Put `SKILL.md` inside it, with the `references/` folder if the bot has one.
4. Start a new conversation.

The folder name and the `name` in the frontmatter must match.

## Configure it

Every bot reads `skill/references/config.md`. That is where thresholds, names, projects and
vocabulary live, and it is why one skill serves many people. Open it before the first real run.

A bot with an unedited config still works on its documented defaults, and will say once that it
used them.

## What it costs you

| Resource | Cap | Note |
|---|---|---|
| Custom skills | **50** | All 23 bots here cost 23 |
| `SKILL.md` size | 1 MB | None here is close |
| Companion files | 20 per skill | None here uses more than 2 |
| Scheduled prompts | **25** | The one that actually binds |

Schedules are the scarce resource. Add one only when the bot card argues for it and you have seen
the bot handle a week with nothing in it.

## Scheduling and triggers

**Scheduled prompts** are created in natural language: "every Monday at 9, run X". Manage them on
the **Automations** page, which has a Runs tab and a Manage schedules tab.

**Event-driven tasks** fire on an incoming email, a Teams channel message, or a Teams chat
message, optionally only when you are @mentioned. That is the whole list. There is no file,
SharePoint, calendar or webhook trigger, so a bot that needs to watch anything else runs on a
schedule or belongs in Power Automate.

Both default to draft-and-approve, both run with your permissions, and both see only what you see.

## Sharing

A skill's detail page has **Share**, offering **Only you** or **Specific users in your
organization**. There is no org-wide publish from there. Organisation-wide distribution is the
plugin path, which packages skills and connectors together.

## Two things not established

Both affect how much of your allowance a pack really costs, and neither is stated in Microsoft's
documentation. Test in your tenant before planning around them:

1. **Do plugin skills count against your 50?** If Legal for Cowork's 20 skills count, a legal user
   has already spent 40% of the allowance before installing anything here.
2. **Does a skill shared with you consume your allowance, or the sharer's?**

## If a skill does not appear

- Did you start a **new** conversation?
- Does the folder name match the frontmatter `name`?
- Are you on mobile? Custom skills are not supported there.
- Has an admin enabled Cowork for you at all?

"""The two blocks of a guide that cannot be derived from SKILL.md.

Both are written, not generated, and build_guides.py refuses to run if a bot is missing from
either map. A new bot breaks the build instead of shipping mangled copy.

TRIGGERS: what a real person would type to start the bot. The frontmatter `description` is
routing logic written for Cowork's matcher, and splitting it mechanically produces fragments
like "Find hidden" that nobody would say out loud. Keep each under about 48 characters.

OUTPUTS: what the reader gets back, in their words. The `## Output` sections are written for a
practitioner reading the repo: some are markdown tables, some are single prose sentences, some
are three. There is no rule that turns all of them into three scannable lines without producing
a pipe-delimited table row on a shareable PDF, so they are rewritten here, faithfully. Keep each
under about 95 characters.

When a skill's Output section changes materially, change its entry here. Nothing can detect that
for you: the gate proves an entry exists, not that it is still true.
"""

TRIGGERS = {
    # comms
    "brand-answer-monitor": [
        "What does the web say about us?",
        "How are we showing up in AI answers?",
        "Run this week's brand check",
    ],
    "competition-monitor": [
        "Anything new from our competitors?",
        "Check the competitor list",
        "Did anyone launch something?",
    ],
    "internal-newsletter-builder": [
        "Draft this month's team newsletter",
        "What should go in the round-up?",
        "Build the internal update",
    ],
    "leadership-update-drafter": [
        "Draft my update for leadership",
        "Write up my monthly report",
        "Prepare my steering committee update",
    ],
    # core-executive
    "calendar-defender": [
        "Check my week for conflicts",
        "Which meetings can I drop?",
        "Do I have any focus time left?",
    ],
    # finance-finops
    "budget-variance-explainer": [
        "Why are we over budget?",
        "Explain this variance",
        "What is behind the overspend?",
    ],
    "cloud-cost-digest": [
        "What moved on the cloud bill?",
        "Explain this month's cloud spend",
        "Anything odd in the billing export?",
    ],
    "expense-reconciliation": [
        "Check my claims against the receipts",
        "What receipts am I missing?",
        "Reconcile last month's expenses",
    ],
    "invoice-vendor-followup": [
        "Which invoices have gone quiet?",
        "Who has not replied about payment?",
        "Draft the chasers for unpaid invoices",
    ],
    "subscription-hunter": [
        "What are we subscribed to?",
        "What renews in the next 30 days?",
        "Find the subscriptions we forgot",
    ],
    # it-ops
    "change-advisory-prep": [
        "Prepare the pack for the next CAB",
        "What changes are up for review?",
        "Which changes have no rollback plan?",
    ],
    "defect-intake-triage": [
        "Turn this bug report into a ticket",
        "Is there enough here to raise a defect?",
        "Triage what came in",
    ],
    "incident-digest": [
        "Build the timeline for this incident",
        "What happened, and when?",
        "Prepare the incident review",
    ],
    # people-hr
    "internal-expert-finder": [
        "Who here has done this before?",
        "Find someone who knows this system",
        "Who should I ask about this?",
    ],
    "interview-loop-coordinator": [
        "Set up the panel for this role",
        "Who covers what in the loop?",
        "Pull the interview feedback together",
    ],
    "onboarding-buddy": [
        "Plan the first two weeks for our joiner",
        "Who should they meet in week one?",
        "What should they read before Monday?",
    ],
    # projects
    "document-transmittal-tracker": [
        "What did we send the client?",
        "Who still owes us a response?",
        "What transmittals are overdue?",
    ],
    "lessons-learned-harvester": [
        "What keeps going wrong across projects?",
        "Pull the lessons from the close-outs",
        "What have we learned more than once?",
    ],
    "rfi-query-tracker": [
        "Which RFIs are still open?",
        "What is blocking work right now?",
        "Who owes us an answer?",
    ],
    # sales-bd
    "account-expert": [
        "Brief me before the customer meeting",
        "What is happening with this account?",
        "Catch me up on them",
    ],
    # team-lead
    "one-to-one-prep": [
        "Prep my 1:1 with Sam",
        "What do I owe them?",
        "What did they raise last time?",
    ],
    "project-decomposer": [
        "Break this project into tasks",
        "Who owns what on this?",
        "Turn this goal into a plan",
    ],
    "team-lead-mode": [
        "Set me up for the week",
        "Run my team lead review",
        "Prepare everything for Monday",
    ],
}

OUTPUTS = {
    # comms
    "brand-answer-monitor": [
        "A spreadsheet row per question, tracked week by week",
        "What moved since last week, and the four-week direction",
        "New sources quoting you for the first time",
    ],
    "competition-monitor": [
        "A before-and-after table of what actually changed",
        "One line on why each change matters",
        "When nothing changed, one line saying so, and nothing else",
    ],
    "internal-newsletter-builder": [
        "A Word document in your usual section order",
        "Every item carrying the link it came from",
        "Empty sections left out rather than padded",
    ],
    "leadership-update-drafter": [
        "Where we are, what changed, what is at risk, what I need from you",
        "A short list of what is still not known",
        "Facts and opinions kept visibly apart",
    ],
    # core-executive
    "calendar-defender": [
        "Your clashes, named meeting by meeting",
        "Meetings with no stated purpose and no decision to make",
        "Focus time against your target, and the exact changes to make",
    ],
    # finance-finops
    "budget-variance-explainer": [
        "Written commentary in your house structure",
        "A table of causes, with evidence and how much each explains",
        "The remainder that stays unexplained, stated plainly",
    ],
    "cloud-cost-digest": [
        "The total for the period against the one before",
        "The three biggest movements, with the owner to ask",
        "Anomalies no explanation could be found for",
    ],
    "expense-reconciliation": [
        "Every claim matched to its receipt, or flagged",
        "Counts by status, and the total value unmatched",
        "A drafted chaser for each person to chase",
    ],
    "invoice-vendor-followup": [
        "Every stalled thread, with its age and amount",
        "Who you are waiting on, and who is waiting on you",
        "A drafted nudge for each one, unsent",
    ],
    "subscription-hunter": [
        "An Excel sheet of every renewal, each row linked to its source",
        "What renews in the next 30 days, and what looks like waste",
        "A drafted cancellation or renegotiation, unsent",
    ],
    # it-ops
    "change-advisory-prep": [
        "The board pack: change, owner, window, risk, rollback",
        "Which changes arrived with fields missing",
        "Prior incidents on the same systems",
    ],
    "defect-intake-triage": [
        "A card turning the report into a ticket draft",
        "The exact fields still missing, written as questions",
        "Possible duplicates, linked",
    ],
    "incident-digest": [
        "A dated timeline of what happened",
        "What was observed, what was believed, what is known",
        "Open questions, each with an owner",
    ],
    # people-hr
    "internal-expert-finder": [
        "A shortlist of people, with the evidence for each",
        "Who to ask first, and who to ask if they are away",
        "Where it looked, so you can see what it missed",
    ],
    "interview-loop-coordinator": [
        "Who covers which competency, and what nobody covers",
        "What each interviewer needs beforehand",
        "Afterwards, the evidence, with disagreements shown",
    ],
    "onboarding-buddy": [
        "A day-by-day plan for the first fortnight",
        "Who they meet, and why that person",
        "What exists for them to read, and what is missing",
    ],
    # projects
    "document-transmittal-tracker": [
        "What was issued, to whom, and on what date",
        "What is overdue, grouped by party",
        "Revisions that quietly superseded an open item",
    ],
    "lessons-learned-harvester": [
        "Themes, and how many separate projects hit each one",
        "The lessons recurring across three projects or more",
        "Where the same recommendation keeps being made",
    ],
    "rfi-query-tracker": [
        "Every open question, with who owes the answer",
        "Which ones are actually blocking work",
        "Overdue items with no stated impact",
    ],
    # sales-bd
    "account-expert": [
        "What changed on the account since last time",
        "Open commitments, both yours and theirs",
        "Who went quiet, and the questions still open",
    ],
    # team-lead
    "one-to-one-prep": [
        "What they raised, quoted and linked",
        "What you owe them, and what is still unanswered",
        "Items carried over from last time, marked and counted",
    ],
    "project-decomposer": [
        "A card per task, each with a named owner",
        "How you will know each task is actually finished",
        "The whole set saved to a file, so it survives the chat",
    ],
    "team-lead-mode": [
        "One document: the three things that need you this week",
        "A section per report and per workstream, plus your calendar",
        "A run report saying which parts worked and which failed",
    ],
}

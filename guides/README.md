# The guides

One A4 page per bot, plus a `00-start-here` cover, plus `all-bots.pdf` with the whole set.

These are for the person who will actually use the bot, not for the person who reads a
repository. They assume no knowledge of Cowork, of skills, or of what a `.zip` is doing in a
folder called `dist`. Hand one to a colleague and they should be able to install the thing and
get a result without asking you anything.

Every page answers the same four questions in the same order:

1. **What is Cowork**, in three sentences, because most readers have not used it
2. **What this bot gives you**, in the words of its own description
3. **How to install it**, in five steps with the real menu names
4. **What it will never do without asking you**, which is the part that earns the trust

Each page also carries the bot's own stated principle, pulled from `## Definition of done` in
its `SKILL.md`. Those lines are the honest part of this catalogue: *a flat week is normal*,
*finding nobody is a real and useful answer*, *silence is the success state*. They are the
reason these bots are worth installing, so they are set in the largest type on the page.

## Rebuilding them

```bash
python3 tools/build_guides.py           # all 24 pages, plus the bundle
python3 tools/build_guides.py --check   # measure fit, build nothing
python3 tools/build_guides.py --only subscription-hunter
```

Rendering is HTML and CSS through headless Chrome's `--print-to-pdf`. The bundle uses
`pdfunite` from poppler.

## How they stay true

Almost everything on a page is read out of the bot's `SKILL.md` at build time: the title, the
one-line job, the description, the boundaries, the principle. Change a skill and its guide
changes with it.

Two blocks cannot be derived and live in [`../tools/guide_copy.py`](../tools/guide_copy.py):

- **Trigger phrases.** The frontmatter `description` is routing logic written for Cowork's
  matcher. Splitting it mechanically produces fragments like "Find hidden", which no human says.
- **What you get back.** The `## Output` sections are written for a practitioner reading the
  repo. Some are markdown tables. No rule turns all 23 into three scannable lines without
  printing a pipe-delimited table row onto a shareable PDF.

`build_guides.py` refuses to run if a bot is missing from either map, so a new bot breaks the
build rather than shipping mangled copy. **The gate proves an entry exists, not that it is still
true.** If you materially change a skill's Output section, change its entry too.

## The check

`--check` exists because a one-page PDF is not proof that the page fits. The footer is
absolutely positioned, so content can run underneath it and Chrome still emits a single page.
The check loads each page at A4 size and measures the millimetres between the last content
block and the footer rule, failing under 2mm. It caught five collisions the page count did not.

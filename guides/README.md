# The guides

One A4 page per bot, plus a `00-start-here` cover, plus `all-bots.pdf` with the whole set.

These are for the person who will actually use the bot, not for the person who reads a
repository. They assume no knowledge of Cowork, of skills, or of what a `.zip` is doing in a
folder called `dist`. Hand one to a colleague and they should be able to install the thing and
get a result without asking you anything.

The top half of every page is two columns answering the only two questions a reader has
before they decide:

- **Do this** — the five steps, led by a **live download button** that points straight at the
  bot's archive in `dist/`. It is a real PDF link annotation, so it is clickable from any
  viewer. A guide that says "download the file" without a link is a dead end.
- **And you get back** — three concrete lines, next to **what it will never do without
  asking you**, which is the pair that decides whether someone installs it.

Below that sits the bot's own stated principle, pulled from `## Definition of done` in its
`SKILL.md`: *a flat week is normal*, *finding nobody is a real and useful answer*, *silence is
the success state*. Those lines are the honest part of this catalogue and the reason the bots
are worth installing, so they are set in the largest type on the page.

Then how to put it on a schedule, and four footnotes. "What is Cowork" is one of those
footnotes rather than the opening, because a reader holding the PDF wants the action first
and the background second.

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

It finds that last block **structurally**, by walking the body's children, rather than by
naming a selector. The first version named `.pre`. Then the cover grew a download bar below
`.pre`, the check went on measuring the block above it, and it passed a page whose download
bar was sitting on top of the footer. A check pinned to a selector stops covering the page the
moment the page changes shape.

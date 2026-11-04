# The guides

**28 A4 pages: four for the people who decide, 23 for the people who use them, a closing page, plus
`all-bots.pdf` with the whole set.**

| Page | Audience | What it answers |
|---|---|---|
| `00-start-here` | Anyone | What this is, what is in it, how to install one |
| `01-for-the-admin` | Microsoft 365 admin | What you switch on, and the spending policy that is also an access control |
| `02-for-the-ciso` | CISO | What a skill actually is, where the risk is, which six read personal data |
| `03-for-the-cfo` | CFO | What is free, what meters, and where the control sits |
| 23 bot pages | The person using it | One job, one page |
| `99-where-to-go-next` | Anyone who finished | The newsletter and the store, once, at the end |

The split exists because the audiences want different facts. Spending policy and region
limits are admin facts; the trust boundary and the six personal-data skills are CISO facts;
Copilot Credits and the schedule ceiling are CFO facts. Putting all of that on the end user's
page made it longer and less useful, which is what the first version did.

## The 23 bot pages

The top half is two columns answering the only two questions a reader has before they decide:

- **Do this** — five steps, led by a **live download button** that points at the bot's archive.
  It is a real PDF link annotation, clickable from any viewer.
- **And you get back** — three concrete lines, beside **what it will never do without asking
  you**, which is the pair that decides whether someone installs it.

Below that: the bot's own principle, pulled from `## Definition of done` in its `SKILL.md`.
*A flat week is normal. Finding nobody is a real and useful answer.* Those lines are why the
bots are worth installing, so they are set in the largest type on the page.

## Rebuilding them

```bash
python3 tools/build_guides.py           # all 28 pages, plus the bundle
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

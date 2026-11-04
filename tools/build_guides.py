#!/usr/bin/env python3
"""Build one shareable A4 PDF guide per bot, from the SKILL.md files themselves.

Generated rather than hand-made, for the same reason the catalogue table is: 23 hand-built
guides drift from the skills the moment a skill changes, and nobody re-exports 23 PDFs.

Rendering is HTML plus CSS through headless Chrome's --print-to-pdf. reportlab is not installed
and would not give the layout control this needs; Chrome is already on the machine.

    python3 tools/build_guides.py            # build guides/*.pdf
    python3 tools/build_guides.py --html     # stop at HTML, for iterating on the design

The reader is a business user who has never heard of a skill file. Every guide answers four
questions in this order: what is this thing, what does this one do for me, how do I get it, and
what will it never do without asking. The fourth is the one that earns trust and it is the one
most vendor material leaves out.
"""
import argparse
import html
import pathlib
import re
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from guide_copy import OUTPUTS, TRIGGERS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs"
OUT = ROOT / "guides"
BUILD = ROOT / ".guide-build"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PACK_TITLES = {
    "core-executive": "Core / Executive",
    "team-lead": "Team Lead",
    "finance-finops": "Finance & FinOps",
    "people-hr": "People & HR",
    "it-ops": "IT & Ops",
    "projects": "Projects",
    "comms": "Comms",
    "sales-bd": "Sales & BD",
}

REPO = "github.com/kesslernity/awesome-copilot-cowork-bots"


def front_matter(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?", text, re.S)
    if not m:
        return {}, text
    out, key, folded = {}, None, []
    for raw in m.group(1).split("\n"):
        kv = re.match(r"^([a-zA-Z_][\w-]*):\s*(.*)$", raw)
        if kv and not raw.startswith((" ", "\t")):
            if key:
                out[key] = " ".join(folded).strip()
            key = kv.group(1)
            v = kv.group(2).strip()
            folded = [] if v in (">-", ">", "|", "|-") else [v]
            continue
        if key:
            folded.append(raw.strip())
    if key:
        out[key] = " ".join(folded).strip()
    return {k: re.sub(r"\s+", " ", v).strip() for k, v in out.items()}, text[m.end():]


def section(body, heading):
    m = re.search(rf"^## {re.escape(heading)}\s*$", body, re.M)
    if not m:
        return ""
    rest = body[m.end():]
    nxt = re.search(r"^## ", rest, re.M)
    return (rest[: nxt.start()] if nxt else rest).strip()


def plain(s):
    """Markdown to readable text. These land in HTML, so markers must not survive."""
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = s.replace("🔴", "").replace("⚠️", "")
    return re.sub(r"\s+", " ", s).strip()


def bullets(text, limit=3, maxlen=152):
    """Markdown bullets wrap across source lines. Joining the continuations first is the
    difference between a whole sentence and one cut off at "the contract are the"."""
    items, cur = [], None
    for line in text.split("\n"):
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            if cur is not None:
                items.append(cur)
            cur = m.group(1)
        elif cur is not None and line.strip() and line.startswith((" ", "\t")):
            cur += " " + line.strip()
        elif cur is not None:
            items.append(cur)
            cur = None
    if cur is not None:
        items.append(cur)

    out = []
    for raw in items:
        t = plain(raw)
        if len(t) < 12:
            continue
        if len(t) > maxlen:
            # These are the "will never do" lines, so where the cut lands matters. A whole
            # sentence reads as finished; a whole clause reads as a partial list; a cut
            # mid-phrase reads as broken and drops the qualifier that carried the meaning.
            head = t[:maxlen]
            dot = head.rfind(". ")
            comma = max(head.rfind(", "), head.rfind("; "))
            if dot > 48:
                t = head[:dot + 1]
            elif comma > 60:
                t = head[:comma] + "…"
            else:
                t = head.rsplit(" ", 1)[0] + "…"
        out.append(t)
        if len(out) == limit:
            break
    return out


def curly(s):
    """Straight quotes set in Georgia at 14pt look like a typo. Open after a space or the
    start of the string, close otherwise."""
    out, prev = [], " "
    for ch in s:
        if ch == '"':
            out.append("\u201c" if prev in " ([" else "\u201d")
        else:
            out.append(ch)
        prev = ch
    return "".join(out).replace("'", "\u2019")


def one_liner(body):
    for line in body.split("\n"):
        t = line.strip()
        if t and not t.startswith("#"):
            return plain(t)
    return ""


E = html.escape

CSS = """
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  width: 210mm; height: 297mm; background: #F5F1E8;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  color: #1C1A17; -webkit-print-color-adjust: exact; print-color-adjust: exact;
  padding: 12mm 13mm 9mm; position: relative;
}
.eyebrow { font-size: 8.5pt; letter-spacing: .1em; color: #9A8F80; margin-bottom: 3mm;
           text-transform: uppercase; }
.eyebrow b { color: #C4603C; font-weight: 700; }
h1 { font-family: Georgia, "Times New Roman", serif; font-size: 32pt; line-height: 1.0;
     letter-spacing: -.015em; margin-bottom: 3mm; }
.job { font-size: 12.5pt; line-height: 1.38; color: #3C362F; max-width: 168mm;
       padding-bottom: 4.2mm; border-bottom: 1.6px solid #E0D8C9; }
.row { display: flex; gap: 4mm; margin-top: 3.7mm; }
.card { background: #FFFDF9; border: 1.2px solid #E6DECF; border-radius: 3mm; padding: 4mm 4.6mm; }
.card.accent { background: #C4603C; border-color: #C4603C; }
.card h2 { font-family: Georgia, serif; font-size: 12pt; margin-bottom: 2.6mm; letter-spacing: -.01em; }
.card.accent h2 { color: #fff; }
.card p, .card li { font-size: 9.4pt; line-height: 1.38; color: #46403A; }
.card.accent p, .card.accent li { color: #FCEFE9; }
ul { list-style: none; }
li { position: relative; padding-left: 3.8mm; margin-bottom: 1.5mm; }
li:last-child { margin-bottom: 0; }
li::before { content: ""; position: absolute; left: 0; top: 1.6mm; width: 1.5mm; height: 1.5mm;
             border-radius: 50%; background: #C4603C; }
.card.accent li::before { background: #F6CDB9; }
.steps { display: flex; gap: 2.6mm; margin-top: 3.7mm; }
.step { flex: 1; background: #FFFDF9; border: 1.2px solid #E6DECF; border-radius: 3mm;
        padding: 3.4mm 2.6mm; text-align: center; }
.step .n { width: 6.6mm; height: 6.6mm; border-radius: 50%; background: #1C1A17; color: #F5F1E8;
           font-size: 9.5pt; font-weight: 700; line-height: 6.6mm; margin: 0 auto 2.2mm; }
.step p { font-size: 8.4pt; line-height: 1.33; color: #46403A; }
.say { margin-top: 3.7mm; }
.say h2 { font-family: Georgia, serif; font-size: 12pt; margin-bottom: 2.6mm; }
.quotes { display: flex; gap: 2.6mm; }
.q { flex: 1; background: #FFFDF9; border: 1.2px solid #E6DECF; border-left: 2.6mm solid #C4603C;
     border-radius: 2mm; padding: 2.8mm 3.4mm; font-size: 9.2pt; color: #3C362F;
     font-style: italic; display: flex; align-items: center; }
.band { margin-top: 3.7mm; background: #1C1A17; border-radius: 3mm; padding: 3.6mm 5.4mm;
        display: flex; align-items: baseline; gap: 5mm; }
.band .tag { font-size: 7.8pt; letter-spacing: .1em; text-transform: uppercase; color: #BFAE97;
             white-space: nowrap; }
.band .line { font-family: Georgia, serif; font-size: 14pt; line-height: 1.22; color: #F8F2E8; }
.pre { margin-top: 3.7mm; display: flex; gap: 2.6mm; }
.chip { flex: 1; border: 1.2px dashed #CFC2AC; border-radius: 2.4mm; padding: 2.4mm 3mm; }
.chip b { display: block; font-size: 8.2pt; color: #C4603C; margin-bottom: .9mm;
          letter-spacing: .04em; text-transform: uppercase; }
.chip span { font-size: 8.4pt; line-height: 1.33; color: #5A5249; }
.foot { position: absolute; left: 13mm; right: 13mm; bottom: 9mm;
        display: flex; justify-content: space-between; align-items: baseline;
        border-top: 1.6px solid #E0D8C9; padding-top: 3mm;
        font-size: 7.6pt; color: #9A8F80; }
.foot b { color: #C4603C; }
.w33 { width: 33.33%; } .w50 { width: 50%; }
"""

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="eyebrow">Microsoft 365 Copilot Cowork &nbsp;·&nbsp; <b>{pack}</b> &nbsp;·&nbsp; Free, MIT licence</div>
<h1>{title}</h1>
<p class="job">{job}</p>

<div class="row">
  <div class="card w33"><h2>What is Cowork?</h2><p>The part of Microsoft 365 Copilot that
    <b>does the work</b>, not just the chatting. It reads your mail, files and meetings, then
    prepares the result. By default it asks you before it sends anything.</p></div>
  <div class="card w33"><h2>What a skill is</h2><p>One file you upload once. It teaches Cowork a
    job you keep repeating, so you stop explaining it every time. It lives in your own OneDrive.</p></div>
  <div class="card accent w33"><h2>What this one gives you</h2><p>{gives}</p></div>
</div>

<div class="steps">{steps}</div>

<div class="say"><h2>Then just say one of these</h2><div class="quotes">{quotes}</div></div>

<div class="row">
  <div class="card w50"><h2>What you get back</h2><ul>{output}</ul></div>
  <div class="card accent w50"><h2>What it will never do without asking you</h2><ul>{never}</ul></div>
</div>

<div class="band"><span class="tag">The rule<br>it follows</span><span class="line">{principle}</span></div>

<div class="pre">
  <div class="chip"><b>You need</b><span>Microsoft 365 Copilot with Cowork switched on by your admin. It is off by default.</span></div>
  <div class="chip"><b>Not on mobile</b><span>Uploaded skills only work on a laptop or desktop.</span></div>
  <div class="chip"><b>It is metered</b><span>Cowork bills on usage. Your admin can cap what you spend.</span></div>
  <div class="chip"><b>Make it yours</b><span>Open <i>references/config.md</i> to set the names and thresholds.</span></div>
</div>

<div class="foot"><span>{repo}</span><span>Not affiliated with, or endorsed by, Microsoft. &nbsp;·&nbsp; <b>Free to share</b></span></div>
</body></html>"""

STEPS = [
    "Download the file for this skill",
    "In Cowork, open <b>Customize</b>",
    "Go to the <b>Skills</b> tab",
    "<b>Add</b> → <b>Upload skill</b>, pick the file",
    "Start a <b>new</b> chat and say the words below",
]


def build_html(bot_dir):
    pack = bot_dir.parent.name
    text = (bot_dir / "skill" / "SKILL.md").read_text(encoding="utf-8")
    fm, body = front_matter(text)

    title = re.search(r"^#\s+(.+)$", body, re.M)
    title = title.group(1).strip() if title else bot_dir.name

    job = one_liner(body)
    if job and job[-1] not in ".?!":
        job += "."
    gives = re.split(r"(?<=\.)\s", plain(fm.get("description", "")))[0]
    if len(gives) > 205:
        gives = gives[:205].rsplit(" ", 1)[0] + "…"

    # The bolded phrase in "Definition of done" is each bot's own stated principle, already
    # written in the skill. Using it keeps the guide's loudest line impossible to drift.
    principle = re.search(r"\*\*(.+?)\*\*", section(body, "Definition of done"), re.S)
    if not principle:
        sys.exit(f"{bot_dir.name}: no bolded principle under '## Definition of done'.")
    principle = plain("**" + principle.group(1) + "**")
    if len(principle) > 1 and principle[0] == '"' and principle[-1] == '"':
        principle = principle[1:-1]

    for label, table in (("trigger phrases", TRIGGERS), ("output lines", OUTPUTS)):
        if bot_dir.name not in table:
            sys.exit(
                f"No {label} for '{bot_dir.name}'. Add them to tools/guide_copy.py.\n"
                "They are written, not derived: see that file's docstring for why."
            )
    quotes = TRIGGERS[bot_dir.name]
    out_items = OUTPUTS[bot_dir.name]
    never = bullets(section(body, "Boundaries"))
    if not never:
        sys.exit(f"{bot_dir.name}: no bullets under '## Boundaries'.")

    return PAGE.format(
        css=CSS,
        pack=E(PACK_TITLES.get(pack, pack)),
        title=E(title),
        job=E(curly(job)),
        gives=E(curly(gives)),
        steps="".join(
            f'<div class="step"><div class="n">{i+1}</div><p>{s}</p></div>'
            for i, s in enumerate(STEPS)
        ),
        quotes="".join(f'<div class="q">“{E(curly(q))}”</div>' for q in quotes),
        output="".join(f"<li>{E(curly(t))}</li>" for t in out_items),
        never="".join(f"<li>{E(curly(t))}</li>" for t in never),
        principle=E(curly(principle)),
        repo=REPO,
    )


PROBE = """<script>
// A single-page PDF is not proof the page fits: the footer is absolutely positioned, so
// content can run underneath it and Chrome still emits one page. Measure the gap instead.
window.addEventListener('load', function () {
  var pre = document.querySelector('.pre').getBoundingClientRect();
  var foot = document.querySelector('.foot').getBoundingClientRect();
  var px = 96 / 25.4;
  document.title = 'GAP ' + ((foot.top - pre.bottom) / px).toFixed(1);
});
</script></body>"""


def check(bots):
    """Report the millimetres between the last content block and the footer rule.

    The cover is measured too. It is the one page nobody would think to re-render after a
    copy change, which makes it the one most likely to overflow unnoticed.
    """
    pages = [("00-start-here", build_cover(bots))] + [(b.name, build_html(b)) for b in bots]
    worst, fails = None, []
    for name, markup in pages:
        h = BUILD / f"probe-{name}.html"
        h.write_text(markup.replace("</body>", PROBE), encoding="utf-8")
        dom = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--dump-dom", "--window-size=794,1123",
             f"--user-data-dir={BUILD}/chrome", "--virtual-time-budget=3000", h.as_uri()],
            capture_output=True, text=True,
        ).stdout
        m = re.search(r"<title>GAP (-?[\d.]+)</title>", dom)
        if not m:
            fails.append((name, None))
            continue
        gap = float(m.group(1))
        if worst is None or gap < worst[1]:
            worst = (name, gap)
        if gap < 2.0:
            fails.append((name, gap))
        h.unlink()

    for name, gap in fails:
        print(f"  FAIL {name}: {'no measurement' if gap is None else f'{gap}mm to the footer'}")
    print(f"tightest: {worst[0]} at {worst[1]}mm" if worst else "nothing measured")
    return not fails


COVER = """<!doctype html><html><head><meta charset="utf-8"><style>{css}
.packs {{ display: flex; flex-wrap: wrap; gap: 2.6mm; margin-top: 3.7mm; }}
.pk {{ width: calc(25% - 2mm); background: #FFFDF9; border: 1.2px solid #E6DECF;
      border-radius: 2.6mm; padding: 3mm 3.4mm; }}
.pk b {{ display: block; font-family: Georgia, serif; font-size: 10pt; margin-bottom: .8mm; }}
.pk span {{ font-size: 8.2pt; color: #8A8073; }}
.grab {{ margin-top: 3.7mm; background: #FFFDF9; border: 1.6px solid #C4603C; border-radius: 3mm;
        padding: 3.4mm 5mm; display: flex; justify-content: space-between; align-items: baseline; }}
.grab .g1 {{ font-family: Georgia, serif; font-size: 11.5pt; color: #1C1A17; }}
.grab .g2 {{ font-size: 10pt; color: #C4603C; font-weight: 700; }}
</style></head><body>
<div class="eyebrow">Microsoft 365 Copilot Cowork &nbsp;·&nbsp; <b>Start here</b> &nbsp;·&nbsp; Free, MIT licence</div>
<h1>Give Copilot a job<br>it can do without you</h1>
<p class="job">{count} ready-made bots for Microsoft 365 Copilot Cowork. Each one is a single file
you upload once. After that you ask in plain English and it does the work, inside your own
mailbox and files, under your own permissions.</p>

<div class="row">
  <div class="card w33"><h2>What is Cowork?</h2><p>The part of Microsoft 365 Copilot that
    <b>does the work</b>, not just the chatting. Chat answers a question in seconds. Cowork reads
    across your mail, files and meetings and comes back with the finished thing.</p></div>
  <div class="card w33"><h2>What a skill is</h2><p>One file that teaches Cowork a job you keep
    repeating, so you stop explaining it every time. It sits in your own OneDrive. Nobody else
    sees it unless you share it.</p></div>
  <div class="card accent w33"><h2>Why these are safe to try</h2><p>Every bot here reads and
    prepares, then stops. Sending, posting and deleting wait for a button you press. You can
    choose to pre-approve things later. No bot here decides that for you.</p></div>
</div>

<div class="steps">{steps}</div>

<div class="say"><h2>What is in the box</h2><div class="packs">{packs}</div></div>

<div class="band"><span class="tag">The rule<br>they follow</span><span class="line">Silence is a
result. A bot that invents a finding to look busy teaches you to stop reading it.</span></div>

<div class="pre">
  <div class="chip"><b>You need</b><span>Microsoft 365 Copilot with Cowork switched on by your admin. It is off by default.</span></div>
  <div class="chip"><b>Not on mobile</b><span>Uploaded skills only work on a laptop or desktop.</span></div>
  <div class="chip"><b>It is metered</b><span>Cowork bills on usage. Your admin can cap what you spend.</span></div>
  <div class="chip"><b>Room for all of them</b><span>You can hold 50 skills. These {count} use under half.</span></div>
</div>

<div class="grab"><span class="g1">Download them all, free</span><span class="g2">{repo}</span></div>

<div class="foot"><span>Every bot ships with its own one-page guide like this one.</span><span>Not affiliated with, or endorsed by, Microsoft. &nbsp;·&nbsp; <b>MIT licence, free to share</b></span></div>
</body></html>"""

COVER_STEPS = [
    "Pick a bot and <b>download its file</b>",
    "In Cowork, open <b>Customize</b>",
    "Go to the <b>Skills</b> tab",
    "<b>Add</b> → <b>Upload skill</b>, pick the file",
    "Start a <b>new</b> chat and ask it for the job",
]


def build_cover(bots):
    by_pack = {}
    for b in bots:
        by_pack.setdefault(b.parent.name, []).append(b)
    order = [p for p in PACK_TITLES if p in by_pack] + [p for p in by_pack if p not in PACK_TITLES]
    packs = "".join(
        f'<div class="pk"><b>{E(PACK_TITLES.get(p, p))}</b>'
        f'<span>{len(by_pack[p])} bot{"s" if len(by_pack[p]) != 1 else ""}</span></div>'
        for p in order
    )
    return COVER.format(
        css=CSS,
        count=len(bots),
        steps="".join(
            f'<div class="step"><div class="n">{i+1}</div><p>{s}</p></div>'
            for i, s in enumerate(COVER_STEPS)
        ),
        packs=packs,
        repo=REPO,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", action="store_true", help="write HTML only")
    ap.add_argument("--check", action="store_true", help="measure fit, build nothing")
    ap.add_argument("--only", help="build one bot by slug")
    args = ap.parse_args()

    bots = sorted(p.parent.parent for p in PACKS.glob("*/*/skill/SKILL.md"))
    if args.only:
        bots = [b for b in bots if b.name == args.only]
    if not bots:
        sys.exit("No bots found.")

    BUILD.mkdir(exist_ok=True)
    if args.check:
        sys.exit(0 if check(bots) else 1)

    OUT.mkdir(exist_ok=True)
    pages = [("00-start-here", build_cover(bots))] if not args.only else []
    pages += [(b.name, build_html(b)) for b in bots]

    made = []
    for name, markup in pages:
        h = BUILD / f"{name}.html"
        h.write_text(markup, encoding="utf-8")
        if args.html:
            made.append(h)
            continue
        pdf = OUT / f"{name}.pdf"
        subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={pdf}", f"--user-data-dir={BUILD}/chrome",
             "--virtual-time-budget=4000", h.as_uri()],
            check=True, capture_output=True,
        )
        made.append(pdf)

    if not args.html and not args.only:
        # One file to hand someone who wants the whole set. pdfunite ships with poppler,
        # which is already a dependency of the fit check's rendering workflow.
        bundle = OUT / "all-bots.pdf"
        bundle.unlink(missing_ok=True)
        subprocess.run(["pdfunite", *[str(p) for p in made], str(bundle)], check=True)
        print(f"bundle: {bundle.relative_to(ROOT)} ({len(made)} pages)")

    print(f"{len(made)} {'HTML files' if args.html else 'PDFs'} written to "
          f"{(BUILD if args.html else OUT).relative_to(ROOT)}/")


if __name__ == "__main__":
    main()

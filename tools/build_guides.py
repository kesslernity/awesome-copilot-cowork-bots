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
# Where the download buttons point. `raw/main` serves the file itself rather than GitHub's
# page about the file, which is the difference between a working link and a confused reader.
RAW = f"https://{REPO}/raw/main"


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
h1 { font-family: Georgia, "Times New Roman", serif; font-size: 34pt; line-height: 1.0;
     letter-spacing: -.015em; margin-bottom: 3mm; }
.job { font-size: 14.2pt; line-height: 1.34; color: #3C362F; max-width: 168mm;
       padding-bottom: 4.2mm; border-bottom: 1.6px solid #E0D8C9; }
.row { display: flex; gap: 4mm; margin-top: 3.7mm; }
.card { background: #FFFDF9; border: 1.2px solid #E6DECF; border-radius: 3mm; padding: 4.4mm 5mm; }
.card.accent { background: #C4603C; border-color: #C4603C; }
.card h2 { font-family: Georgia, serif; font-size: 14pt; margin-bottom: 2.6mm; letter-spacing: -.01em; }
.card.accent h2 { color: #fff; }
.card p, .card li { font-size: 11pt; line-height: 1.42; color: #46403A; }
.card.accent p, .card.accent li { color: #FCEFE9; }
ul { list-style: none; }
li { position: relative; padding-left: 4mm; margin-bottom: 1.8mm; }
li:last-child { margin-bottom: 0; }
li::before { content: ""; position: absolute; left: 0; top: 1.9mm; width: 1.5mm; height: 1.5mm;
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
.band .line { font-family: Georgia, serif; font-size: 17pt; line-height: 1.22; color: #F8F2E8; }
/* The hero answers the only two questions a new reader has, side by side: what do I do,
   and what do I get. Everything that was competing with them is now below the fold. */
.hero { display: flex; gap: 4mm; margin-top: 4mm; align-items: stretch; }
.do { width: 53%; background: #1C1A17; border-radius: 3mm; padding: 4.4mm 4.8mm 4.8mm;
      display: flex; flex-direction: column; }
.note { margin-top: auto; padding-top: 4mm; font-size: 9.6pt; line-height: 1.4; color: #A79C8D;
        border-top: 1px solid #38332C; }
.note b { color: #E0D6C8; }
.hh { font-family: Georgia, serif; font-size: 14.4pt; color: #F8F2E8; margin-bottom: 3mm; }
.dl { display: flex; align-items: center; gap: 3mm; text-decoration: none;
      background: #C4603C; border-radius: 2.6mm; padding: 3.2mm 3.6mm; margin-bottom: 3mm; }
.dln { width: 6.6mm; height: 6.6mm; border-radius: 50%; background: #FFF3EC; color: #C4603C;
       font-size: 9.5pt; font-weight: 700; line-height: 6.6mm; text-align: center; flex: none; }
.dlt { flex: 1; min-width: 0; }
.dlt b { display: block; font-size: 11.4pt; color: #fff; letter-spacing: .005em; }
.dlf { display: block; font-size: 11pt; font-weight: 700; color: #FFE8DC; }
.dlr { display: block; font-size: 7.4pt; color: #F2C4AE; margin-top: .6mm;
       white-space: nowrap; }
.dla { font-size: 15pt; color: #FFD9C6; flex: none; }
.ms { display: flex; gap: 3mm; align-items: baseline; margin-bottom: 1.9mm; }
.n2 { width: 6.6mm; font-size: 9pt; font-weight: 700; color: #C4603C; flex: none;
      text-align: center; }
.ms span:last-child { font-size: 10.8pt; line-height: 1.4; color: #E6DFD4; }
.ms b { color: #fff; }
.getcol { width: 47%; display: flex; flex-direction: column; gap: 4mm; }
.getcol .card { margin: 0; }
.getcol .grow { flex: 1; }
/* The phrases sit under step 5, indented to its text column, so "say one of these" and the
   things to say read as one instruction rather than two blocks. */
.do .quotes { display: block; margin: 2.2mm 0 0 9.6mm; }
.do .q { display: block; flex: none; background: #2B2722; border: none;
         border-left: 2.2mm solid #C4603C; border-radius: 1.6mm; padding: 1.9mm 3mm;
         font-size: 10.6pt; color: #F6DCCD; margin-bottom: 1.7mm; }
.do .q:last-child { margin-bottom: 0; }
.sched { margin-top: 3.7mm; border: 1.2px solid #E0D8C9; border-radius: 3mm;
          padding: 3.6mm 5mm; font-size: 10.6pt; line-height: 1.42; color: #4A443C; }
.sched b { color: #1C1A17; }
.pre { margin-top: 3.7mm; display: flex; gap: 2.6mm; }
.chip { flex: 1; border: 1.2px dashed #CFC2AC; border-radius: 2.4mm; padding: 2.4mm 3mm; }
.chip b { display: block; font-size: 8.8pt; color: #C4603C; margin-bottom: .9mm;
          letter-spacing: .04em; text-transform: uppercase; }
.chip span { font-size: 9.8pt; line-height: 1.38; color: #5A5249; }
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

<div class="hero">
  <div class="do">
    <h2 class="hh">Do this, about two minutes</h2>
    <a class="dl" href="{zip_url}">
      <span class="dln">1</span>
      <span class="dlt"><b>Download the skill file</b><span class="dlf">{zip_name}</span>
        <span class="dlr">{repo}</span></span>
      <span class="dla">&#8595;</span>
    </a>
    <div class="ms"><span class="n2">2</span><span>In Cowork, open <b>Customize</b> in the side panel</span></div>
    <div class="ms"><span class="n2">3</span><span>Go to the <b>Skills</b> tab</span></div>
    <div class="ms"><span class="n2">4</span><span>Select the arrow next to <b>Add</b>, then <b>Upload skill</b>, and choose the file</span></div>
    <div class="ms"><span class="n2">5</span><span>Start a <b>new</b> chat and say one of these</span></div>
    <div class="quotes">{quotes}</div>
    <p class="note">Nothing is sent, posted or deleted unless you press a button.
      <b>Changed your mind?</b> Remove the skill from the same <b>Skills</b> tab.</p>
  </div>

  <div class="getcol">
    <div class="card accent grow"><h2>And you get back</h2><ul>{output}</ul></div>
    <div class="card"><h2>What it will never do without asking you</h2><ul>{never}</ul></div>
  </div>
</div>

<div class="band"><span class="tag">The rule<br>it follows</span><span class="line">{principle}</span></div>

<div class="sched"><b>Runs when you ask for it.</b> Want it on a timer? Say <i>“do this every
Monday at 9”</i> and Cowork schedules it. You get 25 schedules, so spend them on the jobs you
would otherwise forget.</div>

<div class="pre">
  <div class="chip"><b>New to Cowork?</b><span>It is the part of Copilot that <i>does the work</i>, not just the chatting. A skill is one file that teaches it a job you repeat.</span></div>
  <div class="chip"><b>You need</b><span>Microsoft 365 Copilot with Cowork switched on by your admin. It is off by default, and not on mobile.</span></div>
  <div class="chip"><b>It is metered</b><span>Cowork bills on usage. Your admin can cap what you spend.</span></div>
  <div class="chip"><b>Make it yours</b><span>Open <i>references/config.md</i> inside the file to set the names and thresholds.</span></div>
</div>

<div class="foot"><span>{repo}</span><span>Not affiliated with, or endorsed by, Microsoft. &nbsp;·&nbsp; <b>Free to share</b></span></div>
</body></html>"""


def build_html(bot_dir):
    pack = bot_dir.parent.name
    text = (bot_dir / "skill" / "SKILL.md").read_text(encoding="utf-8")
    fm, body = front_matter(text)

    title = re.search(r"^#\s+(.+)$", body, re.M)
    title = title.group(1).strip() if title else bot_dir.name

    job = one_liner(body)
    if job and job[-1] not in ".?!":
        job += "."

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
        zip_url=f"{RAW}/dist/{bot_dir.name}.zip",
        zip_name=f"{bot_dir.name}.zip",
        quotes="".join(f'<div class="q">“{E(curly(q))}”</div>' for q in quotes),
        output="".join(f"<li>{E(curly(t))}</li>" for t in out_items),
        never="".join(f"<li>{E(curly(t))}</li>" for t in never),
        principle=E(curly(principle)),
        repo=REPO,
    )


PROBE = """<script>
// A single-page PDF is not proof the page fits: the footer is absolutely positioned, so
// content can run underneath it and Chrome still emits one page. Measure the gap instead.
// Measure the LAST block in the flow, found structurally. Naming a selector here once meant
// the cover grew a download bar below the one being measured, and the check passed a page
// whose last element sat on top of the footer.
window.addEventListener('load', function () {
  var last = null;
  document.body.querySelectorAll(':scope > *').forEach(function (el) {
    if (el.classList.contains('foot') || el.tagName === 'SCRIPT') return;
    if (!last || el.getBoundingClientRect().bottom > last) {
      last = el.getBoundingClientRect().bottom;
    }
  });
  var foot = document.querySelector('.foot').getBoundingClientRect();
  var px = 96 / 25.4;
  document.title = 'GAP ' + ((foot.top - last) / px).toFixed(1);
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
      border-radius: 2.6mm; padding: 2.2mm 3mm; display: flex; justify-content: space-between;
      align-items: baseline; }}
.pk b {{ font-family: Georgia, serif; font-size: 10.4pt; }}
.pk span {{ font-size: 8.6pt; color: #8A8073; }}
.band .line {{ font-size: 14.5pt; }}
.grab {{ margin-top: 3.7mm; background: #C4603C; border-radius: 3mm; text-decoration: none;
        padding: 3.8mm 5mm; display: flex; justify-content: space-between; align-items: baseline; }}
.grab .g1 {{ font-family: Georgia, serif; font-size: 13pt; color: #fff; }}
.grab .g2 {{ font-size: 10.6pt; color: #FFE8DC; font-weight: 700; }}
</style></head><body>
<div class="eyebrow">Microsoft 365 Copilot Cowork &nbsp;·&nbsp; <b>Start here</b> &nbsp;·&nbsp; Free, MIT licence</div>
<h1>Give Copilot a job<br>it can do without you</h1>
<p class="job">{count} ready-made bots for Microsoft 365 Copilot Cowork. Each is one file you
upload once. After that you ask in plain English, and the work happens inside your own mailbox
and files, under your own permissions.</p>

<div class="row">
  <div class="card w33"><h2>What is Cowork?</h2><p>The part of Microsoft 365 Copilot that
    <b>does the work</b>, not just the chatting. Chat answers a question in seconds. Cowork reads
    across your mail, files and meetings and comes back with the finished thing.</p></div>
  <div class="card w33"><h2>What a skill is</h2><p>One file that teaches Cowork a job you keep
    repeating, so you stop explaining it every time. It sits in your own OneDrive. Nobody else
    sees it unless you share it.</p></div>
  <div class="card accent w33"><h2>Why these are safe to try</h2><p>Every bot here reads and
    prepares, then stops. Sending, posting and deleting wait for a button you press, and no bot
    here decides otherwise for you.</p></div>
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

<a class="grab" href="{raw}"><span class="g1">Download them all, free</span><span class="g2">{repo} &nbsp;&#8595;</span></a>

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
        raw=f"https://{REPO}",
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

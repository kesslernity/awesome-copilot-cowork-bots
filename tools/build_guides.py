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
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from guide_copy import OUTPUTS, TRIGGERS  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs"
OUT = ROOT / "guides"
BUILD = ROOT / ".guide-build"
# Per-run Chrome profile: a shared one makes two concurrent builds fight over its lock,
# and the loser dies mid-render looking like a bug in whichever page it was on.
PROFILE = BUILD / f"chrome-{os.getpid()}"

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
  width: 210mm; height: 297mm; background: #F7F8FA;
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  color: #0F172A; -webkit-print-color-adjust: exact; print-color-adjust: exact;
  padding: 12mm 13mm 9mm; position: relative;
}
.eyebrow { font-size: 8.5pt; letter-spacing: .1em; color: #64748B; margin-bottom: 3mm;
           text-transform: uppercase; }
.eyebrow b { color: #2563EB; font-weight: 700; }
h1 { font-family: Georgia, "Times New Roman", serif; font-size: 34pt; line-height: 1.0;
     letter-spacing: -.015em; margin-bottom: 3mm; }
.job { font-size: 14.2pt; line-height: 1.34; color: #334155; max-width: 168mm;
       padding-bottom: 4.2mm; border-bottom: 1.6px solid #CBD5E1; }
.row { display: flex; gap: 4mm; margin-top: 3.7mm; }
.card { background: #FFFFFF; border: 1.2px solid #E2E8F0; border-radius: 3mm; padding: 4.4mm 5mm; }
.card.accent { background: #2563EB; border-color: #2563EB; }
.card h2 { font-family: Georgia, serif; font-size: 14pt; margin-bottom: 2.6mm; letter-spacing: -.01em; }
.card.accent h2 { color: #fff; }
.card p, .card li { font-size: 11pt; line-height: 1.42; color: #334155; }
.card.accent p, .card.accent li { color: #EFF6FF; }
ul { list-style: none; }
li { position: relative; padding-left: 4mm; margin-bottom: 1.8mm; }
li:last-child { margin-bottom: 0; }
li::before { content: ""; position: absolute; left: 0; top: 1.9mm; width: 1.5mm; height: 1.5mm;
             border-radius: 50%; background: #2563EB; }
.card.accent li::before { background: #BFDBFE; }
.steps { display: flex; gap: 2.6mm; margin-top: 3.7mm; }
.step { flex: 1; background: #FFFFFF; border: 1.2px solid #E2E8F0; border-radius: 3mm;
        padding: 3.4mm 2.6mm; text-align: center; }
.step .n { width: 6.6mm; height: 6.6mm; border-radius: 50%; background: #0F172A; color: #F7F8FA;
           font-size: 9.5pt; font-weight: 700; line-height: 6.6mm; margin: 0 auto 2.2mm; }
.step p { font-size: 8.4pt; line-height: 1.33; color: #334155; }
.say { margin-top: 3.7mm; }
.say h2 { font-family: Georgia, serif; font-size: 12pt; margin-bottom: 2.6mm; }
.quotes { display: flex; gap: 2.6mm; }
.q { flex: 1; background: #FFFFFF; border: 1.2px solid #E2E8F0; border-left: 2.6mm solid #2563EB;
     border-radius: 2mm; padding: 2.8mm 3.4mm; font-size: 9.2pt; color: #334155;
     font-style: italic; display: flex; align-items: center; }
.band { margin-top: 3.7mm; background: #0F172A; border-radius: 3mm; padding: 3.6mm 5.4mm;
        display: flex; align-items: baseline; gap: 5mm; }
.band .tag { font-size: 7.8pt; letter-spacing: .1em; text-transform: uppercase; color: #94A3B8;
             white-space: nowrap; }
.band .line { font-family: Georgia, serif; font-size: 17pt; line-height: 1.22; color: #F8FAFC; }
/* The hero answers the only two questions a new reader has, side by side: what do I do,
   and what do I get. Everything that was competing with them is now below the fold. */
.hero { display: flex; gap: 4mm; margin-top: 4mm; align-items: stretch; }
.do { width: 53%; background: #0F172A; border-radius: 3mm; padding: 4.4mm 4.8mm 4.8mm;
      display: flex; flex-direction: column; }
.note { margin-top: auto; padding-top: 4mm; font-size: 9.6pt; line-height: 1.4; color: #94A3B8;
        border-top: 1px solid #1E293B; }
.note b { color: #E2E8F0; }
.hh { font-family: Georgia, serif; font-size: 14.4pt; color: #F8FAFC; margin-bottom: 3mm; }
.dl { display: flex; align-items: center; gap: 3mm; text-decoration: none;
      background: #2563EB; border-radius: 2.6mm; padding: 3.2mm 3.6mm; margin-bottom: 3mm; }
.dln { width: 6.6mm; height: 6.6mm; border-radius: 50%; background: #EFF6FF; color: #2563EB;
       font-size: 9.5pt; font-weight: 700; line-height: 6.6mm; text-align: center; flex: none; }
.dlt { flex: 1; min-width: 0; }
.dlt b { display: block; font-size: 11.4pt; color: #fff; letter-spacing: .005em; }
.dlf { display: block; font-size: 11pt; font-weight: 700; color: #DBEAFE; }
.dlr { display: block; font-size: 7.4pt; color: #93C5FD; margin-top: .6mm;
       white-space: nowrap; }
.dla { font-size: 15pt; color: #BFDBFE; flex: none; }
.ms { display: flex; gap: 3mm; align-items: baseline; margin-bottom: 1.9mm; }
.n2 { width: 6.6mm; font-size: 9pt; font-weight: 700; color: #2563EB; flex: none;
      text-align: center; }
.ms span:last-child { font-size: 10.8pt; line-height: 1.4; color: #E6DFD4; }
.ms b { color: #fff; }
.getcol { width: 47%; display: flex; flex-direction: column; gap: 4mm; }
.getcol .card { margin: 0; }
.getcol .grow { flex: 1; }
/* The phrases sit under step 5, indented to its text column, so "say one of these" and the
   things to say read as one instruction rather than two blocks. */
.do .quotes { display: block; margin: 2.2mm 0 0 9.6mm; }
.do .q { display: block; flex: none; background: #1E293B; border: none;
         border-left: 2.2mm solid #2563EB; border-radius: 1.6mm; padding: 1.9mm 3mm;
         font-size: 10.6pt; color: #DBEAFE; margin-bottom: 1.7mm; }
.do .q:last-child { margin-bottom: 0; }
.sched { margin-top: 3.7mm; border: 1.2px solid #CBD5E1; border-radius: 3mm;
          padding: 3.6mm 5mm; font-size: 10.6pt; line-height: 1.42; color: #4A443C; }
.sched b { color: #0F172A; }
.pre { margin-top: 3.7mm; display: flex; gap: 2.6mm; }
.chip { flex: 1; border: 1.2px dashed #CBD5E1; border-radius: 2.4mm; padding: 2.4mm 3mm; }
.chip b { display: block; font-size: 8.8pt; color: #2563EB; margin-bottom: .9mm;
          letter-spacing: .04em; text-transform: uppercase; }
.chip span { font-size: 9.8pt; line-height: 1.38; color: #475569; }
.foot { position: absolute; left: 13mm; right: 13mm; bottom: 9mm;
        display: flex; justify-content: space-between; align-items: baseline;
        border-top: 1.6px solid #CBD5E1; padding-top: 3mm;
        font-size: 7.6pt; color: #64748B; }
.foot b { color: #2563EB; }
.w33 { width: 33.33%; } .w50 { width: 50%; }
"""

PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>
<div class="eyebrow">Microsoft 365 Copilot Cowork &nbsp;·&nbsp; <b>{pack}</b> &nbsp;·&nbsp; Free, MIT license</div>
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
    <div class="ms"><span class="n2">2</span><span>In Cowork, open <b>Customize</b> from the left navigation</span></div>
    <div class="ms"><span class="n2">3</span><span>Go to the <b>Skills</b> tab</span></div>
    <div class="ms"><span class="n2">4</span><span>Select the arrow next to <b>Add</b>, then <b>Upload skill</b>, and choose the file</span></div>
    <div class="ms"><span class="n2">5</span><span>Start a <b>new</b> chat and say one of these</span></div>
    <div class="quotes">{quotes}</div>
    <p class="note">Written to prepare and stop. Cowork still asks before it sends, so approve
      one action at a time and avoid <b>always allow</b> while you are trying it.
      <b>AI prepares, people decide.</b></p>
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
  <div class="chip"><b>Desktop only</b><span>Cowork runs on mobile. Uploaded skills do not. Use a laptop.</span></div>
  <div class="chip"><b>You need</b><span>Microsoft 365 Copilot, and Cowork switched on by your admin. Off by default.</span></div>
  <div class="chip"><b>It is metered</b><span>Cowork bills Copilot Credits as you use it. Your admin sets the policy.</span></div>
  <div class="chip"><b>Read it first</b><span>A skill is instructions to the AI. Open the zip and read SKILL.md first; it is plain text.</span></div>
</div>

<div class="foot"><span>By Mathieu Kessler &nbsp;·&nbsp; <b>kesslernity.com/store</b> &nbsp;·&nbsp; v1.0, Nov 2026</span><span>© 2026 Kesslernity &nbsp;·&nbsp; MIT license &nbsp;·&nbsp; Not affiliated with, or endorsed by, Microsoft</span></div>
</body></html>"""


# Chrome stamps the render time into every PDF, so an unchanged guide still produces
# different bytes on every build. These are committed, so that is 7.7 MB of identical-content
# churn per rebuild. Same fix as the zips in lint_skills.py: pin the clock.
#
# The replacement must be the SAME LENGTH. A PDF's cross-reference table holds byte offsets,
# so shortening a string by one character moves everything after it and corrupts the file.
PDF_EPOCH = b"D:19800101000000+00'00'"


def pin_pdf_dates(pdf):
    raw = pdf.read_bytes()
    fixed = re.sub(
        rb"/(CreationDate|ModDate)\s*\(([^)]*)\)",
        lambda m: b"/" + m.group(1) + b"(" + PDF_EPOCH.ljust(len(m.group(2)))[: len(m.group(2))] + b")"
        if len(m.group(2)) >= len(PDF_EPOCH)
        else m.group(0),
        raw,
    )
    if fixed != raw:
        pdf.write_bytes(fixed)


def pin_pdf_id(pdf):
    """pdfunite stamps a random /ID into the trailer on every run.

    All 28 pages are byte-identical build to build, but the bundle was not, so every rebuild
    produced a diff that looked like a content change and wasn't. That is worse than untidy:
    it means `git status` can no longer tell you whether a guide actually changed, which is
    the one question the reproducible build was there to answer.

    The two ID values are sixteen RANDOM bytes each, so they can contain "(", ")" or a
    backslash. Two earlier attempts failed on exactly those bytes. A regex plus a search for
    the closing "]" broke whenever a random byte was one of those characters. Walking the
    strings with PDF's escaping rules fixed the parse but not the churn, because preserving
    each file's own length faithfully preserves the difference: a byte that needs escaping
    makes the string seventeen bytes rather than sixteen, so two runs stayed two files.

    So the whole /ID array is replaced with one canonical value, not padded to match. That
    changes the trailer's length, which is safe here and only here: the trailer sits after
    the cross-reference table, and startxref points backwards at that table, so nothing in
    the file holds an offset that moves. pin_pdf_dates cannot take this liberty, which is
    why it is strict about length and this is not.
    """
    raw = pdf.read_bytes()
    start = raw.rfind(b"/ID")
    if start < 0:
        return
    i = raw.find(b"[", start)
    if i < 0:
        return
    i += 1

    spans = []
    for _ in range(2):
        while i < len(raw) and raw[i:i + 1] in b" \r\n\t":
            i += 1
        if raw[i:i + 1] != b"(":
            return
        depth, j = 0, i
        while j < len(raw):
            c = raw[j:j + 1]
            if c == b"\\":
                j += 2
                continue
            if c == b"(":
                depth += 1
            elif c == b")":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        else:
            return
        spans.append((i, j))
        i = j

    while i < len(raw) and raw[i:i + 1] in b" \r\n\t":
        i += 1
    if raw[i:i + 1] != b"]":
        return

    canonical = b"/ID [(" + b"0" * 16 + b") (" + b"0" * 16 + b")]"
    pinned = raw[:start] + canonical + raw[i + 1:]
    if pinned != raw:
        pdf.write_bytes(pinned)


def bot_facts(bot_dir):
    """Everything a guide page states about one bot, parsed once.

    The PDF and guides/catalogue.json both come from this, so the site cannot describe a bot
    differently from the bot's own one-pager. Adding a second parser on the website side is
    exactly how two surfaces start disagreeing about the same artifact.
    """
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
    never = bullets(section(body, "Boundaries"))
    if not never:
        sys.exit(f"{bot_dir.name}: no bullets under '## Boundaries'.")

    return {
        "slug": bot_dir.name,
        "title": title,
        "job": curly(job),
        "pack": pack,
        "packLabel": PACK_TITLES.get(pack, pack),
        "description": plain(fm.get("description", "")),
        "principle": curly(principle),
        "triggers": [curly(q) for q in TRIGGERS[bot_dir.name]],
        "outputs": [curly(t) for t in OUTPUTS[bot_dir.name]],
        "never": [curly(t) for t in never],
        "zipUrl": f"{RAW}/dist/{bot_dir.name}.zip",
        "guideUrl": f"{RAW}/guides/{bot_dir.name}.pdf",
        "repoUrl": f"https://{REPO}/tree/main/packs/{pack}/{bot_dir.name}/",
    }


def build_html(bot_dir):
    f = bot_facts(bot_dir)
    return PAGE.format(
        css=CSS,
        pack=E(f["packLabel"]),
        title=E(f["title"]),
        job=E(f["job"]),
        zip_url=f["zipUrl"],
        zip_name=f"{f['slug']}.zip",
        quotes="".join(f'<div class="q">“{E(q)}”</div>' for q in f["triggers"]),
        output="".join(f"<li>{E(t)}</li>" for t in f["outputs"]),
        never="".join(f"<li>{E(t)}</li>" for t in f["never"]),
        principle=E(f["principle"]),
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
    pages = ([("00-start-here", build_cover(bots)),
              ("01-for-the-admin", build_admin(bots)),
              ("02-for-the-ciso", build_ciso(bots)),
              ("03-for-the-cfo", build_cfo(bots))]
             + [(b.name, build_html(b)) for b in bots]
             + [("99-where-to-go-next", build_closer(bots))])
    worst, fails = None, []
    for name, markup in pages:
        h = BUILD / f"probe-{name}.html"
        h.write_text(markup.replace("</body>", PROBE), encoding="utf-8")
        dom = subprocess.run(
            [CHROME, "--headless", "--disable-gpu", "--dump-dom", "--window-size=794,1123",
             f"--user-data-dir={PROFILE}", "--virtual-time-budget=3000", h.as_uri()],
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
.pk {{ width: calc(25% - 2mm); background: #FFFFFF; border: 1.2px solid #E2E8F0;
      border-radius: 2.6mm; padding: 2.2mm 3mm; display: flex; justify-content: space-between;
      align-items: baseline; }}
.pk b {{ font-family: Georgia, serif; font-size: 10.4pt; }}
.pk span {{ font-size: 8.6pt; color: #64748B; }}
.band .line {{ font-size: 14.5pt; }}
.grab {{ margin-top: 3.7mm; background: #2563EB; border-radius: 3mm; text-decoration: none;
        padding: 3.8mm 5mm; display: flex; justify-content: space-between; align-items: baseline; }}
.grab .g1 {{ font-family: Georgia, serif; font-size: 13pt; color: #fff; }}
.grab .g2 {{ font-size: 10.6pt; color: #DBEAFE; font-weight: 700; }}
</style></head><body>
<div class="eyebrow">Microsoft 365 Copilot Cowork &nbsp;·&nbsp; <b>Start here</b> &nbsp;·&nbsp; Free, MIT license</div>
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
  <div class="card accent w33"><h2>Why these are safe to try</h2><p>Every bot is written to
    prepare and stop, and Cowork asks before it sends. Approve one action at a time. Cowork
    cannot delete anything in OneDrive or SharePoint at all.</p></div>
</div>

<div class="steps">{steps}</div>

<div class="say"><h2>What is in the box</h2><div class="packs">{packs}</div></div>

<div class="band"><span class="tag">The rule<br>they follow</span><span class="line">Silence is a
result. A bot that invents a finding to look busy teaches you to stop reading it.</span></div>

<div class="pre">
  <div class="chip"><b>You need</b><span>Microsoft 365 Copilot, and Cowork switched on by your admin. Off by default.</span></div>
  <div class="chip"><b>Desktop only</b><span>Cowork runs on mobile. Uploaded skills do not. Use a laptop.</span></div>
  <div class="chip"><b>It is metered</b><span>Cowork bills Copilot Credits as you use it. Your admin sets the policy.</span></div>
  <div class="chip"><b>Room for all of them</b><span>You can hold 50 skills. These {count} use under half.</span></div>
</div>

<a class="grab" href="{raw}"><span class="g1">Download them all, free</span><span class="g2">{repo} &nbsp;&#8595;</span></a>

<div class="foot"><span>By Mathieu Kessler &nbsp;·&nbsp; <b>kesslernity.com/store</b> &nbsp;·&nbsp; v1.0, Nov 2026, checked against Microsoft docs 4 Nov 2026</span><span>© 2026 Kesslernity &nbsp;·&nbsp; MIT license</span></div>
</body></html>"""

COVER_STEPS = [
    "Pick a bot and <b>download its file</b>",
    "Open <b>Customize</b>, left navigation",
    "Go to the <b>Skills</b> tab",
    "<b>Add</b> → <b>Upload skill</b>, pick the file",
    "Start a <b>new</b> chat and ask it for the job",
]


ROLE_PAGE = """<!doctype html><html><head><meta charset="utf-8"><style>{css}
.rrow {{ display: flex; gap: 4mm; margin-top: 3.7mm; align-items: stretch; }}
.rcol {{ flex: 1; display: flex; flex-direction: column; gap: 4mm; }}
.rlist li {{ font-size: 10.4pt; line-height: 1.42; margin-bottom: 2mm; }}
.kv {{ display: flex; gap: 4mm; align-items: baseline; margin-bottom: 2.2mm; }}
.kv b {{ width: 46mm; flex: none; font-size: 10pt; color: #0F172A; }}
.kv span {{ font-size: 10.2pt; line-height: 1.4; color: #334155; }}
.warnbox {{ margin-top: 3.7mm; background: #FEF2F2; border: 1.6px solid #DC2626;
           border-radius: 3mm; padding: 4mm 5mm; }}
.warnbox b {{ color: #B91C1C; }}
.warnbox p {{ font-size: 10.2pt; line-height: 1.42; color: #334155; }}
</style></head><body>
<div class="eyebrow">Microsoft 365 Copilot Cowork &nbsp;·&nbsp; <b>{role}</b> &nbsp;·&nbsp; Free, MIT license</div>
<h1>{headline}</h1>
<p class="job">{standfirst}</p>
{body}
<div class="foot"><span>By Mathieu Kessler &nbsp;·&nbsp; <b>kesslernity.com/store</b> &nbsp;·&nbsp; v1.0, Nov 2026, checked against Microsoft docs 4 Nov 2026</span><span>© 2026 Kesslernity &nbsp;·&nbsp; MIT license</span></div>
</body></html>"""


def _card(title, rows, accent=False):
    items = "".join(f"<li>{E(r)}</li>" for r in rows)
    cls = "card accent" if accent else "card"
    return f'<div class="{cls}" style="flex:1"><h2>{E(title)}</h2><ul class="rlist">{items}</ul></div>'


def build_admin(bots):
    """The prerequisites and rollout facts an end user does not need and an admin does."""
    body = f"""
<div class="rrow">
  {_card("Before anyone can open Cowork", [
      "A Microsoft 365 Copilot license for the user.",
      "Usage-based billing enabled in the tenant. Cowork is off until it is.",
      "A spending policy that selects Cowork: admin center, Copilot, Cost management.",
      "The user in scope of that policy. Cowork is limited to Anthropic-supported regions.",
  ])}
  {_card("The thing that catches people out", [
      "A spending policy is an access control, not only a budget.",
      "Any user in scope who selects Cowork can use it, however small the limit. One credit still grants access.",
      "To keep someone out, leave them out of every policy that selects Cowork. Do not lower their limit.",
      "Enforcement is asynchronous, so a cap is not an instant stop.",
  ], accent=True)}
</div>

<div class="rrow">
  {_card("Rolling these skills out", [
      "Each user uploads their own. There is no tenant-wide install for a custom skill.",
      "A user can hold 50 custom skills and 25 scheduled prompts. Skills are cheap; schedules are scarce.",
      "Per skill: SKILL.md up to 1 MB, up to 20 companion files, 10 MB total.",
      "Uploaded skills do not work on Cowork mobile. Cowork itself does.",
  ])}
  {_card("Test before you schedule", [
      "Upload one skill, run it once on a quiet week, and read the output before anyone schedules it.",
      "After editing references/config.md, start a NEW conversation. Changes apply to new sessions only.",
      "Automated task activity lands in the unified audit log; Purview policies apply.",
  ])}
</div>

<div class="warnbox">
  <b>Microsoft does not validate custom skills created by users.</b>
  <p>A skill runs as instructions to the AI, so treat an uploaded file the way you would treat a
  script. Read SKILL.md before you approve a skill for your organization. Everything in this
  catalog is plain text and readable in under two minutes.</p>
</div>
"""
    return ROLE_PAGE.format(css=CSS, role="For the Microsoft 365 admin",
                            headline="What you switch on, and what it costs you to switch on",
                            standfirst="Cowork is off by default and the way it is turned on changed at general availability. "
                                       "The old per-agent allow list is deprecated; access now comes from spending policy.",
                            body=body)


# Which skills read personal or HR data. Derived from the packs rather than typed,
# plus two finance skills whose inputs are personal spending.
SENSITIVE = {"one-to-one-prep", "interview-loop-coordinator", "onboarding-buddy",
             "internal-expert-finder", "expense-reconciliation", "subscription-hunter"}


def build_ciso(bots):
    sens = [b for b in bots if b.name in SENSITIVE]
    names = ", ".join(sorted(x.name.replace("-", " ") for x in sens))
    body = f"""
<div class="rrow">
  {_card("What a skill actually is", [
      "A plain-text Markdown file in the user's own OneDrive, at /Documents/Cowork/skills/.",
      "It contains instructions, not code. Nothing is executed.",
      "It runs as the user who invoked it and sees only what that user can see.",
      "It cannot reach local files, cannot read encrypted files, and cannot delete anything in OneDrive or SharePoint.",
  ])}
  {_card("Where the risk actually is", [
      "Microsoft does not validate custom skills created by users. A skill is instructions to the AI.",
      "Approval can be skipped: a user may approve and skip similar prompts for the rest of a session, scoped to a recipient, a domain, or always.",
      "Scheduled and event-driven tasks run with nobody watching, though they default to draft-and-approve.",
      "The only durable control is reading the file. Every one here is plain text.",
  ], accent=True)}
</div>

<div class="warnbox">
  <b>{len(sens)} of these {len(bots)} skills read personal or HR data.</b>
  <p>{E(names)}. Before anyone runs one of these against other people's data, clear it with HR,
  your works council and privacy. Sensitivity labels carry through to what Cowork produces, and
  the output lands in the user's own OneDrive.</p>
</div>

<div class="rrow">
  {_card("What this catalog commits to", [
      "Every skill reads and prepares, then stops. Sending, posting and deleting are not in any skill's instructions.",
      "Every output line cites the mail, file or meeting it came from. An unsourced line is a defect.",
      "No skill advises on safety authorisation: permit to work, lock-out tag-out, confined space, JSA, incident classification, inspection sign-off.",
      "Nothing is obfuscated, minified or compiled. MIT license, read it all.",
  ])}
  {_card("Questions worth asking before approval", [
      "Which mailbox, which site, which calendar does this read? It is written in the skill's Inputs section.",
      "What happens on a quiet period? Every skill here states its silent case.",
      "Who sees the output? The creating user only, unless they approve otherwise.",
      "What is in the audit log? Automated task activity is recorded alongside other Cowork activity.",
  ])}
</div>
"""
    return ROLE_PAGE.format(css=CSS, role="For the CISO",
                            headline="Instructions in a text file, running as the user",
                            standfirst="No code executes. The exposure is what the instructions tell the model to read, "
                                       "and whether anyone read the instructions first.",
                            body=body)


def build_cfo(bots):
    body = f"""
<div class="rrow">
  {_card("What this costs", [
      "These {n} skills cost nothing. MIT license, no purchase, no subscription, no email required.",
      "What costs money is Cowork itself, which bills Copilot Credits on usage.",
      "Model responses, tool and skill calls, image generation and browser tasks all consume credits.",
      "There is no per-skill fee. A skill is a text file; running it is what meters.",
  ])}
  {_card("Where the control sits", [
      "A spending policy in Microsoft 365 admin center, Copilot, Cost management.",
      "Limits can be set per tenant, per group or per user.",
      "That policy is also the access control. Any user in scope can use Cowork however small the limit.",
      "Enforcement is asynchronous, so treat a cap as a boundary, not a hard stop.",
  ], accent=True)}
</div>

<div class="rrow">
  {_card("What moves the number", [
      "Reasoning effort, which sits next to the model picker and defaults to Medium.",
      "Which model runs. Auto is the default and picks for the task.",
      "Scheduled prompts, because they run whether or not anyone needed them that week.",
      "Type /cost in a session to see usage so far.",
  ])}
  {_card("The budgeting mistake to avoid", [
      "A user can hold 50 custom skills but only 25 scheduled prompts.",
      "Skills are free to hold and cost nothing until invoked.",
      "Schedules are the recurring line, because each one runs on a clock regardless of need.",
      "Every skill here runs on demand by default. A schedule is opt-in, per skill.",
  ])}
</div>

<div class="warnbox">
  <b>The honest version of the business case.</b>
  <p>These skills remove preparation time, not decisions. Every one drafts and stops, which means
  a person still reads the output. Any saving that assumes nobody reviews the result is not a
  saving this catalog supports.</p>
</div>
"""
    return ROLE_PAGE.format(css=CSS, role="For the CFO",
                            headline="The skills are free. The runtime is metered.",
                            standfirst="Nothing here is a license purchase. The cost is Copilot Credits consumed when a "
                                       "skill runs, and the lever is the spending policy.",
                            body=body.replace("{n}", str(len(bots))))


def build_closer(bots):
    """Back page of the bundle only. The 23 individual guides stay clean artifacts
    somebody will forward; the ask lives here, once, at the end."""
    body = f"""
<div class="rrow">
  {_card("Everything in this pack", [
      f"{len(bots)} skills, free, MIT license. No purchase, no subscription, no email.",
      "One A4 page per skill, plus pages for the admin, the CISO and the CFO.",
      "kesslernity.com/cowork-bots for the browsable version and the downloads.",
      "github.com/kesslernity/awesome-copilot-cowork-bots for the source and the research notes.",
  ])}
  {_card("If this was useful", [
      "AI at Work, a biweekly briefing on getting this to land in a real organization.",
      "Verified facts, tested prompts, and what changed that quarter. Free.",
      "kesslernity.com/newsletter",
  ], accent=True)}
</div>

<div class="rrow">
  {_card("These are portable", [
      "A skill is a plain SKILL.md file: frontmatter, then instructions in Markdown.",
      "The prompt is the asset. The model behind it is a commodity.",
      "Cowork itself runs several model families and picks per task.",
      "The same file shape is read by other agents, so the thinking travels even if the runtime does not.",
  ])}
  {_card("When you want more than a free file", [
      "kesslernity.com/store carries the paid kits: rollout plans, governance checks, cost models.",
      "Written by the same practitioner, under the same rule: nothing claimed that is not verified.",
      "Nothing in this pack is a trial of anything. It is finished and it is yours.",
  ])}
</div>

<div class="warnbox" style="border-color:#2563EB;background:#EFF6FF">
  <b>One last thing, and it is the whole point.</b>
  <p>Every skill here prepares and stops. If you take nothing else from this pack, take the
  habit: write the boundary into the file, name the case where the right answer is silence, and
  make the output checkable in seconds. That works in any tool, including the one you build
  yourself. AI prepares, people decide.</p>
</div>
"""
    return ROLE_PAGE.format(css=CSS, role="Where to go next",
                            headline="That is the whole catalog",
                            standfirst="Free, finished, and not a funnel. If you want the paid work, it is one link away, "
                                       "and if you never click it the skills still work.",
                            body=body)


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
    pages = ([("00-start-here", build_cover(bots)),
              ("01-for-the-admin", build_admin(bots)),
              ("02-for-the-ciso", build_ciso(bots)),
              ("03-for-the-cfo", build_cfo(bots))] if not args.only else [])
    pages += [(b.name, build_html(b)) for b in bots]
    if not args.only:
        pages += [("99-where-to-go-next", build_closer(bots))]

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
             f"--print-to-pdf={pdf}", f"--user-data-dir={PROFILE}",
             "--virtual-time-budget=4000", h.as_uri()],
            check=True, capture_output=True,
        )
        pin_pdf_dates(pdf)
        made.append(pdf)

    if not args.html and not args.only:
        # One file to hand someone who wants the whole set. pdfunite ships with poppler,
        # which is already a dependency of the fit check's rendering workflow.
        bundle = OUT / "all-bots.pdf"
        bundle.unlink(missing_ok=True)
        subprocess.run(["pdfunite", *[str(p) for p in made], str(bundle)], check=True)
        pin_pdf_dates(bundle)
        pin_pdf_id(bundle)
        print(f"bundle: {bundle.relative_to(ROOT)} ({len(made)} pages)")

        # The same parse, as data. kesslernity.com builds its /cowork-bots page from this
        # rather than re-parsing SKILL.md in JavaScript, so the website and the PDF cannot
        # end up describing the same bot differently.
        cat = OUT / "catalogue.json"
        cat.write_text(
            json.dumps(
                {
                    "repo": f"https://{REPO}",
                    "generatedBy": "tools/build_guides.py",
                    "coverUrl": f"{RAW}/guides/00-start-here.pdf",
                    "bundleUrl": f"{RAW}/guides/all-bots.pdf",
                    "bots": [bot_facts(b) for b in bots],
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"data:   {cat.relative_to(ROOT)} ({len(bots)} bots)")

    shutil.rmtree(PROFILE, ignore_errors=True)
    print(f"{len(made)} {'HTML files' if args.html else 'PDFs'} written to "
          f"{(BUILD if args.html else OUT).relative_to(ROOT)}/")


if __name__ == "__main__":
    main()

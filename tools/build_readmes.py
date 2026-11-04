#!/usr/bin/env python3
"""Generate the pack READMEs and the root catalogue table from the skills on disk.

The brief's Phase 4 asks for a check that "the catalogue table in the root README matches the
folders on disk". The cheapest way to pass a check like that forever is to make the table
underivable by hand: it is generated here, between two markers, and `--check` fails if what is
committed differs from what the folders say.

That is not a theoretical preference. A sibling repo in this estate shipped a README claiming
"18 prompts" for a collection holding 28, and a site claiming 27 guides against 29 files, both
because a number was typed once and never retyped.

    python3 tools/build_readmes.py            # write
    python3 tools/build_readmes.py --check    # fail if the committed text is stale
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs"
README = ROOT / "README.md"

START = "<!-- CATALOGUE:start -->"
END = "<!-- CATALOGUE:end -->"

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

FM = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.S)


def front_matter(path):
    m = FM.match(path.read_text(encoding="utf-8"))
    if not m:
        return {}
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
    return {k: re.sub(r"\s+", " ", v).strip() for k, v in out.items()}


def first_sentence(text, limit=150):
    s = re.split(r"(?<=\.)\s", text)[0]
    return s if len(s) <= limit else text[:limit].rsplit(" ", 1)[0] + "…"


def collect():
    packs = {}
    for md in sorted(PACKS.glob("*/*/skill/SKILL.md")):
        bot = md.parent.parent
        pack = bot.parent.name
        fm = front_matter(md)
        packs.setdefault(pack, []).append(
            {"slug": bot.name, "desc": fm.get("description", ""), "name": fm.get("name", bot.name)}
        )
    return packs


def catalogue_table(packs):
    lines = []
    total = sum(len(v) for v in packs.values())
    lines.append(f"**{total} bots in {len(packs)} packs.** Every one ships as an upload-ready "
                 f"archive in `dist/`.\n")
    lines.append("| Pack | Bot | What it owns |")
    lines.append("|---|---|---|")
    for pack in sorted(packs, key=lambda p: list(PACK_TITLES).index(p) if p in PACK_TITLES else 99):
        title = PACK_TITLES.get(pack, pack)
        for i, bot in enumerate(sorted(packs[pack], key=lambda b: b["slug"])):
            cell = f"**{title}**" if i == 0 else ""
            link = f"[`{bot['slug']}`](packs/{pack}/{bot['slug']}/)"
            lines.append(f"| {cell} | {link} | {first_sentence(bot['desc'])} |")
    return "\n".join(lines)


def pack_readme(pack, bots):
    title = PACK_TITLES.get(pack, pack)
    out = [f"# {title}", ""]
    out.append(f"{len(bots)} bots. Generated from the skills on disk by `tools/build_readmes.py`; "
               f"do not edit by hand.")
    out.append("")
    out.append("| Bot | What it owns |")
    out.append("|---|---|")
    for bot in sorted(bots, key=lambda b: b["slug"]):
        out.append(f"| [`{bot['slug']}`]({bot['slug']}/) | {first_sentence(bot['desc'])} |")
    out.append("")
    out.append("## Installing this pack")
    out.append("")
    out.append(f"Each bot is a separate archive. Download the ones you want from `dist/`, then in "
               f"Cowork: **Customize** → **Skills** → the arrow next to **Add** → **Upload "
               f"skill**. Cowork validates each file and writes it to your OneDrive.")
    out.append("")
    out.append(f"This pack costs **{len(bots)} of your 50 custom skills**. Scheduling is optional "
               f"on every bot; each schedule you create costs one of your 25.")
    out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    packs = collect()
    if not packs:
        sys.exit("No skills found under packs/")

    stale = []

    for pack, bots in packs.items():
        path = PACKS / pack / "README.md"
        want = pack_readme(pack, bots)
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != want:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.write_text(want, encoding="utf-8")

    if README.exists():
        text = README.read_text(encoding="utf-8")
        if START in text and END in text:
            want_block = f"{START}\n{catalogue_table(packs)}\n{END}"
            new = re.sub(re.escape(START) + r".*?" + re.escape(END), want_block, text, flags=re.S)
            if args.check:
                if new != text:
                    stale.append("README.md catalogue table")
            else:
                README.write_text(new, encoding="utf-8")
        else:
            stale.append(f"README.md is missing the {START} / {END} markers")

    total = sum(len(v) for v in packs.values())
    print(f"{total} bots across {len(packs)} packs")

    if stale:
        print("\nSTALE, regenerate with python3 tools/build_readmes.py:", file=sys.stderr)
        for s in stale:
            print("  " + s, file=sys.stderr)
        sys.exit(1)
    print("Generated." if not args.check else "Up to date.")


if __name__ == "__main__":
    main()

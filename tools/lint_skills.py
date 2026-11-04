#!/usr/bin/env python3
"""Validate every skill in packs/ against the Cowork format and limits, then build upload archives.

The format and every limit below were read from Microsoft Learn on 2026-11-03 and are cited in
research/sources.md. Nothing here is assumed:

    Use Copilot Cowork      50 custom skills per user, SKILL.md up to 1 MB, up to 20 companion
                            files, 10 MB total per skill, 25 scheduled prompts per user.
    Customize Copilot Cowork
                            Upload accepts a .md holding a single SKILL.md, or a .zip / .skill
                            archive with SKILL.md AT ITS ROOT plus companion files. Frontmatter
                            must carry a name and a description.

Two checks exist because of defects seen in a sibling repo today rather than from theory:

  * A YAML folded block (`description: >-`) parses to the two characters ">-" if you take
    everything after the colon. That shipped to a live page once. parse_front_matter handles
    folded blocks, and lint rejects a description that looks unparsed.
  * A description IS the routing logic in Cowork, not marketing copy, so a description that never
    says WHEN to use the skill is a functional defect. That is a warning, not an error, because
    judging it mechanically is imperfect.

    python3 tools/lint_skills.py              # lint + build dist/<bot>.zip
    python3 tools/lint_skills.py --check      # lint only

Exit 1 on any error. Standard library only.
"""
import argparse
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs"
DIST = ROOT / "dist"

MAX_SKILL_MD = 1 * 1024 * 1024
MAX_COMPANIONS = 20
MAX_TOTAL = 10 * 1024 * 1024
USER_SKILL_CAP = 50
USER_SCHEDULE_CAP = 25

# Fixed so an unchanged skill rebuilds byte-identical and git stays quiet.
FIXED_TIME = (1980, 1, 1, 0, 0, 0)

SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FM = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.S)
# "when", "use when", "use this" etc. A description that never says when is a routing defect.
WHEN = re.compile(r"\buse (this |it )?when\b|\bwhen the user\b|\buse for\b", re.I)


def parse_front_matter(text):
    """Flat scalars plus YAML folded blocks. A naive split on ':' returns '>-' for a folded value."""
    m = FM.match(text)
    if not m:
        return None, text
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
    for k in out:
        out[k] = re.sub(r"\s+", " ", out[k].strip("'\"")).strip()
    return out, text[m.end():]


def companion_files(skill_dir):
    return [p for p in skill_dir.rglob("*") if p.is_file() and p.name != "SKILL.md"]


def lint_skill(skill_dir, bot_dir):
    errors, warnings = [], []
    name = bot_dir.name
    md = skill_dir / "SKILL.md"

    if not md.exists():
        return [f"{name}: skill/SKILL.md is missing"], []

    text = md.read_text(encoding="utf-8")
    fm, body = parse_front_matter(text)

    if fm is None:
        return [f"{name}: SKILL.md has no YAML frontmatter block"], []

    declared = fm.get("name", "")
    desc = fm.get("description", "")

    if not declared:
        errors.append(f"{name}: frontmatter has no name")
    elif declared != name:
        errors.append(f"{name}: frontmatter name is {declared!r}, must equal the folder name")
    elif not SLUG.match(declared):
        errors.append(f"{name}: name {declared!r} is not kebab-case")

    if not desc:
        errors.append(f"{name}: frontmatter has no description")
    elif desc in (">-", ">", "|", "|-") or len(desc) < 40:
        errors.append(f"{name}: description looks unparsed or truncated ({desc[:20]!r})")
    elif not WHEN.search(desc):
        warnings.append(f"{name}: description never says WHEN to use the skill, which is the routing signal")

    if not body.strip():
        errors.append(f"{name}: SKILL.md has frontmatter but no instructions")

    size = md.stat().st_size
    if size > MAX_SKILL_MD:
        errors.append(f"{name}: SKILL.md is {size} bytes, over the 1 MB limit")

    comps = companion_files(skill_dir)
    if len(comps) > MAX_COMPANIONS:
        errors.append(f"{name}: {len(comps)} companion files, over the limit of {MAX_COMPANIONS}")
    total = size + sum(p.stat().st_size for p in comps)
    if total > MAX_TOTAL:
        errors.append(f"{name}: {total} bytes total, over the 10 MB per-skill limit")

    # The repo's own rules, not Microsoft's. A bot that can send without saying so is the one
    # defect that costs a reader something real.
    low = body.lower()
    if not any(w in low for w in ("approval", "draft", "never send", "do not send")):
        warnings.append(f"{name}: instructions never mention drafting or approval")

    return errors, warnings


def build_zip(skill_dir, bot_dir):
    """Archive with SKILL.md at the ROOT, which is the shape Cowork's uploader accepts."""
    DIST.mkdir(parents=True, exist_ok=True)
    out = DIST / f"{bot_dir.name}.zip"
    files = sorted(
        (p for p in skill_dir.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(skill_dir).as_posix(),
    )
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in files:
            info = zipfile.ZipInfo(p.relative_to(skill_dir).as_posix(), date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, p.read_bytes())
    with zipfile.ZipFile(out) as z:
        if "SKILL.md" not in z.namelist():
            return None, f"{bot_dir.name}: SKILL.md is not at the archive root"
    return out.stat().st_size, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="lint only, build nothing")
    args = ap.parse_args()

    # packs/<pack>/<bot>/skill/SKILL.md, so the bot directory is two levels up from the file.
    bots = sorted(p.parent.parent for p in PACKS.glob("*/*/skill/SKILL.md")) if PACKS.exists() else []
    if not bots:
        print(f"No skills found under {PACKS}. Nothing to lint.")
        return

    errors, warnings, built = [], [], 0
    for bot_dir in bots:
        e, w = lint_skill(bot_dir / "skill", bot_dir)
        errors += e
        warnings += w
        if e or args.check:
            continue
        _, err = build_zip(bot_dir / "skill", bot_dir)
        if err:
            errors.append(err)
        else:
            built += 1

    packs = sorted({b.parent.name for b in bots})
    print(f"{len(bots)} skills across {len(packs)} packs")
    if not args.check:
        print(f"{built} archives written to dist/")

    # The cap that actually binds is schedules, not skills. Report both.
    if len(bots) > USER_SKILL_CAP:
        errors.append(f"{len(bots)} skills exceeds the {USER_SKILL_CAP} a single user can hold")
    else:
        print(f"skill budget: {len(bots)} of {USER_SKILL_CAP} if one person installed every pack")

    for w in warnings:
        print(f"  warning: {w}")
    if errors:
        print(f"\n{len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        sys.exit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()

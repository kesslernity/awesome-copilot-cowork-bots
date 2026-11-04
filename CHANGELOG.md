# Changelog

## 2026-11-04

First build. 23 bots in 8 packs.

**Research.** Thirteen vendor pages fetched and cited in `research/sources.md`, every claim
carrying an access date. Two findings changed the plan: the custom skill cap is **50, not 20**
(20 is the companion-file limit), and the design source is reached through X and Cursor plans and
runs on **Cursor-operated infrastructure**, so attribution names both.

**Scope.** Four of the seven published Grok Bot roles do not port and are documented as such with
the right alternative tool. Nine candidates were cut because Microsoft already ships them in the
Legal, Sales, Service and Education plugins. Nine more were cut as duplicates of skills already
live in `awesome-copilot-cowork-skills`, including inbox triage, meeting prep and
transcript-to-actions.

**Tooling.** `lint_skills.py` validates against the published limits and builds one upload-ready
archive per bot with `SKILL.md` at the root. `build_readmes.py` generates the pack READMEs and the
root catalogue table, with a `--check` mode that fails when the committed text drifts from the
folders on disk.

**Not shipped.** An AEO tracker. The idea assumed Deep Research can read ChatGPT, Gemini and
Perplexity answers, which no fetched documentation supports. `brand-answer-monitor` ships the
honest version, tracking what the open web says, and says so on its own card.

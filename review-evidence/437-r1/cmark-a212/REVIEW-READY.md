[A212] REVIEW READY

Commit: `196cb7d99cb06631df514715979a5f82fbb1f7aa`
Tree: `796c734682c7d7dc5c26fd9a92090a3c4a35fc32`

- Branch `437-cmark-gfm`, clean, local only, not pushed.
- Base: dev `759da623072358afdb0e9d570a7b4b6a788492c9`.
- Three commits, each a one-line subject with no trailer: `35cebcf8`, `f91607db`, `196cb7d9`.
- Closes #437 and #516 per the [owner decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5798044806). The material decision is in [TAKEN](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5800875179).

Changed:
- **`scripts/gen_toc.py`** no longer parses Markdown.
  - `blocks()`, `line_kinds()` and `headings()` read cmark-gfm's syntax tree: kinds, source lines, levels, fences, and raw HTML and code literals, containers included.
  - They also read an HTML5 parse of cmark-gfm's own HTML. A heading is listed only when that parse keeps its element; this hides the #516 family, open quoted values and `<select>`.
  - An ATX label is still read off its own line, so labels and anchors are unchanged.
- **`scripts/gen_toc_renderer.py`** (new) is the pinned binding: `cmarkgfm` 2025.10.22 carrying cmark-gfm 0.29.0.gfm.13, and `html5lib` 1.1.
  - It reads the node calls the extension exports.
  - Positions are written unquoted and the `dom` builder is used; both choices were measured.
  - Another release is refused by name.
- **`tools/markdown/requirements.txt`** (new) pins six distributions exactly, with the sha256 of each wheel the hosted runner (CPython 3.12) and this host (3.14) need, and no sdist.
- **`docs.yml`** adds a cache step keyed by `hashFiles` of the lock and an install step with `--require-hashes`; `ci_events.py` pins both.
- **`check_em_dash.py`** answers rc 2 without the renderer, and runs 275 real-Git shape rows.
- **Deleted:** the class table, every block expression, the state machines, and `gen_toc_guards.py` with its 24 decision-site arms.
  - Every existing case is kept and judged by the renderer. The 42 it answers differently are converted and tagged, each with GitHub's rendering of its page.
  - `gen_toc_renderer_cases.py` adds 39 property arms.
  - `gen_toc_shapes.json` and `gen_toc_shape_cases.py` hold 352 shapes with GitHub renderings recorded 2026-09-23 through `gh api` (gfm mode, exact request and response bytes with SHA-256).
- **Docs:** CONTRIBUTING.md 6.1, DOC_GENERATION.md and RUNNING_TESTS.md.

Validation (all at the head, exit 0):
- 72 `docs.yml` gate commands, including:
  - `gen_toc.py --selftest` 1433/1433 (floor 707 to 1433), `--check` 106 pages, `--verify-anchors` 147;
  - `check_em_dash.py --selftest` 332 arms, and `--base 759da623`: 0 findings over 75 lines;
  - docs_check, doc style, doc paths, bare-metal, `ci_events.py --check` and `--selftest`, `act_ci.py --selftest`;
  - `check_py_idiom.py` (long module 10 ≤ 10, long function 9 ≤ 9) and every `check_*`/`measure_*` in the job.
- The gates also run:
  - without submodules;
  - with no git metadata;
  - under CPython 3.12.
- They refuse with rc 2 when the renderer is missing or drifted.
- 30 named mutations are all killed at arms named for their property.
- GitHub renderings:
  - 352 shapes and 700 seeded fuzz pages: the renderer agrees with gfm mode on every heading, apart from finding N1;
  - 0 regressions against the base walk: 221 and 249 agree at both, 131 and 451 fixed.

| Acceptance | Result | Evidence |
|---|---|---|
| 1 (restated, amended) | Met by construction | 352/352 shapes agree with their recorded gfm rendering. The family-one grid, the two-digit boundary, six boundaries, nine R86-5 mappings and the twelve #516 variants (six fixed, six kept) are held by coverage arms. Every shape that agreed at the base still agrees |
| 2 | Met: listed | Five family-two forms are listed. Their anchors equal GitHub's file-view ids (`markdown` mode): `alpha`, `text`, `text`, `q`, `inner` |
| 3 | Met | 30/30 mutations killed at named arms; 13 are also killed through the em-dash consumer |
| 4 | Met for navigation; label differences flagged | 164 tracked pages: refusals, existing block, ownership and generated block are identical, and `--write` changes no file on the base or head tree. Family two adds headings on 6 pages (5 frozen history pages without Contents, and one h3 outside its plan). Line labels differ on 11 pages where the old walk misread container content or pipe lines; each is enumerated with a GitHub-rendered reproduction. The criterion names only family two, so this needs reviewer judgement |
| 5 | Met | Gates as above; no ratchet widened; no budget file changed |

Findings, parser against GitHub:
- **N1.** GitHub's gfm output adds a visually hidden `Footnotes` h2 to a page with a referenced footnote. The pinned cmark-gfm emits none, so the heading is withheld and held as `github_only` in the fixture. No tracked page references a footnote.
- **N2.** GitHub's file rendering (API `markdown` mode) parses `<?`, `<select>` and `<xmp>` differently from gfm mode. That is 8 of 1,052 measured pages: 2 escapes, 4 withholds and 2 text differences relative to the file view. No tracked page is reached. Stated in 6.1. Which mode is the oracle is an owner decision.
- **N3 (pre-existing).** The anchor rule reads raw Markdown, so inline raw HTML in a heading anchors differently. An empty heading has no GitHub id.

Open risks/questions:
- The AC4 wording (above).
- The N2 oracle choice.
- Live dev moved to `26d855a9`. The paths are disjoint, and a scratch merge passes the TOC and em-dash gates; candidate validation stays with the manager.
- Out of scope and not fixed: REGISTER_MAP.md:355-359 and MILAN_V12_ROADMAP.md:135 render table rows as paragraph text on GitHub today.

The author packet holds HANDOFF, PR-BODY, COMMANDS, receipts, reproduction scripts, the render cache and MANIFEST. The manager owns the push, the PR (which supersedes #515), act and hosted contexts, and the candidate. R237 and R238 review cold. This author did no push, PR operation, merge or delegation. Stopping at this head.

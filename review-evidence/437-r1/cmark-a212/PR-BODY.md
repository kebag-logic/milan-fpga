[A212] Read Contents navigation from cmark-gfm, the renderer GitHub uses

Closes #437
Closes #516

This follows the owner decision of 2026-09-23 17:45 ([#437 comment 5798044806](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5798044806)): the Contents walk's hand-written block and container classification is replaced by the renderer GitHub itself uses, pinned and hash-locked in the docs gates. The takeover and material decision are at [5800875179](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5800875179).

- Head `196cb7d99cb06631df514715979a5f82fbb1f7aa`.
- Base dev `759da623072358afdb0e9d570a7b4b6a788492c9`.
- Three one-line commits with no trailers.

## What changes

- **`scripts/gen_toc.py` no longer parses Markdown.**
  - `blocks()`, `line_kinds()` and `headings()` read one page model, built from cmark-gfm's syntax tree: block kinds, source lines, heading levels, fences, and raw HTML and code literals, containers included.
  - The model also reads an HTML5 parse of cmark-gfm's own HTML, so a heading is listed only when GitHub would keep it. This is how the #516 family is hidden: a heading after a raw `<!--` the page leaves open, inside an open quoted value, or inside a `<select>`.
  - An ATX label is still read off its own line, so every existing label and anchor is unchanged.
- **`scripts/gen_toc_renderer.py` (new): the binding.**
  - `cmarkgfm` 2025.10.22, which carries cmark-gfm 0.29.0.gfm.13, read through the node calls its extension exports.
  - `html5lib` 1.1 for the HTML parse.
  - Another release is refused by name.
- **`tools/markdown/requirements.txt` (new).** Every distribution is pinned to one version, with the sha256 of each wheel the hosted runner (CPython 3.12) and the recording host (CPython 3.14) install, and no sdist.
- **`.github/workflows/docs.yml`.** It caches pip downloads keyed by the lock file and installs the lock with `--require-hashes` before the first consumer. `scripts/ci_events.py` pins both steps.
- **`scripts/check_em_dash.py`.** Navigation provenance follows automatically. Without the renderer the gate answers `cannot judge` (rc 2). Its selftest adds a real-Git row per recorded shape.
- **Deleted:** the class table, every block expression, the paragraph, comment and closer state machines, and `scripts/gen_toc_guards.py` with its decision-site arms. Every existing case is kept and judged by the renderer. The 42 it answers differently from the old walk are converted, and each converted page carries GitHub's rendering in the fixture.
- **`scripts/gen_toc_shapes.json` (new): 352 pages** with GitHub's `POST /markdown` gfm rendering, recorded 2026-09-23 through `gh api` as exact request and response bytes with SHA-256. The set covers:
  - family one, and the content-column cases;
  - the twelve #516 variants;
  - every shape the R237 and R238 reviews on PR #515 published;
  - family two;
  - every converted arm;
  - reproductions of every tracked-page difference.
  
  `scripts/gen_toc_shape_cases.py` checks each receipt and requires the renderer's headings to equal GitHub's.
- **CONTRIBUTING.md 6.1, docs/DOC_GENERATION.md and docs/testing/RUNNING_TESTS.md** state the basis, the install and the measured limits.

## Acceptance (#437; #516 closes with it)

| # | Result | Evidence |
|---|---|---|
| 1 | Met by construction | 352/352 shapes agree with their recorded gfm rendering; two carry GitHub's hidden footnote label, finding N1. The family-one grid, the two-digit boundary, the six agreeing boundaries, nine R86-5 mappings and the twelve #516 variants are held by coverage arms. Against the base walk: 0 regressions (221 agree at both, 131 fixed). All twelve #516 variants agree |
| 2 | Met: listed | The five family-two forms are listed. Their anchors equal GitHub's own file-view ids: `alpha`, `text`, `text`, `q`, `inner` |
| 3 | Met | 30 named mutations, each killed by the TOC selftest at an arm named for its property; 13 are also killed by the em-dash selftest |
| 4 | Met for navigation; line labels flagged | All 164 pages: refusals, existing block, ownership and generated block are identical under both walks, and `--write` changes no file. Family two adds headings on 6 pages (5 frozen history pages that own no Contents, and one h3 outside its page's plan). Line labels differ on 11 pages where the old walk misread container content or pipe lines, each enumerated with a GitHub-rendered reproduction |
| 5 | Met | 72 `docs.yml` gate commands exit 0 at the head; TOC selftest 1433/1433 (floor 707 to 1433); em-dash 332 arms; no ratchet widened; no budget file changed |

## Findings (parser against GitHub), reported

- **N1.** GitHub's gfm output opens a referenced footnote's section with a visually hidden `Footnotes` h2, which the pinned cmark-gfm does not emit. It is withheld and held as `github_only` in the fixture. No tracked page references a footnote.
- **N2.** GitHub's file rendering (API `markdown` mode) parses some raw HTML differently from its gfm mode: `<?`, `<select>` and `<xmp>`, on 8 of 1,052 measured pages.
  - Relative to the file view: 2 escapes (a processing instruction carrying `<!--`), 4 withholds and 2 text differences.
  - No tracked page carries these as raw HTML. Stated in 6.1.
  - Whether file rendering should be the oracle is an owner decision.
- **N3 (pre-existing).** The anchor rule reads raw Markdown, so inline raw HTML in a heading anchors differently. An empty heading has no GitHub id.

Observed and not fixed (out of scope): docs/reference/REGISTER_MAP.md:355-359 and docs/MILAN_V12_ROADMAP.md:135 render table rows as paragraph text on GitHub.

## Validation

- **Constraints.** The gates run without submodules (a clone with none initialised), with no git metadata (`docs_check`, `check_feature_status`), and on CPython 3.12. They refuse with rc 2 when the renderer is missing or drifted.
- **Fuzz.** 700 seeded pages rendered through GitHub: the renderer agrees with gfm mode on all 700, with 0 regressions against the base.
- **Candidate.** A scratch merge with live dev `26d855a9` (paths disjoint) passes the TOC and em-dash gates.

Receipts, reproduction scripts and the render cache are in the author packet: HANDOFF, COMMANDS, MANIFEST.

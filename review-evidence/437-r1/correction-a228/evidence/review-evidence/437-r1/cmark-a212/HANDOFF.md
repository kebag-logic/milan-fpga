# A212 handoff: #437 and #516, the Contents walk read from cmark-gfm

- Branch `437-cmark-gfm`, local only, not pushed. Clean tree and index.
- Head `196cb7d99cb06631df514715979a5f82fbb1f7aa`, tree `796c734682c7d7dc5c26fd9a92090a3c4a35fc32`.
- Base: dev `759da623072358afdb0e9d570a7b4b6a788492c9`. Live dev has since moved to `26d855a9` (see Open items).
- Three commits, each a one-line subject with no trailer:
  - `35cebcf8` Pin the Markdown renderer GitHub uses and install it hash-locked in the docs gates
  - `f91607db` Read Contents headings and line kinds from cmark-gfm and an HTML5 parse, retiring the hand-written walk
  - `196cb7d9` State the measured differences between GitHub's file rendering and the gfm renderings the walk is judged on
- Authority: owner decision [5798044806](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5798044806); assignment [5800600405](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5800600405); #437 body (acceptance 1 restated and amended); #516 body and [5798045125](https://github.com/kebag-logic/milan-fpga/issues/516#issuecomment-5798045125); AGENTS.md 4, 6 and 7; CONTRIBUTING.md 6.1; REQ-VER-04.
- Takeover and material decision: [5800875179](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5800875179). REVIEW READY: [5802079096](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5802079096).

## What changed

**The walk.** `scripts/gen_toc.py` no longer classifies Markdown.

- `blocks()`, `line_kinds()` and `headings()` read one page model, `_page()`. It is built from:
  - cmark-gfm's syntax tree: block kind, source lines and columns, heading level, the fenced flag, and raw HTML and code literals;
  - an HTML5 parse of cmark-gfm's own HTML, which carries each block's source position.
- A heading is listed only when its element survives that parse.
  - This is how GitHub hides a heading after a raw `<!--` it leaves open (#516), or inside an open quoted attribute value or a `<select>`.
  - Headings are listed in rendered order.
- An ATX label is read off its own line with CommonMark 4.2's content rule (`_atx_text`), so every existing label and anchor is byte-identical.
- A setext label is its rendered text; its line break reads as a space in the label.

**Deleted as obsolete:**

- The character-class table and all block expressions.
- The paragraph, comment, fence and closer state machines.
- The decision-site enumerator `scripts/gen_toc_guards.py`, its 24 guard arms, and `--sites`.

**Kept:** the TOC output contract, `TOC_ENTRY_RE`, the anchor rule, provenance (`generated_block`), ownership, the 26-character refusal policy (its reason restated), exemptions and budgets.

**`scripts/gen_toc_renderer.py` (new)** is the pinned binding.

- It loads `cmarkgfm` and `html5lib` and refuses another release by name, including another bundled cmark-gfm.
- It declares the node calls it reads and calls them on the same extension library: the binding's Python surface only parses and renders, but its extension exports the whole C API.
- It renders with GitHub's extensions (table, strikethrough, autolink, tagfilter, tasklist), raw HTML kept and footnotes on.
- It writes cmark-gfm's position attributes unquoted before the HTML parse. Quoted, they closed a raw value GitHub leaves open (measured).
- It reads with html5lib's `dom` builder. The `etree` builder drops foster-parented nodes from a fragment, which GitHub keeps (measured).
- A page that spells the position attribute renders nothing: a withholding limit, stated.

**`tools/markdown/requirements.txt` (new)**, installed with `--require-hashes`:

- Pins `cmarkgfm==2025.10.22` (cmark-gfm `0.29.0.gfm.13`), `cffi==2.1.1`, `pycparser==3.0`, `html5lib==1.1`, `six==1.17.0` and `webencodings==0.6.1`.
- Carries one sha256 per wheel for CPython 3.12 x86_64 (the hosted runner) and 3.14 x86_64 (this host), and no sdist.

**`.github/workflows/docs.yml`** gains two steps after the pyyaml install:

- `Cache the pinned Markdown renderer downloads`: `actions/cache@v4`, keyed by `hashFiles('tools/markdown/requirements.txt')`.
- `Install the pinned Markdown renderer`: `pip install --cache-dir ... --require-hashes -r tools/markdown/requirements.txt`.

`scripts/ci_events.py` pins both steps in `CARRIER_STEP_LISTS`. Its hard-coded docs-check step counts move from 47 to 49, and two position arms move by two.

**`scripts/check_em_dash.py`:**

- A missing or drifted renderer is `cannot judge` (rc 2), never a verdict.
- The selftest adds one real-Git row per recorded shape that carries a single `## Old` line: 275 rows.

**Case tables:**

- `scripts/gen_toc_cases.py`: every arm kept and judged by the renderer. 42 arms the renderer answers differently were converted, each tagged `(renderer)` where its expectation changed, with its page's GitHub rendering in the fixture:
  - 21 tag arms and 8 walk arms: the blank line that ends a type-6/7 block is no longer labelled with it;
  - 3 comment arms: an arrow written as Markdown text closes nothing on GitHub;
  - 8 predecessor rows: setext, indented and empty ATX headings are now listed;
  - 2 I440 CR arms: CRLF closes the fence, as on GitHub.
  - The guard family loses the decision-site arms and gains the pin arms.
- `scripts/gen_toc_renderer_cases.py` (new, split for the long-module ratchet): 13 walk, 16 heading and 10 pin arms, one per new property.
- `scripts/gen_toc_shape_cases.py` and `scripts/gen_toc_shapes.json` (new): the committed shape set, 352 pages, each with GitHub's recorded gfm rendering. Per shape there are two arms: receipt integrity, and `rendered_headings(page)` equal to GitHub's headings. Seven coverage arms spell acceptance 1's grid, the nine R86-5 mappings, the twelve #516 variants, and the one measured disagreement.
- `MIN_ARMS` rises from 707 to 1433. `scripts/gen_toc_closer_cases.py`: the CR arms.

**Docs:**

- CONTRIBUTING.md 6.1 gains the basis, the install, the three withholding limits, and the measured file-rendering difference.
- `docs/DOC_GENERATION.md`: the renderer section replaces the #440 closer notes, and the gate list asks for the lock.
- `docs/testing/RUNNING_TESTS.md`: the install line.

## Acceptance

| # | Criterion | Result | Evidence |
|---|---|---|---|
| 1 | Restated and amended: shape set committed with GitHub gfm renderings recorded at the fix's head; bullet, ordered and two-digit items at and past the content column with inline and unknown tags; the agreeing boundaries; nine R86-5 mappings; every shape agrees; every shape that agreed at the base still agrees | Met, by construction | `scripts/gen_toc_shapes.json`, 352 shapes rendered 2026-09-23 through `gh api` (`POST /markdown`, mode gfm). The selftest renders each with the pinned parser and requires GitHub's headings: 352/352 pass. Two of them carry GitHub's hidden footnote label as `github_only` (finding N1). Coverage arms hold the family-one grid (51 shapes), the two-digit below-column boundary, the six boundaries, nine `r86_5` mappings and the twelve #516 variants. Three-way (base walk / renderer / GitHub): 221 agree at both, 131 fixed, 0 regressed, 0 wrong at both. All twelve #516 variants agree: six fixed, six kept |
| 2 | Five family-two shapes listed with the renderer's anchors, or named as limits | Met: listed | Setext `===`, `---` and `-`, a block-quote heading and a list-item heading are listed. Their anchors equal GitHub's own file-view ids (`markdown` mode renders `id="user-content-…"`): `alpha`, `text`, `text`, `q`, `inner` (`family-two-anchors.json`) |
| 3 | Each new property has an arm that fails when removed | Met | 30 named mutations, all killed by the TOC selftest at arms named for the property; 13 are also killed by the em-dash selftest (`mutations-final.json`) |
| 4 | Per-page classification unchanged except where family two adds a heading, difference enumerated | Met for navigation; line labels differ on 11 pages, enumerated below, needing reviewer judgement | Identical on all 164 tracked pages under both walks, on the base tree, the head tree and a scratch candidate with live dev: refusals, existing block, ownership and generated block. `gen_toc.py --write` writes 0 pages on either tree. Family two adds headings on 6 pages (table below). Labels and line kinds differ on 11 pages where the old walk misread container content or pipe lines |
| 5 | Selftests, `--check`, `--verify-anchors`, em-dash selftest and documentation gates pass; no ratchet widened | Met | 72 gate commands from `docs.yml` exit 0 at the head (`gates/EXITS.txt`). TOC selftest 1433/1433; `--check` 106 pages; `--verify-anchors` 147; em-dash selftest 332 arms; `--base 759da623` 0 findings over 75 added lines. Python idiom: long module 10 ≤ 10, long function 9 ≤ 9, parameters 7 ≤ 7. No budget file changed; `MIN_ARMS` only rises |

## AC4 enumeration: every tracked page the two walks classify differently

The same 16 pages on the base tree, the head tree and the candidate tree. "Old" is dev 759da623's walk.

| Page | Difference (old to renderer) | Why, as GitHub renders it | Shape that shows it |
|---|---|---|---|
| CONTRIBUTING.md | 320-328 indented code to fence and prose | a fence five columns in, inside a nested list item | corpus: fence in a nested list item |
| CONTRIBUTING.md (head tree only) | 582-666 comment to prose | the old walk opens a comment at the `` `<!--` `` code span in the new 6.1 text | R237-2 F2 row 8; comment: code span arrow closes nothing |
| QUICKSTART.md | 24-28 prose to fence | a fence inside a block quote | corpus: fence in a block quote |
| docs/design/SAVED_STATE_MATERIALIZATION.md | 336-339 indented code to prose | a paragraph four columns into a nested item | corpus: paragraph four columns into a nested item |
| docs/testing/CI_WORKFLOWS.md | 120 lines from 509, indented code to prose | the same | the same |
| docs/history/v1/design/TIME_SYNC.md | 477 indented code to prose; 495 table row to prose | a blank line after indented code is not code; a pipe-led paragraph line is no table | corpus: blank line after indented code; pipe-led line inside a paragraph |
| tb/verilator/gptp_txts/README.md | 80, 87 indented code to prose | a blank line after indented code | corpus: blank line after indented code |
| docs/design/SAVED_STATE_FASTCONNECT.md | 19 kinds, prose to table row | tables inside block quotes | corpus: table in a block quote |
| docs/limitations/TROUBLESHOOTING.md | 11 kinds, prose to table row | the same | the same |
| docs/reference/REGISTER_MAP.md | 355-359 table row to prose | rows after a blank line are a paragraph | corpus: pipe row after a blank line is no table row |
| docs/MILAN_V12_ROADMAP.md | 135 table row to prose | a row after comment lines is a paragraph | corpus: pipe row after a comment line is no table row |
| docs/testing/TESTING.md | adds h3 in a block quote (family two; its plan lists h2 only, unchanged); 605 table row to prose | family two; a pipe-led line | family two: heading in a block quote |
| docs/history/v1/SPEC_TRACEABILITY.md | adds h2 in a block quote; plan gains it | family two; the page owns no Contents (`owns()` false) | corpus: heading two in a block quote |
| docs/history/v1/reference/MILAN_V12_DEPENDENCY_MATRIX.md | the same | the same | the same |
| docs/history/v1/testing/MILAN_COMPLIANCE_MATRIX.md | the same | the same | the same |
| docs/history/v1/testing/PDU_GETTER_SETTER_VERIFICATION.md | the same | the same | the same |
| docs/history/v1/testing/PROTOCOL_SWEEP_PLAN.md | the same | the same | the same |

**Contents blocks:** no file changed. Every block regenerates byte-identical on the base tree and on the head tree.

**Line labels:** the differences change only the wording of an em-dash finding on such a line (for example "added table row" for "added prose line"). They change no navigation, provenance or exemption. The criterion's literal clause names only family-two headings, so this is flagged for reviewer and owner judgement rather than claimed as met.

## Findings (parser against GitHub), reported and not papered over

**N1. GitHub's hidden footnote label.**

- A page with a referenced footnote renders on GitHub (gfm) with `<h2 id="footnote-label" class="sr-only">Footnotes</h2>`. The pinned cmark-gfm 0.29.0.gfm.13 emits none, so the walk lists no such heading.
- Direction: withholding of a visually hidden, non-section heading.
- Held as `github_only` on the two affected shapes, with an arm that spells it.
- Reach: no tracked page references a footnote. The `markdown` mode (file view) has no such heading either.

**N2. GitHub's file rendering differs from gfm mode.**

- The Markdown API's `markdown` mode renders "just like README.md files" and parses some raw HTML differently from its `gfm` mode.
- Over the 352 shapes and 700 fuzz pages it differs from the renderer, which follows gfm mode, on 8 pages. All involve `<?`, `<select>` or `<xmp>`:
  - 2 escapes relative to the file view: a processing instruction carrying `<!--`;
  - 4 withholds;
  - 2 heading-text differences.
- Reach: no tracked page carries these as raw HTML.
- Stated in CONTRIBUTING.md 6.1. Whether acceptance should be judged against file rendering instead of gfm mode is an owner decision.

**N3. Pre-existing, unchanged anchor behaviour.**

- The anchor rule reads raw Markdown, so a heading carrying inline raw HTML anchors differently from GitHub (R237-3 E8: GitHub `a--`, walk `a-p-----`).
- GitHub gives an empty heading no id, where the walk gives `""`. A bare `##` is now listed as an empty heading, as `# ` already was.
- Otherwise every anchor on the 352 shapes and on all 694 fuzz pages whose headings agree equals GitHub's file-view id.

**Observed, out of scope, not fixed:** two tracked pages render table rows as paragraph text on GitHub today.

- docs/reference/REGISTER_MAP.md:355-359: a blank line splits the table.
- docs/MILAN_V12_ROADMAP.md:135: comment markers split the table.

These look worth an Issue; the manager decides.

## Prior findings on PR #515, re-judged against the renderer

Every page those reports published is in the fixture and agrees with its GitHub rendering, including those given as descriptions and reconstructed. This covers:

- R237-r1 F1 (the 15-row tag matrix), F2 (family one, nine R86-5 mappings) and F3 (3 marker shapes);
- R238-r1 C01-C08, D01-D07, P01-P04 and F09;
- R237-2 F1 (3), F2 (10), F3 (2) and S1 (2);
- R237-3 E1-E12 and Q1;
- R238-2 (a)-(d) (17), C17, H06, H10, `<select>` and the link destination;
- R237-4 F1 (5) and its F3 pages;
- R238-3 T2-T8, the six definition forms and M21.

The hand-written emulation those findings were raised against is deleted.

## Open items

- **Live dev.** It moved to `26d855a9` (#528). The path intersection with this lane is empty. A scratch merge passes the TOC selftest, `--check`, `--verify-anchors` and the em-dash gate, with the same AC4 table. Candidate validation stays with the manager.
- **Local installs.** Contributors on other interpreters or platforms need their wheel's sha256 added to the lock; the lock's header says so. A local run without the lock is refused with the install command.
- **Owner decision.** Whether N2 (the file-view oracle) needs its own Issue.

## For the manager and reviewers

- Push; open the PR from `PR-BODY.md`.
- Trusted act replica and hosted contexts at the head.
- Candidate validation against live dev.
- R237 and R238 cold review with reviewer-owned five-lens coverage, then merge authorisation.

This author did no push, PR edit, merge or delegation. Evidence is in this directory (`COMMANDS.md`, `MANIFEST.sha256`).

# [A190] Handoff: issue #437 / PR #515, correction round for R237-2

## Identity

| | |
|---|---|
| Head | `e4906bfca65c61e7e109e3532ac1b2dd5b4c0096` |
| Tree | `f5d2e8c022d39684f458f7d2d0ee97b350533353` |
| Branch | `437-container-paragraph-scopes`, local only, not pushed |
| Parent | merge `ef39ecc4e7ccdaee8f64559350041d1e96044dc1` (tree `6fdccfce8ea34d98cde27b3409ff97a82d739dcb`) |
| Base | live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2`, which is the merge base with `origin/dev` |
| Starting head | `4741498f3b2b4f67f431037d327c96cf65691278` (R237-2 NEGATIVE) |
| Working tree | clean (`receipts/integrity.json`, `receipts/status.log`) |

Two author commits, both with a one-line subject and no trailers:

1. `ef39ecc4` Integrate disjoint live dev 574c29fa before the issue 437 container walk.
2. `e4906bfc` Read containers with a container walk and raw HTML comments as the page parser does.

## Dev integration

`receipts/integration-proof.json`:
- Dev paths since `483a133e`: 14. Issue paths: 7. The intersection is empty.
- `git merge-tree` gave tree `6fdccfce…`, and the merge commit has exactly that tree.
- The binary issue patch is byte-identical before and after the merge. Both copies hash to SHA-256 `1bd01330338539eb11432a1c05e064ac11ebe9080cf7014a388abbec0a0afb9b`.
- The four gitlinks and `.gitmodules` are unchanged.

## Public record on #437

- TAKEN: <https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5790805814>
- DECISION: <https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5791031813>. A container-aware block walk replaces the flat paragraph and container classification. The comment records the choice, the reason and the module split before any dependent edit.
- REVIEW READY: <https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5791751430> (`comment-review-ready.md`).

## What changed and why

R237-2 showed that targeted patches cannot close this family: at the base, several flat-walk errors cancel on the same page, so each fix exposed another. The fix is structural.

- **`scripts/gen_toc_containers.py` (new, the container layer).** It tracks block quotes, list items and GFM footnote definitions line by line:
  - continuation per CommonMark 0.31.2 sections 5.1 and 5.2 (quote `>` and one optional column, item content column, footnote four columns or an empty line, tab stops of four);
  - lazy paragraph continuation, and the list-item interruption rules;
  - the existing leaf machine (`gen_toc._opens`, `_still_open`, `_paragraph_after`) run on each line's content inside its containers.

  For each line it answers three questions and changes no label:
  1. the paragraph state a lone type-7 tag meets (`Scope.gate`);
  2. which containers are open after the line (`Scope.held_by`);
  3. which content GitHub emits verbatim as raw HTML (including types 3 to 5) or parses as inline text. Footnote content counts as neither, because GitHub renders it at the page end.
- **`scripts/gen_toc_html.py` (new, the HTML stage).** It models HTML's tokenizer, reduced to what decides a comment:
  - `<!--` opens only in data state. It opens nothing inside a tag's quoted attribute value, inside a bogus comment (`<!X`, `<?`, CDATA outside foreign content, `</` plus a non-letter), or after a tag GFM's tag filter escapes.
  - `-->`, `--!>`, `<!-->` and `<!--->` close.
  - In Markdown text, a closer counts only inside inline raw HTML per CommonMark 6.6. Declarations need GitHub's uppercase name. A closer never counts inside a code span or after an escape.
  - A raw run is read whole when it ends, and a paragraph's text when the paragraph ends.
- **`scripts/gen_toc.py` (the walk).** `blocks()` keeps the base's column-0 labels, so tracked-page classification is unchanged. It now asks the container layer three things:
  1. the type-7 gate (`_opens` takes `gate`);
  2. whether the container a fence, raw HTML block or comment opened in has ended, in which case the block ends with it;
  3. whether a comment opened in prose (or indented into a paragraph) has reached a line that is not paragraph text, which ends it.

  Lines the HTML stage says GitHub hides are labelled COMMENT.
- `gen_toc.py` also gained:
  - `RAW_3_5_RE`;
  - three measured classes: `html space`, `declaration name` and `escapable`;
  - `WALK_MODULES` and `walk_source()`, so the class guard enumerates the decision sites of all three walk modules (34, all single-source).

  `_list_paragraph_after` and the old rendered-comment flag are gone. The HELD comment is back to the base wording.
- **Tests.** `scripts/gen_toc_container_walk.json` is a new fixture of 71 shapes. Each carries GitHub's `gfm` rendering (request and response bytes, both SHA-256 values, headings) and a `pins` field naming the finding or rule it holds. `gen_toc_container_cases.py` scores:
  - two arms per shape;
  - nine label arms, each tied to the recorded HTML (under a nested block or an empty item the tag and the next line are raw; under the item's own paragraph the tag is inline);
  - two spelled-list arms: `WALK_MODULES`, and the nine tag-filter names.

  `gen_toc_cases.py`:
  - spells the three new classes;
  - reads the site guard over `walk_source()`;
  - moves the site count from 27 to 34;
  - drops the now unused `gen_toc_file()`.

  The arm floor is `MIN_ARMS = 1244` (was 1091).
- **Docs.**
  - CONTRIBUTING 6.1 replaces the lane's paragraph with the container rule, the HTML-stage rule and the two remaining escapes. It spells no comment opener, so the base walk reads the page the same way.
  - `docs/DOC_GENERATION.md` names the two walk modules and replaces "Container behavior remains the separate scope of issue #437".

No exemption or provenance function, workflow, RTL, firmware, budget file or gitlink changes.

## Sizes and ratchets

| File | Lines |
|---|---:|
| `scripts/gen_toc.py` | 996 (ratchet 1000, was 999) |
| `scripts/gen_toc_containers.py` | 256 |
| `scripts/gen_toc_html.py` | 139 |
| `scripts/gen_toc_cases.py` | 992 (was 995) |
| `scripts/gen_toc_container_cases.py` | 337 |

- `check_py_idiom`: long module 10 <= 10, long function 9 <= 9, too many parameters 7 <= 7, and every other ratchet in budget.
- No budget file changed.
- The split follows CODE_QUALITY rule 1. Each new module has its own state, policy and tests, and no pass-through wrapper was added.

## Validation at `e4906bfc` (all exit 0; `receipts/exits.tsv`, one log each)

| Receipt | Result |
|---|---|
| toc-selftest | TOC selftest PASS 1244/1244 |
| toc-check | 106 pages carry Contents, 17 below threshold |
| toc-anchors | 144 cross-page fragment links reproduced |
| toc-sites | 34 decision sites, all single source, no notes |
| emdash-selftest | 416 arms (was 345) |
| emdash-base-mergebase (`574c29fa`) | 0 findings over 28 added lines, 0 exempt |
| emdash-base-483a133e / -88e9276b | 0 findings over 365 / 377 added lines |
| docs-check, docs-check-selftest | 0 findings over 164 md + 839 text files; 23 + 4 arms |
| doc-style, doc-style-selftest, doc-paths | OK |
| py-idiom, py-idiom-selftest | ratchets in budget; 54/54 |
| hygiene, hygiene-selftest | PASS 714 files; 35/35 |
| naming, fail-fast, test-evidence | ratchets PASS |
| cohesion-selftest, control-flow-selftest | 18/18, 45/45 |
| todo-ownership, feature-status | OK |
| diff-check-branch (`574c29fa..HEAD`), diff-check-worktree, status | clean |
| ac4-corpus | 0 differences on all three trees (below) |
| prior-arms | the 707 base-era arms classify identically under all three walks (below) |
| final-sweep | 0 regressions, 0 unrendered differences, every disagreement family two (below) |
| mutations | 33/33 killed at arms named for their property (below) |
| fixtures-at-head | 162/162 fixture shapes re-rendered byte-identical; the walk agrees with each |
| r237-2-findings | F1 252/252 and F2 10/10 R237-2 regression rows agree at HEAD |
| emdash-probe-base / -head | R237-2's em-dash probe (module list extended): all three escape shapes `exempt=0` at HEAD |
| integrity | clean; merge base is the live dev tip; commit messages one-line, no trailers |

### AC4: tracked-page classification

`receipts/ac4-corpus.json`. For every tracked page, the comparison covers blocks, line_kinds, headings with anchors, plan, generated_block, owns and refusals under three walks:
- base `88e9276b`;
- starting head `4741498f`;
- the new three-module walk.

| Tree | Pages | Lines | Differences | Digest |
|---|---:|---:|---:|---|
| `88e9276b` | 163 | 46,252 | 0 | `3b53cfe1…` (R238-r1 recorded the same) |
| `574c29fa` | 164 | 46,596 | 0 | `860d2e49…` |
| HEAD | 164 | 46,623 | 0 | `eb8d2efc…` |

No family-two heading is added.

### Agreement with GitHub (`receipts/final-sweep.json`)

- Renderings: 5,573 recorded renderings, of which 1,367 come from the public receipts.
- Fresh renders this session: 4,276 in `work/render-cache.jsonl` and `receipts/walk-fixture-render.jsonl`, plus the 162 fixture re-renders.
- Every request was a synthetic page sent to `POST /markdown`, mode `gfm`, context `kebag-logic/milan-fpga`.
- The receipts keep exact request bytes, exact response bytes and both SHA-256 values.
- Where the new walk answers like the base, no rendering is needed: the page agrees exactly when the base does.
- In the table, "vs base" counts pages against GitHub for the base walk and the new walk. "Same" means both walks answer alike, and "same" pages were not rendered. "Family two" counts the pages both walks still get wrong; every one of them differs only on a setext or container heading.

| Corpus | Pages | vs base: fix | agree | same | family two | regressions |
|---|---:|---:|---:|---:|---:|---:|
| public receipts (R237-1/2, R238-1, A168, A172, A184) | 1,367 | 628 | 680 | 0 | 59 | 0 |
| R237-2 combinatorial (its own generator) | 2,070 | 429 | 253 | 1,346 | 42 | 0 |
| containers (51 prefixes x tags x columns x followers) | 9,330 | 1,709 | 153 | 7,370 | 98 | 0 |
| comments (openers, closers, wrappers) | 405 | 223 | 13 | 169 | 0 | 0 |
| prose comments | 216 | 144 | 1 | 65 | 6 | 0 |
| fuzz (seed 437) | 5,816 | 484 | 0 | 5,307 | 25 | 0 |
| fuzz2 (seed 516, richer vocabulary) | 7,909 | 1,655 | 1 | 6,221 | 32 | 0 |
| tabs | 770 | 28 | 0 | 742 | 0 | 0 |
| rules, fixtures | 173 | 82 | 91 | 0 | 0 | 0 |

The same run against the starting head `4741498f` also has no regression.

### Preservation

- **Base-era arms (`receipts/prior-arms.json`).** All 707 arms (walk, tag, guard, heading, predecessor, provenance, refusal, I440) classify identically, blocks and headings, under base, start and new walks.
- **Earlier I437 arm pages.** Every one from A168, A172 and A184 classifies as at the starting head. The 50 I437 pages that differ from the start are all shapes of the new fixture, where the start disagrees with GitHub.
- **Existing suites.** All 1091 prior TOC arms and 345 prior em-dash arms still pass. None was changed except the guard family: its three site arms now read all walk modules and the count is 34.

### Mutations (`receipts/mutations.json`)

Each mutation replaces one span in a disposable `git archive HEAD scripts` copy. Both self-tests then run in that copy.

| ID | Property removed | Killed at (examples) |
|---|---|---|
| M01 | type-7 gate read from the container layer | family-one `two spaces`, `labels live bullet paragraph` |
| M02 | a tag under a nested block opens raw HTML in the item | `labels nested quote`, `labels nested bullet` (labels only: TOC self-test) |
| M03 | a block opened in a container ends with it | `live bullet paragraph, in-item fence would escape`, R238 `P02` |
| M04 / M05 | lazy continuation; an indented lazy line | `lazy line retains item`; `lazy indented comment opener is prose` |
| M06 / M07 | an empty item ends at a blank; a blank at its column keeps it | `empty item ends at blank`; `empty item kept by a blank of its column` |
| M08 | an empty item's first line meets no paragraph (R237-2 F3) | `labels empty item, tag opens HTML` (labels only: TOC self-test) |
| M09 | a quote's one optional column | `a quote's optional space leaves a raw opener` (opening and continued) |
| M10 / M11 / M12 / M13 | footnote four columns; code padding; interruption rule; thematic break | `footnote two spaces`; `code padding uses one`; `noninterrupting ordinal is no item`; `thematic break is no item` |
| M14 / M15 / M16 | types 3 to 5 raw; footnote content not read; tab stops | `type-3/4/5 block`; `footnote content is read at the page end`; tab arms |
| M17 / M21 / M22 | opener only in data state; bogus comments; quoted values | `double-quoted attribute`, `CDATA is a bogus comment`, `a quoted value hides a greater-than` |
| M18 / M19 / M20 | `--!>` closes; abrupt comments; tag filter | `--!> closes…`; `abrupt empty comment in a block`; `tag filter leaves the attribute as text` |
| M23 – M27 | inline closers; not in prose or code; code spans; uppercase declarations; whole paragraphs | `closed by an inline comment`; `prose arrow closes nothing`; `code span hides the tag`; `lowercase declaration is text`; `tag across lines closes` |
| M28 / M29 / M30 | prose comment ends with its paragraph; indented opener is prose; inline comment is no block | `heading after a prose opener`; `indented comment opener continues a paragraph`; `type-3 block` |
| M31 | hidden lines are commented | the twelve #516 variants |
| M32 | markers inside a block open nothing (R237-r1 F3) | `R237 fenced-marker-indented-closer`, `commented marker is inert` |
| M33 | a dedented quote or footnote ends the item (R238-r1 F2) | `R238 D01`, `R238 D02` |

M02 and M08 change only the labels of lines inside an item. The block now ends with the item, so no heading moves, and the em-dash gate, which reads headings and generated navigation, cannot observe them. Their arms are the label arms, each checked against the recorded HTML. The old `not item_context[1]` guard R237-2 F3 names no longer exists. Its property is structural now: the empty item's first line meets no open paragraph, the item ends at a blank, and a blank at its column keeps it. M06, M07 and M08 remove each part.

## Resolution of every public finding

| Finding | Severity, lenses | Resolution at `e4906bfc` | Evidence |
|---|---|---|---|
| R237-r1 F1: tag inside the resumed item paragraph hides a heading | MAJOR; Conformance, Robustness, Tests | kept resolved: the deepest matched block is the item's open paragraph, so the tag continues it | arms `R238 C01`–`C03`, `resumed tag column 2/3 …`, family-one `… inside`; M01 |
| R237-r1 F2: historical cases | MAJOR; Conformance, Tests, Docs | kept resolved against restated AC1 (R237-2's disposition); the 51-shape family-one fixture is unchanged and re-renders byte-identical | `fixtures-at-head` |
| R237-r1 F3: block-marker inertness unarmed | MAJOR; Conformance, Tests | kept resolved; in the container layer a line inside a fence, comment or raw HTML block opens no container | M32 killed at `R237 …-marker-indented-closer`, `… marker is inert` |
| R238-r1 F1: content-column tag, C01–C08, P01, P04 | MAJOR; Conformance, Robustness, Tests, Docs | kept resolved | `R238 C01`–`C08`, `P01`, `P04` arms; M01, M03 |
| R238-r1 F2: item survives a dedented quote or footnote | MAJOR; Conformance, Robustness, Tests, Docs | kept resolved: a column-0 quote or footnote starts a block, so it is no lazy line and the item ends | `R238 D01`–`D07`, `quote/footnote column 0-2 …`; M33 |
| R238-r1 F3: item HTML block outlives the item (P02, P03, F09) | SUGGESTION; Conformance, Robustness | resolved: a block ends with its container | fixture `R238 P02/P03/F09 …`; M03 |
| R237-2 F1: content-column continuation whatever holds the item; in-item block never ends | MAJOR; all five | resolved at the root: the gate reads the deepest matched block, and blocks end with their container | 252/252 regression rows agree; 0 regressions over 28,056 page checks; fixture `nested …`, `live …`; em-dash probe `exempt=0` x3; M01–M03 |
| R237-2 F2: rendered-comment flag opens on any `<!--` substring | MAJOR; all five | resolved: HTML-tokenizer model over the lines GitHub emits raw | 10/10 regression rows agree; fixture `double-quoted attribute`, `CDATA is a bogus comment`, `--!> closes …`, `item block ends before …`, `inline tag closes after the block`; M17–M27 |
| R237-2 F3: empty-item guard unarmed | MINOR; Tests | resolved: the guard is gone and the property is structural and armed | R237-2's two F3 pages are fixture shapes; M06, M07, M08 |
| R237-2 S1: comment opener four columns into an item | SUGGESTION; Conformance, Robustness | resolved (both pages agree; em-dash probe refuses it) | fixture `R237-2 S1 …` |
| #516 twelve variants (six resumed regressions) | manager-tracked | kept resolved | comment fixture `#516 …` arms; M31 |
| A184 decision residues (`--!>`/inline-tag withholding; code-span/escape escape) | author-declared | resolved | fixture `--!> closes …`, `inline tag closes after the block`, `code span hides the tag`, `escape hides the tag` |

## Remaining, stated with direction (CONTRIBUTING 6.1, docstrings)

- **Family two (withholding, as selected).** The five forms stay omitted: `Alpha` over `===`, `text` over `---`, `text` over `-`, `> ## Q`, and `## Inner` in an item. Every disagreement left in every corpus above is one of these.
- **Escape, as at the base (#413 residue).** A raw HTML block of types 3 to 5 is labelled prose, so a heading inside a multi-line one is listed.
- **Escape, as at the base (measured).** Raw HTML that ends inside an unclosed tag or a bogus comment turns GitHub's next heading into text, and inside an open quoted value every later one. The walk lists them (`work/probe-residue.json`, 4 rows, both walks identical).
- **Labels only.** Blocks four or more columns into an item keep their column-0 labels (indented code or text). No heading depends on them.
- **Unmeasured.** Foreign content's real CDATA, and a DOCTYPE's quoted identifiers.

## Limits of this evidence

- The oracle is GitHub's Markdown API on 2026-09-23 (UTC times in the receipts). It returns sanitized HTML with no anchor ids, so heading presence is measured and anchors are the walk's.
- The sweeps are bounded (28,056 page checks) and not exhaustive. A reviewer's new corpus can still find a shape outside them.
- No full parent, PP, gPTP, Yosys or builder bank, Docker/act, hosted run, push or PR edit was run or made by this author.

## Remains for the manager and reviewers

- Push, the PR #515 update (`PR-BODY.md` proposed), and publication of this packet.
- The full native and builder banks, trusted act, hosted contexts, and current-candidate validation.
- Dispositions of #516 and #495, and whether the measured unclosed-tag escape needs an owning Issue.
- R237 and R238 cold re-review with reviewer-owned five-lens coverage at this head.
- Maintainer merge authorization.

## Packet layout

| Path | Contents |
|---|---|
| `comment-*.md` | the three public comments as posted |
| `PR-BODY.md` | proposed PR #515 body |
| `COMMANDS.md` | every recorded command with exit, head and UTC |
| `scripts/` | every script used, with `reproduce.sh` running them in order |
| `receipts/` | logs, JSON results, `exits.tsv`, `integration-proof.json`, `walk-fixture-render.jsonl` |
| `work/` | corpora, `public-cache.json` (harvested from the public receipts by `scripts/harvest.py`), `render-cache.jsonl` (4,205 fresh renders), `prototype/` (the scratch prototypes the decision was measured with) |
| `MANIFEST.sha256` | SHA-256 of every file above |

`inputs/` (the public review evidence at `de3f6688`) is not kept; `scripts/fetch_inputs.sh` recreates it.

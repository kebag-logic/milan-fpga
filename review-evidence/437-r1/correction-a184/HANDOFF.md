# [A184] Handoff: #437 / draft PR #515, restated acceptance 1

## Identity

- Head `4741498f3b2b4f67f431037d327c96cf65691278`, tree `ee70aaf8faadbced21dfdd0cf7719597e9fbe8eb`.
- Branch `437-container-paragraph-scopes`, local only, **not pushed**. Tree and index clean; see `receipts/integrity.json`.
- Parent `a09ff881d31850e91866e301c846579173d7aa61`. That is this author's merge of the starting head `b5e6c23e1b9802b5cacbc62db212064d7e429862` with live dev `483a133ed08867ea0d300d2b4a027b5b48a4282f` (tree `0e9e503dbbd236bbee6d499ac2d613f008a02c6a`).
- Base: live dev `483a133e`, which is the merge base; the head descends from it. The original issue base is `88e9276b2a220c716f64a843f7e1eb8f9265e896`. Its walk files are byte-identical to live dev's: `git diff 88e9276b 483a133e` over the walk files and CONTRIBUTING.md is empty.
- This author's commits: `a09ff881` "Integrate disjoint live dev 483a133e before issue 437 shape set" and `4741498f` "Record the family-one shape set and hide prose after comments left open in raw HTML". Each has a one-line subject, no trailers and no attribution.
- Submodule gitlinks and `.gitmodules` are identical to live dev, to `88e9276b` and to the starting head:
  - `external` `efeb541a`, uninitialised;
  - `gptp-processor` `c1b61743`;
  - `protocol-processor` `424c688f`;
  - `third_party/verilog-axis` `48ff7a7e`.

  The three initialised submodules are checked out at their gitlinks.

## 1. Live-dev integration (step 1)

`receipts/integration-proof-pre.json` was computed before the merge and `receipts/integration-proof.json` after it:

- The issue paths since `52711029` are CONTRIBUTING.md, `scripts/check_em_dash.py`, `scripts/gen_toc.py`, `scripts/gen_toc_cases.py` and `scripts/gen_toc_container_cases.py`.
- The dev paths `52711029..483a133e` are `docs/ENDSTATION_BUILDER.md`, `sw/builder/endstation_builder.py` and `sw/builder/test_builder.py`.
- The intersection is empty.
- The merge tree `0e9e503d` equals the precomputed `git merge-tree --write-tree` result.
- The complete binary issue patch is byte-identical before and after integration (SHA-256 `1fed0345...211fe`).
- The dev patch is byte-identical as well (`aec58c21...6cdda`).

## 2. What changed at `4741498f` (vs `a09ff881`)

| Path | Change |
|---|---|
| `scripts/gen_toc.py` | 991 to 999 lines (ratchet 1000). `blocks()` gains a rendered-comment flag; `_comment_after` treats `<!-->` and `<!--->` as complete; docstring states the rule and its residues; `MIN_ARMS` floor 909 to 1091. |
| `scripts/gen_toc_container_cases.py` | Loads the two fixtures; two arms per recorded shape (`I437 receipt <name>`, `I437 rendered <name>`); the same shapes feed the real-Git em-dash consumer (`I437 recorded <name>`). |
| `scripts/gen_toc_family_one.json` | New: the restated-AC1 family-one shape set, 51 shapes, with recorded GitHub rendering. |
| `scripts/gen_toc_comment_shapes.json` | New: 40 rendered-comment controls, including #516's twelve published variants, with recorded GitHub rendering. |
| `CONTRIBUTING.md` 6.1 | Two lines saying the flat walk "may list those headings" replaced by the implemented rule, its escaped-closer boundary, its two residue directions, and where the recorded rendering lives. |

`check_em_dash.py`, `gen_toc_cases.py`, `gen_toc_closer_cases.py`, `gen_toc_guards.py`, every budget file and every non-Markdown-tooling path are unchanged from the starting head. The only other paths in the head-vs-start diff come from live dev.

The rendered-comment rule was published before it was implemented, as a material decision: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5789133990

## 3. Restated acceptance 1: the family-one shape set

`scripts/gen_toc_family_one.json` holds 51 shapes. Every page has R86-5's form: a predecessor, a lone tag line wrapping `## Old`, then `## Real`.

- **Resumed paragraph, tag outside the item (21).** The items are bullet `- item` (content column 2), star `* item` (2), ordered `1. item` (3) and two-digit ordered `10. item` (4). Each resumes a paragraph after a blank line at the content column and one column past it. The tag is an inline tag (`<span>`) and an unknown tag (`<custom-tag>`) at column 0. There are also five R86-5 variants: two item paragraphs, task item, list interrupting a paragraph, `<b>`, and two blank lines. GitHub renders only `Real`.
- **Resumed paragraph, tag inside the item (16).** The same items and indentations, with the tag at the paragraph's own column. GitHub renders `Old, Real` (the R237 F1 / R238 F1 direction).
- **Two-digit boundary below its wider column (2).** `10. item`, blank, three-space `text`, then the column-0 tag, for both tags. GitHub renders `Old, Real`, because three columns is outside a four-column item.
- **Boundaries that already agreed (12).** One space, four spaces, block quote, footnote definition at two and at four spaces, and tab, each with both tags.

Each shape records:
- `request_bytes`, the exact JSON body sent, with its SHA-256. The byte length was checked against the transmitted Content-Length.
- `response_bytes`, the exact HTML returned, with its SHA-256.
- `headings`, the heading elements of the response, and `recorded_utc`.

The request was `gh api markdown -f mode=gfm -f context=kebag-logic/milan-fpga -f text=<page>`.

**At this head**, `receipts/fixture-at-head.json` re-rendered all 91 fixture shapes fresh (51 family-one and 40 controls). Every request and response is byte-identical to the committed fixture.

**Mapping of the nine R86-5 descriptions** (PR #428 comment 5644834363), carried in each shape's `r86_5` field:

| R86-5 description | Named shape | GitHub renders |
|---|---|---|
| `- item` + blank + `  text` (two spaces) | bullet at column, inline tag outside | Real |
| the same at three spaces | bullet past column, inline tag outside | Real |
| with `*` | star at column, inline tag outside | Real |
| with `1. item` + `   text` | ordered at column, inline tag outside | Real |
| with two container paragraphs | bullet two paragraphs, inline tag outside | Real |
| with a task item | task at column, inline tag outside | Real |
| with a list that follows a paragraph | interrupting bullet at column, inline tag outside | Real |
| with `<b>` in place of `<span>` | bullet at column, b tag outside | Real |
| with two blank lines | bullet after two blanks, inline tag outside | Real |

The five boundaries R86-5 names (H03 one space, H04 four spaces, H07 block quote, H08/H09 footnote definition, H26 tab) are the twelve `boundary ...` shapes. The shapes are fresh bytes. No archival identity with the unpublished R86-5 files and no per-ID correspondence is claimed; the restated criterion does not require either.

**The walk agrees with the recorded rendering for all 51 family-one shapes and all 40 controls.** 36 family-one shapes agreed at the base and still do. 15 were escapes at the base and now agree.

One fact about the two-digit marker, stated so a reviewer does not over-read the set. Text at or past a four-column content column is at four or more columns. The flat walk reads it as indented code, and that also gives the rendered answer. The two-digit marker's wider column is therefore held by the below-column boundary, not by the at/past shapes. Mutations `content-column-fixed-at-two` and `content-column-fixed-at-three` fail exactly there.

## 4. No regression against the base

**Three-way replay.** `receipts/three-way.json` covers every publicly recorded rendering in the R237-r1, R238-r1, A168 and A172 packets, plus this author's 91 fixture renders and 42 contract probes: 695 unique pages from 957 receipt rows. It judges each against the base walk `88e9276b`, the starting walk `b5e6c23e` and this head.

| Class | Pages |
|---|---:|
| Agree at base and head | 415 |
| Disagree at base, agree at head | 255 |
| Agree at base, disagree at head (**regression**) | **0** |
| Disagree identically at base and head | 21 |
| Disagree at base, disagree differently at head | 4 |

At the starting head `b5e6c23e` the same replay has 6 regressions: exactly the six resumed #516 variants.

**Named items, re-rendered fresh** (`receipts/named-regressions.json`, 119 renders). Every publicly recorded rendering matches today's render.
- R238's 62 probes: A01-A20, B01-B06, C01-C08 (F1), D01-D07 (F2), F01-F12, G01-G05, P01-P04.
- R237's 42 controls (the F1 matrix) and 3 block-marker controls (F3).
- The twelve #516 variants.

Result: 103 agree, 0 regressions, 16 pre-existing (listed below).
- R238 F1 C01-C08, R238 F2 D01-D07, P01 and P04 agree.
- R237 F1's matrix and R237 F3's three indented-closer marker controls agree.
- All twelve #516 variants agree: the six resumed forms that regressed at `b5e6c23e`, and the six first-paragraph forms, which were already wrong at the base.

**Existing corpus.** The 707 base-era arm pages classify identically (`blocks()` and `headings()`) under all three walks: walk 51, tag 43, guard 37, heading 8, predecessor 115, provenance 18, refusal 7, I440 428. In the starting head's 202-arm I437 family, 76 pages differ from the base by design, and this head equals `b5e6c23e` on every one (`receipts/prior-arms.json`).

**Disagreements identical at base and head (21), enumerated:**
- Family two, the declared omissions: `Alpha`/`===`, `text`/`---`, `text`/`-`, `> ## Q`, `## Inner` in an item. Also their real-Git page forms and three setext-in-context probes (R237 setext-outside, R237 control "setext dash is no item", R238 `  text`/`  ===`).
- #495 item-HTML residues: R238 P02 and P03 (both walks list `Old`), F09 (`- item`, blank, `  text`, blank, `  <span>`: both walks withhold `Old`), R238's real-Git P02 page, and the two empty-item counterparts (`-` / `  <span>`, `- item` / `-` / `  <span>`).
- The A172 real-Git setext page (`text` over `-`).
- Prose `text <!--` with no closer: GitHub shows `Real` and both walks withhold it.

**Disagreeing differently (4):**
- R237 setext-inside (family two): the base lists `Old`; this head lists `Real` only, still omitting the setext `title`.
- Rendered-comment residues, all disagreeing at the base:
  - V07 code-span `` `<!-- a -->` ``: the base invents `Old` and `Real`; this head invents `Real` only.
  - V10 `x <!--`, blank, `-->`: the same pattern.
  - V12 `--!>`: the base invents `Old`; this head withholds `Real`.

## 5. The rendered-comment rule (#516 shapes)

The contract was measured with 42 fresh probes (`receipts/contract-probes-{1,2}.json`). GitHub passes raw HTML block content through. A `<!--` left open there hides the rest of the page until raw HTML carries `-->`. This holds after types 1, 6 and 7, inside list items and inside quotes.

- A later HTML block line of any type closes it, as do a type-2 block, an inline comment, and an inline comment in a heading.
- `-->` in paragraph, heading, code span, indented code or fence text is escaped and closes nothing.
- `<!-->` and `<!--->` are complete empty comments.
- `--!>` in raw HTML also closes it.

The implemented rule in `blocks()`:
- The flag is read with `_comment_after` on lines labelled raw HTML or commented, and on prose lines carrying `<!--`.
- While the flag is open, a prose line is labelled commented.
- Block and paragraph/item state is computed from the unrelabelled label, so classification is otherwise unchanged.
- The rule only turns prose into commented lines, so it cannot list a heading the starting walk omitted.
- Without a raw-HTML comment, the flag mirrors the existing type-2 comment state.
- No tracked page carries an unclosed comment in an HTML block, `<!-->` or `<!--->`.

**Residues, documented with direction** in the `blocks()` docstring and CONTRIBUTING 6.1:
- Withholding: `--!>`, or a non-comment inline tag carrying `-->`, closes the comment for GitHub only.
- Escape, also present at the base: a closed comment inside a code span, or an escaped `-->` after a prose `<!--`, closes it here only.

## 6. Acceptance 2 to 5

- **AC2** is unchanged. The five family-two forms stay omitted, and the docstring and CONTRIBUTING 6.1 name them with their withholding direction.
- **AC3**: 16 new named mutations, each killed at its named arms (`receipts/mutations.json`). TOC exit is 1; em-dash exit is 2, except the two receipt-only mutations, which only the TOC runner reads.

  | Mutation | Property removed | TOC / em-dash failing arms |
  |---|---|---:|
  | comment-never-opens | a raw-HTML `<!--` opens the flag | 31 / 46 |
  | raw-html-lines-ignored | raw HTML lines are read | 31 / 46 |
  | no-prose-relabel | prose under the flag is commented | 31 / 46 |
  | raw-lines-never-close | raw lines close the flag | 49 / 23 |
  | escaped-arrow-closes | escaped `-->` closes nothing | 8 / 12 |
  | prose-comment-ignored | an inline comment closes the flag | 2 / 2 |
  | code-opener-counts | fenced/indented `<!--` opens nothing | 3 / 2 |
  | abrupt-comment-not-empty | `<!-->`/`<!--->` are complete | 4 / 4 |
  | item-context-dropped | item context is kept | 85 / 135 |
  | tag-inside-opens | an inside tag continues the paragraph | 75 / 91 |
  | content-column-fixed-at-two | the content column is measured | 10 / 12 |
  | content-column-fixed-at-three | the two-digit column is wider | 61 / 95 |
  | blank-forgets-item | blank lines keep a nonempty item | 55 / 98 |
  | response-byte-altered | response bytes match their SHA-256 | 1 / 0 |
  | recorded-headings-altered | recorded headings match the response | 2 / 2 |
  | page-without-request | the request carries the page | 1 / 0 |

  All 23 published A172 mutants still fail both selftests at their required arms (`receipts/a172-mutants.json`).
- **AC4**: every tracked Markdown page of the base tree (163 pages, 46 252 lines), the live-dev tree (163, 46 263) and the head tree (163, 46 283) was compared under all three walks. Blocks, line kinds, headings with anchors, plan, generated block, ownership and refusals are identical, with zero differing pages (`receipts/corpus-compare.json`). The base-tree digest `3b53cfe1...` equals R238-r1's published one. No family-two heading is added.
- **AC5**: all 33 focused commands exit 0 at `4741498f` (`receipts/exits.tsv`, logs beside it).
  - TOC selftest 1091/1091; `--check` 105 pages; `--verify-anchors` 144 links; `--sites` 27 sites, unchanged.
  - Em-dash selftest 345 arms. `--base 483a133e` gives 0 findings over 20 added lines. `--base 88e9276b` gives 0 findings over 32 added lines in 4 pages.
  - `docs_check` reports 0 findings over 163 + 830 files, and its selftest passes. Doc style, its selftest and doc paths pass.
  - Idiom: long module 10 <= 10, long function 9 <= 9, over-long line 0 <= 0; its selftest passes. Hygiene and its selftest pass.
  - Naming, fail-fast, test-evidence, control-flow, cohesion, TODO ownership, ci_events, feature status, solution/submodule/gPTP docs and archive gates pass.
  - The "can be lowered" notes printed by fail-fast (82, 4, 0) and test-evidence (75) are identical in the A168 packet's logs for `65df1df5`. Neither gate reads any file this change touches.
  - No budget file changed. `MIN_ARMS` is a floor and only rose.

## 7. Findings: author evidence only

Identities, severities and lenses stay with their reviewers. Nothing here clears a finding or a lens.

- **R237 F1 and R238 F1**: every C row and the R237 F1 matrix agree. The fixture adds 16 inside-tag shapes, and `tag-inside-opens` kills them.
- **R238 F2**: D01-D07 agree. The A172 quote/footnote release mutants still fail.
- **R237 F3**: the three indented-closer marker controls agree. `block-marker-only` still fails exactly its three arms.
- **R237 F2**: this is for re-judgement against the restated AC1. Section 3 is the evidence.
- **R238 F3** (SUGGESTION, #495) was not adopted, and its residues are unchanged.
- The #516 six resumed variants are addressed as described in section 5.

## 8. What remains for the manager and the reviewers

- Publish the source (push), update PR #515, and publish this packet with path neutralisation.
- Run the full parent, PP, gPTP, Yosys and builder banks, trusted act on the pushed head, the required hosted contexts, current-candidate validation if dev moves, and post-merge containment.
- R237 and R238 cleared-context re-review at the published head, with reviewer-owned five-lens coverage.
- Disposition of #516, whose measured shapes this head now matches, and of #495.
- Maintainer merge authorisation.

## 9. Evidence limits and boundaries

- The renderer oracle is GitHub's Markdown API as of 2026-09-23, 04:31 to 04:46 UTC. The three-way replay otherwise uses renderings recorded publicly on 2026-09-22; the 119 named items were re-rendered and match them.
- Every request carried a synthetic page only.
- The first `integrity` run exited 1 because of a bug in this author's harness: it counted the merged dev commits as author commits. The script was corrected and rerun (exit 0). Both rows are in `receipts/exits.tsv`.
- This author did not push, edit the PR, merge, or run Docker/act, full native banks, hardware, installs, privilege or sub-agents. No other checkout was used; scratch copies of `scripts/` lived only in temporary directories. At most 8 jobs ran at once.
- Public comments: TAKEN (5789055769), the material decision (5789133990) and REVIEW READY (5789254166).
- Reproduce with `scripts/reproduce.sh`; see `COMMANDS.md`.

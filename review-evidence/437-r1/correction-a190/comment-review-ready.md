[A190] REVIEW READY

Commit: `e4906bfca65c61e7e109e3532ac1b2dd5b4c0096`
Tree: `f5d2e8c022d39684f458f7d2d0ee97b350533353`

- Base: live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2`, which is the merge base.
- Integration: the disjoint merge `ef39ecc4`. The path intersection is empty, and the issue patch is byte-identical before and after (SHA-256 `1bd01330…fb9b`).
- Branch `437-container-paragraph-scopes`: clean, local only, not pushed.
- Two author commits, both with a one-line subject and no trailers.

Changed, per the [decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5791031813):
- `scripts/gen_toc_containers.py` (new). The container layer: block quotes, list items and GFM footnote definitions under CommonMark 0.31.2 sections 5.1 and 5.2, lazy lines included, with the leaf machine run on each line's content. It gives the type-7 gate (the deepest block the line matches), the containers open after each line, and which lines GitHub emits raw, types 3 to 5 included. Footnote content is excluded.
- `scripts/gen_toc_html.py` (new). The rendered comment, from a model of HTML's tokenizer:
  - `<!--` opens only in data state: not in a quoted attribute value or a bogus comment such as CDATA, and not after a tag GFM's tag filter escapes;
  - `-->`, `--!>`, `<!-->` and `<!--->` close;
  - a closer in Markdown text counts only inside inline raw HTML (uppercase declarations only), never in a code span or after an escape.
- `scripts/gen_toc.py` (996 lines, ratchet 1000):
  - Labels stay the base's column-0 labels.
  - A fence, raw HTML block or comment ends with the container it opened in.
  - A prose comment ends at the first line that is not paragraph text.
  - The class guard reads all three walk modules: 34 sites, all single-source.
  - `_list_paragraph_after` and the old flag are gone.
- `scripts/gen_toc_container_walk.json` holds 71 shapes. Each carries GitHub's `gfm` rendering: exact request and response bytes, both SHA-256 values, and the finding or rule it pins. `gen_toc_container_cases.py` adds two arms per shape, nine label arms tied to the recorded HTML, two spelled lists, and one em-dash real-Git row per shape. `gen_toc_cases.py` spells the three new classes; the site count goes from 27 to 34.
- CONTRIBUTING 6.1 and `docs/DOC_GENERATION.md`.

Validation at this head: 36 recorded commands, all exit 0.
- `gen_toc.py`: `--selftest` 1244/1244, `--check` 106 pages, `--verify-anchors` 144, `--sites` 34.
- `check_em_dash.py`: `--selftest` 416 arms. `--base 574c29fa` gives 0 findings over 28 added lines; `--base 483a133e` and `--base 88e9276b` give 0 findings.
- Every other gate passes:
  - `docs_check` and its selftest; `check_doc_style` and its selftest; doc paths;
  - `check_py_idiom` and its selftest (long module 10 <= 10, long function 9 <= 9, parameters 7 <= 7);
  - hygiene and its selftest; naming, fail-fast and test-evidence;
  - cohesion and control-flow selftests; TODO ownership; feature status;
  - `git diff --check 574c29fa HEAD`, and a clean status.
- GitHub `gfm` renderings: 28,056 page checks over every public receipt (1,367 pages), R237-2's own combinatorial corpus (2,070) and new corpora (24,619).
  - Against the base: 0 regressions and 5,382 fixes. No page where the two walks differ lacks a rendering.
  - Every remaining disagreement is a family-two heading.
  - 4,276 fresh renders, each with exact bytes and SHA-256.
- R237-2's regression rows: F1 252/252 and F2 10/10 agree. Its em-dash probe, with the two new modules added to the files it copies, reads `exempt=0` for all three escape shapes.
- AC4: 0 classification differences on the base, dev and head trees (163, 164 and 164 pages) under the base, starting and new walks. The base digest is `3b53cfe1…`, as R238-r1 recorded.
- All 707 base-era arms classify identically under the three walks. Every earlier I437 arm page classifies as at the starting head.
- 162/162 fixture shapes re-render byte-identical, and the walk agrees with each.
- 33/33 named mutations are killed at arms named for the property. M02 and M08 change labels only, so only the TOC self-test can see them.

Acceptance criteria:
- AC1 (restated): met by author evidence. The 51-shape family-one fixture is unchanged, re-renders byte-identical, and the walk agrees with it. No page that agreed at the base disagrees here over 28,056 checks.
- AC2: the five family-two forms stay named as withheld.
- AC3: 33 mutations, each killed at a named arm.
- AC4: 0 differences; no heading added.
- AC5: the gates pass, no ratchet is widened, and no budget file changed.

Every public finding at this head:

| Finding | Severity, lenses | At this head | Evidence |
|---|---|---|---|
| R237-r1 F1: tag in the resumed paragraph | MAJOR; Conformance, Robustness, Tests | kept resolved | arms `R238 C01`–`C03`, `resumed tag column 2/3`, family-one `inside`; M01 |
| R237-r1 F2: historical cases | MAJOR; Conformance, Tests, Docs | kept resolved against restated AC1 | family-one fixture byte-identical |
| R237-r1 F3: block-marker inertness | MAJOR; Conformance, Tests | kept resolved | M32 killed at `R237 …-marker-indented-closer` |
| R238-r1 F1: C01–C08, P01, P04 | MAJOR; Conformance, Robustness, Tests, Docs | kept resolved | `R238 C`/`P` arms; M01, M03 |
| R238-r1 F2: dedented quote or footnote | MAJOR; Conformance, Robustness, Tests, Docs | kept resolved | `R238 D01`–`D07`; M33 |
| R238-r1 F3: item HTML outlives item | SUGGESTION; Conformance, Robustness | resolved | fixture `R238 P02`, `P03`, `F09`; M03 |
| R237-2 F1: gate whatever holds the item; in-item block never ends | MAJOR; all five | resolved at the root | 252/252 rows; fixture `nested …`, `live …`; `exempt=0` x3; M01–M03 |
| R237-2 F2: flag on any `<!--` substring | MAJOR; all five | resolved | 10/10 rows; fixture `double-quoted attribute`, `CDATA is a bogus comment`, `--!> closes …`, `item block ends before …`; M17–M27 |
| R237-2 F3: empty-item guard unarmed | MINOR; Tests | resolved: guard gone, property structural | R237-2's two pages in the fixture; M06, M07, M08 |
| R237-2 S1: opener four columns into an item | SUGGESTION; Conformance, Robustness | resolved | fixture `R237-2 S1 …`; refused end to end |
| #516: twelve variants | manager-tracked | kept resolved | comment fixture `#516 …`; M31 |

Open risks/questions:
- Two escapes remain, both present at the base, and both are documented with their direction:
  - A multi-line raw HTML block of types 3 to 5 is labelled prose (#413).
  - Raw HTML that ends inside an unclosed tag or bogus comment turns GitHub's next heading into text; inside an open quoted value it hides every later one. The walk lists them (measured on 4 pages). Whether this needs an owning Issue is the manager's call.
- The walk is now three modules. A probe that copies `gen_toc.py` alone must also copy `gen_toc_containers.py` and `gen_toc_html.py`.
- The sweeps are bounded, not exhaustive.

Remains for the manager:
- Push and the PR #515 update. A proposed body is in the packet.
- Publication of the packet: HANDOFF, PR-BODY, COMMANDS, receipts, reproducible scripts and MANIFEST.
- Full native and builder banks, trusted act, hosted contexts and current-candidate validation.
- Dispositions of #516 and #495.

Remains for reviewers: R237 and R238 cold re-review at this head with reviewer-owned five-lens coverage, then maintainer merge authorization.

This author did no push, PR edit, merge, act/Docker, full bank run or delegation. Stopping at this head.

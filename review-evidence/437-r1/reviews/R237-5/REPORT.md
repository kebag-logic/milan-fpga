[R237] NEGATIVE - exact head 196cb7d99cb06631df514715979a5f82fbb1f7aa

# R237-5: internal cold review of PR #538 (issue #437, closing #516)

- Reviewed head `196cb7d99cb06631df514715979a5f82fbb1f7aa`, tree `796c734682c7d7dc5c26fd9a92090a3c4a35fc32`.
- Source base `759da623072358afdb0e9d570a7b4b6a788492c9`; three one-line commits, no trailers (checked on the raw commit objects).
- Scope reconstructed from AGENTS.md, CONTRIBUTING.md 6.1, docs/README.md, REQUIREMENTS.md REQ-VER-04, the #437 body (acceptance 1 as restated and amended), the #437 decisions 5788996063, 5794734885, 5798044806, 5800600405, the author's TAKEN 5800875179 and REVIEW READY 5802079096, the manager rulings 5802133440, and the #516 body and decisions 5794735214 and 5798045125.
- Then the diff `759da623..196cb7d9`, the public evidence at `171736854c31:review-evidence/437-r1/cmark-a212/`, the original #516 receipts at `9f5e84cee18b:review-evidence/437-r1/correction-a172/`, and the hosted run at the exact head.
- No prior reviewer report was read before the verdict and ledger below were written.

## Verdict

NEGATIVE. The replacement is sound and its evidence is strong.

- The committed shape set agrees with GitHub's recorded renderings by construction: 352 of 352 shapes, 0 regressions against the base walk.
- Acceptances 2, 4 and 5 hold.
- One MAJOR remains open (F1): the guard that stops raw HTML from forging the renderer's source positions is case-sensitive. An upper-case attribute lets a heading that an open raw comment hides (#516) be listed, and the shipped em-dash gate then exempts a label copied from it. The documented invariant ("none can grant an exemption") is false for it.
- Two MINORs remain open: F2, deep container nesting crashes both gates; F3, five of six own-element kinds carry no arm (acceptance 3).

## Findings

### F1 - MAJOR - Conformance, Robustness, Tests, Docs

- **Where:** `scripts/gen_toc_renderer.py:257`, the case-sensitive `if POSITION in text:`. `scripts/gen_toc_renderer.py:332-340` (`_shown`) trusts any parsed element carrying the attribute. `scripts/gen_toc.py:205` and `:222-230` match headings by that position string.
- **Authority:**
  - #437 objective: a label mirrored from a heading the page does not render must not obtain the CONTRIBUTING 6.1 exemption.
  - #516 is closed by this lane under the 17:45 decision ("the parser renders it as GitHub does").
  - `CONTRIBUTING.md:593-599`: "each one withholds a heading; none can grant an exemption", and "a page whose text spells the attribute ... is read as rendering nothing".
  - `scripts/gen_toc_renderer.py:40-44`: "That withholds a heading and cannot invent one".
  - `docs/DOC_GENERATION.md`: "Each limit withholds a heading and grants no exemption".
  - HTML attribute names are ASCII case-insensitive, and the HTML5 tokenizer lowercases them, so `DATA-SOURCEPOS` parses as the renderer's attribute.
- **Evidence** (`receipts/probe_forged_position_emdash.txt`, `scripts/probe_emdash_gate.py`):
  - The base page is the recorded #516 shape "top-level tag leaves comment open" (fixture: GitHub renders no heading). Three plain sections come before it, and one complete raw `<h2 DATA-SOURCEPOS="20:1-20:18">Harmless</h2>`.
  - `gen_toc.headings()` lists `Old <em dash> heading` at `old--heading`, a heading the open comment hides.
  - The shipped `scripts/check_em_dash.py --base <base>` ran inside a disposable repository on real commits, with its 332 controls passing first. It reports `0 finding(s) ... 1 mirrored label(s) exempt`, both for `DATA-SOURCEPOS` and for `Data-SourcePos`.
  - Control without the forged element: no `Old` listed, nothing exempt.
  - Lower-case spelling: the guard withholds every heading.
  - The base walk also listed `Old` on this page, so this is not a regression against the base. It is a residual #516 escape behind a guarantee the head states.
  - Mutation M16 (guard made case-insensitive) survives every arm, as does M06 (heading-tag check removed; `receipts/mutation_probes.txt`). No arm holds the guard's case behaviour.
  - No tracked page spells the attribute in any case (`receipts/scan_tracked_raw_html.txt`).
- **Impact:** escape direction. A Contents label carrying an em dash, copied from a heading GitHub does not render, passes the gate as generated navigation, and the link points at an anchor the page lacks. Reaching it needs deliberately crafted raw HTML, on both the base and the head versions.
- **Required outcome:**
  - No element whose position attribute the page itself could have written is taken as the renderer's own. For example, the guard is ASCII-case-insensitive, or such a page is refused and named through `refusals()` (see S2).
  - The limitation text in CONTRIBUTING 6.1, DOC_GENERATION.md and the module docstring matches the behaviour.
  - An arm fails when the case handling is removed.
- **Verification:** both forged pages list no `Old <em dash> heading` and exempt nothing through the shipped gate. The new arm kills the reverse mutant (guard back to case-sensitive). The lower-case arm still passes.

### F2 - MINOR - Robustness, Tests

- **Where:** `scripts/gen_toc_renderer.py:225-250`. `_nodes()` recurses once per container level.
- **Evidence** (`receipts/probe_nesting_depth.txt`):
  - A page nested 1200 block quotes deep, or 1200 list levels deep, raises `RecursionError`. Depths 600 and below answer.
  - `gen_toc.py --check` and `check_em_dash.py --base` both exit 1 with a traceback. The base walk answers the same page.
  - `check_em_dash.py` uses rc 1 for findings and rc 2 for "cannot judge" (renderer absent, unproven controls), so the crash reports the findings code.
  - The failure is closed (CI red) and nothing escapes.
- **Impact:** a pathological page takes the whole gate down with the wrong exit class. This is a regression against the base walk. Realistic pages stay far below the depth.
- **Required outcome:** such a page is answered (an iterative walk) or refused with rc 2 naming it, and an arm holds that.
- **Verification:** the depth-1200 block-quote and list pages give an answer or a named rc 2 refusal from both gates. The arm fails when reverted.

### F3 - MINOR - Tests, Conformance

- **Where:** `scripts/gen_toc_renderer.py:93-94` (`_OWN_ELEMENT`), read at `scripts/gen_toc.py:217-220`.
- **Authority:**
  - #437 acceptance 3: each new property carries an arm that fails when the property is removed.
  - `blocks()` docstring (`scripts/gen_toc.py:249-252`): "A block the HTML parse swallows renders as nothing and is COMMENT".
- **Evidence** (`receipts/mutation_own_element.txt`, `scripts/mutate_own_element.py`):
  - Dropping any one of `block_quote`, `list`, `code_block`, `thematic_break` or `table` leaves the TOC self-test at 1433/1433 and the em-dash self-test at 332/332.
  - Only dropping `heading` is killed.
  - The swallowed-block property is armed for paragraphs, items and headings only.
- **Impact:** a swallowed fence, table, thematic break or block-quote line can change its label with no arm failing. As measured, this affects only line labels, and so the wording of an em-dash finding. It does not affect headings, provenance or exemptions.
- **Required outcome:** each member whose removal is observable is held by an arm, for example a fence, a table, a thematic break and a block quote after a raw comment left open. A member whose removal is unobservable is recorded as such, with the reason; `list` may be one, since its items cover the same non-blank lines.
- **Verification:** the five mutants in `receipts/mutation_own_element.txt` are each killed, or recorded as equivalent with a reason.

### Suggestions (optional; they do not affect coverage)

- **S1 (Docs).** `docs/DOC_GENERATION.md` says "Each limit withholds a heading and grants no exemption". It does not point at the file-view divergence that CONTRIBUTING 6.1 records as an escape. A one-line pointer would keep the two pages consistent.
- **S2 (Robustness).** An owned page that merely mentions the attribute name in prose loses its headings. `--write` then deletes its Contents block, and `--check` reports TOC DRIFT (`receipts/probe_position_word_write.txt`). Routing that case through `refusals()` would be non-destructive and would name the page: such a page is left alone, neither written nor judged, as `main()` already does. This could be part of F1's fix.
- **S3 (Robustness).** An installed but import-incompatible html5lib (1.0.1 on CPython 3.12) is refused with rc 2, but reported as "not installed (collections)" (`receipts/refusal_drifted.txt`).
- **S4 (Tests).** Raw `template`, `noscript`, `object`, `option` and `frameset` shapes list their headings (`receipts/probe_edges.txt`). None has a recorded GitHub rendering, so recording some would widen the evidence beyond the committed set.

## Acceptance judgement (#437; #516 closes with it)

| # | Judgement | Evidence (reviewer-run unless stated) |
|---|---|---|
| 1 (restated, amended) | **Met on the committed set, by construction.** The #516 closure keeps one residual escape outside the set (F1). | See the notes below the table. |
| 2 | Met | The five family-two forms are listed. Their anchors `alpha`, `text`, `text`, `inner`, `q` equal the file-view ids in the published `markdown`-mode receipts (`receipts/ac2_family_two.txt`). The base withheld all five. |
| 3 | **Partly met** | Of 16 independent mutants, 14 are killed at named arms (`receipts/mutation_probes.txt`). M06 is equivalent unless positions can be forged (F1). The guard's case handling (F1) and five own-element kinds (F3) carry no arm. The pinned hosted install is held: dropping `--require-hashes`, un-keying the cache, deleting the install step or moving it each fail `ci_events.py --check`. |
| 4 | Met for navigation. The label differences are fixes, per the manager ruling. | See the notes below the table. |
| 5 | Met | See the notes below the table. |

Acceptance 1 evidence:

- TOC self-test 1433/1433 under CPython 3.14.7 and 3.12.13 with the lock installed from its hashes (`receipts/local_gates_toc_emdash.txt`, `receipts/lock_wheels.txt`). Every receipt hash, request and recorded heading list checks.
- Independent tally (`receipts/shape_base_vs_head.txt`): 221 shapes agree at base and head, 131 are fixed, 0 regress, and 0 disagree at head. Only the two N1 `github_only` footnote labels are set aside.
- The twelve #516 variants carry response bytes identical to the original 2026-09-22 receipts. GitHub renders no heading on any of them, and the head lists none (`receipts/i516_twelve_compare.txt`).
- Base arm inventory (`receipts/arm_inventory_compare.txt`, `receipts/arm_substantive_compare.txt`): every base arm page is still an arm page.
  - The removed arms are the 25 decision-site guards of the deleted walk, 2 CR fence arms (replaced by renderer CR arms) and 3 comment arms (replaced by `(renderer)` arms).
  - Every substantive label or heading change on an arm page has a recorded GitHub rendering, with two exceptions: the intended position-attribute arm, and a `-\t\titem` line that is now indented code, as CommonMark reads it.

Acceptance 4 evidence:

- Base and head walks over the same bytes of all 164 tracked pages (`receipts/tracked_pages_basewalk_vs_headwalk.txt`): refusals, the existing block, `generated_block`, `owns()` and `--write` output are identical, and `--write` changes no file (`receipts/write_noop.txt`).
- Headings are added on 6 pages: 5 history pages that own no Contents, and the TESTING.md h3 outside its plan.
- Labels differ on 11 pages. These are container fences, block-quote tables, item continuation text, and pipe lines outside tables at REGISTER_MAP.md:355-359, MILAN_V12_ROADMAP.md:135, TESTING.md:605 and TIME_SYNC.md:495.
- Each class is reproduced by a recorded GitHub rendering in the fixture's `corpus` set, whose HTML shows the same structure. Each is a correction.

Acceptance 5 evidence:

- These gates exit 0 under both interpreters at the head (`receipts/local_doc_gates.txt`, `receipts/local_ci_events.txt`): `gen_toc.py --selftest`, `--check` (106 pages), `--verify-anchors` (147), `check_em_dash.py --selftest` (332) and `--base 759da623` (0 findings over 75 lines). So do docs_check, doc style, doc paths, archive, feature status, the matrix, hygiene, TODO ownership, test evidence, `check_py_idiom.py` (long module 10 <= 10, long function 9 <= 9) and `ci_events.py --check` and `--selftest`.
- No budget file changed. `MIN_ARMS` rose from 707 to 1433. `check_em_dash.py` sits at exactly the 1000-line limit, not over it.
- The same gates pass in a clone with no submodule initialised (`receipts/no_submodules_py312.txt`).
- The hosted `docs-check` job at the exact head executed and passed (`receipts/hosted_docs_check_excerpt.txt`).

### Manager rulings and hosted install

- **File view as the reference (N2).** Reproduced from the published receipts (`receipts/recompute_fuzz.txt`).
  - Over the 700 fuzz pages, the renderer differs from gfm mode only on the 2 N1 footnote labels. It differs from the file view on 6: 4 withheld, 2 text differences, 0 escapes.
  - The two shape escapes (`text <? <!-- ?>` and `<div>` + `<? a <!-- ?>`) are confirmed from the published file-view receipts: the file view shows no heading.
  - Total 8, directions as CONTRIBUTING 6.1 states them. No tracked page carries `<?`, `<select` or `<xmp` as raw HTML (`receipts/scan_tracked_raw_html.txt`).
  - The ruling is consistent with the evidence, and 6.1 documents the family with its direction. S1 is only a cross-reference.
- **Hosted install.**
  - `docs.yml` installs the lock before the first consumer, with `--require-hashes` and a cache keyed by the lock's hash, and `ci_events.py` pins both steps.
  - The lock's hashes equal PyPI's cp312 and cp314 manylinux x86_64 wheels, and no sdist is listed (`receipts/lock_wheels.txt`, `receipts/pypi_cmarkgfm_2025.10.22.txt`).
  - The hosted run at the exact head used `ubuntu-24.04`: cache miss, locked install, then the em-dash, TOC and anchor gates passed. The interpreter is inferred as the image's CPython 3.12, since the cp312 wheel satisfied `--require-hashes`; the log does not print a version.
  - The `docs-check-no-git` replica passes with neither the renderer nor git (`receipts/refusal_no_renderer.txt`).
- **Refusal of other releases.** `cmarkgfm` 2024.11.20 makes both gates exit rc 2 and name the release (`receipts/refusal_drifted.txt`). A missing renderer gives rc 2 for both gates, while `check_hygiene.py`, which imports `gen_toc`, still runs. The html5lib and bundled cmark-gfm checks are armed (M08 and M14 killed).

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F3) | #437 acceptances 1-5 and #516 against `scripts/gen_toc.py`, `scripts/gen_toc_renderer.py`, `scripts/gen_toc_shapes.json`. Receipts: `receipts/shape_base_vs_head.txt`, `receipts/i516_twelve_compare.txt`, `receipts/ac2_family_two.txt`, `receipts/tracked_pages_basewalk_vs_headwalk.txt`, `receipts/probe_forged_position_emdash.txt` | R237-5 | `196cb7d99cb06631df514715979a5f82fbb1f7aa` |
| RTL | CLEAN | `receipts/rtl_scope.txt`: the diff touches no path under `hdl/`, `tb/`, `syn/`, `sw/` and no `.sv`, `.v` or `.svh`, and all four gitlinks are identical at base and head. `receipts/hosted_checkruns_196cb7d9.txt`: `verilator-suites` (5 executed shards) and `yosys-portability` (4 executed shards) succeeded at the exact head. No RTL scope is in the diff. | R237-5 | `196cb7d99cb06631df514715979a5f82fbb1f7aa` |
| Robustness | UNCLEAN (F1, F2) | `scripts/gen_toc_renderer.py` guard, `unquoted()`, `_nodes()`, lock checks; `scripts/gen_toc.py` `_page()`, `_rows()`, `_atx_text()`. Receipts: `receipts/probe_edges.txt`, `receipts/probe_nesting_depth.txt`, `receipts/refusal_no_renderer.txt`, `receipts/refusal_drifted.txt`, `receipts/probe_position_word_write.txt` | R237-5 | `196cb7d99cb06631df514715979a5f82fbb1f7aa` |
| Tests | UNCLEAN (F1, F2, F3) | `scripts/gen_toc_cases.py`, `gen_toc_renderer_cases.py`, `gen_toc_shape_cases.py`, `gen_toc_closer_cases.py`, `check_em_dash.py` self-test, `ci_events.py` pins. Receipts: `receipts/mutation_probes.txt`, `receipts/mutation_own_element.txt`, `receipts/arm_inventory_compare.txt`, `receipts/local_ci_events.txt` | R237-5 | `196cb7d99cb06631df514715979a5f82fbb1f7aa` |
| Docs | UNCLEAN (F1) | `CONTRIBUTING.md:574-616`, `docs/DOC_GENERATION.md:26-70`, `docs/testing/RUNNING_TESTS.md:127-140`, module docstrings of `gen_toc.py` and `gen_toc_renderer.py`, and the #437 and #516 threads and public packet, checked against `receipts/recompute_fuzz.txt` and `receipts/scan_tracked_raw_html.txt` | R237-5 | `196cb7d99cb06631df514715979a5f82fbb1f7aa` |

## Real limits of this round

- This reviewer made no live GitHub render.
  - Acceptance 1 and N2 are judged against the committed fixture and the published receipts.
  - F1's hidden heading rests on the recorded rendering of its underlying comment shape, not on a render of the forged page itself.
  - The shapes in S4 have no GitHub rendering.
- The gates ran under CPython 3.14.7 and a standalone CPython 3.12.13 build, not the hosted image. The hosted interpreter version is inferred.
- The full parent, protocol-processor, gPTP, Yosys and builder banks were not run. The manager's source banks at this head are public evidence and were not re-verified here.
- Physical calibration was NOT RUN, and field skips are not hardware proof. This change carries no hardware claim.
- The clone was restored and verified after every probe (`receipts/integrity_before.txt`, `receipts/integrity_after.txt`):
  - identical index hash, tree and `write-tree`;
  - every tracked blob hashes to its index entry;
  - on-disk modes match the index;
  - no untracked or ignored file remains;
  - the three required submodules sit at their gitlinks.

## Pending manager duties

- Candidate merge validation against live dev `26d855a9176d63625e6635a029a0c44e3d57ce9a`. The hosted `docs-check` already judged the PR merge ref, `[26d855a9..HEAD]`.
- act and hosted acceptance.
- The external review.
- Publication of this packet.
- Post-merge containment.

## Prior review findings

The prior rounds below were read only after the verdict and ledger above were written.

- **PR #538** carried no review findings when this round ended. Its only comments are the review-start notices 5803299272, 5803303887, 5805241854 and 5805442493, and it has no review objects. Nothing on it is to resolve or retain.
- **Superseded PR #515** had seven rounds: R237-1 to R237-4 and R238-1 to R238-3, read from `171736854c31:review-evidence/437-r1/reviews/`.
  - Every finding in them targets the hand-written walk: `scripts/gen_toc.py`'s old state machine, `gen_toc_html.py`, `gen_toc_containers.py`, `gen_toc_container_cases.py` and `gen_toc_container_walk.json`. None of that exists at this head; the lane started from dev `759da623`.
  - Every page those reports spell out is in the committed fixture byte for byte (`receipts/prior_shape_coverage.txt`). The reports that give only descriptions (R237-1, R238-1) are carried as `reconstructed` shapes.
  - Every one of those pages agrees with its recorded gfm rendering at this head (352/352).

| Prior finding(s) | Disposition at `196cb7d9` |
|---|---|
| R237-1 F1, R238-1 F1 and F2 (resumed-item and dedented-container shapes) | Resolved. The shapes are in the `R237` and `R238` sets as `reconstructed` and agree with GitHub |
| R237-1 F2 (the eleven historical cases) | Resolved under the restated acceptance 1: nine R86-5 descriptions map to nine named shapes, and a coverage arm holds them |
| R237-1 F3, R237-2 F3, R237-3 F4, R237-4 F3, R238-3 F3 (unarmed properties of the old walk) | Resolved by deletion: the code carrying those properties is gone. The renderer's own unarmed properties are this round's F1 and F3 |
| R237-2 F1 and F2, R237-3 F1 to F3, R238-2 F1 and F2 (content-column and rendered-comment regressions) | Resolved. All 17 R237-2 pages, the 13 R237-3 pages and the 22 R238-2 pages spelled in those reports are in the fixture and agree. One more R238-2 row is truncated with `...` in the report and cannot be checked |
| R237-4 F1, F2 and F4, R238-3 F1 and F2 (link-definition items, item-end shapes, fixture metadata) | Resolved. The R237-4 and R238-3 pages are in the fixture and agree, and the old fixture file is not in this tree |
| R238-2 F3 (documented escape inventory, `<select>`, PI shapes) | Resolved for gfm mode. The file-view difference on these shapes is the N2 limitation, which the manager ruled a documented, directed limitation and which this round reproduced (8/1052). It is not retained |
| #516 (the unclosed raw-comment family, closing with this lane) | The twelve variants are resolved. One residual escape is retained as this round's own F1 (forged upper-case position attribute), a new shape not published by any prior round |

R237-5 FINISHED

[R624] NEGATIVE - exact head ada26e56ac42ee5de311aef84cb86c8435b97cee

# R624-11: composition review of PR #725 (issue #629, lane B16) in the merge-train candidate

Role: independent composition reviewer, cleared context. Round R624-11.
Candidate: `ada26e56ac42ee5de311aef84cb86c8435b97cee`, tree `af715ad7841e88695ce0eaa845c0d3e154cfa424`,
parents `cdb49e7e` (the #726 candidate, tree equal to dev `e81ce82f`) and `f1b2489f` (PR #725's head).
Scope: composition acceptance only. Documents only; no bench, no hardware.

## Verdict in one paragraph

The merge itself is mechanically correct: `git merge-tree` of `cdb49e7e` and `f1b2489f` reproduces tree
`af715ad7` exactly, and the merged findings page equals the PR's page with dev's 7-line counter-law note
inserted after line 3, byte for byte. Every B16, B16b and B16c counter statement stays true under the note,
every link and anchor resolves, and every repository documentation gate passes on the candidate. However, the
B16 figures check as published (`tools/check_b16_figures.py`, packet `author-r10` at `5775cfa7`) keys
each row by the absolute line of the findings page. The note moves every one of those lines down by 7, so
the check fails on the merged page: 1,907 of 1,960 rows are BAD and 12,779 of 15,597 digits are UNCOVERED,
rc 1. A probe copy with every page row moved by +7, and nothing else changed, passes on the merged page.
Its rows, coverage and output equal the source-head run byte for byte once its line numbers are moved
back by 7. So no figure is wrong. But the merged page still says the check passes on it, and the published
check does not. That is finding F1, rated MINOR, so the verdict is NEGATIVE.

## The composition

| Item | Result | Evidence |
|---|---|---|
| Merge reproduces the candidate | `git merge-tree --write-tree cdb49e7e f1b2489f` = `af715ad7` = `ada26e56^{tree}` | `receipts/clone-integrity.txt` (tree); merge-tree output reproduced in this round |
| PR's changed files (vs its base `c20c85bd`) | `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, `docs/findings/README.md` | `git diff --stat c20c85bd f1b2489f` |
| Files a predecessor also changed (`c20c85bd..cdb49e7e`, 91 files) | exactly one: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md`, by `7b491e595` ([A605], #726): a 7-line counter-law note at lines 4-10, above the H1 | `comm` of both name lists; `git log c20c85bd..cdb49e7e -- <page>` |
| Candidate vs dev-side parent `cdb49e7e` | `M` on the same two files, nothing else | `git diff --name-status cdb49e7e ada26e56` |
| Merged page | byte-equal to the source page's lines 1-3, then `cdb49e7e`'s lines 4-10, then the source page from line 4 | `cmp` against that assembly |
| Merged `README.md` | byte-equal to the source head's | `git diff --quiet f1b2489f HEAD -- docs/findings/README.md` |
| Semantic interactions | the figures check's line-keyed rows (F1); the note's counter law against B16's counter statements (clean); links and anchors (clean); TOC, em-dash, docs-check and path gates (clean). No workflow, record pin, registry or gate inventory is touched | below |

## Manager's three questions

**(1) The merged page states both sides correctly.** The images B16, B16b and B16c ran on (`5603c353`), and
the page's earlier images (`ec0cc0c1`, `bbf704ec`), all predate `7b491e595`, the #726 counter change
(`git merge-base --is-ancestor` false for each). So the note's "the measurements below retain their
original image semantics" covers every B16 figure. The B16 counter statements, at candidate lines:

- 2420-2423: MEDIA_LOCKED and FRAMES_RX are the reference peer's listener's counters, not the DUT's.
- 2550-2551: these are the peer's STREAM_INPUT 0 counters.
- 2911-2912 and 3317-3318: the DUT's GET_COUNTERS "advanced with the binds". This is a direction under the
  original image law, with no count claimed.
- 3235-3241 and 3316-3319: MEDIA_RESET 0 to 4. The note keeps MEDIA_RESET on its interval law.
- 3242-3245 and 3319-3320: the CLOCK_DOMAIN LOCKED and UNLOCKED counts, which the note does not touch.

No B16 text mentions #726, per-AVTPDU counting, 32-bit wrap, or the new reset and retention rules, and
none contradicts them. Clean.

**(2) The B16 figures check on the merged tree.** Run with the pinned parser (cmarkgfm 2025.10.22, html5lib
1.1, installed by hash from `tools/markdown/requirements.txt` into a private environment). The check's
SHA-256 is `a9f36f9d…e540`, as published in `REVIEW-READY-r10.md`.

| Run | rc | Rows OK / BAD | Digits by row / by identifier / uncovered | MARKUP | Receipt |
|---|---|---|---|---|---|
| Source head `f1b2489f` (control, git-backed clone) | 0 | 1,960 / 0 | 12,988 / 2,609 / 0 | 0 | `receipts/figcheck/src.*`; rows and coverage TSVs byte-equal to the published `r10/figures-rows.tsv` (`ccaae4a0…`) and `r10/figures-coverage.tsv` (`f8cc3827…`); stdout byte-equal to `r10/figures-check.stdout` |
| Candidate `ada26e56`, check unchanged | **1** | 53 / **1,907** | 129 / 2,689 / **12,779** | 0 | `receipts/figcheck/cand.*` |
| Candidate, probe copy with page rows +7 (`scripts/shift_rows.py`: 1,934 rows moved, README rows unchanged, no other 4-digit constant outside the row block) | 0 | 1,960 / 0 | 12,988 / 2,609 / 0 | 0 | `receipts/figcheck/cand-shift7.*`, `receipts/figcheck/normalised-compare.txt` |

The note's digits (`2026-10-12`, `#726`, `6125741685`, `32`, `726`) lie on candidate lines 4-9. The
check's own `scope()` places them outside the covered text, because:

- the section starts at its `## Dev 5603c353` heading;
- the introduction's covered part starts at the paragraph line "In lane B16, the operator tried…";
- the Contents entry is matched by its own text.

The lowest page line in the probe's coverage is 25, and no block is refused. So the check excludes the
note by its existing rules, with no exemption for the note. But the check does not pass on the merged
tree, so question (2) is answered no; see F1.

**(3) Links.** `scripts/check_page_links.py` reads every `href` the pinned renderer emits:

- the bench page: 255 links, 26 relative paths, 190 fragments;
- the findings `README.md`: 30 links;
- `docs/testing/726_STREAM_COUNTERS.md`, the note's target: 10 links.

All resolve against `gen_toc.headings()` anchors (rc 0). A negative control with one broken fragment
and one broken path is caught: 3 misses, rc 1. Repository gates on the candidate, all rc 0, are listed
in `receipts/gates/SUMMARY.txt`:

- `docs_check.py`, under both the system and the pinned interpreter;
- `check_doc_style.py`;
- `gen_toc.py --check` (146 pages);
- `gen_toc.py --verify-anchors` (486 cross-page links);
- `check_em_dash.py --base cdb49e7e` (2,341 added lines, 0 findings) and `--base c20c85bd`, plus `--selftest`;
- `check_doc_paths.py` (974 paths);
- `ci_events.py --check` and `--selftest`;
- `ci_scope.py --selftest`;
- `git diff --check`, for `cdb49e7e..HEAD` and for `c20c85bd..f1b2489f`.

The em-dash gate first returned rc 2 under the system interpreter, which lacks the pinned renderer. It
named that cause and judged nothing, and was re-run under the pinned interpreter; those logs replace the
first ones.

## Findings

### R624-11-F1: MINOR. Lenses: Conformance, Tests, Docs

- **Where:** `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` in the candidate. Line 3533 says "A row
  gives the document line". Lines 4263, 4414 and 4585 say "With these changes the page passes". The
  artifact is the packet `author-r10/tools/check_b16_figures.py` (`a9f36f9d…`), lines 509-2521
  (`ROWS_TSV`), whose page rows hold absolute lines 2287-4609 of the source page.
- **Authority and evidence:**
  - The round 3 assignment ([6119906508](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119906508)) makes the check hold "the document line" per figure. Rounds 8 to 10 require that "the unchanged page passes".
  - The manager's composition question (2) requires that the check passes on the merged tree.
  - Dev's note (`7b491e595`) inserts 7 lines above every covered line. The unchanged check exits 1 on the candidate, with 1,907 rows BAD, mostly "figure not on the line, or claimed twice" and "line outside the covered text", and 12,779 digits UNCOVERED.
  - The +7 probe proves the cause is the line shift alone: rows, coverage and output equal the source run byte for byte after normalisation.
- **Impact:** Once merged, dev's page says the figures check passes on it, and anyone running the
  published check on dev's page as its usage line directs gets a failure. The executable evidence that
  binds every B16 figure to its receipt no longer verifies the page that lands. Every later reader of
  that page is affected. No figure is wrong, no bench verdict changes, and the check fails closed rather
  than passing falsely. This is not wording alone, since an executable check's stated result is false on
  the merged tree, so it is MINOR, not RESIDUE.
- **Required outcome:** Before merge, either of these.
  - A published check, with its spec and build regenerated as the packet does, whose unchanged run on the
    merge candidate's page exits 0: 1,960 of 1,960 rows, 0 uncovered, 0 MARKUP. Its hashes go in the
    packet, and the page and PR state which page it binds.
  - Or the page and PR bind the check's passing result to the source page explicitly, by commit or blob
    `844ff7fb`, so the merged page claims nothing the published check cannot show on it.
  - In either case, the check's earlier controls and probes keep their stated outcomes, or their changed
    line locators are stated.
- **Verification:** Re-run `scripts/reproduce.sh` (step 1, `cand`) with the new check on the new
  candidate: rc 0 and the totals above. Or confirm the binding text names the page the passing run read,
  and that the run on that page is rc 0.

No other finding.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Manager composition questions (1)-(3); issue #629 body; assignments [6117305187](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6117305187), [6119906508](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6119906508), [6130721355](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6130721355), [6132350672](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132350672), [6134101205](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6134101205); candidate page lines 4-10 against 2420-2423, 2550-2551, 2911-2912, 3235-3245 and 3316-3320; `receipts/figcheck/cand.stdout` | R624-11 | `ada26e56` |
| RTL | CLEAN. The composition does not touch it; for the PR's own scope it is covered by the two POSITIVE source reviews at `f1b2489f` | `git diff --name-status cdb49e7e ada26e56`: two Markdown files; no HDL, firmware, tool, workflow, record or pin changes in the PR (`c20c85bd..f1b2489f`) | R624-11 (composition); source reviews R624-10 and R625-10 | `ada26e56` (composition); `f1b2489f` (source) |
| Robustness | CLEAN | Packet check `scope()` (lines 2690-2707): content-anchored locators unaffected by the note. The unchanged check on the shifted page fails closed (rc 1, no false pass). Conservation and MARKUP refuse nothing in the note-adjacent blocks (0 MARKUP in all three runs). The note is outside every covered block (`receipts/figcheck/cand-shift7-coverage.tsv`, lowest page line 25) | R624-11 | `ada26e56` |
| Tests | UNCLEAN (F1) | `receipts/figcheck/*` (source control, candidate, +7 probe, normalised comparison); `receipts/gates/*` (every gate rc 0); `scripts/check_page_links.py` with its negative control | R624-11 | `ada26e56` |
| Docs | UNCLEAN (F1) | Candidate page lines 1-40 (note, H1, introduction), 91 (Contents), 3519-3626 and 4124-4609 (check rules and "the page passes" claims); `docs/findings/README.md` row line 15; `docs/testing/726_STREAM_COUNTERS.md` links; TOC, anchor, em-dash, docs-check, style and path gates | R624-11 | `ada26e56` |

## Real limits

- Composition only. The PR's own content at `f1b2489f` was not re-reviewed beyond what composition reads.
  Its figures were re-verified only through the published check: source control rc 0, and the merged page
  via the +7 probe. Its receipts were not re-derived from raw bench data.
- The figures check, its spec and the receipts come from the public packet at `5775cfa7`
  (`author-r10`). Their trust rests on that packet and on the source reviews. Only the check's hash was
  matched against the published review-ready table.
- No bench, hardware, Docker or act, and no hosted run inspected. Physical calibration was NOT RUN, and
  field skips are not hardware proof. No manager source bank was claimed or inferred.
- External links (60 on the page) were listed, not fetched.

## Pending manager duties

- Decide F1's route: regenerate the check for the merged lines, or bind the passing claim to the source
  page. Then re-run this composition check on the new candidate.
- Validate the final current-dev merge candidate (builder and native banks) at the merge turn, and link
  its receipts on the PR.
- Own hosted and act acceptance at the exact candidate head.
- Carry R624-10-R1, which is still open in the PR body, to the residue checklist.

## Probes and restoration

All probes ran on copies under `scratch/`: the source-head clone, the shifted check and the link probe
tree. The review clone's only change was the Python bytecode cache the gate runs wrote under
`scripts/__pycache__`. It was created in this session, is ignored by git, and was removed. After removal:

- HEAD is `ada26e56`;
- `git write-tree` = `af715ad7`;
- there is no index or worktree diff and no untracked or ignored file;
- the gitlinks are unchanged (`external` `efeb541a`, `gptp-processor` `7dda9c3b`, `protocol-processor`
  `2ad2f845`, `third_party/lwSRP` `08ee86e8`, `third_party/verilog-axis` `48ff7a7e`).

Receipt: `receipts/clone-integrity.txt`.

## Prior findings

Read only after the verdict and ledger above were written. They do not change either. The source
reviews named in the ledger are:

- [R624-10](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6137929166), POSITIVE;
- [R625-10](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6137837087), POSITIVE.

Both are at `f1b2489f`, with all five lenses clean.

| Finding | Status at `ada26e56` | Evidence |
|---|---|---|
| R624-1 to R624-9 and R625-1 to R625-9: every F finding, including R624-9-F1, R625-8-F1 (settled by decision 6132293481) and the PR-body findings R625-9-F1, R624-9-R1 and R625-9-R1 | RESOLVED, held in content. The PR's text is byte-identical in the candidate; the merged page is the source page plus the note | `cmp` of the assembled page; the source-head check run is byte-equal to the published `r10` receipts |
| The same findings' executable re-verification on the merged page | RETAINED under R624-11-F1. Each standing control and probe, and the check itself, names bench-page lines by number, and on the merged page every such line is 7 lower. Examples: `:18` becomes `:25`, `:2301` becomes `:2308`, and the footnote locator `4604` becomes `4611`. `README.md:15` is unchanged | `receipts/figcheck/cand.stdout` |
| R624-10-R1, RESIDUE (PR body line 500: "Local commit: `f1b2489f…`, not pushed.") | OPEN as RESIDUE. The live PR body still carries it (fetched read-only this round). Wording only; carried to the manager's residue checklist with R624-10's exact fix: "Commit: `f1b2489f5b1c929e81eeae79a469b2b27c47e340`, the PR head." | `GET /pulls/725` body, line 500 |
| R624-10-S1, SUGGESTION (an ordered list's displayed numbers are not judged) | Unchanged by the composition; optional | Not re-run; the note adds no list to the covered text |
| R624-10-S2, SUGGESTION (a numeral entity outside the covered part refuses the index cell) | Unchanged by the composition; optional. `README.md` is byte-equal to the source | `git diff --quiet f1b2489f HEAD -- docs/findings/README.md` |

R625-10 reports no new finding or residue.

R624-11 FINISHED

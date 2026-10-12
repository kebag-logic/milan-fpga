[R624] NEGATIVE - exact head cb5ff79f1f69117efba353484851eceb620e5c92

Round R624-9. Internal, independent, cleared-context review of issue #629 / PR #725 (bench lanes B16, B16b and B16c, documents only), round 9 of the findings. Head `cb5ff79f1f69117efba353484851eceb620e5c92`, tree `6467d108ba0ddd10bf252fe0a241f90e090cefc3`, source base `c20c85bd`.

**Verdict.** One new MINOR is open, R624-9-F1, under Conformance, Robustness, Tests and Docs. RTL is CLEAN. All five lenses were applied. R624-8-F1 is resolved at this head. R625-8-F1 is resolved by the manager's decision 6132293481, which the page and the PR body now record. Every earlier public finding stays resolved. One RESIDUE, R624-9-R1, is PR-body wording only. No finding alleges a DUT defect, and no bench figure, bench verdict or receipt is wrong: every one of the section's 1,909 figure rows equals its receipt at this head.

The new MINOR: the pinned parser gives no source position (line 0) to a link that the GFM autolink extension makes from a bare e-mail address (`x@example.com`, `mailto:x@example.com`), to the link's text, and to the rest of the text node after it. The check then places those characters at the start of the enclosing block. For the page's introduction, that start is line 6, which is not covered. For the index row, it is the cell's first column, which lies before the covered part's column. So a measurement written after such an address on a covered line is never read. `x@example.com 7 ppm`, added to the introduction's second covered line, to the index row's lane B16 part, or to both, leaves the check at exit 0 with 0 uncovered and 0 refused. The repository's documentation gates also pass that altered tree.

## How the task was reconstructed

Read in order:

1. `AGENTS.md` and `CONTRIBUTING.md` (section 6: wording, privacy, the pinned renderer and the em-dash gate).
2. `docs/README.md`.
3. Issue #629's body and its [A10] comments: the B16 assignment 6117305187, the rulings 6117672835 and 6118365090, and the round assignments 6119316763, 6119906508, 6121193402, 6125608002, 6126774639, 6128175910, 6130721355 and 6132350672, with the decision 6132293481.
4. The author's public STOP and REVIEW READY comments (6117604151, 6118143691, 6118971388, 6133625420).
5. `git diff c20c85bd..cb5ff79f` (two files: `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` +2162 lines, `docs/findings/README.md` row 15) and its 12 commits, then `git diff b522bb92..cb5ff79f` (round 9).
6. The published packet on `629-b16-review-evidence` at `4ab00ba575cf1ea2ab17c232886637524c9876cb` (`review-evidence/629-b16-r1/author-r1/` to `author-r9/`, `MANIFEST.json`).

Prior public review reports were read only after my own pass over the diff and my own probe; that pass found F1. No private material was read.

## Round 9 assignment, item by item

| Item | Result at `cb5ff79f` | Evidence |
|---|---|---|
| 1. Real extent: a construct off the allowlist refused at the first covered line its actual source reaches; `html_block` from its literal; every node kind whose end the parser may under-report | Met for the kinds the round names. NOT met for a node the parser leaves with no position at all: R624-9-F1 | `extents()` and `blocks()` in `tools/check_b16_figures.py` (`bafea39b...`); `r9/parser-extents.json` reproduced byte-equal, 37 of 37; `receipts/parser-nodes/dump.txt`; `receipts/probe_r624_9_autolink.json` |
| 2. R624-8's `probe_r624_8_html_block_edge.py`, unchanged (`106710c3...`, equal to the published `reviews/R624-8/tools/` copy) | `intro_pre_from_line_above_with_figure`: exit 1, `MARKUP 629_MEDIA_CLOCK_FOLLOWING_BENCH.md:18 html_block <pre>`, DETECTED (was ESCAPED in R624-8). The other 12 cases keep their exit status and verdict | `receipts/reruns/r624-8-html-block-edge.json`, `receipts/reruns/r624-8-compare.json` |
| 2. Round 8 runner, the 13 review probes, the unchanged page | Round 8 runner 73 of 73. The 14 probe reruns are byte-equal to the published `r9/*-probe-rerun.json`. Every status and verdict equals round 8's, and the only differences are the check's summary counts, its hash and the moved footnote line (4274 to 4424). Unchanged page exit 0 | `receipts/reruns/rerun-r8-controls.json`, `receipts/reruns/probes/`, `receipts/reruns/probe-readings-r8-vs-r9.json`, `receipts/check-at-head.*` |
| 3. Texts; decision 6132293481 recorded where the earlier runners' outcomes are listed | Met. Round 8's "Earlier expectations" (`:4192-4205`) and runner list (`:4226-4233`) point to the decision. Round 9's "The decision" (`:4343-4355`) records 5/5, 7/8, 21/22, 38/39, 48/50 and 73/73, "not reported as wholly green". The index row and the PR body state the round 9 rule. R624-8-S1 is taken as a stated limit (`:4401-4405`). The location paragraph (`:2616`) maps round 8 to `author-r8/` (`b522bb92`, `b0134c63`) and names `author-r9/`, published at `4ab00ba5` | Reruns of the r3 to r8 runners byte-equal to `controls/r9-rerun-r*-controls.json`. Every FAIL is a superseded expectation: "a figure with its unit added as a link label" (r4 to r7) and "a comment inside a code span" (r7). `receipts/reruns/evidence-receipt.json` is byte-equal: 5,646 entries, 98 of 98 rows, 770 of 771 |

The check at the head, run by me in a fresh environment installed from `tools/markdown/requirements.txt` with `--require-hashes`, exits 0:

- 1,909 rows, all OK;
- 14,956 digits: 12,531 in rows, 2,425 in identifiers, 0 uncovered;
- 0 constructs refused.

Its rows and coverage are byte-equal to the published `r9/figures-rows.tsv` and `r9/figures-coverage.tsv`. `r9_figures_build.py` regenerates the check byte for byte.

## Findings

### R624-9-F1 - MINOR - Conformance, Robustness, Tests, Docs

**Where:** the packet's `tools/check_b16_figures.py` (`bafea39b3af1d6ba654cfbfc8c2feaf30e147a0abb5e8226650108d1e3238f11`), `blocks()`: `if not sl: sl, sc = xs, xc`, with `xs, xc` taken from `par[-1]` when the node has no extent, and `place()` when the node's end is 0. Stated at `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4139-4150`, `:4297-4341`, `:4407-4409` and `README.md:15`.

**Authority and evidence:**

- Round 5's frozen rule requires every digit of the covered text to lie in a row's figure or a bound identifier.
- Round 8 requires the check to judge the visible inline text the parser yields, with source maps for line numbers.
- Round 9 item 1 extends the extent rule to "every node kind whose end the parser may under-report".

The pinned cmark-gfm, through the gates' extensions (`table, strikethrough, autolink, tagfilter, tasklist`), reports a bare e-mail autolink with no position at all (`receipts/parser-nodes/dump.txt`, document `a3.md`): `link rep=(0,0)-(0,0)`, its text `(0,0)`, and the trailing `' 7 ppm'` text node `(0,0)`. A bare `https://` or `www.` autolink, a core `<...>` autolink and an entity are reported correctly (`a1.md`, `a2.md`, `a5.md`, `a6.md`). The check gives such nodes the enclosing block's first line and column, so their characters are never read:

| Case (`tools/probe_r624_9_autolink.py`, one phrase appended to a covered line, no line moved) | Exit | Result |
|---|---|---|
| unchanged page | 0 | OK |
| intro line 19 `+ " Write to x@example.com 7 ppm."` | 0 | **ESCAPE**: nothing named |
| intro line 19 `+ " x@example.com, 7 ppm."` | 0 | **ESCAPE** |
| intro line 19 `+ " Write mailto:x@example.com 7 ppm."` | 0 | **ESCAPE** |
| intro line 19 `+ " x@example.com: 7 ppm, 26 s, -3 dB."` | 0 | **ESCAPE** (three measurements) |
| `README.md:15` `+ "; write to x@example.com 7 ppm."` | 0 | **ESCAPE** |
| intro and index together | 0 | **ESCAPE** |
| intro line 19 with `www.example.com` / `https://example.com` / no link | 1 | DETECTED, `UNCOVERED ...:19 7` |
| section paragraph, first and a later line, and a table cell, with the e-mail form | 1 | DETECTED, but a later line's figure is named at the paragraph's first line (2301 for 2302) |

Round 8's check at `b522bb92` gives the same escapes (`receipts/probe_r624_9_autolink_on_r8_check.json`), so this is not new in round 9. It is in round 9's scope, though: the parser under-reports this node completely, and `r9/parser-extents.json`, `r9/self-probes.json` and `controls/r9-controls.json` try no e-mail autolink. The repository's gates do not stop the escape: on the altered tree, `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check` and `--verify-anchors` and `check_doc_paths.py` are all rc 0 (`receipts/gates_on_escape.log`).

**Impact:** a measurement can be added to the introduction's lane B16 part or to the index row with no receipt row while the check passes. That is the class the check exists to close. The page's and the index row's statements that the check judges the visible text it covers do not hold for this form. No figure on the page is wrong today.

**Required outcome:**

- No visible character of the covered text is silently dropped. A node the check reads or judges, other than a soft or hard break, whose reported start line is 0 is either placed at its true source line and column or makes its whole block refused (named, at the first covered line the block reaches). The e-mail and `mailto:` forms of the autolink extension and any other node the parser leaves without a position are included.
- The page, the index row and the PR body state the rule as it then holds.

**Verification:**

- `probe_r624_9_autolink.py`, unchanged, exits with every `detect` case exit 1, each naming its 7 at the true line (19 or `README.md:15`) or refused there, and the unchanged page passing.
- The parser-extents audit gains the zero-position kinds.
- A standing control per form fails on round 9's check and passes on the fix.
- Every earlier runner, probe and the unchanged page keep their outcomes.

### R624-9-R1 - RESIDUE - Docs

**Where:** the PR #725 body, "Round 9", item 2, first sub-bullet: "the earlier probes give round 8's readings byte for byte, but for R624-7's `footnote_ref_and` form: ...".

**Why:** the 13 earlier probe-rerun files are not byte-equal to round 8's. Their statuses, verdicts and named lines are equal, but each carries the check's summary counts, which grow with the page (for example 14,442 to 14,956 digits), and R625-6's carries the check's hash (`receipts/reruns/probe-readings-r8-vs-r9.json`). The page's own wording (`:4388-4390`, "give what round 8's record shows") is accurate. This is PR-body wording only and changes no figure, verdict or test.

**Exact fix:** replace "give round 8's readings byte for byte, but for" with "give round 8's exit statuses, verdicts and named lines (their summary counts and the check's hash follow the new page and check), but for".

## Earlier public findings at this head

| Finding | Lenses | Status at `cb5ff79f` | Evidence |
|---|---|---|---|
| R624-8-F1 (`<pre>` block from the line above the introduction) | Conformance, Robustness, Tests, Docs | RESOLVED | My unchanged probe: DETECTED, `MARKUP ...:18 html_block <pre>`; 24 new standing controls fail on round 8's check, pass here |
| R624-8-S1 (emoji shortcode, link title) | Docs, Tests | TAKEN as stated limits | `:4401-4405`; the probe's cases keep PASS |
| R625-8-F1 (changed earlier expectations) | Conformance, Tests, Docs | RESOLVED by decision 6132293481 | Recorded at `:4201-4205`, `:4230-4233`, `:4343-4355` and in the PR body; the reruns fail only the two superseded controls |
| R624-7-F1 (image syntax), R625-7-F1 (index-row crash) | Conformance, Robustness, Tests, Docs | RESOLVED, held | R624-7's and R625-7's probes, unchanged, give round 8's statuses (no escape; 4 index cases MARKUP at `README.md:15`, receipts written) |
| R625-6-F1, R625-5-F1, R624-5-F2, R624-4-F1, R625-4-F1, R625-3-F1 | Conformance, Robustness, Tests, Docs | RESOLVED, held | The unchanged probes' statuses equal round 8's (`probe-readings-r8-vs-r9.json`) |
| R624-5-F1, R624-6-S2 (line-3200 rows) | Tests, Conformance | RESOLVED, held | Both row probes MISMATCH at line 3200, byte-equal reruns |
| R624-3-F1, R624-5-F3 (where the packet is) | Docs | RESOLVED | `:2608-2616` through `author-r8/` (`b0134c63`), naming `author-r9/` (`4ab00ba5`); evidence receipt byte-equal |
| R624-1-F1 = R625-1-F3, R624-1-F2 = R625-1-F4, R625-1-F1, R625-1-F2, R624-2-F1, R624-2-F2, R625-2-F1 | Conformance, Robustness, Tests, Docs | RESOLVED, held | Text unchanged since round 8. The check's rows are OK, and my independent recomputation agrees (below) |
| R624-1-R1/R2, R625-1-R1/R2, R624-2-R1/R2/R3, R624-5-R1 | Docs | RESOLVED, held | Text unchanged; PR title as requested |
| R624-1-S1/S2, R625-1-S1, R624-2-S1/S2, R625-2-S1, R625-3-S1, R624-4-S1, R624-5-S1, R624-6-S1 | Docs, Tests | TAKEN, held | Text unchanged |

## Bench content checked independently (Conformance, RTL)

`tools/spot_check.py` recomputes the headline grades from the per-block receipts, not from the receipts' own summaries or the author's check (`receipts/spot_check.json`):

- **B0, `b0-2`.** 300 blocks, 0 events. The joint floor holds 169 blocks: -123.98 (-123.91) dB at 997 Hz and -123.95 (-120.18) dB at 9,973 Hz. All blocks give -123.95 (-100.47) and -122.80 (-80.48) dB. 131 blocks are degraded, in runs 0-18, 28-31, 43-44, 46-54 and eleven later runs; 23 of them lie in blocks 0-33. Phase moved 0.0005 frames; the largest offset is 0.030 ppm.
- **Sample comparisons, `b0-2`.** (c) against (a) is SAMPLE-EXACT over 1,637,452 frames, and (c) against (b) over 1,637,980.
- **B-CRF, B-AAF.** All 300 blocks are at the floor in each case: -123.98 (-123.93) / -123.97 (-123.90) and -123.98 (-123.92) / -123.97 (-123.91) dB, with 0 events.
- **Sample comparisons, B-CRF and B-AAF.** 1,647,859 + 1,641,156 = 3,289,015 frames against (a), and 1,646,473 + 1,644,390 = 3,290,863 against (b), 0 differing.
- **`SLIP_LB`.** B-CRF has 5 steps with the servo IDLE between the binds and the set, plus 1 in ACQUIRE. B-AAF has 5 plus 2. None falls after LOCKED.
- **Clock sources.** In `runs/bcrf/events.jsonl` and `runs/baaf/events.jsonl` the peer goes to 0 (read back 0), the DUT to 1 or 2 (read back), the DUT back to 0, and then the peer back to 1, its CRF input (read back 1), in each case.
- **B16's loopback.** In `summary/loop2/acmp-peer-tap.json`, CONNECT_RX_RESPONSE and CONNECT_TX_COMMAND (PROBE_TX) come 99.6 ms after the controller's DISCONNECT_RX_COMMAND, with no CONNECT_TX_RESPONSE. Identities are redacted.

The page's attribution separates what is shown inside the taps' overlap (23 blocks) from inference (108 blocks). The source's route and clock changes are attributed outside the lane. Lane B6's timed ratio and Direction B's INTERNAL mismatch control are stated NOT RUN (`:3202-3207`, `:3321`, `:3326`, `:3344`, `README.md:15`). The reference peer and the external capture are named by role only. The diff holds no host path, address or identity (scan and `docs_check.py` rc 0).

## Lens results

- `[R624] MINOR Conformance - tools/check_b16_figures.py blocks(); docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4139-4150, :4297-4341 - R624-9-F1: text after an e-mail autolink is never read.` The other Conformance items were applied and hold: the round 9 items 1 to 3 table above; the bench figures against `author-r9` receipts (the check's 1,909 rows OK at the head, my spot check); the rulings 6117672835 and 6118365090 against `:2635-2659`, `:2992-3104` and `:3317-3329`.
- `[R624] PASS RTL - git diff --stat c20c85bd..cb5ff79f (2 Markdown files; no hdl/, firmware, tb/ or script change) and the DUT-behaviour claims at :2847-2856, :3165-3238 checked against summary/*/align-*.json, c-b9-grade.json, r2/*-poll-receipt.json and runs/*/events.jsonl - no RTL artifact in scope; every DUT claim (sample-exact render, no discontinuity, servo LOCKED at 596 of 596, SLIP_LB steps only before LOCKED, SLIP_TDM static, no DUT change) equals its receipt.`
- `[R624] MINOR Robustness - the check under an e-mail autolink on a covered line (receipts/probe_r624_9_autolink.json) - R624-9-F1.` Also applied: 13 R624-8 cases, 14 review probes, 97 controls, 156 self-probes, 37 extent cases; the restore records (`restore/census-compare*.txt`, events) and the dry-run controls are unchanged since round 8.
- `[R624] MINOR Tests - r9/parser-extents.json, r9/self-probes.json, controls/r9-controls.json (none tries a zero-position node) - R624-9-F1.` Also applied:
  - each new control fails on round 8's check (`controls/r9-controls-on-r8-check.json` reproduced: 73 PASS, 24 FAIL);
  - the rebuild from `r9_figures_spec.py` is byte-equal;
  - the key scan is byte-equal;
  - `r9_reader_on_r8.py` is byte-equal;
  - the probe copies equal the published reviewer originals (14 of 14 SHA-256).
- `[R624] MINOR Docs - docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md:4139-4150, :4407-4409, README.md:15 - R624-9-F1: the rule as stated does not hold for zero-position nodes;` RESIDUE R624-9-R1 in the PR body. Also applied:
  - 14 gates rc 0 at the head (`receipts/gates/`);
  - 105 of 105 packet-file hash rows equal their `author-r9` files; no row names any of the 65 path-redacted files, and the 65 `MANIFEST.sha256` mismatches are exactly the 65 `path_redacted` entries;
  - the location paragraph, the introduction, the Contents line, the index row and the PR title.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R624-9-F1) | Issue #629 assignments, rulings and decision; findings `:2287-4424`, `README.md:15`, PR body; `author-r9` receipts, summaries, runs, `r2/`; check at the head | R624-9 | cb5ff79f1f69117efba353484851eceb620e5c92 |
| RTL | CLEAN | `git diff --stat c20c85bd..cb5ff79f` (docs only); DUT-behaviour claims against align, grade, poll and event receipts | R624-9 | cb5ff79f1f69117efba353484851eceb620e5c92 |
| Robustness | UNCLEAN (R624-9-F1) | `check_b16_figures.py` `tree()`/`extents()`/`blocks()`/`place()` under my 15 autolink cases, R624-8's 13 cases, 14 probes, 97 controls, 156 self-probes; restore records | R624-9 | cb5ff79f1f69117efba353484851eceb620e5c92 |
| Tests | UNCLEAN (R624-9-F1) | Check `bafea39b...`, rebuild, controls r3 to r9 and r9-on-r8, parser extents, key scan, reader-on-r8, probe reruns, my probe | R624-9 | cb5ff79f1f69117efba353484851eceb620e5c92 |
| Docs | UNCLEAN (R624-9-F1; RESIDUE R624-9-R1 does not affect coverage) | Round 8 and 9 subsections, location paragraph, intro, Contents, index row, PR title and body; 14 gates; 105 hash rows; manifest and redaction | R624-9 | cb5ff79f1f69117efba353484851eceb620e5c92 |

## Real limits

- Documents only: no bench, no hardware, no physical calibration. Printed precision is not calibrated accuracy.
- Raw captures stay on the bench host and were not read. Bench figures were checked against the retained reduced and summary receipts only.
- The B16 loopback and B16b/B16c runs are one run per case, as the page states.
- No manager source bank was run or inferred at this head.
- Hosted evidence at this head, read once (`receipts/hosted-checks.tsv`):
  - completed with success: Yosys shards 0 to 3, the firmware mutants and unit tests, yosys-elaboration, verilator-lint, bdd-conformance, docs-check-no-git, full-ci-gate and others;
  - skipped: Physical gPTP;
  - still running or queued: rtl-fast, docs-check, elaborate and Verilator shards 0 to 4.
- The probes edit copies only. The clone stayed at the exact head, tree `6467d108...`, with a clean status, index and worktree and its five gitlinks as recorded (`receipts/clone-integrity.txt`).

## Pending manager duties

- Hosted and act acceptance at the exact head: the running rtl-fast, docs-check, elaborate and Verilator contexts.
- The current-dev merge-candidate validation (builder and native banks; source base `c20c85bd`, live dev `dc4d06cbfec209cc2ff76806f4b49c51f46639ae`) at the merge turn.
- Carrying R624-9-R1 to the residue checklist.
- A round for R624-9-F1.
- #629 stays open in any case: Direction B's INTERNAL mismatch control, lane B6's timed ratio for B-CRF and B-AAF, and #645.

## Receipts

Every published file is listed with its SHA-256 in `MANIFEST.sha256`. Paths are relative to the review packet.

- **Scripts.** `tools/probe_r624_9_autolink.py` (the escape probe), `tools/dump_nodes.py` (the parser's nodes as the check reads them), `tools/gates_on_escape.sh`, `tools/spot_check.py`, `tools/compare_r624_8.py`, `tools/compare_probe_readings.py`.
- **Probe results.** `receipts/probe_r624_9_autolink.json`, `receipts/probe_r624_9_autolink_on_r8_check.json`, `receipts/parser-nodes/`, `receipts/gates_on_escape.log`, `receipts/spot_check.json`.
- **Check at the head.** `receipts/check-at-head.stdout`, `.rows.tsv` and `.coverage.tsv`.
- **Re-runs.** `receipts/reruns/` (byte-equal re-runs, R624-8's probe and its comparison, the probe readings).
- **Gates and environment.** `receipts/gates/` (14 gates), `receipts/hosted-checks.tsv`, `receipts/clone-integrity.txt`.

R624-9 FINISHED

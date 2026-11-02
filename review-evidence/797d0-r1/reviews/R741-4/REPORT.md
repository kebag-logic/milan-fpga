[R741] POSITIVE - exact head 8d8c2e366a2d49506b91a195de0094a440e7bc39

Internal independent review, round R741-4, PR #815 / issue #797 lane D0. Tree `24d3429b66ec52b7fb48782fbb78d289abab668b`. Delta judged: `808602e0..8d8c2e36`, three commits, four files.

## Verdict basis

All five lenses are clean at this head. No BLOCKER, MAJOR or MINOR is open. Two wording residues and four suggestions are recorded below.

This verdict does not clear the hosted bar. **`rtl-full` was cancelled at this head, so `verilator-suites` and `yosys-portability` have no exact-head result.** The cancellation came from a hosted watcher timeout, not from a failed job (check 2). The manager owns that acceptance.

| Focus check | Result | Evidence |
|---|---|---|
| (1) D0-063 to D0-065 keep their meaning; the source-list gate passes, untouched | PASS | See check 1 |
| (2) Hosted `rtl-fast` at this head | Context `rtl-fast` **success**; source-list step success; run conclusion **cancelled** | See check 2 |
| (3) Search catches the planted forms and adds no row on the real tree | PASS, 28 of 28 plants graded correctly; 87 rows before and after | See check 3 |
| (4) Residue applied | Three of four resolved; the PR-body item now needs a new fix (R1) | See prior findings |

### Check 1: citations and the source-list gate

- With the respelling undone, each of the six D0-063 to D0-065 cells equals its round-3 text except for one added comma per citation. The only other change is D0-064's `(line 3621)` becoming `(lines 3621-3622)` (`receipts/citations-diff.txt`).
- `protocol_processor_top.sv` is unique in the submodule at pin `a9e84b66`. I re-read the cited lines 3593-3595, 3621-3622 and 3624-3648, and each says what the cells claim.
- `python3 -I scripts/pp_srcs.py --check --selftest` gives rc 0 (`receipts/pp_srcs-check-selftest.log`).
- `git diff 1f29f189 8d8c2e36 -- scripts/pp_srcs.py` is empty, so neither the gate nor its permitted list changed.

### Check 2: hosted runs at this head

Snapshot taken 2026-11-02 at 01:16 UTC (`receipts/hosted-runs.tsv`, `receipts/hosted-rtl-fast-jobs.tsv`, `receipts/hosted-rtl-full-jobs.tsv`, `receipts/hosted-cancel-cause.txt`).

| Run | Conclusion | What executed |
|---|---|---|
| `docs` 41358971769 | success | All 9 jobs succeeded, including step "Documentation inventory freshness gate" |
| `elaborate` 41358971702 | success | All 6 jobs succeeded |
| `rtl-fast` 41358971669 | **cancelled** | 15 of 16 jobs succeeded, including context `rtl-fast` and `verilator-lint` step 10, which printed "46 tracked source(s) derived ... (self-test passed)" |
| `rtl-full` 41358971729 | **cancelled** | 12 of 19 Verilator and 1 of 4 Yosys shards succeeded; the rest were cancelled. `Physical gPTP` was skipped |

The cause, read from the logs:

1. The `rtl-fast` watcher "Fail fast across this head" has `timeout-minutes: 120`. Its observe step ran from 23:12:04 to 01:12:12 and ended "The operation was canceled", because the jobs were still queued or running.
2. No job in that run had failed. `Cancel late CI failures` (`scripts/ci_fail_fast.py tail`) counts a `cancelled` need as a failure, and logged `Cancelled runs: [41358971729, 41358971669]`.
3. The `rtl-full` failures are all consequences: six `Union ...` jobs, `verilator-suites` and `yosys-portability` report cancelled owners ("one or more ... workers ended: cancelled").

The PR does not touch `scripts/ci_fail_fast.py`, `rtl-fast.yml` or `rtl-full.yml`. Three other recent `rtl-full` runs on other heads also read cancelled; I did not read their causes. So I attribute this head's cancellation to the watcher and queue, not to its content. An executed job has passed for only part of the `rtl-full` work, so that part remains unproved.

### Check 3: cross-page search

**Real tree.** The ID, page and line of all 87 rows are identical at `808602e0` and `8d8c2e36`. The page differs in only 4 lines, the D0-024, D0-063, D0-064 and D0-065 rows. Counts are 212 documents, 166 current, 25 stale, 21 obsolete, 22 copy rows, and no row reads "re-verify" (`receipts/real-tree-rows.txt`).

**Plants.** I wrote 28 plants of my own on new pages in a disposable clone (`scripts/plant_forms.py`, `receipts/plant-forms.txt`). `--check` gave rc 1 after planting, and rc 0 after `--write`.

- **Should get a row (24 of 24 got a row and a stale page):**
  - underscore emphasis: whole, double, around a code span, and mixed with asterisks;
  - links: inline with a title, reference, wrapped over lines, and image;
  - sentence ends: comma, semicolon, colon, and none;
  - each `also` sentence of the ten entries, including both of D0-036's.
- **Should get no row (4 of 4 got none, page stays current):** an inner `_`, a longer word, an unrelated link, and a statement split by a blank line.
- **Line numbers:** two wrapped links sit above each plant, and every row still cites the plant's real line 7.

Three notes on reading that receipt:

- My first grader run expected line 6, which was my own off-by-one. The published receipt is the corrected run, and the row lines did not change.
- The D0-058 plant gets its row under D0-040, which records the same words. That is the documented `held` behaviour, and the page still gets one row and goes stale.
- The D0-036 plant could match through either `also` entry, so it does not separately prove the comma strip. `receipts/needle-direct.txt` proves that directly.

## Findings

No BLOCKER, MAJOR or MINOR.

### R1 - RESIDUE - Docs - PR #815 body lines 16, 42 and 99 - the hosted status is stale again

- **Authority/evidence:** the head is pushed and hosted runs exist, but the body says "GREEN locally, hosted not yet run" (line 16) and "Head `8d8c2e36` has no hosted run until it is pushed" (line 99). Line 42 says the body states the hosted result. Snapshot: `receipts/pr-body-snapshot.md`.
- **Impact:** a cold reader is told hosted evidence does not exist. No measurement, code or verdict changes.
- **Required outcome, exact fix, using the result current when applied:**
  - Line 16: replace "hosted not yet run" with "hosted at `8d8c2e36`: `docs` and `elaborate` success; `rtl-fast` context success, run cancelled by its 120-minute watcher; `rtl-full` cancelled by that watcher's tail, so no exact-head `verilator-suites` or `yosys-portability` result".
  - Line 99: replace the final sentence with the same result.
- **Verification:** read the body against `gh run list --commit 8d8c2e36`.

### R2 - RESIDUE - Docs - `scripts/docs_inventory.py:32`, PR body line 41 - "the punctuation ending it" is wider than the code

- **Authority/evidence:** `needle_of()` at `scripts/docs_inventory.py:374` strips only `.,;:`. `All five!` and `All five?` keep their mark (`receipts/needle-direct.txt`).
- **Impact:** wording only. No recorded statement ends in `!` or `?`.
- **Required outcome, exact fix:** write "the full stop, comma, semicolon or colon ending it" in both places. Changing the docstring also moves the digest at `ci/image/command-table.json:13701`, so this can wait for the next edit of the file.
- **Verification:** read the text against `:374`.

### S1 - SUGGESTION - Robustness, Docs - `scripts/docs_inventory.json:28`, `:355`, `:445` - some `also` fragments are broader than the false claim

- **Evidence:** "is **not met by this build**" has no subject, so my plant "The clause is not met by this build." gets a D0-059 row and a stale page, with a correction about a different clause. "open is the write side" is similarly generic. HANDOFF limit 4 discloses D0-002 only, and the PR body does not mention the class.
- **Impact:** over-reporting, which is the safe direction. A person judges the row, and no real page does this today.
- **Suggested outcome:** add one limit line to the PR body naming this class, or give those fragments a subject where the quote allows it. The R742-3 F2 plants need the D0-059 and D0-002 clauses found, so test any rewording against them.
- **Verification:** rerun the plants.

### S2 - SUGGESTION - Robustness - `scripts/docs_inventory.py:342` against `:347` - a quote that normalises to nothing is still accepted

- **Evidence:** round 4 refuses an `also` entry with an empty needle, but `quote` only passes `value.strip()`. A finding with quote `.` or `**` gives `--write` rc 0 and 180 D0-999 rows (`receipts/empty-quote-probe.txt`). `.` newly normalises to nothing because of this delta's punctuation strip; `**` already did.
- **Impact:** loud in the diff, data-entry only, and absent from the real data.
- **Suggested outcome:** apply `needle_of()` to the quote too, with one refusal arm.
- **Verification:** the probe gives rc 2.

### S3 - SUGGESTION - Tests - `scripts/docs_inventory.py:374`, self-test arms `:896` onward - two of my 14 delta mutants survive

- **Evidence:** 12 of 14 killed (`scripts/mutate_selftest.py`, `receipts/selftest-mutants.txt`). The arm for each new form does fail when that form is removed. The survivors are:
  - `.rstrip(".")`: no arm records a quote ending in `,`, `;` or `:`, though the real data has three (D0-019, D0-036, D0-037). The behaviour is correct by direct call.
  - `held` built from `normal_form` instead of `needle_of`: this changes only a narrow overlap case, so it is close to equivalent.
- **Suggested outcome:** one arm whose recorded quote ends in a comma.
- **Verification:** the first mutant is killed.

### S4 - SUGGESTION - Tests, Docs - `scripts/docs_inventory.py`, 999 lines against `LONG_MODULE_LINES = 1000` - no margin remains

- **Evidence:** the limit passes (`receipts/py-idiom.log`, rc 0). Room came from inlining `relative()` and packing table rows and fixture entries, which the PR discloses. The rendered page is unchanged, and no test was weakened.
- **Impact:** the next arm or fix, including S2 and S3, needs more packing or a split.
- **Suggested outcome:** when next edited, move the fixture and controls to their own self-test module instead of packing further.
- **Verification:** `python3 scripts/check_py_idiom.py`.

## Prior public findings at this head

Read after my diff pass and my first plant run, and before writing this verdict. I read the published R741-3 and R742-3 reports, including their ledgers. I read no other reviewer's round-4 report; none was published when I listed the PR comments.

| Prior item | Disposition | Evidence |
|---|---|---|
| R741-3 F1 and R742-3 F1 BLOCKER, literal path fails the source-list gate | **RESOLVED** at cause | Check 1; hosted step 10 success |
| R742-3 F2 MINOR, search misses real copies | **RESOLVED** | Check 3; the docstring at `:30-35` states what is and is not normalised; the author's replay of that report's own script also shows rows and stale pages (`r742-probe-e2e.txt`) |
| R741-3 R1 RESIDUE, PR body "not pushed" | **Applied, then overtaken** | The old sentence is gone, but its replacement is stale after the push; carried as R1 |
| R741-3 R2 RESIDUE, D0-064 one line short | **RESOLVED** | "(lines 3621-3622)"; the status test is on line 3622 |
| R741-3 R3 RESIDUE, "emphasis" | **RESOLVED** | The report's fix was "asterisk emphasis"; underscores are now normalised too, so "asterisk and underscore emphasis" is true |
| R742-3 R1 RESIDUE, D0-024 line reads as the wrong file | **RESOLVED** | The cell names the firmware file; `milan_baremetal.c:1405` is `nvm_commit` |
| R741-3 S1 SUGGESTION, markup forms | **Partly resolved, rest retained** | Links and underscores done; HTML, a backslash break and D0-013 wrapped before `+` stay disclosed as limits, not extended, per the brief |
| R741-3 S2 SUGGESTION, spelling normalising to nothing | **Partly resolved** | `also` refused with an arm, mutant killed; `also: ["the"]` retained; the quote side is my S2 |
| R741-3 S3 and R742-3 S1 SUGGESTION, surviving mutants | **RETAINED, optional** | The author's receipt at this head still shows `no-nfkc`, `no-whitespace-collapse`, `held-not-updated` and `origin-rows-use-search` surviving |
| R741-3 S4 and R742-3 S2 SUGGESTION, second copy of D0-066's claim | **RETAINED, optional** | The cell is unchanged; recorded for the owner in the author's `findings/README.md` per HANDOFF |
| R741-2 F1, R742-2 F1, F2 and F3 | **Stay RESOLVED** | The delta changes only D0-063 to D0-065's path spelling and one line range |
| R741-2 S1 to S3, R742-2 S1, R741-1 S1 to S3 | **RETAINED, optional** | The delta does not touch them |

Unresolved decisions (not findings, and not mine to settle): what "Mark II default" names, and the owner additions of 2026-10-30. Both remain published in the PR body.

## Delta checks

- **Comment rule:** no bench label, lane name, review round, reviewer ID or comment ID in `scripts/docs_inventory.py` or in any `scripts/docs_inventory.json` finding. One commit subject names a review round; the rule covers source comments, so this is not a finding.
- **Digest:** `sha256sum scripts/docs_inventory.py` equals `ci/image/command-table.json:13701` (`2756e5b5...`).
- **Tail census:** the ten `also` entries are each inside their own quote and carried on their own page. A census of the other quotes found none that runs past its sentence into a next clause (`receipts/also-vs-quote.txt`). D0-019 ends at a semicolon and D0-037 at a colon, both on their own clause, and the punctuation strip now covers those ends.
- **Local gates at this head:**
  - `docs_inventory.py --check` rc 0, also on a clean clone without submodules;
  - `--selftest` rc 0, 50 controls;
  - `check_py_idiom.py` rc 0;
  - `git diff --check 1f29f189 8d8c2e36` rc 0.
- **Author packet:** evidence commit `02c1c4c3` is **unsigned** (`verification.reason` = `unsigned`), so no signature could be verified; the brief's "signed packet" is not what was published. `HANDOFF.md` and `receipts/INDEX.md` match the public manifest's `published_sha256`, and five spot-checked receipts match `INDEX.md` (`receipts/author-packet-check.txt`). The author's local `pp_srcs` log says the same as the hosted step. HANDOFF's "not pushed" and "hosted CI has not run" were true when it was written.
- **PR-body counts confirmed:** 50 controls, 65 findings, 87 rows, 22 copies, area split 57 + 14 + 6 + 1 + 9, ten `also` entries, 999 lines.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #797 acceptance and rules; `CONTRIBUTING.md:514-515`; D0-024, D0-063 to D0-065 against `protocol_processor_top.sv:3593-3595,3621-3622,3624-3648` at `a9e84b66`, `milan_datapath.sv:6048-6053,6444-6445`, `milan_baremetal.c:1405`; `receipts/citations-diff.txt` | R741-4 | `8d8c2e366a2d49506b91a195de0094a440e7bc39` |
| RTL | CLEAN | `git diff 808602e0 8d8c2e36` has no change under `hdl`, `tb`, `syn`, `sw`, the submodules or `.github`; gitlinks unchanged; `scripts/pp_srcs.py --check` derives 46 sources; hosted `verilator-lint` and `yosys-elaboration` success. Cited RTL read, no behaviour claim changed | R741-4 | `8d8c2e366a2d49506b91a195de0094a440e7bc39` |
| Robustness | CLEAN (S1, S2 optional) | `scripts/docs_inventory.py:136-137,342-347,365-418`; `receipts/plant-forms.txt` (28 plants); `receipts/empty-quote-probe.txt`; `receipts/needle-direct.txt` | R741-4 | `8d8c2e366a2d49506b91a195de0094a440e7bc39` |
| Tests | CLEAN (S3, S4 optional) | Self-test arms `scripts/docs_inventory.py:853-904`, 50 controls; `receipts/selftest-mutants.txt` (12 of 14 killed; each new form's arm can fail); author mutant receipts; hosted `docs` and `rtl-fast` jobs. `rtl-full` incomplete, see limits | R741-4 | `8d8c2e366a2d49506b91a195de0094a440e7bc39` |
| Docs | CLEAN (R1, R2 residue; S1 optional) | `docs/DOCUMENTATION_AUDIT.md` fresh, rows compared across rounds (`receipts/real-tree-rows.txt`); `scripts/docs_inventory.py:13-35`; PR body (`receipts/pr-body-snapshot.md`); `ci/image/command-table.json:13701` | R741-4 | `8d8c2e366a2d49506b91a195de0094a440e7bc39` |

## Real limits

- Physical calibration NOT RUN. No hardware, Vivado, Docker, local replica, builder bank or source bank ran. Field skips are not hardware proof. No manager source bank exists or is inferred at this head.
- `rtl-full` was cancelled, so 7 of 19 Verilator shards, 3 of 4 Yosys shards and the summary jobs produced no result at this head. The delta changes no RTL, but that evidence is still absent.
- Round-4 scope: statements outside the delta keep their prior lens verdict. Round 2's read-only statements and dev's newer lines on release-facing pages stay unchecked, as the PR says.
- Plants cover the forms named in the brief. I did not look for further escape forms, per the brief.
- Standards clause text was not re-derived; the delta changes no clause claim.
- Only seven packet files were hash-checked, of 289 listed.

## Pending manager duties

- Re-run `rtl-full` at this head and read `verilator-suites` and `yosys-portability`; the completion bar needs both. Decide whether the `rtl-fast` run's cancelled conclusion is acceptable given its `rtl-fast` context success, or re-run it.
- Consider a separate Issue, outside #797: a watcher reaching its 120-minute limit in a queue backlog is treated as a terminal failure, and its tail cancels healthy sibling runs.
- Local-replica acceptance, the second independent verdict, the current-dev merge candidate banks, merge authorization and post-merge containment.
- Carry R1 and R2 to the residue checklist. R1 should be applied before merge, with the hosted result current at that time.
- Obtain the maintainer decision on "Mark II default" and the decision on the owner additions of 2026-10-30.

No merge approval is given.

Exact bytes after probes (`receipts/exact-head.txt`): `HEAD` `8d8c2e36`, tree `24d3429b`, no tracked or ignored change, index modes and blobs equal the tree listing, gitlinks `a9e84b66`, `135afd04`, `08ee86e8`, `70936b77`, `48ff7a7e` unchanged with no submodule marked modified, and optional `external` uninitialised. All probes ran in disposable clones; the review clone ran gates only.

R741-4 FINISHED

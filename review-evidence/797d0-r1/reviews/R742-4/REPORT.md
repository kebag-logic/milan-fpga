[R742] POSITIVE - exact head 8d8c2e366a2d49506b91a195de0094a440e7bc39

PR #815, issue #797, external independent round R742-4. Tree `24d3429b66ec52b7fb48782fbb78d289abab668b`. Delta judged: `808602e0..8d8c2e36`, 3 commits, 4 files (`ci/image/command-table.json`, `docs/DOCUMENTATION_AUDIT.md`, `scripts/docs_inventory.json`, `scripts/docs_inventory.py`). Code the delta does not touch keeps its round 3 lens verdict.

## Verdict

No BLOCKER, MAJOR or MINOR is open. Round 3's BLOCKER and MINOR are resolved at their causes, and all four residue items are applied. This round adds one RESIDUE and five SUGGESTIONS.

**This POSITIVE covers the source at this head. It does not clear the merge bar.** Two required hosted contexts, `verilator-suites` and `yosys-portability`, read `failure` at this exact head because their runs were cancelled. I found no test failure, but 7 Verilator shards and 3 Yosys shards never finished, so they are owed a rerun or candidate evidence. The manager owns that acceptance (see "Pending manager duties").

## The four assigned checks

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | D0-063 to D0-065 keep their meaning, and the gate passes untouched | MET | See "Check 1" |
| 2 | Hosted `rtl-fast` at this head | `rtl-fast` context SUCCESS; run conclusion `cancelled` afterwards | See "Check 2" |
| 3 | Planted forms caught, and no new row on the real tree | MET | See "Check 3" |
| 4 | Residue applied | MET: R741-3 R1, R2, R3 and R742-3 R1 | See "Prior findings" |

### Check 1: D0-063 to D0-065

- **Meaning kept.** `receipts/data_checks.txt` reverses the path rewrite and compares with `808602e0`. The D0-063 and D0-065 source and correction cells and the D0-064 source cell differ only in the path spelling. D0-064's correction also changes "(line 3621)" to "(lines 3621-3622)", which is residue R2. D0-024's source gains the firmware file, which is residue R1. No other finding's `source` or `correction` changed, and all 65 finding ids are the same and in the same order.
- **Cited lines are right at the processor pin `a9e84b66`.**
  - `protocol_processor_top.sv:3621-3622`: the settled test.
  - `:3625-3626`: the pass-through and its input guard.
  - `:3628-3633`: selectors 4 to 7.
  - `:3641-3643`: the three masks.
  - `hdl/milan/milan_datapath.sv:6444-6445` and `:6048-6050` were also read and agree.
  - `sw/firmware/milan_baremetal/milan_baremetal.c:1405`, `:1656` and `:1914` are `nvm_commit()`, `nvm_boot()` and its call.
- **Gate passes and was not touched.**
  - `python3 scripts/pp_srcs.py --check` rc 0, and with `--selftest` rc 0 (`receipts/pp_srcs_check.rc`, `receipts/pp_srcs_selftest.rc`).
  - `git log 1f29f189..8d8c2e36 -- scripts/pp_srcs.py` is empty, so its permitted list is untouched.
- **The gate can still fail.** Restoring one literal path into the data file in a disposable clone gives rc 1 (`receipts/punct_and_gate_probe.txt`).

### Check 2: hosted result at this head

Read from the exact-head check runs (`receipts/hosted/exact_head_checks.tsv`, `required_contexts.tsv`).

- **`rtl-fast` context: SUCCESS**, job `125039441563`, with all 12 needed jobs `success` (`receipts/hosted/job_125039441563.log`). The step "Prove protocol-processor source lists are derived" passed in `verilator-lint`, job `125012101877`. That is the step that failed at round 3.
- **`docs-check`, `docs-check-no-git` and `elaborate`: SUCCESS.** The docs and elaborate workflow runs concluded `success`.
- **The rtl-fast and rtl-full runs both concluded `cancelled`.** The sequence in the logs:
  1. The rtl-fast watcher job "Fail fast across this head" (`timeout-minutes: 120`, `.github/workflows/rtl-fast.yml:1436`) ran from 23:12 and its observe step was cancelled at 01:12:12.
  2. Its result reached "Cancel late CI failures" as `cancelled`, with `observer_only_error: false`. `scripts/ci_fail_fast.py:26,169-173` counts that as a failure.
  3. At 01:14 that job printed `Cancelled runs: [41358971729, 41358971669]` (`receipts/hosted/job_125042165257.log`).
- **`rtl-full` state after that cancellation:**
  - Verilator: 12 of 19 shards `success`, 7 `cancelled` (1, 5, 6, 7, 9, 11, 17).
  - Yosys: shard 3 `success`, shards 0, 1 and 2 `cancelled`.
  - Six `Union` jobs, `verilator-suites` and `yosys-portability` read `failure`.
- **No test failure was found.**
  - The earliest `failure` conclusion at this head is 01:15:16, after the cancel. The sampled Union job (`milan_dp`) fails an assertion that sees `verilator-shards: cancelled`; the other five were not read.
  - `verilator-suites` refuses a cancelled worker's partial record, then reports "one or more Verilator workers ended: cancelled" (`receipts/hosted/job_125042771870.log`).
  - `yosys-portability` reports `expected=61 observed=45` and "one or more Yosys workers ended: cancelled" (`receipts/hosted/job_125042885073.log`).
  - The cancelled shards produced no verdict, so this is absence of evidence, not a pass.
- **Target commit.** The hosted jobs report `target_sha 514d0f07`, GitHub's merge of this head into dev `1f29f189`. It is not a manager candidate.

### Check 3: the cross-page search

| Probe | Result | Receipt |
|---|---|---|
| Round 3's missed forms replanted on `docs/guides/BOARD_DEPLOYMENT.md`, a page with no row at this head: underscore emphasis, inline and reference link, and sentence-ended copies for D0-002, 005, 024, 025, 035, 036 (both sentences), 040/058, 047, 059, 062 | 14 of 14: `--check` rc 1, `--write` rc 0, `--check` rc 0, one row on the right line, page stale | `receipts/probe_round3_forms.log`, rc 0 |
| Forms planted on a new page against D0-063 and D0-024: underscore and mixed emphasis, inline, reference, collapsed, wrapped, block-quoted and image links, closing comma, semicolon and colon, no closing mark, a dash clause, and a link above the copy | 18 of 18 give a row on the right line and a stale page | `receipts/probe_search.log`, rc 0 |
| Negatives: longer word, inner underscore, snake identifier, paragraph break, different number | 5 of 5 give no row and a current page | same |
| A quote ending in each of `.,;:` with a copy ending otherwise | 4 of 4 give a row | `receipts/punct_and_gate_probe.txt` |

On the real tree, the `808602e0` and head audit pages both hold 87 finding rows, with an identical id, page and line in every row. The raw audit diff changes only the D0-024, D0-063, D0-064 and D0-065 rows. `python3 scripts/docs_inventory.py --check` rc 0 (550 lines). `--selftest` rc 0 (50 controls).

One first-pass probe arm reported no row under D0-058. That was my probe's expectation, not a miss. D0-040 records the same words earlier in the data file, so the copy row is D0-040's and D0-058 is held by it. The page does get a row and renders stale. The arm now names D0-040.

No further escape forms were sought, as assigned.

### Packet verification

Evidence commit `02c1c4c3`, `review-evidence/797d0-r1/author-r4`, 290 files (`receipts/author_r4_hashes.txt`).

- All 290 match `published_sha256` in `MANIFEST.json`.
- Of the 289 rows in `receipts/INDEX.md`, 273 match the published bytes. The other 16 match `original_sha256`, on files the publisher rewrote, and none matches neither.
- The handoff's head and tree and its 45-of-45 mutant count agree with its receipts. The 50 controls agree with my own `--selftest` run.
- **The packet carries no signature.** The assignment calls it signed, but the evidence commit reads `unsigned` and no signature file is present. Integrity here rests on these digests and the commit, not on a signature.

## Findings

### R1 - RESIDUE - Docs - PR #815 body, "Status" (line 16) and "Known limitations" - The hosted statements are now stale

- **Evidence:** the body says "GREEN locally, hosted not yet run" and "Head `8d8c2e36` has no hosted run until it is pushed". The head is pushed and hosted ran (Check 2).
- **Impact:** a cold reader of the PR gets the wrong hosted state. Prose only.
- **Exact fix (manager, PR body):**
  - Status opening: "GREEN locally. Hosted at `8d8c2e36`: `rtl-fast`, `docs-check`, `docs-check-no-git` and `elaborate` succeeded; the `verilator-suites` and `yosys-portability` contexts are owed a rerun."
  - Known limitations: "At `8d8c2e36` the rtl-fast watcher hit its 120-minute job limit and its tail job cancelled the rtl-fast and rtl-full runs (41358971669, 41358971729), so `verilator-suites` and `yosys-portability` read failure with shards unfinished."
- **Verification:** read the PR body.

### S1 - SUGGESTION - Tests - `scripts/docs_inventory.py:374`, `:403` - Two delta mutants survive the self-test

- **Evidence:** 13 mutants of the delta, 11 killed, 2 survived (`receipts/mutants_delta.txt`).
  - `comma-not-stripped`: the arms pin a closing `.` and not the other marks.
  - `held-keeps-punctuation`: no arm distinguishes it.
- **Impact:** none today. Behaviour is right at this head, and with either mutant the real tree renders the same 87 rows (`receipts/punct_and_gate_probe.txt`).
- **Optional outcome:** an arm with a quote ending in `,`, and one where only the normalised held quote holds the copy.
- **Verification:** both mutants report KILLED.

### S2 - SUGGESTION - Robustness - `scripts/docs_inventory.py:341-343`, `:347` - A quote that normalises to nothing is still accepted

- **Evidence:** the delta guards `also` with `needle_of()`, but `quote` keeps `value.strip()`. A data entry with quote `.` or `**.` gives `--write` rc 0 and 180 `D0-901` rows (`receipts/punct_and_gate_probe.txt`).
- **Impact:** only on a malformed hand edit, and very visible in the diff. This keeps the remaining part of R741-3 S2.
- **Optional outcome:** refuse a quote whose `needle_of()` is empty, with one self-test arm.
- **Verification:** the same entry gives rc 2.

### S3 - SUGGESTION - Robustness, Docs - `scripts/docs_inventory.json`, D0-059 `also` - The recorded sentence has no subject

- **Evidence:** the `also` entry is `is **not met by this build**`. A planted "Requirement 9.9 of another standard is **not met by this build**." gets a D0-059 row (`receipts/d0059_subject_probe.txt`). D0-002 is similarly broad, which the handoff already discloses as open limit 4.
- **Impact:** future only. A true statement about a different requirement would get a D0-059 row and turn its page stale until a lane judges it. No such row exists today, and the failure is visible.
- **Optional outcome:** record a spelling that includes the clause's subject, provided the sentence form round 3 planted stays caught.
- **Verification:** `scripts/probe_round3_forms.py`'s D0-059 arm, adjusted to the new spelling, and the same 87 rows.

### S4 - SUGGESTION - Robustness - `scripts/docs_inventory.py` (999 lines; limit 1,000 at `scripts/check_py_idiom.py:148`) - The module has one line of room

- **Evidence:** the delta made room by packing list rows, fixture rows and comments, and by inlining `relative()`. Output is unchanged: `--check` rc 0 and the same rows.
- **Impact:** the next arm or normalisation will meet the limit again and invite more packing. The gate itself is untouched.
- **Optional outcome:** move the self-test and its fixture to their own module when the area lanes next change this file.
- **Verification:** `check_py_idiom.py` passes with the packed rows unpacked.

### S5 - SUGGESTION - Robustness - `.github/workflows/rtl-fast.yml:1436`, `scripts/ci_fail_fast.py:26,169-173` - A watcher reaching its job limit cancels healthy runs

- **Evidence:** Check 2. `docs/testing/CI_WORKFLOWS.md:3151` says watcher and collector read outages never authorize cancellation. A watcher that reaches its own 120-minute limit while jobs are still queued counts as `cancelled`, and that does cancel. The delta does not touch this, so it is not a finding on this PR.
- **Impact:** queue delay alone can cost a head its rtl-full evidence.
- **Optional outcome:** a separate Issue deciding whether watcher expiry is an observer-only result.
- **Verification:** a self-test of `tail_failed()` for that case.

## Prior findings at this head

Read after my own pass over the delta. The concurrent R741-4 report was not read before this report and ledger were written; only its first line appeared in a comment index.

| Finding | Status | Evidence |
|---|---|---|
| R742-3 F1 / R741-3 F1 BLOCKER, literal path fails `pp_srcs.py --check` | RESOLVED at cause | Check 1; hosted source-list step passed |
| R742-3 F2 MINOR, search misses | RESOLVED at cause | Check 3; `scripts/docs_inventory.py:136-137`, `:372-374`, `:381`; ten `also` entries; docstring `:30-35` agrees (HTML and backslash forms stated as not normalised, and the author's `r741-plant-probes.txt` shows them unfound) |
| R742-3 R1 RESIDUE, D0-024 file | APPLIED | `scripts/docs_inventory.json` D0-024 source names the firmware file; `milan_baremetal.c:1405` |
| R741-3 R1 RESIDUE, PR body push statement | APPLIED, and superseded by R1 above | The old sentence is gone; the replacement went stale when the head was pushed |
| R741-3 R2 RESIDUE, D0-064 line | APPLIED | "(lines 3621-3622)"; the status test is on `:3622` |
| R741-3 R3 RESIDUE, "emphasis" | APPLIED | Docstring and PR body say what is normalised; arms hold both emphasis kinds |
| R742-3 S1 / R741-3 S3 SUGGESTION, surviving mutants | RETAINED, optional | Author's receipts; S1 above for the delta's two |
| R742-3 S2 / R741-3 S4 SUGGESTION, D0-066's second copy | RETAINED, optional | Not a Markdown page; the author's findings README records it |
| R741-3 S1 SUGGESTION, unseen markup forms | RETAINED, optional | Stated in the docstring; not extended, as assigned |
| R741-3 S2 SUGGESTION, spelling normalising to nothing | PARTLY TAKEN | `also` guarded with an arm; `quote` not, see S2 |
| R741-2 S1-S3, R741-1 S1-S3, R742-2 S1 SUGGESTION | RETAINED, optional | As recorded at round 3; not re-examined, since the delta does not touch them |

**Comment rule.** A raw scan of the delta's added lines in the generator and data file (`receipts/comment_rule_scan.txt`) has three matches, none of them a workflow label in a comment. One is a flash "single-lane fast read". Two are the audit page's existing "area lane" sentences, repacked onto one line, and findings pages may name lanes. Commit subject `acc10192` names a review round, which the source-comment rule does not cover. All three commits are one-line with no body.

## Lens results

```text
[R742] PASS Conformance - scripts/docs_inventory.json D0-024, D0-063 to D0-065 against protocol_processor_top.sv:3621-3643 at a9e84b66, milan_datapath.sv:6444-6445, milan_baremetal.c:1405; #797 rules - meaning kept, citations exact, no workflow labels added
[R742] PASS RTL - receipts/changed_paths_base.txt has no hdl, tb, syn, sw, configs or gitlink path; protocol_processor_top.sv:3621-3643 read for the audit's RTL claims; hosted source-list step at this head - no RTL changed, cited RTL behaviour as recorded
[R742] PASS Robustness - scripts/docs_inventory.py:136-137,341-347,365-417 against 32 planted forms, 5 negatives, 4 closing marks and malformed data; real-tree row comparison - forms caught, negatives clean, S2 to S5 optional
[R742] PASS Tests - scripts/docs_inventory.py copy_controls() arms; --selftest rc 0, 50 controls; 13 own delta mutants, 11 killed; author receipt 45 of 45; pp_srcs gate rc 1 on the restored literal - new arms kill the mutants they target, S1 optional
[R742] PASS Docs - docs/DOCUMENTATION_AUDIT.md rows, docstring scripts/docs_inventory.py:30-35, PR #815 body - audit regenerated and fresh, docstring agrees with behaviour, one PR-body wording residue R1
```

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | D0-024, D0-063 to D0-065 against cited lines; 65 ids unchanged; #797 rules; Check 1 | R742-4 | 8d8c2e366a2d49506b91a195de0094a440e7bc39 |
| RTL | CLEAN | `receipts/changed_paths_base.txt` has no RTL or gitlink path; `protocol_processor_top.sv:3621-3643`; `milan_datapath.sv:6444-6445`; hosted source-list step | R742-4 | 8d8c2e366a2d49506b91a195de0094a440e7bc39 |
| Robustness | CLEAN (S2 to S5 optional) | `docs_inventory.py:136-137`, `:341-347`, `:365-417`; planted forms and negatives; 87-row comparison | R742-4 | 8d8c2e366a2d49506b91a195de0094a440e7bc39 |
| Tests | CLEAN (S1 optional) | `--selftest` 50 controls; delta mutants; author receipts; gate rc 1 probe | R742-4 | 8d8c2e366a2d49506b91a195de0094a440e7bc39 |
| Docs | CLEAN (R1 residue) | Audit page rows; `docs_inventory.py:30-35`; PR body; author packet | R742-4 | 8d8c2e366a2d49506b91a195de0094a440e7bc39 |

## Real limits

- **Delta-scoped round.** Round 2 and round 3 statement verification was not repeated, and sampling was not extended.
- **Mutants ran one at a time.** The session's permission mode refused my first, concurrent form of the mutant run, so I ran the same 13 mutants serially in the foreground. Results are unaffected.
- **No RTL suite was run by me.** Source execution evidence is the author's published receipts, the hosted jobs above, and my focused probes. The author's gate receipts were hash-verified and sampled, not re-executed. No full bank, Docker, act or hardware was used. Physical calibration NOT RUN, and field skips are not hardware proof.
- **Hosted coverage is partial at this head.** The cancelled Verilator and Yosys shards produced no verdict. The `Physical gPTP` job was skipped.
- **The packet is hash-verified, not signature-verified.** It carries no signature.
- **Tree integrity:** `receipts/tree_integrity.log` rc 0. 1,461 tracked blobs match in bytes, modes and index. Five initialised gitlinks are at their pins and clean, and optional `external` stays uninitialised. Probes ran in a scratch clone.

## Pending manager duties

1. **Hosted acceptance at the merge turn:** obtain complete `verilator-suites` and `yosys-portability` evidence by rerun or candidate. Neither passes at this head.
2. **Merge candidate:** build and validate the current-dev candidate (builder and native banks), and link its receipts. No manager source bank ran at this head, and none is claimed.
3. **Act replica:** this reviewer did not run or read it.
4. **Apply RESIDUE R1** to the PR body.
5. **Open maintainer decisions remain:** what "Mark II default" names (D0-001, D0-033, D0-056 and nine copy pages), and the owner additions of 2026-10-30. The PR says "Relates to #797", so it does not close the Issue.
6. **The second independent positive and the post-merge containment** remain outside this report.

R742-4 FINISHED

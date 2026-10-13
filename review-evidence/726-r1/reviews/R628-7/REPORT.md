[R628] POSITIVE - exact head cdb49e7ec8b2e03f835a9bda2230ef3e26788c16

Round R628-7, composition review of issue #726 / PR #729. Merge-train candidate `cdb49e7ec8b2e03f835a9bda2230ef3e26788c16`, tree `ab5a465c81b38a05600c2f006cfe0aaf1eadcaef`. Parents: dev `49da9fd974e8805d56c90e29dcfcb67994c2c430` and PR source head `12f00129349c889e6dbbb7de11529ab38c9d164d`. The PR's source base is `c6bd08c6f52632c6d33d834ce842ac3cf63f29cc`.

Scope: composition acceptance only. Source head `12f00129` already holds two independent POSITIVE source reviews: R629-6 ([6134944325](https://github.com/kebag-logic/milan-fpga/pull/729#issuecomment-6134944325)) and R628-6 ([6137485949](https://github.com/kebag-logic/milan-fpga/pull/729#issuecomment-6137485949)). This round asks one question: does the composed tree introduce any defect beyond the reviewed sources?

Verdict: the composed tree is the conflict-free automatic merge. The one shared file, `docs/README.md`, carries both sides' entries, with no broken link or anchor. The counters fixtures build and pass on the composed tree under #727's measured-time split. Every applicable documentation, inventory, pin and scheduling gate passes. No statement in either side became false in combination. This round has no new BLOCKER, MAJOR, MINOR or RESIDUE finding, and one optional SUGGESTION. One prior PR-body RESIDUE is retained.

## 1. Composition facts

Receipt: `receipts/composition.txt`.

- `git merge-tree --write-tree 49da9fd9 12f00129` gives `ab5a465c81b38a05600c2f006cfe0aaf1eadcaef`, which is exactly the candidate tree. The merge commit adds no manual resolution.
- The merge-base of dev and the source head is `c6bd08c6`, the PR's recorded base.
- The PR changes 33 files (`c6bd08c6..12f00129`).
- Dev changes 25 files since that base, through three first-parent merges:
  - PR #724 (#716): firmware-unit job split.
  - PR #721 (#640 M8a-1): split control memory.
  - PR #728 (#727): measured-time Verilator shards with a 60 % headroom gate.
- **Overlap: exactly one file, `docs/README.md`.**
- `dev..candidate` changes exactly the PR's 33-file set.
- Every PR file's candidate blob equals its source blob, except `docs/README.md`. Every dev file's candidate blob equals its dev blob, except `docs/README.md`.
- Submodule gitlinks are identical at `c6bd08c6`, `12f00129`, `49da9fd9` and `cdb49e7e`:
  - `protocol-processor` `2ad2f845`
  - `gptp-processor` `7dda9c3b`
  - `third_party/verilog-axis` `48ff7a7e`
  - `external` `efeb541a`
  - `third_party/lwSRP` `08ee86e8`
- Dev changes nothing under `hdl/`, `tb/`, `tests/`, `protocol-processor` or `sw/firmware/ctrl/aecp/`. The PR changes nothing that dev changed except the README.

## 2. Semantic interactions examined

| Interaction | Evidence | Result |
|---|---|---|
| `docs/README.md` three-way merge | PR adds Verification row "Check stream counters" (line 90). Dev adds Architecture row "Review the split placement's firmware memory" (line 79). `receipts/readme_links.txt`: candidate 62 relative links, 0 problems; each new entry occurs exactly once. `docs_check.py`, `gen_toc.py --check`/`--verify-anchors`/`--selftest`, `check_doc_paths.py`, `DOC_MAP.gen.py --check` all rc 0 | correct |
| #727 duration table vs PR's suites | The PR adds no Verilator suite and renames none. It changes suites `avtp_rxmon`, `crf_rx`, `milan_dp` (four `counters` legs inside `milan_dp`'s run) and `tkdiag`, all already in `SUITE_SECONDS`. So #727's new-suite steps do not apply. `suite_shards.py --selftest` PASS on the candidate (`receipts/docs_gates/38.log`, `receipts/suite_shards_selftest.txt`) | correct |
| Real durations with the PR's legs vs #727's table | `--measure` over all five Verilator worker logs of the source head's hosted rtl-full run 38322428967 (`receipts/suite_shards_measure_source_head.txt`). The PR's suites measure at or under their table figures: `milan_dp` 2227 s vs 2797, `crf_rx` 827 vs 832, `tkdiag` 28 vs 28. The one exception is `avtp_rxmon` at 74 vs 73 s. Re-predicting the candidate's 5-worker split with per-suite max(table, measured) gives workers [4219, 4217, 4218, 4222, 2877] s, against the 4320 s ceiling (60 % of 120 min) (`receipts/predict_workers.txt`) | headroom holds |
| milan_dp placement | Candidate split (`receipts/suite_shards_split.txt`): shard 4/5 = `milan_dp` alone (DEDICATED_SUITES, last worker). rtl.yml still uploads `suite-logs-${{ matrix.shard }}`. So the PR's `docs/testing/726_STREAM_COUNTERS.md:177` ("Hosted shard 4/5 ... `suite-logs-4`") stays true. So do `tb/verilator/milan_dp/README.md:447` and dev's `docs/testing/CI_WORKFLOWS.md:230` | consistent |
| `ci_events.py` / `rtl-fast.yml` / `rtl.yml` pins (#716, #727) | The PR changes no workflow. `ci_events.py --check` and `--selftest` rc 0 on the candidate | correct |
| `ci_scope.py` (dev added a gate-read page) | The PR's gate-read pages (`REGISTER_MAP.md`, `MILAN_V12_AUDIT_2026-08-16.md`) were already listed. The PR adds no doc that code reads. `ci_scope.py --selftest` rc 0, and `dev..candidate` classifies RTL-relevant (`true`) | correct |
| `check_py_idiom.py` (changed on dev) vs the PR's new Python (`stream_counters.py`, `stream_counter_f5.py`, `torture_campaign.py`, step files) | `check_py_idiom.py` and `--selftest` rc 0 on the candidate. So do `measure_naming --check`, `measure_test_evidence --check` (the PR changes `measure_test_evidence_readers.py`), `check_cpp_idiom`, `check_sh_idiom`, `check_sv_idiom` and `check_hygiene --check` | correct |
| M8a-1 firmware changes (`ctrl_split.ld`, `ctrl_split_start.S`, firmware test drivers) vs the PR's F5 mailbox fixture | `stream_counter_f5.py` imports `aecp_arms`, `ctrl_build`, `fw_gtest` and `test_aecp.cpp`. Dev changed none of these. `make counters-f5` passes on the candidate at both shapes, and its three plants detect then escape. `check_nvm_capture.py` rc 0 | no interaction |
| `before` control reading `c6bd08c6` engines via `git show` | `c6bd08c6` is an ancestor of the candidate. The three engines read from it are unchanged by dev. On the candidate, `--variant before --shape 1` gives exactly TX ×6, RX ×2, CADENCE ×4 (12) named failures, and the driver accepts them | correct |
| Statements that could become false in combination | PR text naming `c6bd08c6` (`726_STREAM_COUNTERS.md:81,184`, `stream_counters.py:79`) is historical provenance. The PR commits no area/LUT/BRAM figure; those figures sit only in issue/PR comments as source-head measurements against `c6bd08c6`. "No firmware implementation ... changes" (`726_STREAM_COUNTERS.md:149`) describes this PR and stays true. Dev's TESTING/CI_WORKFLOWS edits state no counter law | none found |

## 3. Executed evidence on the candidate

All runs used the candidate tree. Docs gates ran in the clone itself. Simulations ran in a byte-identical copy under `scratch/tree`, at the same HEAD and tree, with clean status and matching gitlinks. Simulator: the scoped 5.050 wrapper, which prints `Verilator 5.050 2026-07-01 rev v5.050`.

- **Documentation-workflow gates.** `scripts/docs_gates.list`, summary in `receipts/docs_gates/summary.tsv`. The doc dependencies are the pinned Markdown renderer, wavedrom and PyYAML, installed in a private venv (`receipts/venv-freeze.txt`). Results:
  - 41 of 42 commands rc 0. These include `docs_check.py`, `check_em_dash.py --base 49da9fd9` and `--base c6bd08c6`, `gen_toc.py --check/--verify-anchors/--selftest`, `ci_events.py --check/--selftest`, `suite_shards.py --selftest`, `ci_scope.py --selftest`, every idiom/naming/evidence/hygiene/port/source-list gate and `git diff --check 49da9fd9 cdb49e7e`.
  - The 42nd, `gen_hdl_reference.py --selftest`, first refused because its pinned parser was not installed. After installing `tools/hdl_reference/requirements.txt`, `--selftest` (44/44) and the full reference build (80 sections, 77 modules) passed (`receipts/hdlref_gates/`). This needed `core.commitGraph=false`, set through the environment only, because the clone's stale commit-graph warning on stderr trips the generator's dirty check.
- **Composition test legs.** `scripts/test_gates.list`, `receipts/test_gates/`, 5 min 27 s, peak RSS 0.79 GB:
  - `make -C tb/verilator/milan_dp counters`: four `RESULT: PASS`, failures=0 (1×1 and 8×8, uncertain and frames-only).
  - `make counters-f5`: both shapes rc 0.
  - `cd tests && python3 -m behave --no-capture -f plain`: 14 features, 406 scenarios, 1977 steps passed; 0 failed, 0 skipped.
  - `torture_campaign.py --self-test`: 80 tests OK.
- **Standing plants on the composed tree.** `scripts/mutant_gates.list`, `receipts/mutant_gates/`, `receipts/mutant_runs/`, `receipts/mutant_named_groups.txt`, 4 min 05 s, 8 jobs. Every plant fails only its own named group, then escapes clean (0 FAIL) with that check omitted:
  - tx-interval: TX ×6
  - rx-interval: RX ×1
  - tx-reset: TX_RESET ×4
  - aaf-reset: RX_RESET ×1
  - crf-reset: RX_RESET ×1
  - rx-saturation: RX ×1
  - late: CADENCE ×4
  - rate: RATE ×8
  - tx-nodirty (frames-only): OUTPUT_CADENCE ×4
  - fixed-grid: PHASE ×8
  - egress-stall 1×1: CADENCE ×8
  - egress-stall 8×8: CADENCE ×36
  - F5 late: CADENCE ×8
  - F5 rate: RATE ×8
  - F5 fixed-grid: PHASE ×8
- **Hosted, read only.** At source head `12f00129`, rtl-full run 38322428967 executed all five Verilator workers and all four Yosys shards, plus `verilator-suites` and `yosys-portability`, all success. `Physical gPTP (nightly and manual)` was skipped and is not evidence (`receipts/hosted/rtl-full-38322428967-jobs.tsv`). Worker 4/5 log: `shard: 4/5 selected suites: 1`, then `PASS milan_dp`. No hosted run exists at candidate `cdb49e7e`.

## 4. Findings

This round adds no new BLOCKER, MAJOR, MINOR or RESIDUE. The prior RESIDUE R628-6-R1 = R629-6-R01 (PR-body wording) is retained; see section 6.

**R628-7-S1 (SUGGESTION). Lenses: Docs, Tests.**
- Location: `docs/testing/726_STREAM_COUNTERS.md:177` ("Hosted shard 4/5 must retain these results in `suite-logs-4`").
- Evidence: it is true on the candidate, because #727 places `milan_dp` on the last of five workers. But #727's add-a-worker procedure (`scripts/suite_shards.py` docstring, step 2) moves `milan_dp` to the new last index. That procedure lists rtl.yml, `ci_events.py` and `suite_shards.py`, not this page. The same applies to the older `tb/verilator/milan_dp/README.md:447` and `docs/testing/CI_WORKFLOWS.md:230`.
- Impact: none today. The page would go stale the day a sixth worker is added.
- Optional outcome: phrase it as "the hosted Verilator worker that runs `milan_dp` alone (its `suite-logs-<index>` artifact)".
- Verification: `docs_check.py`, `check_em_dash.py`.

## 5. Reviewer-owned ledger

| Lens | Result | Composition touches its scope? | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | No. Dev changes no protocol behavior: no `hdl/`, no processor gitlink, no AECP core/adapter. The PR's counter law, cadence and rate limit are unchanged in the composed tree | `receipts/composition.txt` (file sets, blobs, gitlinks); counters legs 4× `RESULT: PASS` and F5 legs on the candidate (`receipts/test_gates/1.log`, `2.log`); behave 406/1977 (`receipts/test_gates/3.log`). Source coverage: R628-6 6137485949 and R629-6 6134944325 at `12f00129` | R628-7 (composition), plus source rounds R628-6 and R629-6 | `cdb49e7ec8b2e03f835a9bda2230ef3e26788c16` (sources at `12f00129349c889e6dbbb7de11529ab38c9d164d`) |
| RTL | CLEAN | No. Dev changes no file under `hdl/` or `tb/`, and all five gitlinks are identical. The PR's RTL blobs are byte-equal to the source | `receipts/composition.txt`; `check_rtl_source_lists.py` (+selftest), `check_sv_idiom.py`, `check_port_contracts.py`, `check_soc_sources.py` rc 0 (`receipts/docs_gates/22,24,29,21.log`); HDL reference build 77 modules (`receipts/hdlref_gates/2.log`); candidate Verilator builds of the counters fixtures | R628-7, plus R628-6 and R629-6 | `cdb49e7e...` (sources `12f00129...`) |
| Robustness | CLEAN | No. No dev change reaches reset, backpressure, stall or saturation paths of the changed engines | 15 standing plants detect by name and escape on the candidate (`receipts/mutant_named_groups.txt`, `receipts/mutant_runs/`), including rx-saturation, egress-stall at both shapes, aaf-reset and crf-reset; `before` control 12 named failures | R628-7, plus R628-6 and R629-6 | `cdb49e7e...` |
| Tests | CLEAN | Yes: #727 re-schedules the Verilator inventory that runs the PR's legs, and dev changes the Python idiom gate | `suite_shards.py --selftest` PASS; 5-way split; measured-duration re-prediction ≤ 4222 s vs 4320 s ceiling (`receipts/predict_workers.txt`); counters/F5/behave/torture/plant runs on the candidate; `check_py_idiom`, `measure_test_evidence --check`, `measure_naming --check` rc 0 | R628-7 | `cdb49e7ec8b2e03f835a9bda2230ef3e26788c16` |
| Docs | CLEAN | Yes: `docs/README.md` is changed by both sides | Merged `docs/README.md:79,90`; `receipts/readme_links.txt` (62 links, 0 problems); `docs_check.py`, `gen_toc.py --check/--verify-anchors`, `check_em_dash.py --base 49da9fd9`, `check_doc_paths.py`, `check_doc_style.py`, `DOC_MAP.gen.py --check` rc 0 (`receipts/docs_gates/`); statement review in section 2. SUGGESTION S1 is optional and does not un-cover the lens | R628-7 | `cdb49e7ec8b2e03f835a9bda2230ef3e26788c16` |

## 6. Prior public findings at this head

I read these only after the sections above were written. The source rounds' own resolution tables are R629-6 6134944325 and R628-6 6137485949.

| Prior finding(s) | Status at `cdb49e7e` |
|---|---|
| R628-1-F1 = R629-1-F01 (MAJOR), R628-1-F2/F3/F4 (MINOR) | RESOLVED. Resolved at source by R628-6 / R629-6. The composed tree carries the same blobs, and behave passes 406/1977 on the candidate |
| R628-2-F1 (MAJOR), R628-2-F2 (MINOR), R629-2-F01 (MINOR) | RESOLVED. The docs-workflow gates (naming, test-evidence, Python/C++ idiom, every later step) rc 0 on the candidate. `torture_campaign.py --self-test` 80 OK and behave pass on the candidate |
| R628-3-F1 (MAJOR), R628-3-F2 (BLOCKER) | RESOLVED. Gap grading and the recursive-make capture pass on the candidate: `make -C tb/verilator/milan_dp counters`, 4× `RESULT: PASS`. R628-6 left one limit open: hosted shard 4/5 at `12f00129` was still in progress. It is now discharged. Run 38322428967 job "Verilator shard 4/5" succeeded, and artifact `suite-logs-4` shows the four counters legs `RESULT: PASS` inside `milan_dp` (`receipts/hosted/suite-logs-4-counters-excerpt.txt`, log sha256 `0f71b170...`) |
| R629-4-F01 (MINOR), R628-5-F1 (MINOR) | RESOLVED. Candidate blobs equal source. The egress-stall plant fails CADENCE at both shapes on the candidate and escapes when omitted |
| Earlier RESIDUE (R629-1-F02, R628-2-RS1–RS5, R628-3-R1/R629-3-R01, R628-4-R1/R2, R628-5-R1–R6/R629-5-R01) | RESOLVED per R628-6 / R629-6. No composition effect |
| **R628-6-R1 = R629-6-R01 (RESIDUE, Docs)**: PR body calls the published Round 6 head local/unpublished | **RETAINED as RESIDUE.** The live PR body (updated 2026-10-13T03:55:59Z) still reads, at lines 17-18, "Round 6 local source head ..." and "two new commits await publication". Line 89 reads "Both Round 6 commits remain local pending authorized publication.", and lines 160-161 read "authorized publication" / "After publication". Exact fix as stated in R628-6-R1 / R629-6-R01. Wording only; it does not affect the verdict or any lens |
| R628-6-S1–S4 (SUGGESTION; carried from R628-1 to R628-5) | RETAINED as optional SUGGESTION, unaffected by composition |

## 7. Real limits

- This is a composition review. Lenses whose scope the composition does not touch rest on the source reviews named above for depth, plus the candidate re-runs listed here.
- Not run here, by the round's rules:
  - full parent, processor, gPTP, Yosys and builder banks;
  - the full `milan_dp` suite (`make -C tb/verilator/milan_dp run`) and the other three PR-touched suites (`avtp_rxmon`, `crf_rx`, `tkdiag`), whose code is byte-equal to the source and dependency-disjoint from dev;
  - `act_ci.py` and its self-test, the RV32 SDK download, the builder test, `make -C gptp-processor docs` and `check_gptp_docs.py --with-submodule`.
- No hosted run exists at the candidate head. Hosted duration evidence is from the source head's run, which used the pre-#727 hash split. `milan_dp`'s dedicated worker is the same under both splits.
- Simulation results are finite compressed-time measurements. Physical calibration was NOT RUN. Field and physical-gPTP skips are not hardware proof. No bench, controller-display or reference-peer reset comparison was performed. Those remain merge-turn acceptance items 1 (reset vs reference peer), 2 (link-tap cadence) and 3 (controller display).
- No manager source bank is claimed or inferred at this head.

## 8. Pending manager duties

- Current-dev merge-candidate builder and native banks at the merge turn, with receipts linked on the PR.
- Hosted and act acceptance at the exact merge head.
- The merge-turn bench check from acceptance items 1 to 3, and the Records item 4 cross-check against measured physical cadence.
- Carry the retained RESIDUE R628-6-R1 = R629-6-R01 (PR-body publication wording, exact fix in those rounds) to the residue checklist.
- Optional R628-7-S1 and R628-6-S1–S4, at the manager's discretion.
- Post-merge containment, and closing the issue (the PR body says `Relates to #726`).

## 9. Clone integrity

Receipt: `receipts/clone_integrity.txt`.
- HEAD, HEAD tree and index tree equal `cdb49e7e` / `ab5a465c`; worktree vs HEAD identical in content and mode.
- Gitlink checkouts match and are clean.
- The gate runs created `__pycache__` directories (dry run listed 4, all `__pycache__`); `git clean -fdX` removed them. Afterwards the status, including ignored files, is empty.
- No commit, push, GitHub write or source edit.

R628-7 FINISHED

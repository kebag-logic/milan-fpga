[R328] POSITIVE - exact head f80525e695ce7937ba1a2c1caa01ec9cdde93904

# R328-4 composition review: issue #502 / PR #579 merge-train candidate

Reviewer: [R328], internal composition reviewer, cleared context.
Candidate: `f80525e695ce7937ba1a2c1caa01ec9cdde93904`, tree `20b9e49f38cf575cb9980c5c49d4b6af89310b42`.
Parents: train candidate `dab01daf2c574727bd9b1a5ecc63a05538695b12` (C_565) and PR #579 source head `90ab4a3da5b676f90b768b4f22b77ce7d0bd911d`.
Scope: composition acceptance only. POSITIVE means the composed tree adds no defect beyond the reviewed sources.

## 1. Verdict

POSITIVE. None of the five lenses has an open BLOCKER, MAJOR or MINOR finding.
One SUGGESTION (S1) is recorded; it does not affect lens coverage.
The composition merges cleanly: `git merge-tree --write-tree dab01daf2 90ab4a3da` reproduces tree `20b9e49f`.
The two textual overlaps compose consistently. #502's RTL and tests pass on the candidate:
the pooled `milan_dp` default, `pp_shadow` default, the late-mark mutant, the single-top OOC run and its ROM ledger check.
The capture gate and every repository docs/pin/record gate the composition reads also pass.

## 2. Reconstruction (public state only)

- Contract: AGENTS.md sections 3 and 5-7 and CONTRIBUTING.md 2.1-2.2/3 (merge validation, pin/ROM ledger, verification bar).
- Issue #502 body; the scope decisions in issue comments 5844866872, 5845129498 and 5846418959,
  the merge-dev decision in 5847404798, and the round decisions in 5848417938 (option (a): the map source is the
  parent's actual phase-5 write), 5854008765, 5854288100 and 5854533678.
  Frozen acceptance: K10/K12 on the shipping glue pass, with the unchanged, reset and both-group controls kept.
  A mutant that triggers on the mark again must fail. Docs cover MATERIALIZATION and the SNAPSHOT_OWNERSHIP pending section.
  Area and the capture gate apply, and the capture is re-measured only if firmware changes.
- Train: `831f94f4` (#502 base) -> #517 `de4862cb` -> #509 `72dcb14c` -> #231 `3d430164` -> #565 `dab01daf` -> + #579 = `f80525e6`.

## 3. Composition surface (verified with git)

`git diff --name-only dab01daf2 f80525e69` is exactly the 25-path set of `git diff --name-only 831f94f4 90ab4a3d`.
23 of those paths are blob-identical to the PR head. Two differ: the files predecessors also changed.

| Overlap | Predecessor | #502 change | Composed result |
|---|---|---|---|
| `docs/testing/TESTING.md` | #517: 19-line pool paragraph after the highlights (`:294-311`) | one campaign row (`:268`) | disjoint hunks; row count 1, pool paragraph count 1 |
| `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` | #565: section 18 timing (`:1591-1612`) and section 20 item 6 (`:1770-1778`) | sections 5.3/5.4/6.1/11/13/17 and section 20 item 2 (`:1754-1758`) | disjoint hunks; no statement contradicts another (section 5 below) |

Semantic (non-textual) interactions checked:

| Interaction | Evidence | Result |
|---|---|---|
| #565 8x8 `milan_clk_hz` 50 MHz (`configs/endstation_ax7101_8x8.yaml:56`) | Changes a configuration value the builder and the capture gate consume, not RTL. The `milan_dp` 8x8 leg elaborates from tracked `configs/generated/endstation_ax7101_8x8` headers, which no train member changes (`milan_dp_default.log:2710`). The composed default run passes and `check_nvm_capture.py` checks `configured_cpu_hz` | pass; no interaction with #502's RTL |
| #517 pooled `milan_dp` runner with #502's `sim_nxn.cpp` VERSION check | the `#502 now reports` check is `[ok]` in all five `sim_nxn` legs | pass |
| #517 pool tests read the Makefile only (`test_sim_pool.py:890`, `test_sim_pool_backpressure.py:86`) | #502 does not change `tb/verilator/milan_dp/Makefile` | no interaction |
| `pp_shadow` sources from `make -C ../milan_dp print-srcs` (`tb/verilator/pp_shadow/Makefile:107`) after #517 | `pp_shadow` default and `pending-mutant` on the candidate | pass |
| #231 CI steps (`rtl-fast.yml:209-211`, `ci_events.py` RTL_STEP_LISTS) and `KL_pp_shadow` hierarchy names | `pp_baseline.py --selftest`, `pp_baseline_mutants.py`, `pp_baseline_reports_selftest.py`, `dp_srcs.py --top KL_pp_shadow`; instance is still `pp_shadow` (`hdl/milan/milan_datapath.sv:7428`) | pass |
| #231 baseline figures vs #502's area change | `docs/findings/PP_SHADOW_BASELINE.md:4,29` binds RTL `7eb3b0d4` and processor `990f9652` | dated measurement; no contradiction |
| #565 capture receipt vs #502 RTL/pin | `check_nvm_capture.py` pass; see S1 | pass; S1 |
| Processor pin | no predecessor changes it (`dab01daf` = `0922e434`); `0922e434` is an ancestor of `870ff88a` | forward move |
| ROM ledger | `syn/yosys/rom_digests.tsv:27-28` rows for `870ff88a`; OOC rc 0; two refusal probes | pass |
| Line-anchored references from predecessor text into #502-changed files | scan of every predecessor-changed file | none found |

## 4. Executed on the candidate (all at `f80525e6`, tracked bytes verified afterwards)

Tools: Verilator 5.050 (`rev v5.050`, the CI pin in `.github/workflows/rtl-fast.yml:18`), Yosys 0.66, sv2v v0.0.13.
Markdown gates use an interpreter holding the six `tools/markdown/requirements.txt` pins at their exact versions.
Suites ran bounded to 8 CPUs.

| Gate | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/pp_shadow` | rc 0; 591 + 591 + 591 + 295 checks, 0 failures; 346 K10/K12 PASS lines, 0 FAIL lines | `receipts/suites/pp_shadow_default.log` |
| `make -C tb/verilator/pp_shadow pending-mutant` | rc 0; clean control 295/0; late-mark mutant 12 named failures (K10 x4, K12 input/output/remove x8); `PASS: late-mark mutant killed by K10 and K12` | `receipts/suites/pp_shadow_pending_mutant.log` |
| `make -C tb/verilator/milan_dp` (pooled default, `sim_pool.py --jobs=2`) | rc 0 in 1512 s; eleven ordinary legs plus the `gptp`/`gptp-lat`/`gmstep` prerequisites; render-law 6/6 and gmstep 4/4 controls; 0 FAIL lines | `receipts/suites/milan_dp_default.log`, `milan_dp_pool_invocation.txt` |
| `syn/yosys/ooc.sh KL_pp_shadow` | rc 0; LUT 60846, LUTRAM 6136, LUT_TOT 66982, FF 30187, RAMB36 15, RAMB18 4, DSP 6 | `receipts/suites/ooc_KL_pp_shadow.log` |
| ROM ledger probes (disposable) | removing the `870ff88a` rows gives `no recorded content digest`, rc 2; zeroing its `ucode.hex` digest gives `content digest mismatch`, rc 2; the generated digest `23605682...` equals row 28; ledger restored to blob `b565dc2c` | `receipts/rom_probe*` |
| `check_nvm_capture.py` | `PASS: capture census, clocks, both timing arms and receipt agree` | `receipts/gates-mdvenv/nvm_capture.log` |
| `docs_check.py` (Git and `GIT_DIR=/dev/null`) | 0 findings over 169 md + 902 files, both modes | `receipts/gates-mdvenv/docs_check*.log` |
| `gen_toc.py --check` / `--verify-anchors` | OK (111 pages); 180 cross-page fragments reproduced | `receipts/gates-mdvenv/gen_toc_*.log` |
| `check_em_dash.py --base dab01daf` / `--base 831f94f4` | 0 findings over 292 / 1559 added lines, arms 339/339 | `receipts/gates-mdvenv/em_dash_*.log` |
| `check_doc_style.py`, `check_doc_paths.py`, `check_submodule_docs.py` | rc 0; submodule docs `OK (4 exact gitlinks)` | `receipts/gates-mdvenv/` |
| `ci_events.py --check` / `--selftest` | OK, 1655 contract items; selftest rc 0 | `receipts/gates-mdvenv/ci_events_*.log` |
| `measure_test_evidence.py --check` | PASS (75 <= 77, 10 <= 10, 0 <= 0, 3 <= 3) | `receipts/gates-mdvenv/measure_test_evidence.log` |
| `lint_rtl.py --check`, `check_rtl_source_lists.py`, `check_port_contracts.py`, `pp_srcs.py --check` | rc 0; lint 90 <= 90 | `receipts/gates-mdvenv/` |
| `dp_srcs.py --top KL_pp_shadow` / `--top milan_datapath`; the three #231 `pp_baseline` self-tests | rc 0 | `receipts/gates-mdvenv/` |
| `git diff --check dab01daf f80525e6` | rc 0 | `receipts/gates-mdvenv/diff_check_train.log` |
| Code-token comparison `dab01daf` -> `f80525e6` | `KL_nvm_backend.sv`, `milan_csr.sv`, `cosim_top.sv` code-identical; only `KL_pp_shadow.sv` and `milan_datapath.sv` change code | `receipts/code_token_diff.log` |
| Post-probe state | HEAD/tree/index exact; every tracked blob and mode re-hashed equal; no index flags; three submodules at their gitlinks and clean. Build residue removed from the parent and processor checkouts afterwards: 31 ignored entries plus one processor `__pycache__`, all created by this round after the clone at 11:40:42 local. 0 untracked or ignored entries remain in the parent and all three submodules | `receipts/verify_clean.log` |

A first gate pass with the default interpreter refused three Markdown gates: the pinned renderer was missing.
That is an environment refusal, kept as `receipts/gates/`. The pinned-renderer rerun above is the result.

## 5. Decisive composition questions

1. **SAVED_STATE_SNAPSHOT_OWNERSHIP.md is internally consistent.** Section 18 (#565) measures only the capture copy.
   It states `An accepted RELOAD closes every allocated backend record` (`:1632`), which agrees with #502's section 6.1 (`:983-987`) and its section 5.4 table row (`:827`).
   Section 20 item 2 (#502, `:1754-1758`) and item 6 (#565, `:1770-1778`) are separate items. Neither restates the other's subject.
   #502's section 6.1 pending sources equal the RTL at the candidate (`hdl/milan/KL_pp_shadow.sv:945-957`, `hdl/milan/milan_datapath.sv:4269,7498`).
   Anchors `#18-cost` and `#61-the-pending-bit-owner-decision` both resolve (`gen_toc.py --verify-anchors`).
2. **TESTING.md lists each entry once.** The #502 row appears exactly once (`:268`) among the 7 campaign rows.
   #517's eleven-leg default-run paragraph appears exactly once (`:294`). `pp_shadow` is not a `milan_dp` pool leg, so the "eleven ordinary commands" inventory stays accurate.
3. **#502's RTL composes with #517's pooled `milan_dp` default.** Both targets pass on the candidate (section 4). #502's K10/K12 pass, and the mutant is killed.
4. **The capture gate passes on the candidate.** Firmware is unchanged. The product firmware never reads the pending bit: `NVM_RD_PEND` is defined at `sw/firmware/milan_baremetal/milan_baremetal.c:201` and used nowhere.
5. **The ROM ledger holds rows for the candidate's pin 870ff88a** (`syn/yosys/rom_digests.tsv:27-28`). The ooc.sh digest check passes and is shown live by the two refusal probes.
6. **The repository docs gates pass on the candidate** (section 4).

## 6. Findings

### S1 SUGGESTION - Docs, Tests - `tb/verilator/nvm_capture_cpu/measurements.json:303-306` - capture receipt records processor `0922e434`; the composed tree pins `870ff88a`

- Evidence: #565 added a `processor_pins` provenance field (`protocol-processor` `0922e434...`, measured at base `831f94f4`).
  #502 moves the gitlink to `870ff88a`. `scripts/check_nvm_capture.py:62-66` binds the firmware and harness hashes but not the processor pin, so the gate passes.
- Why it is not a defect: the receipt is a dated record of what was measured. The issue's decision (5844866872 item 4, 5846418959 item 4) requires re-measurement only on firmware change.
  The processor delta `0922e434..870ff88a` touches 3 HDL files (+25/-2) and adds the name-write export. ROM digests are identical for both pins (ledger rows 7-8 vs 27-28).
  The only parent code change is pending reporting, which the firmware never reads. The capture traffic is READ_DESCRIPTOR only.
- Impact: a later reader comparing the receipt's pins with the gitlink could take the receipt for stale evidence.
- Optional outcome: the merge note (or the next capture re-measurement) states that the receipt's gateware predates #502 and why the figures still apply.
- Verification: reader check; `check_nvm_capture.py` stays green.

No BLOCKER, MAJOR or MINOR finding.

## 7. Reviewer-owned completion ledger (composition round)

| Lens | Status | Composition touches scope? | Examined artifacts (at `f80525e6`) | Covering round | Exact head |
|---|---|---|---|---|---|
| Conformance | CLEAN | Indirectly: the acceptance evidence runs in a tree whose `milan_dp` runner (#517) and `pp_shadow` source list (read through `milan_dp print-srcs`) changed | K10/K12 and the controls in `pp_shadow_default.log`; the mark-trigger mutant in `pp_shadow_pending_mutant.log`; pending composition `KL_pp_shadow.sv:945-957` vs SNAPSHOT section 6.1 `:962-987` | R328-4 | `f80525e695ce7937ba1a2c1caa01ec9cdde93904` |
| RTL | CLEAN | Not textually: no predecessor changes RTL, the pin or the generated shape headers. Re-applied because #502's RTL now elaborates inside #517's pooled runner and #231's OOC/baseline tooling | code-token diff (`code_token_diff.log`); `milan_datapath.sv:4243-4271,7498`; `lint_rtl --check`, `check_port_contracts`, `check_rtl_source_lists`, `pp_srcs --check`; OOC `KL_pp_shadow` rc 0; ROM ledger rows 27-28 and probes | R328-4 | `f80525e695ce7937ba1a2c1caa01ec9cdde93904` |
| Robustness | CLEAN | No: the refusal, unchanged, repeated and reset controls live in `tb/verilator/pp_shadow/sim_main.cpp`, which no predecessor changes. Re-executed as a composition check | `pp_shadow_default.log`: K10/K12 refusal lines 98 PASS, unchanged 20, partial refusal 40, repeat 20, `K12 remove` 50, `K reset` 20, and 0 FAIL lines anywhere. Source cover: [R329] R329-5 POSITIVE at `90ab4a3d` and [R328] R328-3 POSITIVE at ancestor `867a2e38` | R328-4 (composition re-execution); source: R329-5, R328-3 | `f80525e6...`; `90ab4a3d...`; `867a2e38...` |
| Tests | CLEAN | Yes: the TESTING.md overlap, #517's pooled `milan_dp`, #502's `sim_nxn.cpp`, `measure_test_evidence` dispositions | TESTING.md `:266-276,294-311`; pooled `milan_dp` default rc 0; `pending-mutant` rc 0; `measure_test_evidence --check` PASS; `ci_events --check/--selftest`; #231 `pp_baseline` self-tests | R328-4 | `f80525e695ce7937ba1a2c1caa01ec9cdde93904` |
| Docs | CLEAN | Yes: SNAPSHOT_OWNERSHIP and TESTING overlaps; SUBMODULES/CHANGELOG pins; the docs map | SNAPSHOT `:29-31,949-1000,1251-1282,1358-1395,1539-1689,1746-1778`; TESTING `:268,294`; `docs_check` in both modes, `gen_toc --check/--verify-anchors`, `check_em_dash` (both bases), `check_doc_style`, `check_doc_paths`, `check_submodule_docs` | R328-4 | `f80525e695ce7937ba1a2c1caa01ec9cdde93904` |

Source-review status is from the public verdict lines: R328-3 (issuecomment-5854285010) and R329-5 (issuecomment-5854723436).
The `867a2e38..90ab4a3d` delta changed docs, comments and diagnostic tags only.
Section 8 records my check of the source reviews' findings.

## 8. Prior public review findings at this head

I read these only after sections 1-7 above were written. Each item is re-checked at `f80525e6`.
The receipt is `receipts/prior_findings_check.log`, produced by `scripts/prior_findings_check.sh`.
Nine finding-bearing files are blob-identical between `90ab4a3d` and `f80525e6`.
The only differing files are SNAPSHOT_OWNERSHIP and TESTING. Their changed lines `90ab4a3d -> f80525e6` equal the predecessors' `831f94f4 -> dab01daf` changed lines exactly (`receipts/overlap_hunk_identity.log`).

| Finding | Severity, lenses | State at `f80525e6` | Evidence at the candidate |
|---|---|---|---|
| R328-1 F1 = R329-1 F2: no refused-at-validation map control | MINOR, Tests (+Robustness) | RESOLVED | `K12 refused record input/output` checks all PASS: status 7, count 0, pending and sticky bits 0 (`pp_shadow_default.log`) |
| R328-1 F2: MATERIALIZATION section 1 named the mark trigger | MINOR, Docs | RESOLVED | `docs/design/SAVED_STATE_MATERIALIZATION.md:127-141` states the four-term `pend_i` and the live-write sources |
| R328-1 F3: campaign not listed in TESTING | MINOR, Docs | RESOLVED | `docs/testing/TESTING.md:268`, once, after composition with #517 |
| R328-1 S1 = R329-1 F3: unchanged duplicate set pending | SUGGESTION / MINOR, Conformance, Robustness (+Tests, Docs) | RESOLVED | `hdl/milan/milan_datapath.sv:4269-4271` requires an in/out change; `K12 duplicate input/output` pending checks PASS; 0 tree hits for "conservative duplicate" |
| R328-1 S2: observer anchored on trigger inputs | SUGGESTION, Tests | RESOLVED | `tb/verilator/pp_shadow/sim_main.cpp` is blob-identical to `90ab4a3d`, where it was confirmed; live-state checks `live_state_changed` PASS |
| R329-1 F1: REMOVE legs could not fail | MINOR, Tests, Robustness | RESOLVED | `K12 remove input/output` PASS; the late-mark mutant fails `K12 remove input/output` on both durability checks (`pp_shadow_pending_mutant.log`) |
| R328-2 F1 = R329-2 F1: CHANGELOG/SUBMODULES trigger text | MINOR, Docs | RESOLVED | `CHANGELOG.md:38-40`, `docs/reference/SUBMODULES.md:59-62`; 0 tree hits for "every commit beat" |
| R328-2 S1: P4 phase-5 term unguarded | SUGGESTION, Tests, Robustness | RESOLVED | `K12 partial refusal input/output` checks all PASS (40 lines) |
| R328-2 S2 = R329-2 S1: SNAPSHOT wording; PR body sentence | SUGGESTION, Docs | RESOLVED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1273` "from the first actual write". The PR body is outside the tree; R328-3 and R329-5 found the sentence absent from the live body |
| R329-3 F1 / S1: MATERIALIZATION listed #502 as open | MINOR / SUGGESTION, Docs | RESOLVED | `SAVED_STATE_MATERIALIZATION.md:2097` "RESOLVED by #502"; `:1731`, `:2087` labelled historical |
| R328-3 S1 / R329-4 S1: untagged refusal and exact-record diagnostics | SUGGESTION, Tests | RESOLVED | every `GET_AUDIO_MAP exact record` line carries its case tag in `pp_shadow_default.log` |
| R329-4 F1: section 13 gave the pre-#502 `pend_i` | MINOR, Docs, Conformance | RESOLVED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1361-1362` equals `hdl/milan/KL_pp_shadow.sv:945-957`; D2 use labelled "Original" at `:1388`; the whole-tree `pend_i *=` search returns only the two current equations, two proposed D3 equations and two harness drives |
| R329-4 S2: CSR comment wrap | SUGGESTION, Docs | RESOLVED | `hdl/common/csr/milan_csr.sv:195-199`; code tokens identical to `dab01daf` (`code_token_diff.log`) |
| R329-5 S1: MATERIALIZATION stage table omits the pulse term | SUGGESTION, Docs | RETAINED (optional) | `SAVED_STATE_MATERIALIZATION.md:1697-1698` unchanged |
| R329-5 S2: `K12 preloaded baseline durable` untagged | SUGGESTION, Tests | RETAINED (optional) | `tb/verilator/pp_shadow/sim_main.cpp:1447` unchanged |
| R329-5 S3: "That manager" antecedent | SUGGESTION, Docs | RETAINED (optional) | `SAVED_STATE_FASTCONNECT.md:1380` unchanged |
| R329-5 S4: "now REPORTED, because donor scope D2 landed" | SUGGESTION, Docs | RETAINED (optional) | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1280` unchanged; composition does not touch it |

No prior MINOR, MAJOR or BLOCKER remains open at the candidate. The retained items are SUGGESTIONs and do not affect coverage.

Source-review ledgers, confirmed after reading:

- R329-5 (issuecomment-5854723436) covers all five lenses CLEAN at `90ab4a3d`.
- R328-3 (issuecomment-5854285010) covers Conformance, Robustness, Tests and Docs CLEAN at `867a2e38`, and RTL through R328-2 at `5d4cf33e`, with RTL bytes identical at `867a2e38`.
- Neither source round examined the composed tree. Section 7's composition coverage is this round's.

## 9. Real limits

- The instructed simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist.
  I used an equivalent wrapper around the same 5.050 install used by the train's other candidate directories.
  `--version` gives `Verilator 5.050 2026-07-01 rev v5.050`; `verilator_bin` sha256 is `44898b22af4178b45214a0820a04eeac8632ae721ff005e69ef1cf69121bbfdd`.
- Raw receipts keep local absolute paths as produced; the publisher may abbreviate them.
- Not run, by assignment: the full parent/PP/gPTP/Yosys/builder banks, act/Docker, hardware and physical calibration.
  Field-campaign skips are not hardware proof. The single-top OOC run is Yosys area only, not timing.
- The candidate commit `f80525e6` has no hosted runs (GitHub answers 422 for it). Hosted evidence exists only for source head `90ab4a3d`.
- The named public evidence tree `dc9d0928:review-evidence/502-r1` holds the round-1 author packet at `87e263fd` and a manifest.
  I found no manager bank receipt for `90ab4a3d` or `f80525e6` there. The manager's bank statement is taken as stated, not re-verified.

## 10. Pending manager duties

- Hosted `docs-check` at PR head `90ab4a3d` concluded failure because of infrastructure (job 108591678428).
  The step `Install the pinned sv2v release` got `curl: (22) ... error: 500`, so no docs gate executed there.
  It needs a rerun before the protected contexts are green. The local docs gates pass on the candidate (section 4).
  Other contexts at `90ab4a3d`: `rtl-fast`, `verilator-suites`, `yosys-portability`, `elaborate`, `docs-check-no-git` and others succeeded. `Physical gPTP` was skipped (not executed).
- Build the final current-dev candidate at the merge turn and run the candidate banks. This round validates `f80525e6` only.
- Hosted/act acceptance, the post-merge containment check and moving the Issue to Done.
- Optionally act on S1.

R328-4 FINISHED

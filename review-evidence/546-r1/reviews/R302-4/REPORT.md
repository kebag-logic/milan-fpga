[R302] POSITIVE - exact head f5532c4c3f94a516b748cc4627dc5f78d05fa73e

# R302-4 internal independent review: issue #546 / PR #554, merge-delta round

- Head under review: `f5532c4c3f94a516b748cc4627dc5f78d05fa73e`, tree `afce979ba040ba63ca104a714de2245123d796a9`. The review ran in a detached clone at this head.
- Parents: `0c61d458941088f3847513b7c6fe6589c75b4270` (the R302-3 POSITIVE head) and dev `c266432dcb0cdd464205823a3d82cad260eedde2`. Merge base: `57456af96b3127b9d309a995bbbd35a6113ce52d`.
- Scope: the round-4 assignment (issue #546 comment 5824704845). The task is a merge of dev (#387b and #408) with one manual text resolution in `docs/design/GM_LOSS_RECOVERY.md`. No content change was requested.
- Verdict: **POSITIVE**. No BLOCKER, MAJOR or MINOR finding is open. There are two new SUGGESTIONs, and two earlier ones are retained. None of them affects coverage.
- I wrote my own verdict and ledger before reading any prior review finding: `receipts/ledger_before_prior_findings.md`.

## Context reconstructed

- AGENTS.md sections 6-7: the five lenses, the verdict line, and coverage banked per head.
- Issue #546 body. Acceptance: (1) discard the talker-discontinuity rate sample, with a failing arm; (2) a GM change with steps at both ends stays locked or produces one counted re-lock; (3) gates green.
- Manager/assignment comments on #546: 5816510279 (detector preference), 5824704845 (round-4 union rule, the five overlaps, the gate list) and 5824951589 (the executor's REVIEW READY for this head).
- PR #554 body at this head. Published author evidence `review-evidence/546-r1/author-r4/` at `7643d188`: `gates.json`, `merge-metadata.txt`, `submodules.txt`, `merge-resolution.patch`.
- The diff `57456af9..f5532c4c`, the dev delta `57456af9..c266432d` and the PR delta against new dev `c266432d..f5532c4c`.

## Merge-delta proofs (`scripts/merge_delta_checks.sh`, `receipts/merge_delta/`)

1. **The PR's own change against new dev matches the reviewed content exactly.** `git diff c266432d..f5532c4c` and `git diff 57456af9..0c61d458` touch the same 22 files, and every added and removed line matches in order (`cmp` equal).
2. **The merge adds nothing beyond dev on the author side.** `git diff 0c61d458..f5532c4c` matches `git diff 57456af9..c266432d` line for line (37 files, +5751/-1615).
3. **Unchanged files match the reviewed blobs.** 16 of the 22 PR files are byte-identical at the merge head and at `0c61d458`, including every PR RTL file (`KL_crf_rx.sv`, `KL_mmcm_drp_servo.sv`), every test file and `MODULE_MATRIX.md`. Dev did not touch them (`receipts/blob_compare.txt`). The six files that differ are the overlaps.
4. **The only manual resolution is `GM_LOSS_RECOVERY.md`.** `git show --remerge-diff` lists that file alone (`receipts/merge_delta/remerge_diff.txt`). The other five overlaps merged automatically, and the merged result is the plain union of the two sides.
5. **Submodule gitlinks did not move.** `protocol-processor` `09f9bf38`, `gptp-processor` `e5dcea6e`, `third_party/verilog-axis` `48ff7a7e` and `external` `efeb541a` are the same at the base, both parents and the merge (`receipts/gitlinks.txt`).

### The `GM_LOSS_RECOVERY.md` resolution against the assignment's union rule

| Assignment item | At `f5532c4c` | Result |
|---|---|---|
| Render, `mr`, MEDIA_RESET and pending-restart rows use #387b's landed wording | Lines 151, 155, 156 and 157 are byte-equal to dev `c266432d` | Met |
| Media grid aligner row adds "the receiver excludes talker-step rate samples (#546)" | Line 152 carries it, plus "A policy-legal local slew remains tracked by #545" | Met; identical to the reviewed `0c61d458` row |
| CRF servo row: rate history invalidated on tu transitions or timestamp jumps; 256 clean intervals, then resume; lock and integrator hold | Line 154 | Met; identical to the reviewed row |
| `milan_dp` gmstep test row as landed ("three negative controls in the sweep") | Line 234 | Met |
| Both `crf_rx` rows kept | Lines 235 and 236; dev's `tkdiag` row follows at line 237 | Met |

The remerge diff shows that the executor took exactly one side per conflicted row, and that each side is the one the rule names. Nothing outside the conflict markers changed. Dev's new prose (lines 162-208: one re-base, the per-stream pending restart, and the gmstep grade and non-grade lists) auto-merged unchanged. It does not contradict any #546 sentence.

### The auto-merged overlaps are semantically consistent

- **`hdl/milan/milan_datapath.sv`.** The PR adds exactly three lines (1725, 5502, 5561), wiring `KL_crf_rx.rate_valid_o` to `KL_mmcm_drp_servo.crf_rate_valid_i`. Dev's edits (3070-3131 and 5936-6027) change `mcr_restart_p_w`, `media_rebase_p_w` and `render_recentre_p_w`. They touch neither instance nor `crf_rate_w` or `crf_locked_w`. The CRF lock-loss trigger of `mr` still reads `crf_locked_w`, and #546 keeps LOCKED through a refill, so #546 cannot add a restart. The merged datapath elaborates and builds under Verilator 5.050 in the gmstep leg with `-Werror-UNDRIVEN`. That build raises no warning on a PR-touched file.
- **`docs/reference/REGISTER_MAP.md`.** The PR's `CRF_RATE` row (841) and dev's paragraph on the `mr` triggers (126-131) cover different topics. Dev's "CRF triggers of the `mr` machinery (the disruption and the received toggle)" agrees with the PR's statement that validity is internal and `CRF_RATE` holds its last clean value.
- **`docs/testing/TESTING.md`.** The PR's `crf_rx` row (463) sits beside dev's milan_dp 3600 s deadline, gmstep-mutants row and `tkdiag` row. Nothing overlaps.
- **`docs/design/TIME_SYNC.md`.** The PR's additions (147 and 167-233) and dev's Recentre row are separate. The PR's line "The separate `mr` restart follows 4.4.4.3 and 10.4.3" stays true now that dev makes a PHC step toggle `mr`: the receiver keys on `tu` and timestamp jumps, not on `mr`.
- **`scripts/measure_test_evidence.py`.** The PR's `crf_rx/mutants.py` disposition (597-600) and dev's `gmstep_mutants.py` and `mcr_mutants.py` dispositions are separate keys, and dev's 3600 s budget contract is untouched. `--check` returns 0 with "0 <= 0 unexplained DUT-source reader(s)", and `--selftest` passes 101/101.

## Reviewer-run evidence at `f5532c4c`

The simulator is Verilator 5.050 (`receipts/verilator_identity.txt`; wrapper sha256 `905795b9...`). Runs used a tracked export of the head plus the three submodules, extracted at their gitlinks, capped at 8 CPUs. No command ran in the background.

| Command | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/crf_rx unit` | rc 0; 13836 checks, 0 failures | `crf_rx_unit.log` |
| `make ... discontinuity` | rc 0; 1658 checks, 0 failures | `crf_rx_discontinuity.log` |
| `make ... talker_step` | rc 0; 69 checks, 0 failures | `crf_rx_talker_step.log` |
| `make ... mutants` (default `all` = `run mutants`) | rc 0; 8/8. The clean arms pass. `tu_ignored`, `jump_removed`, `refill_short`, `accept_edge_late`, `servo_ignores_valid` and `servo_never_resumes` each fail with their named rejection | `crf_rx_mutants.log` |
| `make -C tb/verilator/mmcm_servo` | rc 0; unit 85/0, rails 8/0, phc_step 113/0 | `mmcm_servo.log` |
| `python3 scripts/measure_test_evidence.py --check` | rc 0 | `measure_check.log` |
| `python3 scripts/measure_test_evidence.py --selftest` | rc 0; 101/101 | `measure_selftest.log` |
| `docs_check.py`, Git inventory mode | rc 0; 0 findings | `docs_check_git.log` |
| `docs_check.py`, clean tracked export without Git | rc 0; 0 findings; inventory parity skipped as designed | `docs_check_no_git.log` |
| `check_em_dash.py --base c266432d` | rc 0; 0 findings over 81 added lines | `check_em_dash.log` |
| `check_doc_style.py`, `gen_toc.py --check`, `check_doc_paths.py`, `gen_module_matrix.py --check` | all rc 0 | `docs_gates.rc` |
| `git diff --check c266432d f5532c4c` | rc 0 | `git_diff_check.log` |
| Focused integration leg `make -C tb/verilator/milan_dp gmstep` (feed delay 0) | rc 0; 48 checks, 0 failures. One `mr` toggle (+116 cycles), one MEDIA_RESET, one render re-base (+132), listener stays locked | `milan_dp_gmstep.log` |
| Disposable probe: gmstep leg with `crf_rate_valid_w` exposed in a copy (`scripts/gmstep_rate_valid_probe.sh`) | rc 0; 48/0. `rate_valid` stays 0 for the whole leg (next paragraph) | `probe_gmstep_rate_valid.log` |

The documentation gates used the repository's hash-locked Markdown renderer, installed into a disposable environment under the unpublished scratch area. The host does not provide that renderer.

**Why the gmstep probe matters.** The gmstep leg is the one place where the newly landed #387 behaviour and the #546 receiver share an elaboration. Its CRF feed sends a PDU every 4000 cycles, and its PHC advances 8 ns per cycle. The timestamps are therefore 32 us apart, not 2 ms, so the #546 jump backstop fires on every PDU and the rate is never valid in that leg. Before #546 the same feed gave a rate far above the servo's 1024 ppm discard. So the leg neither exercises nor is perturbed by #546 validity. It still passes all 48 of its checks with the gate wired in. The connected `crf_rx talker_step` harness remains the evidence for acceptance 1 and 2, and it passes at this head.

## Findings

No BLOCKER, MAJOR or MINOR finding at this head.

### Suggestions (optional; they do not affect coverage)

- **R302-4 S1 - SUGGESTION - Docs, Tests - `docs/design/GM_LOSS_RECOVERY.md:185-190`.**
  - Evidence: the gmstep "It does not grade these" list names `Vphc_step` for the servo's local-step discard (#539). It does not say where the talker-side step (#546) is graded.
  - Evidence: the probe shows that the leg's time-compressed CRF feed keeps `crf_rate_valid_w` low throughout, so a reader could wrongly assume that gmstep covers the receiver path.
  - Impact: none on behaviour. The test table at lines 235-236 already names the `crf_rx` legs.
  - Optional outcome: one line in that list, such as "the receiver's talker-step invalidation: `crf_rx` talker_step (#546); the leg's feed keeps the CRF rate invalid".
  - Verification: docs gates.
- **R302-4 S2 - SUGGESTION - Docs - PR #554 body, "Status".**
  - Evidence: the body says "Round 4 is committed locally ... Publication and independent review of the merge delta remain pending". The head is now published, and the hosted checks ran on it.
  - This is the same kind of stale status line as R302-3 S1 / R303-3-S1.
  - Optional outcome: refresh the line at the merge turn.

## Prior public findings on this PR, at this head

I read these only after my own pass and ledger (R302-3 comment 5823041800 and R303-3 comment 5822947169, with the tables they carry forward).

| Prior finding | Status at `f5532c4c` | Evidence |
|---|---|---|
| R302-1-F1 = R303-1 F1 MAJOR (Tests, Docs): the connected harness could not fail for the defect | **Still resolved** | The harness and RTL are blob-identical to `0c61d458`. The default campaign's `jump_removed`, `tu_ignored` and related arms fail by name here |
| R302-1 S2 = R303-1 F3 (Tests, Docs): mutation arm in no gate | **Still resolved** | `tb/verilator/crf_rx/Makefile` `all: run mutants` is unchanged; 8/8 here |
| R302-2-F1 = R303-2-F1 MINOR (Conformance, Docs): the media bound cited a clause that does not state it | **Still resolved** | `TIME_SYNC.md` citation lines are unchanged by the merge (identical PR changed lines); the `KL_crf_rx.sv` comment is blob-identical |
| R303-1 F2 MINOR = R302-1 S1: authority for the 100 ppm term | **Still resolved** | As above |
| R303-2 S1: U13 could not fail for a servo that never resumes | **Still resolved** | `servo_never_resumes` fails with "[U13] valid offset resumes PI trim" here |
| R303-2 S2 = R302-2 S1: stale disposition text | **Still resolved** | `scripts/measure_test_evidence.py:597-600` is unchanged; `--check` rc 0 |
| R303-1 S2 = R302-1 S5 (wording) and R302-1 S3 (servo banner) | **Still resolved** | `GM_LOSS_RECOVERY.md:152` keeps the #546 wording through the merge; `KL_mmcm_drp_servo.sv` is blob-identical |
| R302-2 S2 (Tests): per-event attribution across one lock | **Retained, optional** | `sim_talker_step.cpp` is unchanged |
| R302-2 S3 (Tests): receiver mutants run only against the discontinuity harness in the gate | **Retained, optional** | `mutants.py` is unchanged |
| R302-3 S1 = R303-3-S1 (Docs): stale PR status line | **Superseded by R302-4 S2** (same kind, new text) | PR body |
| R302-1 S4 = R303-1 S1 (Robustness): discards are not counted | **Out of scope by decision** (#495) | Round-2 manager assignment |

## Lens results

[R302] PASS Conformance - docs/design/GM_LOSS_RECOVERY.md:148-158,234-237; issue #546 comment 5824704845 item 1; receipts/merge_delta/remerge_diff.txt; receipts/crf_rx_talker_step.log; receipts/crf_rx_discontinuity.log; receipts/crf_rx_mutants.log - the resolution is the union the assignment names, row for row. #387b's landed "Yes" rows are kept verbatim, and #546's receiver sentences, both `crf_rx` rows and the landed gmstep row are present. Issue acceptance at this head: AC1 through the discontinuity leg and the tu/jump/refill/accept-edge mutants; AC2 through talker-only and both-end steps staying LOCKED with one counted local step (69/0); AC3 through the assigned local gates, all rc 0. IEEE 1722-2016 4.4.4.3 `mr` and 4.4.4.7 `tu` roles stay distinct in the merged text.

[R302] PASS RTL - hdl/milan/milan_datapath.sv:1725,5502,5561 and 3070-3131,5936-6027; receipts/blob_compare.txt; receipts/merge_delta/*; receipts/milan_dp_gmstep.log - `KL_crf_rx.sv` and `KL_mmcm_drp_servo.sv` are blob-identical to the R302-3 head. The merged datapath is dev's file plus the PR's three wiring lines. Dev's `mcr_restart_p_w`/`media_rebase_p_w`/`render_recentre_p_w` edits share no signal with the receiver-to-servo validity path. The merged datapath elaborates and runs (gmstep 48/0) with `-Werror-UNDRIVEN`. One clock domain and the rest of the round-3 RTL argument carry over unchanged.

[R302] PASS Robustness - receipts/crf_rx_discontinuity.log; receipts/crf_rx_talker_step.log; receipts/crf_rx_mutants.log; receipts/milan_dp_gmstep.log; receipts/probe_gmstep_rate_valid.log - the tu edges, unmarked jumps, refill boundaries, accept-edge ordering, ignored validity and PI resume paths are rejected by name at the merge head. In the newly merged interaction (a local PHC step toggling `mr` under CRF selection, alongside a 1.5 s talker-epoch jump on the CRF feed), the leg keeps exactly one `mr`, one MEDIA_RESET and a locked listener. The receiver's continuous invalidation under that feed causes no extra restart or lock loss.

[R302] PASS Tests - tb/verilator/crf_rx/{Makefile,mutants.py,sim_*.cpp,crf_talker_wrap.sv}; tb/verilator/mmcm_servo/*; scripts/measure_test_evidence.py:597-600; receipts/crf_rx_*.log; receipts/mmcm_servo.log; receipts/measure_check.log; receipts/measure_selftest.log - every test file is blob-identical to the reviewed head. The default targets pass at the merge head (13836/0, 1658/0, 69/0, 8/8; 85/0, 8/0, 113/0). The evidence ratchet passes with the PR's disposition and dev's two new ones side by side, and the self-test passes 101/101. Dev's gmstep regression still passes with #546 wired in.

[R302] PASS Docs - docs/design/GM_LOSS_RECOVERY.md:142-237; docs/design/TIME_SYNC.md:147,167-233; docs/reference/REGISTER_MAP.md:126-131,841; docs/testing/TESTING.md:463; receipts/docs_gates.rc; receipts/docs_check_git.log; receipts/docs_check_no_git.log; receipts/check_em_dash.log - the merged pages agree with each other and with both parents. The #546 statements (receiver invalidation, 256-interval refill, lock and integrator held, `CRF_RATE` holds its last clean value, no new CSR) and the #387 statements (one re-base, the step toggles `mr`, MEDIA_RESET counts it, pending restarts merge) do not conflict. All documentation gates return 0 in both modes, with the pinned renderer. S1 and S2 are optional.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Merged `GM_LOSS_RECOVERY.md` rows against assignment 5824704845; issue #546 AC1-AC3 through the crf_rx legs and mutants; remerge diff | R302-4 | `f5532c4c3f94a516b748cc4627dc5f78d05fa73e` |
| RTL | CLEAN | `KL_crf_rx.sv` and `KL_mmcm_drp_servo.sv` blob identity; `milan_datapath.sv` three-line PR delta against dev's re-base edits; merged elaboration in the gmstep build | R302-4 | `f5532c4c3f94a516b748cc4627dc5f78d05fa73e` |
| Robustness | CLEAN | Discontinuity 1658/0; talker_step 69/0; named mutant rejections 8/8; gmstep leg plus rate-valid probe | R302-4 | `f5532c4c3f94a516b748cc4627dc5f78d05fa73e` |
| Tests | CLEAN (S1 optional; R302-2 S2 and S3 retained optional) | crf_rx default target; mmcm_servo default target; `measure_test_evidence` `--check` and `--selftest`; gmstep regression | R302-4 | `f5532c4c3f94a516b748cc4627dc5f78d05fa73e` |
| Docs | CLEAN (S1 and S2 optional) | `GM_LOSS_RECOVERY.md`, `TIME_SYNC.md`, `REGISTER_MAP.md`, `TESTING.md`; documentation gates in Git and no-Git modes; PR body | R302-4 | `f5532c4c3f94a516b748cc4627dc5f78d05fa73e` |

All five lenses are banked against the exact head under review.

## Real limits

- This is a delta review. The round-2/3 reviewer probe campaigns (47 robustness rows and the harness-integrity probes) were not rerun. They carry over because every PR RTL and test file is blob-identical to the head they covered, and the merge proofs above show that no other PR content changed.
- The gmstep leg ran at feed delay 0 only. The 42-delay sweep and `gmstep-mutants` were not run. Full parent, protocol-processor, gPTP, Yosys and builder banks were not run (not allowed). `check_cpp_idiom`, `check_py_idiom` and `xvlog_gate --check` were not rerun; the PR's files for those gates are unchanged, and the executor recorded rc 0 at this head.
- I did not independently open the manager's source static/builder and native bank receipts for this head. The only published evidence directory I read at `7643d188` was `author-r4`. The `reviews/` directory was not opened before this verdict was written.
- Hosted snapshot (`receipts/hosted_checks_snapshot.txt`): rtl-fast, verilator-lint, elaborate, yosys-elaboration, all four Yosys shards, docs-check (both), bdd-conformance and Verilator shards 0, 2 and 3 were success. Verilator shards 1/5 and 4/5 were still in progress. Physical gPTP was skipped: that is a skipped context, not an executed job and not hardware proof.
- Physical calibration was not run. Field skips are not hardware proof.

## Pending manager duties

- Build and validate the final current-dev candidate at the merge turn (source base `57456af9`; live dev `c266432d` at review time) and accept the hosted and local-replica results, including the two Verilator shards that were in progress.
- Post-merge containment under CONTRIBUTING, and maintainer authorization for the merge.
- Optional: S1 and S2 above.

## Clone integrity after probes

All probes ran in disposable copies under the unpublished scratch area. The clone check (`scripts/verify_clone_exact.sh`, `receipts/clone_exact_verify.txt`) confirms:
- HEAD and tree match the head under review.
- The index matches the HEAD tree in modes and blobs.
- Each of the 892 tracked paths hashes to its blob with its mode.
- There are no untracked or ignored paths.
- The checked-out submodules sit at their gitlinks with clean trees, and `external` is uninitialised as before.

R302-4 FINISHED

[R303] POSITIVE - exact head 59e7f5fd76786faa673b4522018f4e9590d294d0

Round R303-4, composition acceptance for issue #546 / PR #554.
Candidate: merge-train commit `59e7f5fd76786faa673b4522018f4e9590d294d0`, tree
`21557de92fc191e37e357a330e7a1a6077618f1b`. First parent: the queued predecessor train
`2ab66c9de3a63942c4d3251e1354e8ad3a50d88c` (live dev content plus #548 and #501).
Second parent: the PR #554 source head `f5532c4c3f94a516b748cc4627dc5f78d05fa73e`
(live dev `c266432dcb0cdd464205823a3d82cad260eedde2` merged in).

The composed tree introduces no defect beyond the reviewed sources. No finding is open.

## 1. Reconstruction

Read in order: AGENTS.md, CONTRIBUTING.md (sections 2.2, 3 and 6.1), docs/README.md,
then the issue #546 body and its public assignment and decision comments.

- Frozen acceptance: (1) discard the CRF rate sample that spans a talker discontinuity,
  with a failing arm in simulation; (2) a GM change with steps at both ends stays locked,
  or gives exactly one counted re-lock; (3) gates green.
- Recorded decisions:
  - Discard counting is out of scope and goes to the #495 telemetry checklist.
  - The clock-bound citation is IEEE 802.1AS Annex B.1.1 plus Milan v1.2 section 7.4.
  - The round-4 dev merge resolves `GM_LOSS_RECOVERY.md` by union.
- Linked authority: the CSR ABI in `docs/reference/REGISTER_MAP.md` against
  `hdl/common/csr/milan_csr.sv`, and the datapath instantiation contract in
  `hdl/milan/milan_datapath.sv`.
- Public executable evidence: the author round-4 packet at
  `review-evidence/546-r1/author-r4` (tree `7643d188`), taken at source head `f5532c4c`.
  It shows 15/15 gates at rc 0.
- Hosted checks at `f5532c4c` (`receipts/hosted_checks_f5532c4c.txt`): 21 executed and
  succeeded. One context, "Physical gPTP (nightly and manual)", was skipped and is not
  evidence.

Source reviews this round builds on: R302-3 and R303-3 are POSITIVE at `0c61d458`, and
R302-4 is POSITIVE at `f5532c4c` (the dev-merge delta).

## 2. Composition topology (receipt `receipts/composition_topology.txt`)

- `git merge-tree --write-tree 2ab66c9d f5532c4c` = `21557de9...`, the candidate tree
  exactly: a clean automatic merge with no manual resolution.
- The candidate adds 22 files on top of the train (`2ab66c9d..59e7f5fd`, +867/-29).
  That patch is textually identical to `c266432d..f5532c4c`, the PR against live dev.
  Only blob-id header lines and two hunk offsets in `milan_datapath.sv` differ
  (`receipts/patch_equivalence.diff`).
- The predecessors change 19 files relative to live dev. Exactly two of them are also
  changed by this PR, both first changed by #548 commit `e41703b2`:
  - `docs/reference/REGISTER_MAP.md`
  - `hdl/milan/milan_datapath.sv`

  This matches the declared overlap map. The four blobs of each file (dev, train,
  source, candidate) are all distinct, which is what a two-sided merge should produce.
- The overlapping hunks are disjoint in both text and meaning:

  | File | #548 changes | This PR changes |
  |---|---|---|
  | `milan_datapath.sv` | CTLR_DIAG comments at 1500-1503 and 3218-3221; the `32'd0` tie-off is unchanged | Declares `crf_rate_valid_w` at 1725 and connects it at 5504 (`KL_crf_rx.rate_valid_o`) and 5563 (`KL_mmcm_drp_servo.crf_rate_valid_i`) |
  | `REGISTER_MAP.md` | The 0x6A4 Contents entry (line 191), the `0x6F4` row (1247) and the CTLR_DIAG prose (1251-) | The `0x748` `CRF_RATE` row (841) |

  No signal, address or anchor is shared.
- Other predecessor files (#501: NVM record space, saved-state docs, firmware, builder
  test; #548: `milan_csr.sv`, `sim_nxn.cpp`, the #117 findings page) meet this PR only
  through shared registries and gates, so those were re-run below.
- Source-only paths are byte-identical between the source head and the candidate:
  `hdl/ieee1722/crf`, `tb/verilator/crf_rx`, `tb/verilator/mmcm_servo` and
  `tb/verilator/mmcm_servo_autorepair`.
- `KL_crf_rx` and `KL_mmcm_drp_servo` are instantiated only in `milan_datapath.sv` and
  the PR's own wrappers. No predecessor adds or changes an instantiation.
- Required gitlinks are identical at the train, the source and the candidate:
  - gptp-processor `e5dcea6e`
  - protocol-processor `09f9bf38`
  - third_party/verilog-axis `48ff7a7e`
  - external `efeb541a`, not initialised and read by no gate.

## 3. Gates run on the candidate

Script: `scripts/run_static_gates.sh`. Results: `receipts/static/summary.tsv` plus one log
per gate. All 41 invocations returned rc 0:

- **Documentation:**
  - `docs_check.py`, in the Git tree and in a no-Git `git archive` export, plus `--selftest`
  - `check_feature_status.py`, in the Git tree and in the export
- **Em-dash:** `check_em_dash.py --base 2ab66c9d` and `--base c266432d` (dev, the base CI
  would derive), plus `--selftest`. Against the first parent: 0 findings over 81 added
  lines on 7 pages, arms 339/339.
- **Style and paths:** `check_doc_style.py` plus selftest, `check_gptp_docs.py`,
  `check_doc_paths.py`
- **Generated diagrams and maps:**
  - `DOC_MAP.gen.py --check`
  - `timesync_chain.gen.py --check`
  - `submodule_boundaries.gen.py --check`
  - `check_solution_docs.py`, `check_submodule_docs.py`
  - `gen_module_matrix.py --check`
- **Contents and anchors:** `gen_toc.py --check`, `--verify-anchors` (173 cross-page
  fragment links reproduced) and `--selftest`, run with the hash-locked
  `tools/markdown/requirements.txt` renderer.
- **Test-evidence ratchet:** `measure_test_evidence.py --check` and `--selftest`
- **NVM record space:** `check_nvm_record_space.py` and `--self-test` (the #501 gate)
- **RTL sources and contracts:** `check_rtl_source_lists.py`, `check_port_contracts.py`,
  `measure_naming.py --check`, `measure_fail_fast.py --check`
- **Hygiene:** `check_todo_ownership.py`, `check_hygiene.py --check`, `check_archive.py`,
  `check_baremetal_only.py --check`
- **Idiom:** `check_sv_idiom.py`, `check_cpp_idiom.py`, `check_py_idiom.py`,
  `check_sh_idiom.py`
- **Workflow contract:** `ci_events.py --check` and `--selftest`
- **Front-end and lint:**
  - `xvlog_gate.py --check`: this was a real analysis, not a skip. PASS, 4 findings equal
    to the ratchet: 0 under `hdl/`, 4 in the pinned processors.
  - `lint_rtl.py --check` with the pinned Verilator 5.050: PASS, 90 <= 90.
- **Whitespace:** `git diff --check 2ab66c9d 59e7f5fd`

The evidence ratchet is neutral under composition (`receipts/ratchet_parents.txt`). The
suites without a mutation arm number 73 at dev and at the train, and 72 at the source and
at the candidate. This PR's campaign accounts for the one-step drop, and the predecessors
add none. The advisory "can be lowered to 72" predates the composition.

Focused integration over the composed `milan_datapath` (script `scripts/run_composed_legs.sh`,
wrapper `scripts/r303_notify.mk`, results `receipts/legs/`):

- The Verilator identity is recorded in `receipts/verilator_identity.txt`: 5.050
  (rev v5.050); the wrapper's sha256 and the underlying binary's sha256 are both recorded.
- Builds went to scratch with 4 jobs, and every elaboration had `-Werror-UNDRIVEN` set.
- **Timed notification leg** (`obj_notify` recipe copied verbatim from the suite's `run`
  target): 147 checks, 0 failures. That includes #548's
  `[NOTIFY-T] CTLR_DIAG (0x6F4) is STRUCTURAL ZERO after controller traffic = 0x0`,
  running on the datapath that carries this PR's `crf_rate_valid_w` wiring.
- **`gmstep` leg** (a 1.5 s grandmaster step under CRF selection): 48 checks, 0 failures,
  RESULT PASS, 8,042,838 simulated cycles.
  - This shows that the composed datapath, including this PR's receiver-to-servo wire,
    elaborates and that the leg still passes.
  - It does not grade this PR's receiver gating. `GM_LOSS_RECOVERY.md:189` states that the
    leg does not grade the CRF servo. That gating is graded by the `crf_rx` and
    `mmcm_servo` legs, which are byte-identical to the source head.
  - This scope statement was narrowed after the prior findings were read; see section 7.

Clean-up is recorded in `receipts/restore_verification.txt`:

- HEAD is `59e7f5fd`, `write-tree` = `21557de9`, and all 893 index entries equal the HEAD
  tree in mode and blob.
- There are no untracked or ignored files. The worktree-vs-index and index-vs-HEAD diffs
  are both empty.
- Each required submodule is clean at its gitlink.

## 4. Lens results

Every line below is at head `59e7f5fd76786faa673b4522018f4e9590d294d0`.

```text
[R303] PASS Conformance - docs/reference/REGISTER_MAP.md:841 and :1247, hdl/common/csr/milan_csr.sv:768,783,2357,2402 - the composed CSR ABI keeps both edits: 0x748 CRF_RATE (this PR) says the word holds the last clean value and does not expose validity, which matches milan_csr's unchanged A_CRF_RATE decode; 0x6F4 CTLR_DIAG (#548) is structural zero and matches the 32'd0 tie-off at milan_datapath.sv:3221. No address, field or claimed behaviour is shared, and acceptance 1-2 stay carried by source files that are byte-identical to f5532c4c.
[R303] PASS RTL - hdl/milan/milan_datapath.sv:1500-1503,1725,3221,5504,5563 - #548's comment and tie-off regions and this PR's wire declaration and two port connections are disjoint. The composed module elaborates under the suite's flags with -Werror-UNDRIVEN in two configurations (obj_notify, obj_gmstep); lint_rtl --check PASS (90<=90); xvlog_gate --check PASS with real analysis (0 hdl/ findings); check_port_contracts and check_rtl_source_lists PASS. There are no other KL_crf_rx or KL_mmcm_drp_servo instances.
[R303] PASS Robustness - hdl/milan/milan_datapath.sv:3221 vs :1725/5504/5563, receipts/legs/gmstep.log - the composition adds no state, reset or ordering path. The only new composed interaction is a constant CSR tie-off next to a combinational validity wire, with no shared reset, clock or enable. The discontinuity, refill and resume paths live in KL_crf_rx.sv and KL_mmcm_drp_servo.sv, which are byte-identical to the source head; for those, the source reviews R302-4 (f5532c4c) and R303-3 (0c61d458, the same RTL bytes) remain the coverage. The composed grandmaster-step leg still passes 48/48; it is integration evidence, not a grader of the receiver gating.
[R303] PASS Tests - tb/verilator/milan_dp/sim_nxn.cpp:1596, receipts/legs/notify_run.log, receipts/legs/gmstep.log, receipts/ratchet_parents.txt - #548's harness check runs and passes over the datapath that carries this PR's wiring (147/0), the gmstep leg still passes over the composed datapath (48/0; it does not grade the CRF servo, GM_LOSS_RECOVERY.md:189), and the test-evidence ratchet and selftest pass with a composition-neutral delta. The PR's own suites (crf_rx, mmcm_servo, mmcm_servo_autorepair) are byte-identical to f5532c4c, where the author packet records rc 0 and hosted verilator-suites succeeded.
[R303] PASS Docs - docs/reference/REGISTER_MAP.md (Contents at :191, rows :841 and :1247), receipts/static/summary.tsv - all 13 documentation gates run on the composed tree pass. They are docs_check in Git and no-Git modes, feature status, em-dash against both the first parent and dev, doc style, doc paths, gen_toc --check and --verify-anchors, DOC_MAP, timesync_chain, submodule diagrams, solution and submodule docs, and the module matrix. #548's rewritten Contents entry and this PR's CRF_RATE row coexist without anchor or registry drift.
```

## 5. Findings

None. There is no BLOCKER, MAJOR, MINOR or SUGGESTION at this head from this round's
independent pass.

## 6. Reviewer-owned completion ledger (composition)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | REGISTER_MAP.md 0x6F4/0x748 rows vs milan_csr.sv decode and milan_datapath.sv tie-off; issue acceptance vs byte-identical source paths | R303-4 (composition). Untouched source scope: R302-4 @ f5532c4c, R303-3 @ 0c61d458 | 59e7f5fd76786faa673b4522018f4e9590d294d0 |
| RTL | CLEAN | milan_datapath.sv overlap regions; composed elaboration (obj_notify, obj_gmstep); lint_rtl, xvlog_gate, port contracts, source lists | R303-4 | 59e7f5fd76786faa673b4522018f4e9590d294d0 |
| Robustness | CLEAN | composed overlap (no new state or reset path); gmstep leg as integration evidence only | R303-4 (overlap). Discontinuity, refill and resume paths not touched by composition: R302-4 @ f5532c4c, R303-3 @ 0c61d458 | 59e7f5fd76786faa673b4522018f4e9590d294d0 |
| Tests | CLEAN | sim_nxn.cpp CTLR_DIAG check over the composed datapath; gmstep leg; measure_test_evidence --check/--selftest across dev, train, source and candidate | R303-4. PR suites byte-identical: R302-4 @ f5532c4c | 59e7f5fd76786faa673b4522018f4e9590d294d0 |
| Docs | CLEAN | REGISTER_MAP.md Contents and rows; 13 documentation gates including both em-dash bases and anchor verification | R303-4 | 59e7f5fd76786faa673b4522018f4e9590d294d0 |

The composition touches the scope of every lens through the two overlap files and the
shared gates, so each lens was applied at the candidate head.

## 7. Prior public findings on this PR (read after sections 1-6 were written)

Read from the public PR thread only after sections 1-6 were written: R302-1/R303-1,
R302-2/R303-2, R302-3/R303-3 and R302-4. Receipt: `receipts/prior_findings_at_candidate.txt`.

Every artifact these items name is blob-identical between the source head `f5532c4c` and
this candidate:

- `crf_rx` Makefile, `mutants.py`, `sim_talker_step.cpp`
- `mmcm_servo` `sim_main.cpp`
- `KL_crf_rx.sv`, `KL_mmcm_drp_servo.sv`
- `TIME_SYNC.md`, `GM_LOSS_RECOVERY.md`
- `measure_test_evidence.py`

So no prior disposition can be changed by the composition.

| Prior finding | Status at `59e7f5fd` | Evidence |
|---|---|---|
| R302-1-F1 = R303-1 F1, MAJOR (Tests, Docs): the connected harness could not fail for the defect | **Resolved (retained resolution)** | The harness and mutation files are blob-identical to the source, where R302-4 re-verified the resolution. `tb/verilator/crf_rx/Makefile:53` `all: run mutants` |
| R303-1 F2, MINOR = R302-1 S1, and R302-2-F1 = R303-2-F1, MINOR (Conformance, Docs): the authority for the 100 ppm term | **Resolved** | `KL_crf_rx.sv:275-276` and `TIME_SYNC.md:193,197` cite IEEE 802.1AS Annex B.1.1 and Milan v1.2 section 7.4 |
| R303-1 F3, MINOR = R302-1 S2 (Tests, Docs): mutation arm in no gate | **Resolved** | `Makefile:53`. `servo_never_resumes` is present in `mutants.py:100,112` |
| R303-2 S1 (Tests): U13 could not fail for a servo that never resumes | **Resolved** | `mmcm_servo/sim_main.cpp:604` `[U13] valid offset resumes PI trim` |
| R303-2 S2 = R302-2 S1 (Docs): stale disposition text | **Resolved** | `measure_test_evidence.py:597-600` names the receiver and servo reads and the ignored-validity and PI-resume defects. `--check` rc 0 here |
| R303-1 S2 = R302-1 S5 (wording) and R302-1 S3 (servo banner) | **Resolved** | `REGISTER_MAP.md:841` restores "the talker's media clock measured against gPTP"; `GM_LOSS_RECOVERY.md:152` reads "(#539); the"; `KL_mmcm_drp_servo.sv:79-81` banner names the `crf_rate_valid_i` skip |
| R302-2 S2 (Tests): per-event attribution across one lock | **Retained, optional SUGGESTION**; no effect on coverage | `sim_talker_step.cpp` is unchanged |
| R302-2 S3 (Tests): receiver mutants run only against the discontinuity harness in the gate | **Retained, optional SUGGESTION**; no effect on coverage | `mutants.py` is unchanged |
| R302-4 S1 (Docs, Tests): the gmstep "does not grade" list does not name where the talker-side step is graded | **Retained, optional SUGGESTION**; no effect on coverage | `GM_LOSS_RECOVERY.md:189` is unchanged. The composition does not touch it |
| R302-3 S1 = R303-3-S1, superseded by R302-4 S2 (Docs): stale PR-body Status line | **Retained, optional SUGGESTION** | This is PR-body metadata, not tree content. The body still says round 4 is "committed locally" and review "remain[s] pending". A manager refresh at the merge turn |
| R302-1 S4 = R303-1 S1 (Robustness): receiver discards are not counted | **Out of scope by recorded decision** (manager, #495 telemetry checklist) | Issue #546 comment 5818237636 |

Correction made after reading the prior findings:

- R302-4 S1 records that the gmstep leg does not grade the receiver gating, and
  `GM_LOSS_RECOVERY.md:189` states that the leg does not grade the CRF servo.
- My section 3 description of that leg had called it the path this PR gates. It is now
  narrowed to integration evidence: composed elaboration, and the leg still passes.
- The Robustness and Tests lines in section 4 and the ledger row are narrowed the same way.
- No lens result changes. Neither lens relied on gmstep for this PR's behaviour, which is
  carried by the byte-identical `crf_rx` and `mmcm_servo` sources and their source reviews.
  The composition-specific Tests evidence is #548's check running over the composed
  datapath.

No prior BLOCKER, MAJOR or MINOR is open at this head.

## 8. Real limits

- **Not run at the candidate:**
  - the full `milan_dp` sweep
  - the `crf_rx`, `mmcm_servo` and `mmcm_servo_autorepair` suites; their sources are
    byte-identical to `f5532c4c`
  - the parent, PP, gPTP, Yosys and builder banks, which are excluded from this round
  - Docker/act and any hosted run

  Only the two focused composed legs above were simulated.
- **Candidate commit not on the remote:** `59e7f5fd` has no hosted checks. The hosted
  results cited are for `f5532c4c`, and the skipped "Physical gPTP" context there is not
  executed evidence.
- **Manager's banks not located:** the manager's full static, builder and native banks at
  this head were not in the cited public tree. `7643d188` archives the author packet at
  `f5532c4c`, so this verdict does not rely on those banks.
- **Not hardware proof:** physical calibration was NOT RUN, and simulation or field skips
  are not hardware proof.
- **Scope of this verdict:** it covers this exact candidate. The final current-dev
  candidate the manager builds at the merge turn is a different tree if dev or the queue
  moves, and needs its own validation.
- **Renderer install:** the documentation renderer was installed from the repository's
  hash-locked `tools/markdown/requirements.txt` into a private environment under scratch.

## 9. Pending manager duties

- Publish this report and its manifest.
- Complete hosted and act acceptance on the exact merge candidate.
- Run the full source and candidate banks.
- Validate the candidate merge against live dev at the merge turn.
- Complete post-merge containment.
- Obtain maintainer authorization for the merge.
- Keep the out-of-scope discard-counting item on the #495 checklist as decided.

R303-4 FINISHED

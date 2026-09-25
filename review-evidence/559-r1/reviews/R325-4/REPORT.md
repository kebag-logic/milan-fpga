[R325] POSITIVE - exact head d47a04ebf2a5193dd06ed4eecf8be00f5c8502ce

# R325-4: composition review of issue #559 / PR #564 on the merge-train candidate

Reviewer: [R325], composition reviewer, cleared context. Candidate `d47a04ebf2a5193dd06ed4eecf8be00f5c8502ce`, tree `808c97c034eab4a1f24f50e86ffbbb16ab731e84`.

- Parents: `4ee96a61` (C_443: #443 on C_541 on C_508 on C_532 over dev) and PR head `b02af048` (source base `a3d795ae`).
- Scope: composition acceptance only. The source head already has two POSITIVE source reviews, R325-3 and R324-3, both at `b02af048`.
- Question answered here: does the composed tree introduce any defect beyond the reviewed sources?

## Verdict summary

- **No BLOCKER, MAJOR or MINOR finding is open.** There is one new SUGGESTION (S1), and the round-3 SUGGESTIONs are retained. None of them affects lens coverage.
- **The textual composition is exact.**
  - `git merge-tree --write-tree 4ee96a61 b02af048` reproduces tree `808c97c0`.
  - The candidate changes the same 15 files against parent 1 that the source changes against its base.
  - Every per-file `git patch-id --stable` is identical in both diffs.
- **Two files overlap with the train:** `docs/testing/CI_WORKFLOWS.md` (#532) and `docs/testing/TESTING.md` (#508, #541, #443). Their hunks are disjoint, and every gate that reads them passes on the candidate.
- **The significant semantic interaction is the RTL under the measured SoC.** Between the receipt's base `a3d795ae` and the candidate, several changes landed:
  - the processor gitlink moved `09f9bf38 -> 990f9652`, adding `KL_aecp_desc_mem_guard.sv` on the AECP descriptor-memory fetch path and `KL_pp_nvm_mgr_arb.sv`, and reworking `protocol_processor_top.sv`;
  - `milan_datapath.sv` and `milan_csr.sv` also changed.

  The input gate does not bind RTL, by the round-2 decision, so it cannot see this. I therefore re-measured the product-CPU capture on the candidate with the committed harness:
  - **8x8, 50 MHz, traffic ON (16-capture build):** candidate rows 0-2 are identical, field for field, to `measurements.json` rows 0-2. That covers `sys_cycles` 2,429,800 / 2,429,322 / 2,429,864 and the request, response and descriptor-read counters. The BIOS, instrumented firmware and CPU netlist hashes equal the receipt's.
  - **8x8, 50 MHz, traffic OFF (2 captures):** the candidate and the source head give identical rows (2,426,154 twice). That equals the receipt's OFF maximum, 24.26154 ms. Both builds share BIOS `344b8a6a...` and firmware `040b8450...`; the source RTL has 115 sources without the guard, the candidate 118 with it.
  - Within what was sampled, the composed RTL is cycle-neutral on the capture path. The published 24.30454 ms / 2.0161x figure is not contradicted.

## Reconstruction (order followed)

1. AGENTS.md, CONTRIBUTING.md (section 2 step 7, candidate merge validation; section 6.1, em-dash rule), docs/README.md.
2. Issue #559 body and frozen acceptance. Decisions `5831090112` (round 2: 50 MHz contract clock, 49 ms floor, 24.5 ms STOP, census/clock gate) and round 3 (pin the step in `ci_events.py`), plus the executor's public takeover and review-ready comments.
3. PR #564 body and the manager's review-start and void comments.
4. Interface authorities: `.github/workflows/docs.yml`, `scripts/ci_events.py`, `scripts/act_ci.py` (workflow sandbox rules, read statically), `scripts/suite_shards.py`, the harness README and `measurements.json`, and snapshot ownership section 18 and UNRESOLVED 6.
5. `git diff 4ee96a61..d47a04eb`, `a3d795ae..b02af048` and `a3d795ae..4ee96a61`, plus train history.
6. Public evidence: the `review-evidence/559-r1` manifest at `c73f1dc8` (listing and environment revisions only), and the hosted check list for PR #564.
7. Prior public review findings, read only after my own pass (section "Prior findings").

## Manager items

| # | Item | Result on d47a04eb | Receipt |
|---|---|---|---|
| 1 | `ci_events.py --check` and `--selftest` | rc 0 / rc 0. 1655 contract items across 4 workflows and `CI_WORKFLOWS.md`; 2197 arms. `docs-check` composes to 50 steps, with the capture gate at position 28, between `NVM record-space gate` and `Saved-state writer gate`. The four #559 arms (removed, reordered, renamed, `if: false`) and the four act-runner-step arms (dropped, disabled, swallowed, parse-only) all report `caught`. | `receipts/gates/ci_events_*.log`, `receipts/composition.txt` |
| 1b | Act runner contract | Not run on the host (forbidden). #532 changed `act_ci.py` but pins no `docs.yml` step name or count: its `WORKFLOWS` map and `validate_workflow_sandbox` read only `uses:`, `runs-on`, `container` and `services`. My own static re-implementation over the composed `docs.yml` finds 0 untrusted `uses` and `ubuntu-latest` for all three jobs. The new step is a plain `run:`. | `receipts/composition.txt` (tail) |
| 2 | `CI_WORKFLOWS.md` coexistence | #559's paragraph (`CI_WORKFLOWS.md:1184-1195`) sits in its own hunk, away from #532's act-slot sections. Neither states a `docs-check` step count. The paragraph's order claim matches `docs.yml:222-224`, and `ci_events --check` (which parses this page) passes. | `receipts/gates/ci_events_check.log` |
| 3 | `TESTING.md` rows | #559 hunks: `:164-172` and `:378-383`. Predecessor hunks: `:268` (#443 campaign), `:271` (#508 campaign) and `:473` (#541 `crf_rx`). All four are disjoint. `suite_shards.discover_suites` requires a `Makefile` (`scripts/suite_shards.py:53`), so `run_all_suites.sh --list` gives 55 suites and excludes `nvm_capture_cpu`, as `TESTING.md:172` says. `make -n` resolves `render-csr-controls` and `gsi-mutants`. The `crf_rx` mutant names are present. | `receipts/gates/test_evidence_*.log`, `sweep_shape.log` |
| 4 | `check_nvm_capture.py` | rc 0 on the candidate (processor `990f9652`) and rc 0 on the source clone (processor `09f9bf38`). The census is 12,634 B / 156 records at 8x8 and 3,218 B / 53 at 1x1, unchanged by the pin. The four `--mutation` arms each give rc 1 with the named cause. `check_nvm_record_space.py` gives rc 0. | `receipts/gates/nvm_capture*.log`, `src_nvm_capture.log` |
| 5 | Documentation gates | `docs_check` in git mode and with `GIT_DIR=/dev/null`: 0 findings (the no-Git mode reports only the expected inventory-parity skip). `gen_toc --check`, `--verify-anchors` (179 links) and `--selftest` (1501 arms) pass. `check_em_dash --base 4ee96a61` finds 0 in 319 added lines and `--base a3d795ae` finds 0 in 1011. `check_doc_style`, `check_doc_paths`, `DOC_MAP --check` and `gen_module_matrix --check` pass. | `receipts/gates/*.log` |

Other gates on the candidate, all rc 0: `check_baremetal_only --check/--selftest` (875 files, 441 arms), `measure_test_evidence --check/--selftest`, `measure_naming --check`, `check_hygiene --check`, `check_todo_ownership`, the py/cpp/sh idiom gates, `measure_fail_fast --check`, `check_sweep_shape --self-test` and `git diff --check 4ee96a61 HEAD`. The runner is `run_gates.sh`.

## Timing composition probe

- **Method.** I ran the committed harness unchanged, from the candidate and from a scratch clone of the source head at its own submodule pins. See `run_measure.sh`, `measure_env.sh` and `compare_rows.py`.
- **Environment.**
  - LiteX component revisions equal the receipt's `soc_component_revisions`.
  - The cached CPU netlist's sha256 equals the receipt's `c208df0b...`.
  - The simulator is 5.052, the receipt's version, so no row difference can come from the simulator. The scoped 5.050 binary was identity-checked but not used.
  - The SDK compiler is 14.3.0, reached through `riscv32-linux-*` wrappers.
- **Bound.** Each foreground call is limited to 590 s.
  - The 16-capture ON run completed rows 0-2 before the bound, which matches the receipt's own build (BIOS `841e894f...`).
  - The OFF arm used 2 captures on both heads. A 2-capture build has a different BIOS from the receipt's 16-capture build, so its index 0 is compared head against head, not against the receipt.

| Run | Rows | Compared with | Result |
|---|---|---|---|
| Candidate 8x8 50 MHz ON, 16-capture build | 0-2 | receipt rows 0-2 | 3/3 identical, all fields |
| Candidate 8x8 50 MHz OFF, 2 captures | 0-1 | source head, same build | 2/2 identical; max 24.26154 ms = receipt OFF max |
| Candidate OFF vs receipt (control of the method) | 0-1 | receipt rows 0-1 | row 1 identical; row 0 differs (2,426,154 vs 2,425,516) because the 2-capture BIOS differs; the source head shows the same difference |

Receipts: `receipts/measure/row-comparison.txt`, `artifact-hashes.txt`, `*.capture.log`, `*.sources.json` (paths redacted), `tool-identity.txt`, and the full build/run logs.

## Findings

### S1 - SUGGESTION - Docs, Robustness - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1575-1576`; `tb/verilator/nvm_capture_cpu/measurements.json:3` - the merged figure will rest on RTL it was not measured on

- **Evidence.**
  - The receipt records `"base": "a3d795ae..."`.
  - Section 18 says the remedy "applies only while measured inputs remain unchanged" and "Product firmware, RTL and builder census lists remain unchanged".
  - The composed tree carries processor `990f9652` and #443/#508 datapath/CSR RTL that the measured SoC did not contain, and `check_nvm_capture.py` passes, because by decision it binds no RTL.
  - This is a live instance of the residual that R325-3 S1 and R324-3 S2 describe.
- **Impact.** None on correctness at this head: the probe above shows the capture path is cycle-identical for every sampled row. The only guard, though, is this review's re-measurement, and it is not recorded where a later reader of section 18 would look.
- **Suggested outcome.** Optional. At merge, the manager's evidence names the RTL/pin delta and cites this re-measurement. Alternatively, a later change adds the README sentence R325-3 S1 proposed.
- **Verification.** The merge evidence or README carries the statement.

No other finding. Every lens was applied to the composition; see the ledger.

## Prior findings on this PR, resolved or retained at d47a04eb

The candidate's 15 source files are patch-identical to `b02af048`, so every resolution verified at `b02af048` carries unchanged. The rows below also note where the composition could reopen a finding.

| Finding | Status at d47a04eb | Composition check |
|---|---|---|
| R325-1 F1 MAJOR (8x8 clock) | Resolved | `configs/*.yaml` and `recipe.py` are untouched by the train. The gate checks the configured and explicit clocks (rc 0). |
| R325-1 F2 MINOR (OFF-arm grading) | Resolved | The `ignore-off-timing` control is detected on the candidate. |
| R325-1 F3 MINOR (TESTING/README Makefile exception) | Resolved | The composed `TESTING.md:164-172,378-383` keeps the exception. `suite_shards` agrees. |
| R325-1 S1 SUGGESTION (substituted models) | Resolved (README "Substitutions and limits", `README.md:114`) | The file is unchanged by the train. |
| R324-1 F1 MAJOR (max over every arm) | Resolved | The receipt maxima are regraded by the gate on the candidate. |
| R324-1 F2 MAJOR (clock basis of margin) | Resolved | Same as R325-1 F1. The candidate re-measurement at 50 MHz matches. |
| R324-1 F3 MINOR (Makefile exception docs) | Resolved | Same as R325-1 F3. |
| R324-1 F4, F5 SUGGESTION (49 ms floor, phase) | Resolved (section 18 states the floor; README states the phases) | Unchanged. |
| Round-2 VOID defect (`ci_events` step pin) | Resolved | `--check` and `--selftest` pass on the composed workflows. |
| R325-3 S1, S2; R324-3 S1-S3 (SUGGESTIONs) | Retained, open, non-blocking | R325-3 S1 / R324-3 S2 are exercised by this composition; see S1 above. |

## Lens results (clean-lens format)

- [R325] PASS Conformance - `scripts/ci_events.py:1012-1015,7129-7140`; `.github/workflows/docs.yml:222-224`; `measurements.json` vs candidate re-measurement - the composed `docs-check` has 50 steps with the capture gate at 28; the #559 acceptance figure (24.30454 ms, 2.0161x against 49 ms) is not contradicted on the composed RTL (ON rows 0-2 identical to the receipt; OFF identical to the source head).
- [R325] PASS RTL - `protocol-processor` `09f9bf38..990f9652` (`KL_aecp_desc_mem_guard.sv:58`, `KL_pp_nvm_mgr_arb.sv` header, `protocol_processor_top.sv`); `hdl/milan/milan_datapath.sv`, `hdl/common/csr/milan_csr.sv`, `hdl/milan/KL_pp_shadow.sv` diffs `a3d795ae..4ee96a61` - the guard is a combinational pass-through without debt; the arbiter is on the flash device face with manager 1 tied idle; the datapath and CSR changes are GET_STREAM_INFO fields and one RO register; the `KL_pp_shadow` change is comments only; the cycle-level probe confirms no capture-path latency change in the sampled rows.
- [R325] PASS Robustness - `scripts/check_nvm_capture.py` on both processor pins; four `--mutation` arms on the candidate; `ci_events` #559 and act-runner mutation arms - the gate refuses each named drift on the composed tree, and the composed pin leaves the census unchanged.
- [R325] PASS Tests - `receipts/gates/SUMMARY.txt` (29 gates rc 0, 4 mutations rc 1); `scripts/suite_shards.py:53` with `run_all_suites.sh --list` (55 suites, harness excluded); `make -n` of the #443/#508 campaigns - the composed suite inventory and the #559 exception agree.
- [R325] PASS Docs - `docs/testing/CI_WORKFLOWS.md:1184-1195`, `docs/testing/TESTING.md:164-172,268,271,378-383,473`, section 18 and UNRESOLVED 6 (`SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1505,1734`) - disjoint hunks, no step-count prose, docs_check in both modes, TOC/anchors, em-dash against both bases, style and cited paths all clean.

## Ledger (reviewer-owned)

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN (S1 open, non-blocking) | composed `docs.yml` step list and `ci_events` pin; receipt vs candidate re-measurement; issue decisions | R325-4 | d47a04ebf2a5193dd06ed4eecf8be00f5c8502ce |
| RTL | CLEAN | processor pin delta and parent RTL delta under the measured SoC; composed build source list (118 files, guard present) | R325-4 | d47a04ebf2a5193dd06ed4eecf8be00f5c8502ce |
| Robustness | CLEAN (S1 open, non-blocking) | capture gate on both pins with 4 mutations; `ci_events` mutation arms on the composed workflows | R325-4 | d47a04ebf2a5193dd06ed4eecf8be00f5c8502ce |
| Tests | CLEAN | 29 composed gates, 4 mutations, suite inventory, campaign targets, cycle comparison | R325-4 | d47a04ebf2a5193dd06ed4eecf8be00f5c8502ce |
| Docs | CLEAN | overlap pages `CI_WORKFLOWS.md` and `TESTING.md`; section 18 and UNRESOLVED 6; all documentation gates in both modes | R325-4 | d47a04ebf2a5193dd06ed4eecf8be00f5c8502ce |

**Inherited coverage.** The composition does not touch these harness-internal artifacts:
- `sim_main.cpp` clock scheduling;
- `firmware.py` anchors;
- `probe.py` counters;
- `run.py` grader internals.

They are byte-identical to `b02af048`, so their coverage is inherited from R325-3 and R324-3 (both POSITIVE, all five lenses at `b02af0480d3a3061df24683d522799d1759f7c33`, an ancestor through parent 2). Nothing in those files changed since.

## Real limits

- **ON arm.** Only rows 0-2 of the 16 were re-measured on the candidate, because a run is limited to one 590 s foreground call. The ON worst row (index 10, 24.30454 ms) was not re-reached. The equality rests on an identical trajectory through boot plus three captures, including all traffic counters.
- **Other points not re-measured.** The 1x1 shape and the 100 MHz non-contract points were not re-measured on the candidate.
- **OFF arm.** OFF was compared head against head at 2 captures. It reaches the receipt's OFF maximum value, but not through the receipt's own 16-capture build.
- **Act runner.** Its self-test and act replay were not run (not permitted). Only a static re-implementation of its workflow sandbox rules was applied.
- **docs-check steps not replayed.** These need network, SDK installation, sv2v, the builder bank, Tcl or the donor docs build: HDL reference, diagram, solution, submodule, gPTP, wavedrom and PNG gates; feature status; builder, SoC and RTL source-list gates; the saved-state writer gate; port contracts; the SV idiom gate; archive; AEM; deploy and entity shape. None of them reads a file in the #559 overlap.
- **Hosted checks.** The listed hosted checks (`receipts/hosted-pr564-checks.txt`) ran on the PR's own merge ref against dev, not on this train candidate. `Physical gPTP` is `skipping` there, which is not an execution.
- **Physical calibration.** Physical calibration was NOT RUN, and simulation is not hardware proof. Physical timing, DDR leveling, debounce and memory ordering remain UNRESOLVED 6.
- **Out-of-scope observation (not a finding against this PR).** `docs/testing/RUNNING_TESTS.md:83` says "The default selection contains 54 suites". Both the candidate and dev `864b36f5` list 55. The composition does not change this: the Makefile count is 56 on every head, and the file is unchanged since dev. It may deserve its own issue.

## Pending manager duties

- Build and gate the final current-dev candidate at the merge turn. The live dev tip and the queue may differ from `4ee96a61`.
- Own act replay and exact-head hosted acceptance, including the act runner self-test inside the CI job boundary.
- Record the RTL/pin delta and this re-measurement in the merge evidence (S1, optional).
- Run post-merge containment and the review-integrity audit.

## Restoration

The review clone is at the exact head, with the index tree equal to HEAD's tree `808c97c0`. Worktree and index match HEAD, and tracked blob hashes and modes were re-verified (905 entries). There are 0 untracked or ignored entries after removing only the session-created caches and generated files. Submodule gitlinks: `protocol-processor 990f9652`, `gptp-processor e5dcea6e`, `third_party/verilog-axis 48ff7a7e` (all clean); `external` is uninitialized, as delivered. See `receipts/restore-verification.txt`.

R325-4 FINISHED

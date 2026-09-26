# [A324] Round 5 handoff

Status: Round 5 implemented and locally validated at `1d694677c8f376ec44e3b59b1d7fa7abccda106b`. All requested positive gates exit 0. Independent re-review and publication of the local head remain.
Start head: f36b40ddb5bf7fa5b12bba47d136e0b9d429403c.
Branch: 517-bounded-simulation-pool.
Origin confirmed: https://github.com/kebag-logic/milan-fpga.git.

## Assignment

Assignment: https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5843777653.

1. Measure complete per-leg writes and positive control, remove unsupported exclusivity, correct write-set documentation, preserve mutation sensitivity, compare pooled cold runs.
2. Normalize cancellation fixture signals and avoid concurrent ledger reads; repeat under both SIGINT dispositions and reject restored defects.
3. State eleven legs and include obj_crflic in the no-handler rationale.

Suggestions remain outside this round.

## Measured write sets and exclusivity

| Leg | Measured writes | Shared path | Exclusive decision | Positive control |
|---|---|---|---|---|
| obj_dir | No data files; stdout/stderr only | None observed | Remove/omit exclusive mark | PASS |
| obj_notify | 14 files in common-TMPDIR private `milan_nxn_tyvO5F/` for `endstation_ax7101_1x1_tdm8`; no repository writes | None | Remove exclusive mark | PASS |
| obj_crflic | No data files; stdout/stderr only | None observed | Remove/omit exclusive mark | PASS |
| obj_nxn | 14 files in common-TMPDIR private `milan_nxn_peDWb2/` for `endstation_arty_4x4`; no repository writes | None | Remove exclusive mark | PASS |
| obj_nxndv | 14 files in common-TMPDIR private `milan_nxn_bpWcY8/` for `endstation_arty_4x4`; no repository writes | None | Remove exclusive mark | PASS |
| obj_nxn8 | 14 files in common-TMPDIR private `milan_nxn_ntrLem/` for `endstation_ax7101_8x8`; no repository writes | None | Remove exclusive mark | PASS |
| obj_nxn4c | 14 files in common-TMPDIR private `milan_nxn_1syG7l/` for `endstation_arty_4x4`; no repository writes | None | Remove exclusive mark | PASS |
| obj_nolpf | No data files; stdout/stderr only | None observed | Remove/omit exclusive mark | PASS |
| obj_prune | No data files; stdout/stderr only | None observed | Remove/omit exclusive mark | PASS |
| obj_ax1x1 | No data files; stdout/stderr only | None observed | Remove/omit exclusive mark | PASS |
| obj_aclk | No data files; stdout/stderr only | None | No exclusive mark | PASS |

The positive-control column refers to the common timestamp observer control, applied to the audit mechanism used for every row; it is not eleven separately planted writes.

The private set is `generator.log`, `image.bin`, `image.json`, plus eleven files in `builder/<config>/`: `soc_params.json`, `aem_overlay.json`, `build_plan.md`, `adp_shape_defaults.svh`, `aecp_aem_rom.svh`, `gptp_ucode.hex`, `lwsrp_csr_defaults.svh`, `lwsrp_table.json`, `lwsrp_table.svh`, `platform_shape.json`, and `gen/adp_shape_defaults.svh`. Each leg opens `generator.log` twice, so 15 successful write opens name 14 distinct files. Exact generated directory names and nanosecond timestamps are preserved in `write-audit/` and `write-audit-shared/`.

Each leg also writes its distinct stdout/stderr capture. `obj_legs/replay.log` is written by the runner alone. Audit executions use separate output captures outside the repository. The first audit ran all eleven legs with separate temporary parents. The corroborating audit reran all five writers under one common `TMPDIR`; their own `mkdtemp` suffixes, shown in the table, still produced seventy distinct file paths with no pairwise intersection. Both audits reported no repository file timestamp changes. Each audit includes its own same-byte timestamp positive control. File-operation traces supplement before/after tree timestamps and 25 ms private timestamp sampling. Deletion syscalls are delayed by 100 ms only during this audit so transient files remain observable; benchmark executions are uninstrumented.

The private same-byte write positive control advanced nanosecond timestamps. The unchanged internal reviewer probe also detected a real repository-root builder write to `configs/generated/endstation_arty_4x4/gen/adp_shape_defaults.svh`, while all three suite-directory invocations wrote only private headers. Its exit was 0.

Optional frame dump: the dumping legs share the exact path named by `MILAN_COUNTER_FRAME_OUT`. Its presence, including an empty value, continues to force the entire inventory into original sequential order. The synthetic exclusivity API and overlap controls remain intact.

## Changes

| Artifact | Change |
|---|---|
| `tb/verilator/milan_dp/Makefile:544` | Document measured disjoint private writes and remove the five unsupported exclusivity marks. Arguments, banners, order, builds and post-drivers remain identical. |
| `tb/verilator/milan_dp/sim_nxn.cpp:399` | Restore the accurate base comment, including "touches nothing tracked"; executable tokens unchanged. |
| `tb/verilator/milan_dp/sim_pool.py:8` | State eleven legs and measured private writes; retain the shared-group API. |
| `tb/verilator/milan_dp/sim_pool.py:48` | Include `obj_crflic` in the eleven-leg no-handler rationale. Runtime code unchanged. |
| `tb/verilator/milan_dp/test_sim_pool.py:858` | Expect the measured unmarked inventory; retain synthetic shared-group controls. |
| `tb/verilator/milan_dp/test_sim_pool_backpressure.py:144` | Reuse the saved runner PID, without reading a live ledger after release. |
| `tb/verilator/milan_dp/test_sim_pool_backpressure.py:191` | Establish default INT/TERM/HUP dispositions and an empty signal mask before launching the runner. |
| `tb/verilator/milan_dp/test_sim_pool_backpressure.py:203` | Read the ledger while both writers are held; save the PID in the result record at line 228. |
| `tb/verilator/milan_dp/README.md:24` | Describe fourteen files per private writer and six legs with no data writes. |
| `docs/testing/TESTING.md:294` | Record the same measured contract and continued frame-dump serialization. |

Seven files changed, 49 insertions and 25 deletions. No workflow, budget, RTL, firmware, gitlink or donor change. Suggestions remain assigned to #495 and were not implemented.

## Wall clock

Pinned Verilator 5.050; eight build jobs; default two-child pool. Each timed run follows `make clean`. The host is shared. Both benchmarks had test controls on disjoint CPUs 24-31; the after run also overlaps static checks there. Timing is one shared-host sample per state. No dedicated-worker timing claim.

| Run | CPUs | Wall seconds | Exit |
|---|---|---:|---:|
| Before | 16-23 | 1356.114 | 0 |
| After | 16-23 | 1361.378 | 0 |

The after sample is 5.264 s (0.388%) slower. This pair demonstrates no incremental wall-clock gain from removing the five marks. Both complete runs report 10074 checks, zero failures, and 16 tallies. All executable hashes, all eleven leg captures, and replay bytes match. Each is one shared-host cold sample; final-head sequential/warm and hosted timing remain unmeasured in this round. The measured write-set correction is retained under the explicit Round 5 decision; no speedup is claimed.

## Backpressure repeats

| SIGINT disposition | Repeat | Verdict | Exit |
|---|---:|---|---:|
| Default | 1 | 28 PASS, 0 FAIL | 0 |
| Default | 2 | 28 PASS, 0 FAIL | 0 |
| Default | 3 | 28 PASS, 0 FAIL | 0 |
| Default | 4 | 28 PASS, 0 FAIL | 0 |
| Default | 5 | 28 PASS, 0 FAIL | 0 |
| Default | 6 | 28 PASS, 0 FAIL | 0 |
| Default | 7 | 28 PASS, 0 FAIL | 0 |
| Default | 8 | 28 PASS, 0 FAIL | 0 |
| Default | 9 | 28 PASS, 0 FAIL | 0 |
| Default | 10 | 28 PASS, 0 FAIL | 0 |
| Default | 11 | 28 PASS, 0 FAIL | 0 |
| Default | 12 | 28 PASS, 0 FAIL | 0 |
| Default | 13 | 28 PASS, 0 FAIL | 0 |
| Default | 14 | 28 PASS, 0 FAIL | 0 |
| Default | 15 | 28 PASS, 0 FAIL | 0 |
| Default | 16 | 28 PASS, 0 FAIL | 0 |
| Default | 17 | 28 PASS, 0 FAIL | 0 |
| Default | 18 | 28 PASS, 0 FAIL | 0 |
| Default | 19 | 28 PASS, 0 FAIL | 0 |
| Default | 20 | 28 PASS, 0 FAIL | 0 |
| Ignored | 1 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 2 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 3 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 4 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 5 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 6 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 7 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 8 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 9 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 10 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 11 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 12 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 13 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 14 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 15 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 16 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 17 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 18 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 19 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |
| Ignored | 20 | 28 backpressure controls: 28 PASS, 0 FAIL | 0 |

## Full default sweep

All 55 default suites passed: 2121993 checks, zero failures or timeouts, 4 declared skips. The inventory contains no missing or duplicate suite, and tally accounting is complete.

| Chunk | Suites | Checks | Exit | Seconds |
|---|---:|---:|---:|---:|
| 0/5 | 11 | 401931 | 0 | 497.306 |
| 1/5 | 21 | 173056 | 0 | 1265.875 |
| 2/5 | 10 | 1522972 | 0 | 622.153 |
| 3/5 | 12 | 13960 | 0 | 305.959 |
| 4/5 | 1 | 10074 | 0 | 1415.400 |

Each chunk ran `env VERILATOR_JOBS=16 taskset -c 16-31 scripts/run_all_suites.sh <output>/sweep-N --shard N/5`, sequentially and without a timeout override. `sweep-exits.json` records every exit. `sweep-summary.json` records every suite and declared skip. `sweep-accounting.log` is the repository tally's successful `--expect-suite-root tb/verilator` check across all five directories. The four `tsn_fuzz` field-campaign/freshness skips contribute no checks and are not hardware evidence.

## Reviewer probes

All finding-specific public probe scripts were run unchanged. SHA-256 identities are in `public-probe-hashes.json`; source commit is `f0ff6b8f51b6f1da6b1f9d37f3bf2feb9f369576` on `517-review-evidence`.

| Role | Probe | Verdict | Receipt |
|---|---|---|---|
| Internal | `probe_builder_writes.sh` | Exit 0; three suite-directory configs cause no tree write; root positive control detects a tracked-header rewrite | `reviewer-builder-internal.log`, `builder-writes/` |
| External | `builder_premise_probe.py` | Exit 0; all three configs take the private branch, no tracked rewrite, both private shape copies present | `reviewer-builder-external.log`, `builder-premise.json` |
| External | `flake_repeat.py` | 20/20 exact-head repeats, every one 28/28 and exit 0; raw logs independently checked because the probe itself does not fail on a bad repetition | `confirmed-default-results.json`, `confirmed-default-run-*.log` |
| External | `sigint_disposition_probe.py` | Exit 0; default and inherited-ignored both 28/28 | `final-signal-probe.log`, `final-signal-disposition/` |
| Internal | `probe_blocked_cancel.py` | Exit 0; INT, TERM and HUP all pass, original signal returned, no survivor | `reviewer-blocked-cancel.log`, `blocked-cancel/` |
| External | `inventory.py` | Exit 0; fourteen total legs, eleven pooled, identical executable order, banners, builds, post-drivers and interleaving; zero duplicates; one-worker inventory identical; no exclusive marks | `inventory.txt` |
| Internal | `mutate_pool.py`, eleven selected cases | All reported KILLED; see the timeout qualification below | `mutants-internal/` |
| External | `mutants.py`, seven selected cases | All reported KILLED by assertion failures | `mutants-external/` |
| External | `integrity.py` | Exit 0 and INTEGRITY PASS; tracked bytes, kinds, modes, index and gitlinks agree with the final head; no hidden index flags | `reviewer-integrity.log` |

The inherited-ignored twenty-run batch is recorded separately in `confirmed-ignored-results.json` and `confirmed-repeat-ignored-*.log`. Every run is 28/28, exit 0. The table above plus the repeat table records every selected finding-specific probe verdict.

Every mutation's individual unit/backpressure exit is in [MUTATION-VERDICTS.md](MUTATION-VERDICTS.md) and `mutation-verdicts.json`. The internal no-independent-overlap mutant reaches the unchanged guard TIMEOUT with no assertion catch: that is an UNKNOWN/hang rejection. The default-one mutant has a unit assertion failure plus a backpressure guard TIMEOUT. All other selected mutants yield assertions. Exclusivity removal fails the shared-state contention assertion, and inventory mutations fail their controls. Fixture guard improvements remain outside this round under #495.

The restored old runner blob `761ec858` produces exit 1 and 28/28 failures: 24 blocked-cancellation assertions and four missing replay-file failures. After byte restoration, unit controls pass 17/17 and backpressure controls 28/28. Real-leg cancellation corroboration also passes:

| Role | Mode | Signal | Exit | Evidence |
|---|---|---|---:|---|
| Internal | blocked | SIGINT | 0 | make status -2; 0.003 s; no survivors |
| Internal | blocked | SIGTERM | 0 | make status -15; 0.008 s; no survivors |
| Internal | blocked | SIGHUP | 0 | make status -1; 0.007 s; no survivors |
| Internal | file | SIGTERM | 0 | make status -15; 0.007 s; no survivors |
| External | blocked; live generator | SIGTERM | 0 | runner status -15; 0.05 s; no survivors |

Both public scripts ran unchanged under the repository ownership wrapper. Internal probes exercised the actual Makefile with real built legs; the external probe signaled while a real builder/image-generator descendant was live and stdout stayed unread. Raw receipts retain attribution, delivered-prefix checks, exit signals and survivor observations.


## Gates

Normal gates below all exit 0; deliberate restored defects have their expected nonzero outcomes in the probe table. No gate command was shell-piped. Each named gate has matching `.json` and `.log` receipts.

| Gate | Command | Result | Exit |
|---|---|---|---:|
| builder-sdk | `python3 builder-sdk.py` | complete test_builder.py --require-rv32; one declared NOT RUN arm; 664.974 s | 0 |
| builder-no-compiler | `python3 builder-no-compiler.py` | complete test_builder.py; two declared NOT RUN arms; 475.153 s | 0 |
| pool-unit-restored | `python3 tb/verilator/milan_dp/test_sim_pool.py` | 17/17; 6.830 s | 0 |
| pool-backpressure-restored | `python3 tb/verilator/milan_dp/test_sim_pool_backpressure.py` | 28/28; 13.242 s | 0 |
| benchmark-before | `taskset -c 16-23 make -C tb/verilator/milan_dp` | default cold pool before; 10074/0; 1356.114 s | 0 |
| benchmark-after | `taskset -c 16-23 make -C tb/verilator/milan_dp` | default cold pool after; 10074/0; 1361.378 s | 0 |
| sweep-accounting | `python3 scripts/suite_tally.py --expect-suite-root tb/verilator <five log directories>` | 55 suites; 2121993 checks; zero failures; four declared skips; complete inventory; 0.465 s | 0 |
| baremetal | `python3 scripts/check_baremetal_only.py --check` | PASS; 14.323 s | 0 |
| baremetal-selftest | `python3 scripts/check_baremetal_only.py --selftest` | PASS; 4.933 s | 0 |
| docs-git | `python3 -B scripts/docs_check.py` | PASS; 4.132 s | 0 |
| docs-no-git | `python3 -B scripts/docs_check.py` | PASS; 4.081 s | 0 |
| em-dash | `python3 scripts/check_em_dash.py --base 5c78ce2e9d831e588e759b696ed549804327e4d8` | PASS; 2.877 s | 0 |
| doc-style | `python3 scripts/check_doc_style.py` | PASS; 0.065 s | 0 |
| toc | `python3 scripts/gen_toc.py --check` | PASS; 2.476 s | 0 |
| anchors | `python3 scripts/gen_toc.py --verify-anchors` | PASS; 1.568 s | 0 |
| doc-paths | `python3 scripts/check_doc_paths.py` | PASS; 0.064 s | 0 |
| matrix | `python3 docs/traceability/gen_module_matrix.py --check` | PASS; 0.917 s | 0 |
| xvlog | `python3 scripts/xvlog_gate.py --check` | PASS; 136.387 s | 0 |
| rtl-sources | `python3 scripts/check_rtl_source_lists.py` | PASS; 1.368 s | 0 |
| sv-idiom | `python3 scripts/check_sv_idiom.py` | PASS; 0.415 s | 0 |
| rtl-lint | `python3 scripts/lint_rtl.py --check` | PASS; 8.174 s | 0 |
| cpp-idiom | `python3 scripts/check_cpp_idiom.py` | PASS; 1.166 s | 0 |
| py-idiom | `python3 scripts/check_py_idiom.py` | PASS; 3.223 s | 0 |
| port-contracts | `python3 scripts/check_port_contracts.py` | PASS; 2.270 s | 0 |
| naming | `python3 scripts/measure_naming.py --check` | PASS; 0.467 s | 0 |
| test-evidence | `python3 scripts/measure_test_evidence.py --check` | PASS; 5.227 s | 0 |
| ci-events | `python3 scripts/ci_events.py --check` | PASS; 0.214 s | 0 |
| ci-events-selftest | `python3 scripts/ci_events.py --selftest` | PASS; 14.502 s | 0 |
| phase-observation | `python3 tb/verilator/milan_dp/test_render_phase_observation.py` | PASS; 0.114 s | 0 |
| diff-check | `git diff --check` | PASS; 0.032 s | 0 |
| behave | `cd tests && behave --no-capture -f plain` | PASS; 1.166 s | 0 |
| final-diff-check | `git diff --check` | PASS; clean final worktree | 0 |
| commit-diff-check | `git diff --check HEAD^ HEAD` | PASS; committed Round 5 patch | 0 |

BDD: 344 scenarios, 1739 steps. Bare-metal self-test: 700 arms. CI event check: 1647 items; self-test: 2188 arms. Phase observation: 24/24. Git-free docs: zero findings, one declared inventory-parity skip. Xvlog and RTL-lint ratchets remain unchanged.

## Validation scope and limits

The after benchmark began at `7e57d2611a51982b2bb3bbce653aaa89f36de4d9`. Its sole difference from final head is the cancellation fixture's PID packaging, added to keep the seven-parameter idiom ratchet. `benchmark-amendment-proof.json` proves the runtime artifacts did not change. Both twenty-run signal batches, restored positive controls and static gates were rerun at final head.

The supplied read-only SDK is `$VALIDATION_STORAGE/504-manager-r1/sdk-install`. `builder-sdk.py` redirects only the existing absolute compiler selector; the unmodified complete `sw/builder/test_builder.py --require-rv32` executes with all other argv preserved. Its 855 SDK invocations are in `builder-sdk-argv.jsonl`. This is local compiler compatibility evidence, not hosted selector provisioning. The no-compiler adapter makes all RV32 candidates unavailable while retaining real host compilers. Both modes exit 0: 664.974 s and 475.153 s respectively. The pinned run declares the unavailable utilization-report gate; the no-compiler run additionally declares the compiler-dependent census/resolving instruments unavailable. These arms are NOT RUN, not passes.

The public scripts are unchanged from evidence commit `f0ff6b8f51b6f1da6b1f9d37f3bf2feb9f369576`; identities are in `public-probe-hashes.json`. Only finding-specific mutation cases were selected, as listed in `MUTATION-VERDICTS.md`. All temporary mutations were byte-restored before final-head tests. No private transcript was used.

Exploratory failures are retained in the receipts: an initial fixture edit used a missing PID field in the FIFO announcement; the final code instead uses the held-writer ledger. The first Python idiom run rejected eight parameters; the final helper keeps seven. A first git-free docs export omitted empty gitlink directories; the corrected export preserves them, matching CI. No test or budget was weakened.

## Final integrity and handoff

The final tracked worktree and initialized submodules are clean; the index matches the committed tree. The single Round 5 commit has a one-line subject and no body or trailers. `final-integrity.json` records the checks. The full original PR body was retrieved with `gh pr view 524 --json body`; `PR-BODY.md` is its updated local artifact, preserving `Closes #517`.

The public-evidence fetch and extracted scripts were read only during use, verified unchanged, and removed from temporary scratch after their final probes. No toolchain, SDK, installed package, virtual environment, tool prefix or tree export is stored in this output directory.

The head is local. No push, PR mutation, merge, additional checkout, hardware operation or donor edit was performed. Independent review, reviewer-owned lens coverage, trusted replication, hosted gates/timing, candidate validation, authorized merge and post-merge containment remain outside this author handoff. The review-ready issue comment is recorded below after posting.

Posted: [A324 REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/517#issuecomment-5844820638).

# Notification cancellation handoff

Status: REVIEW READY at `1411117e646023cb236de02e3acaf9bdfcef49e3`. Round 2 is the current result; the earlier evidence below is historical.

Base: `ed340b9b85258194247334b85e62cf9c23d4d051`.
Round-one head: `f3fef22448ce4f9bed8fd249a21a5d472148bd3d`. Branch: `pp167-notify-cancel`.
The origin URL and clean base matched the assigned processor repository and revision.
The complete assignment, issue #167, issue #69, and PR #165 HANDOFF Notes were read.
The issue has the required TAKEN notice; completion is reported with this head.

## Changes

| File and line | Change and reason |
| --- | --- |
| `hdl/aecp/KL_aecp_notify.sv:464`, `:619`, `:785` | Add a count-one pending bitmap to the existing cancellation selection. Union in live command cancellations, then clear only the owner actually selected. Preserve drain priority and the immediate cancellation of an uncontended command. |
| `hdl/aecp/KL_aecp_notify.sv:718` | Tie the added pick input to zero at count two. The existing count-two implementation is otherwise byte-identical. |
| `tb/aecp_notify/sim_main.cpp:295` | SC1 creates the exact coincidence with both probes live, for either row order; it counts both owners exactly once and checks the targeted deregistration and surviving registration. |
| `tb/aecp_notify/sim_main.cpp:185`, `:1037` | Extract unchanged input initialization to keep the entry function within the parent gate's size limit, and select the isolated SC1 run. |
| `tb/aecp_notify/Makefile:59`, `:63` | Add `collision` and a default `check` target. The existing `run` still produces the original three-run mutation record; the default suite adds SC1 as a fourth run. |
| `tb/pp_top/notify_mutants.py:440`, `:567` | Keep the existing late-cancel fault at the output, with pending acknowledgment immediate, and add the control that discards the second cancellation. |
| `tb/aecp_notify/README.md:30`, `:323` | Document four-run accounting, the same-cycle stimulus, and its planted control. |
| `tb/pp_top/README.md:2648`, `:2743` | Document the added campaign arm and why the existing delay control's insertion point preserves its exact record. |
| `docs/architecture/06_aecp_engine.md:919`, `:936` | Explain count-one draining and one pending bit per row. |

No port, parameter, register-map, top-level RTL, package, or count-two harness changes.
No STOP condition was encountered.

## Same-cycle proof

For distinct owners D (the TIME_LIMITED drain) and C (the command), both with live probes:

| Cycle | Cancellation output | Pending state after the edge | Registry action |
| --- | --- | --- | --- |
| Coincidence | D, by the existing priority | C retained; emitted D cleared | D removed; both old probe flags clear |
| Following idle cycle, without a new request | C, selected from pending state | Empty | C remains registered |
| Next cycle | None | Empty | No repeated cancellation |

The update unions old pending bits with command hits before clearing only the emitted owner. Clearing the probe flag therefore cannot erase a losing command's cancellation. Every unsent owner remains represented; another request cannot overwrite it. A command and drain for the same owner coalesce into the cancellation already emitted. Reset clears the pending bits. Existing CX1 still checks that an uncontended command cancels in its own clock and never repeats in the following eight clocks.

## New check and failing controls

SC1 launches both probes, observes the drain's cancellation before its clock edge, and presents the other controller's command in that same cycle. It observes every cancellation before the edge and runs both row orders. Setup success, probe tuples, the collision, exactly one cancellation for each owner, the expired controller's targeted DEREGISTER, and one surviving registration all contribute to its one result.

The final harness on original RTL fails SC1: the two orders produce cancellation counts `{1,0}` and `{0,1}`. The implementation produces `{1,1}` in both orders. The new planted control `cancel_collision_drops_command` replaces pending accumulation with zero and must fail SC1. This is the only new check and its only new campaign arm. The default suite totals 66 checks: 42 ordinary, 4 identify, 19 interfaces, and 1 collision.

The old `cancel_one_clock_late` fault now delays the output while leaving the internal pending acknowledgment immediate. Delaying that acknowledgment would also repeat the late pulse, changing its diagnostic from one to two pulses. The revised control restores the exact original IX3/CX1 record, including one late pulse in eight clocks. SC1 runs independently so it adds no failures to existing arms.

Planting audits cover all 298 patch arms, 234 existing exact-edit arms (235 at head), 94 other source-edit arms, and two observation edits. Every existing arm still plants. The small JSON proofs preserve each result, rather than only a total.

## Count-two evidence

The count-two generate branch is byte-identical after removing the new constant-zero tie; the count-two planted control and complete `port_tuple.hpp` harness are byte-identical. The common golden records retain 19 notification checks and six integrated interface checks. The existing `cancel_one_per_command` control retains its exact two failures, CA1 and CA1b. CA1b therefore continues to detect dropping a count-two pending cancellation. See `scope-proof.json`, `count-two-proof.json`, and the notification campaign manifest for source and run evidence.

## Processor gates and record comparison

| Gate | Base | Head | Comparison |
| --- | --- | --- | --- |
| `scripts/run_suites.sh` | rc 0; 1,028,291 checks | rc 0; 1,028,292 checks | Only SC1 added; all 33 suite counts below |
| `scripts/lint_hdl.sh` | rc 0 | rc 0 | Identical output |
| `make -j16 check` | rc 0 | rc 0 | Identical output, including 556-file ID scan |
| `scripts/gen_matrix.py --check` | rc 0 | rc 0 | Identical; 94 rows, zero untested |
| `syn/yosys/run.sh` | rc 0 | rc 0 | Same records after generated source line offsets and ordering are normalized |

The ten affected campaigns cover every campaign compiling the changed notification RTL or harness. Every common result object is compared field-for-field. Log comparison retains failing-check text, tallies, guard records, and reported observations. The only added records are the SC1 golden and its new control. No failed check is removed from comparison. The table below records each command's final return code; superseded attempts are retained separately.

Parent comparisons retain findings and graded records. The Python inventory changes from 317 modules / 200,295 lines to 317 modules / 200,316 lines; its ratcheted findings are identical. This explicitly recorded 21-line inventory delta is the campaign edit, not a changed verdict. Shadow outputs from the parallel target were interleaved, so all four retained base/head binaries were rerun into independent logs: 2,249 records including observations match. All 124 NVM case logs match after normalizing only two host-buffer pointer fields; cycles, states, payloads, events, and checks are unchanged. Build paths, elapsed time, revision metadata, and host pointers are not behavioral records.

## OOC 1x1 area

| Resource | Base | Head | Delta |
| --- | ---: | ---: | ---: |
| LUT | 23,160 | 23,101 | −59 |
| FF | 19,787 | 19,802 | +15 |
| BRAM | 17.5 | 17.5 | 0 |
| DSP | 8 | 8 | 0 |

Both OOC runs and their preparation gates returned zero. The +20 LUT / +20 FF acceptance limit is met. The notification hierarchy maps from 2,157 LUT / 1,258 FF to 2,078 LUT / 1,276 FF; the table above is the complete OOC result used for acceptance.

Both runs use the shipping 1x1 audio shape, `KL_pp_shadow`, `xc7a100t-fgg484-2`, a 20 ns clock, the area-oriented synthesis directive, and identical parameters and six image hashes. The audio shape includes CRF, hence two protocol input/output streams; the AVB-interface count is one. The measured head is `521373f6672f0058c859961e33f2cab04afb328c`. Subsequent commits change only harness initialization, campaign controls, and documentation. All production area inputs remain identical at final head, as recorded in `scope-proof.json` and `area-comparison.json`.

The simulation compiler is pinned to 5.050. Resource runs held the global lock and all local simulation build slots, with no other lane build from this assignment alongside them. Independent validations run concurrently; outer make uses 16 jobs, campaign drivers two workers, and native simulations the supported pool of two. A four-slot build admission wrapper limits each admitted compilation to four compiler jobs for the 12 GiB cap. No out-of-memory kill occurred. Package, compiler-wrapper, and firmware SDK sizes and hashes are in `environment-receipts.json`; packages and build trees remain outside the output directory.

## Scratch parent and provenance

The scratch parent remains at dev `28f9666feab2b2ba287643c63ed3a16b1e0bb863`, with both supplied adoption patches applied and its staged processor gitlink at final head. It has never been committed or pushed. Submodule Git operations verify the submodule root first. Base/head source exports match all 581 tracked processor files at their recorded revisions; these are exports, not extra checkouts.

The base and final parent commands use the same adopted source. Native gates were first attempted in a source export, then rerun successfully in the actual scratch parent because they require Git metadata. The head C++ gate initially found the new entry function over its size limit; unchanged initialization was extracted and the complete gate rerun. A head datapath invocation requested an unsupported simulation pool of 16; the runner refused it after compilation, and the final retry uses pool 2, matching base. These failed or interrupted attempts are explicitly retained and are not passing receipts.

An early documentation-gate adapter leaked Git context into self-test fixtures. Its replacement permits only read-only metadata queries; the transient worktree setting was removed and root, HEAD, edits, and configured identity were checked. The successful firmware export uses the verified pinned SDK. The compiler cache uses normal source/header validation without relaxed matching; package hashes match the local repository database. No claim of signature verification is made.

<!-- validation tables -->
## Campaigns

| Campaign | Existing arms | Base | Head |
| --- | ---: | --- | --- |
| notify | 91 | rc 0 | rc 0 |
| d3 | 110 | rc 0 | rc 0 |
| adp | 57 | rc 0 | rc 0 |
| aecp | 61 | rc 0 | rc 0 |
| dispatch | 40 | rc 0 | rc 0 |
| acmp | 33 | rc 0 | rc 0 |
| gsi | 20 | rc 0 | rc 0 |
| name | 1 | rc 0 | rc 0 |
| ctr | 17 | rc 0 | rc 0 |
| maap | 29 | rc 0 | rc 0 |

The head notify campaign adds one arm for SC1. Common records are compared without removing any failing check.

## Parent consumer gates

| Gate | Base | Head |
| --- | --- | --- |
| `check_cpp_idiom.py` | rc 0 | rc 0 |
| `check_py_idiom.py` | rc 0 | rc 0 |
| `check_rtl_source_lists.py` | rc 0 | rc 0 |
| `pp_srcs.py --check --selftest` | rc 0 | rc 0 |
| `check_port_contracts.py` | rc 0 | rc 0 |
| `measure_naming.py --check` | rc 0 | rc 0 |
| `measure_test_evidence.py --check` | rc 0 | rc 0 |
| `docs_check.py` | rc 0 | rc 0 |
| `xvlog_gate.py --check` | rc 0 | rc 0 |
| `sw/builder/test_builder.py` | rc 0 | rc 0 |
| `lint_rtl.py --check` | rc 0 | rc 0 |
| `tb/verilator/pp_shadow` | rc 0 | rc 0 |
| `tb/verilator/nvm_cosim lint` | rc 0 | rc 0 |
| `tb/verilator/nvm_cosim quick` | rc 0 | rc 0 |
| `tb/verilator/milan_dp` | rc 0 | rc 0 |
| `tb/verilator/milan_dp_render` | rc 0 | rc 0 |
| `check_sh_idiom.py` | rc 0 | rc 0 |

The builder ledger records the unavailable external calibration report explicitly; it is not covered by this validation. This is the same skipped arm as the preceding lane.

## Suite counts

| Suite | Base checks | Head checks |
| --- | ---: | ---: |
| acmp_listener | 3111 | 3111 |
| acmp_nvm | 388 | 388 |
| acmp_talker | 1342 | 1342 |
| adp_engine | 1359 | 1359 |
| aecp_notify | 65 | 66 |
| ca_originator | 16 | 16 |
| desc_mem_guard | 78 | 78 |
| desc_store | 586 | 586 |
| dispatch | 211 | 211 |
| dyn_state | 118 | 118 |
| event_router | 81 | 81 |
| lsn_admit | 18 | 18 |
| maap | 196 | 196 |
| nvm_port | 1219 | 1219 |
| originator | 107 | 107 |
| pp_top | 10469 | 10469 |
| prng | 76 | 76 |
| release_merge | 18 | 18 |
| resp_buf | 64 | 64 |
| rx_slots | 130 | 130 |
| rx_validator | 555 | 555 |
| scoreboard | 3705 | 3705 |
| side_port | 368 | 368 |
| srp_admission | 991231 | 991231 |
| srp_decoder | 190 | 190 |
| srp_encoder | 581 | 581 |
| srp_stream_fsms | 1347 | 1347 |
| srp_top | 8656 | 8656 |
| timer_map | 1360 | 1360 |
| timer_service | 48 | 48 |
| tx_arbiter | 66 | 66 |
| tx_slots | 95 | 95 |
| ucpu | 437 | 437 |

<!-- end validation tables -->

## Commits and retained evidence

```text
81d42bac0727a9f1ad997d7b7c09e7be6fc1ae73 Retain coincident availability cancellations at one interface
521373f6672f0058c859961e33f2cab04afb328c Run the collision check separately to preserve mutation records
9e907de9821a07d6e80cbc9adf85ec127ac94782 Separate notification harness input initialization
b5c1cce956477d7ee754fd300797dadd855436a6 Preserve the delayed cancellation control at the output
f3fef22448ce4f9bed8fd249a21a5d472148bd3d Document the delayed cancellation control boundary
```

`final-receipts.json` names the authoritative final logs and return-code files. `suite-comparison.json`, `record-comparison.json`, `parent-comparison.json`, `parent-nvm-records.json`, and `processor-static-comparison.json` hold comparisons. `run-artifacts.json`, `recipe-artifacts.json`, `export-artifacts.json`, the ten `campaign-*-artifacts.json` files, and `area-artifacts.json` record each retained artifact's relative path, size, and SHA-256. Paths are relative to the assignment's scratch area. Large reports, checkpoints, binaries, toolchains, packages, and exports remain there. `evidence-index.json` hashes the small handoff package, including the two supplied patches. No file in the output directory exceeds 200 KB.

No push, pull request creation or editing, rebase, hardware access, or bench action was performed. No existing issue or pull request comment was changed. The only issue notices are TAKEN and the final REVIEW READY (or STOP if acceptance is not met).

## Round 2

Status: REVIEW READY at `1411117e646023cb236de02e3acaf9bdfcef49e3`. The starting head was `f3fef22448ce4f9bed8fd249a21a5d472148bd3d`, confirmed against open PR #169, with the assigned processor origin and branch. One new commit, `Ignore failures while command cancellation is pending`, is directly on that head. No merge, rebase, amend, push, PR edit or additional TAKEN notice occurred. The adopted scratch parent remains uncommitted.

Sources: [round-two assignment](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/167#issuecomment-6052908672) and [review](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/169#issuecomment-6052904340). The reused probes come from `review-evidence/pp167-r1/reviews/R554-1` on `pp167-review-evidence`.

This closes the required outcome of R554-1-F1: a failure for the commanding owner one cycle after the collision cannot remove its live registry row or send it a targeted DEREGISTER. No port, parameter or register-map change was needed; no STOP condition was encountered.

### Changes at the new head

| File:line | Change |
| --- | --- |
| hdl/aecp/KL_aecp_notify.sv:803 | Gate count-one cf_ok_w with !cx_wait_w[cf_ix_w]. Pending state is read before the edge that emits and clears the deferred cancel. |
| tb/aecp_notify/sim_main.cpp:367 | SC2 repeats the coincidence in both row orders, presents the commanding owner failure at offset 1, and checks both cancels once, the surviving registration, and no DEREGISTER to that live controller through 400 cycles. |
| tb/aecp_notify/sim_main.cpp:243 | Select the isolated failure-window run; the existing default, identify, interfaces and SC1 runs retain their records. |
| tb/aecp_notify/Makefile:63 | Add failure-window and include SC2 as a fifth default run; keep the three-run mutation target and isolated SC1 target. |
| tb/pp_top/notify_mutants.py:575 | Add cancel_pending_accepts_failure, which removes only the new guard and must fail SC2. |
| docs/architecture/06_aecp_engine.md:919 | State the count-one pending-cancel failure rule and the new standing check. |
| tb/aecp_notify/README.md:344 | Document SC2, its failing control and the 67-check accounting. |
| tb/pp_top/README.md:2657 | Document the 93-control notification inventory and unchanged prior records. |

### Cycle proof and controls

D is the TIME_LIMITED drain row; A is the controller issuing the command. At the coincidence, D wins the cancellation output. A's command clears its probe and retains its cancel in cx_wait_r. At the following cycle, A's cancel is emitted while cx_wait_w[A] is still one; the new guard therefore rejects the failure before the same edge clears the pending bit. Both cancels still occur exactly once.

P2 establishes the reachable failure timing: if D is still in the builder, D's cancel misses the originator and A's parked second timeout may be serviced in the coincidence cycle. Its registered failure appears one cycle later. Once A's deferred cancel arrives, it either takes the action lane or is parked behind a response; both response and cancel have priority over expiry, preventing a later expiry failure. An uncontended command's cancel still lands in its own cycle and prevents the failure.

The reused P1 sources and recipes are hashed in round2/review-artifacts.json. Probe stdout and the explicit assertions are recorded in round2/probe-proof.json.

| P1 failure offset | Reviewed head: entries / live DEREGISTER | New head: entries / live DEREGISTER | Cancels at both |
| --- | --- | --- | --- |
| 0 | 1 / 0 | 1 / 0 | {1,1} |
| 1 | 0 / 1 | 1 / 0 | {1,1} |
| 2 | 0 / 1 | 0 / 1 | {1,1} |

Offset 2 is a forced unit injection outside the reachable originator window just proved; it remains in the raw probe results, rather than being omitted.

| P2 cancellation at expiry service | Failure for A at reviewed and new head |
| --- | --- |
| D, absent from the table | Yes, offset +1 |
| A, uncontended timing | None |
| None | Yes, offset +1 |

SC2 passes with one surviving row, zero DEREGISTERs to the live controller and cancellation counts {1,1} in each row order. Removing the guard fails SC2 in both orders: zero rows remain and one DEREGISTER targets the live controller. The planted RTL is byte-identical to the reviewed notification RTL. The control builds successfully, reaches its tally, fails the named check and returns nonzero; its campaign returns zero. SC1 and its second-cancel-loss control still retain their previous records.

### Count two and uncontended timing

The count-two generate block and port_tuple.hpp are byte-identical to the reviewed head. Relative to processor main, that block differs only by the already-reviewed constant-zero tie. The two-interface golden retains all 19 checks; the integrated interface golden retains six. cancel_one_per_command still fails exactly CA1 and CA1b. The late-cancel control retains IX3 and CX1 with the same observations. The top, package, register map, builder and originator are byte-identical to main. See round2/scope-proof.json, round2/count-two-proof.json and both campaign comparisons.

### Processor gates

| Gate | Main base | New head |
| --- | --- | --- |
| scripts/run_suites.sh | rc 0 | rc 0 |
| scripts/lint_hdl.sh | rc 0 | rc 0 |
| make -j16 check | rc 0 | rc 0 |
| scripts/gen_matrix.py --check | rc 0 | rc 0 |
| syn/yosys/run.sh | rc 0 | rc 0 |

All 33 suites pass: 1,028,291 to 1,028,293 checks. Only SC1 and SC2 are added relative to main; relative to the reviewed head, only SC2 is added. Lint, documentation and matrix records are identical. The portability-synthesis records match after normalizing only generated source line numbers and parallel output ordering.

| Suite | Main checks | New-head checks |
| --- | --- | --- |
| acmp_listener | 3111 | 3111 |
| acmp_nvm | 388 | 388 |
| acmp_talker | 1342 | 1342 |
| adp_engine | 1359 | 1359 |
| aecp_notify | 65 | 67 |
| ca_originator | 16 | 16 |
| desc_mem_guard | 78 | 78 |
| desc_store | 586 | 586 |
| dispatch | 211 | 211 |
| dyn_state | 118 | 118 |
| event_router | 81 | 81 |
| lsn_admit | 18 | 18 |
| maap | 196 | 196 |
| nvm_port | 1219 | 1219 |
| originator | 107 | 107 |
| pp_top | 10469 | 10469 |
| prng | 76 | 76 |
| release_merge | 18 | 18 |
| resp_buf | 64 | 64 |
| rx_slots | 130 | 130 |
| rx_validator | 555 | 555 |
| scoreboard | 3705 | 3705 |
| side_port | 368 | 368 |
| srp_admission | 991231 | 991231 |
| srp_decoder | 190 | 190 |
| srp_encoder | 581 | 581 |
| srp_stream_fsms | 1347 | 1347 |
| srp_top | 8656 | 8656 |
| timer_map | 1360 | 1360 |
| timer_service | 48 | 48 |
| tx_arbiter | 66 | 66 |
| tx_slots | 95 | 95 |
| ucpu | 437 | 437 |

### Campaigns

| Campaign | Main controls | New-head controls | Main / head |
| --- | --- | --- | --- |
| notify | 91 | 93 | rc 0 / rc 0 |
| d3 | 110 | 110 | rc 0 / rc 0 |
| adp | 57 | 57 | rc 0 / rc 0 |
| aecp | 61 | 61 | rc 0 / rc 0 |
| dispatch | 40 | 40 | rc 0 / rc 0 |
| acmp | 33 | 33 | rc 0 / rc 0 |
| gsi | 20 | 20 | rc 0 / rc 0 |
| name | 1 | 1 | rc 0 / rc 0 |
| ctr | 17 | 17 | rc 0 / rc 0 |
| maap | 29 | 29 | rc 0 / rc 0 |

All 459 existing controls retain their result objects, named failures, tallies and observations. Head has 461 controls. Relative to main, the only added records are the SC1 and SC2 goldens and their controls. Relative to the reviewed packet, only SC2 and its control are added. All 298 patch arms, 234 existing exact-edit arms, 94 other edit arms and two observation anchors still plant; head adds two exact-edit arms. The full notification campaign includes the new control, in addition to its earlier focused run.

### Parent consumers

The scratch parent is still dev 28f9666feab2b2ba287643c63ed3a16b1e0bb863 with both supplied adoption patches. Their application was verified by reverse checks. Its staged processor gitlink and submodule HEAD are the new head. Each submodule Git operation verifies its top-level directory first. No parent commit or push was made.

| Consumer gate | Main base | New head |
| --- | --- | --- |
| python3 scripts/check_cpp_idiom.py | rc 0 | rc 0 |
| python3 scripts/check_py_idiom.py | rc 0 | rc 0 |
| python3 scripts/check_rtl_source_lists.py | rc 0 | rc 0 |
| python3 scripts/pp_srcs.py --check --selftest | rc 0 | rc 0 |
| python3 scripts/check_port_contracts.py | rc 0 | rc 0 |
| python3 scripts/measure_naming.py --check | rc 0 | rc 0 |
| python3 scripts/measure_test_evidence.py --check | rc 0 | rc 0 |
| python3 scripts/docs_check.py | rc 0 | rc 0 |
| python3 scripts/xvlog_gate.py --check | rc 0 | rc 0 |
| python3 sw/builder/test_builder.py | rc 0 | rc 0 |
| python3 scripts/lint_rtl.py --check | rc 0 | rc 0 |
| make -j16 -C tb/verilator/pp_shadow | rc 0 | rc 0 |
| make -j16 -C tb/verilator/nvm_cosim lint | rc 0 | rc 0 |
| make -j16 -C tb/verilator/nvm_cosim quick JOBS=4 POOL=2 | rc 0 | rc 0 |
| make -j16 -C tb/verilator/milan_dp SIM_JOBS=2 | rc 0 | rc 0 |
| make -j16 -C tb/verilator/milan_dp_render | rc 0 | rc 0 |
| python3 scripts/check_sh_idiom.py | rc 0 | rc 0 |

All behavioral records match. Python inventory remains 317 modules and changes from 200,295 to 200,324 lines: 21 from round one and eight from the new control. Findings are unchanged. All 11,615 datapath records match. Four retained shadow binaries per side are rerun into separate logs to compare all 2,249 records without parallel-output interleaving. All 124 NVM case logs match after normalizing only the two host-buffer address diagnostics; cycles, state, payload, events and checks remain compared. The existing external calibration-report arm remains explicitly not run; no physical calibration or hardware result is claimed.

### OOC 1x1

| Resource | Fresh main baseline | Exact new head | Delta |
| --- | --- | --- | --- |
| LUT | 23,160 | 23,171 | +11 |
| FF | 19,787 | 19,807 | +20 |
| BRAM | 17.5 | 17.5 | +0 |
| DSP | 8 | 8 | +0 |

Both fresh measurements and their preparation, elaboration and resource gates return zero. Both LUT and FF deltas meet the +20 limits. The measurements use identical parameters and all six image hashes, the shipping 1x1 audio shape including CRF, KL_pp_shadow, the same target and a 20 ns clock. The interface count is one. Every synthesis invocation holds the shared lock and all build slots; no simulation build overlaps it.

### Evidence and limits

Build links are removed after validation and generated parent files are retained outside the scratch checkout. parent-final-state.json records the final gitlink, adoption patches and cleanup.

All round-two evidence is indexed under round2/. final-receipts.json identifies each authoritative log, return code, size and SHA-256. source-base.json and source-head.json hash all 581 tracked source files; export-proof.json verifies the head export. The campaign, parent, probe, static, count-two and area comparisons retain their exact scope. shadow-record-inputs.json binds the separate captures to their binary, ROM and output hashes. Recipe, review-input, run, campaign, NVM and area manifests hash the retained scratch artifacts. No tree export, installed package, toolchain or file over 200 KB is in the output packet.

The simulation compiler is pinned to 5.050. Outer make uses 16 jobs, campaign drivers two workers, and the build admission wrapper four slots with four compiler jobs each. The 12 GiB service cap is enforced; page-cache reclamation occurred, with no out-of-memory events.

Completion notice: `[A568] REVIEW READY 1411117e646023cb236de02e3acaf9bdfcef49e3` on processor issue #167.

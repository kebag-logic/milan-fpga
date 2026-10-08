# Notification cancellation handoff

Status: REVIEW READY; every required final gate passed.

Base: `ed340b9b85258194247334b85e62cf9c23d4d051`.
Head: `f3fef22448ce4f9bed8fd249a21a5d472148bd3d`. Branch: `pp167-notify-cancel`.
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

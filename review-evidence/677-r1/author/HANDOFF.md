[A556]

# Firmware robustness fixes handoff (#677, #678)

Status: REVIEW READY, posted on #677 (comment 6024328677). Every assigned gate ran at the exact head and returned
0. The two long CONTRIBUTING gates are owed (see Remaining responsibilities).
Branch `677-fw-fixes` -> `dev`, not pushed.
Head: `6c94e9f5f496ac25f8c4e31f9e3685c725de29f3` (one commit on the base).
Base: `6714181d0c8a16e2983f85b724f4d688f5111835` (dev with FT, PR #675, merged).
Assignment: #677 comment 6021510152, covering #677 and the manager ruling in #678.
Executor: [A556]. Internal reviewer: [R524]. External reviewer: [R525].
The origin URL and the initial head matched the assignment, and the initial tree was clean.

## What the change is

This is a bounds-checking fix and a re-entrancy robustness fix in the
bare-metal control firmware. Both changes are host-tested at the FT coverage
ratchet. Firmware stays freestanding C11, with no heap and no OS.

- **#677, out-of-bounds read.** `nvm_klj2_record` checked an erased
  record's payload against the container end only. That end comes from the
  container's own length field. A caller holding just a loaded prefix could
  have `nvm_all_erased` read past its buffer. The codec now refuses a payload
  that extends beyond `loaded` (`NVM_VD_REC`, incomplete prefix) before any
  read. The existing `end` check still runs first, so a payload that overruns
  the container still gets `NVM_VD_LEN`.
- **#678, re-entrant port callbacks.** The ADP core assumed, without
  stating it, that no port calls back into the core while the core is calling
  it. A zero-delay timer that expires inline, for example, would mutate state
  mid-transition. The rule is now written in `adp.h` and in every firmware port
  header. A shared guard enforces it: it brackets all six port calls, and every
  public ADP entry checks it before touching its arguments. That includes
  `adp_init` (uninitialized destination) and `adp_build` (const instance, no
  cast). A violation asserts in debug and test builds. In release builds the
  call is ignored and counted in a lifetime counter (modulo 2^32). A rejected
  `adp_poll` returns false. The guard spans every instance owned by the one
  event loop; it is a diagnostic, not a concurrency lock.

| File:line | Change |
|---|---|
| `sw/firmware/ctrl_nvm/nvm_klj2.c:298` | Refuse an erased payload beyond `loaded` before reading; the container-length verdict is preserved. |
| `sw/firmware/ctrl/adp/adp.c:22` | Shared guard and lifetime counter; all six port calls bracketed; every public entry refuses re-entry before touching arguments. Debug asserts; release counts and ignores. |
| `sw/firmware/ctrl/adp/adp.h:130` | No-callback contract, zero-delay dispatch, cross-instance scope, build-mode behavior and diagnostic accessor (`adp_reentry_count`, line 214). |
| `sw/firmware/ctrl/adp/adp_mbx.h:89` | Adapter port rule. |
| `sw/firmware/ctrl/mbx/mbx.h:19` | Mailbox port rule. |
| `sw/firmware/ctrl/mbx/mbx_hal.h:24` | HAL port rule. |
| `sw/firmware/ctrl/port/ctrl_debug.h:13` | Debug sink port rule. |
| `sw/firmware/ctrl/port/ctrl_pool.h:19` | Pool port rule. |
| `sw/firmware/ctrl/port/shlan_port.h:27` | Protocol port rule, including F2-F5 inheritance. |
| `sw/firmware/ctrl_nvm/nvm_flash.h:30` | Flash port rule. |
| `sw/firmware/ctrl_nvm/nvm_state.h:49` | Store state-port rule. |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.h:6` | LiteSPI port rule. |
| `sw/firmware/ctrl/test/test_adp_reentry.cpp:147` | Two inline-expiry probes and 120 port/entry/instance combinations, each in debug and release; real assertions and deferred positive controls. |
| `sw/firmware/ctrl/test/ctrl_arms.py:36` | Build and run the debug and release arms; flush child gcov counters in assertion tests. |
| `sw/firmware/ctrl/test/ctrl_mutants.py:58` | Three new guard/count/refusal defects; the 76 previous mutants retained; job limit respected. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:82` | Run the new arms in the default and coverage gates; propagate `--jobs`; document the assertion symbol in RV32 builds. |
| `sw/firmware/ctrl_nvm/test/test_nvm_prefix.cpp:18` | Exact-sized sanitizer buffers at 40/47/48 bytes and both sides of the last-payload boundary. |
| `sw/firmware/ctrl_nvm/test/test_nvm_codec.cpp:86` | Obsolete deferred-work note replaced by the new sanitizer test reference. |
| `sw/firmware/ctrl_nvm/test/nvm_bench.py:81` | Dedicated sanitizer binary in the default and coverage gates; named fatal-test attribution preserved. |
| `sw/firmware/ctrl_nvm/test/nvm_mutants.py:142` | Restored `end` bound and both off-by-one guard defects; all 106 previous mutants retained. |
| `sw/firmware/gtest/fw_gtest.py:59` | Host-only AddressSanitizer build/link option, compatible with coverage; non-PIE sanitizer executable. |
| `sw/firmware/gtest/fw_coverage.py:427` | Honor the requested worker limit in both firmware drivers. |
| `sw/firmware/gtest/coverage.ratchet:5` | Regenerated only through `fw_coverage.py --write`: ADP 168/73 -> 204 lines/95 arcs, codec 195/104 -> 198 lines/106 arcs; 100% retained. |
| `sw/firmware/gtest/README.md:263` | The five ADP exclusion proofs cite the public no-callback rule; new arms and ASan documented; no exclusion added. |
| `sw/firmware/ctrl/README.md:57` | List the new arms and the RV32 assertion dependency. |
| `sw/firmware/ctrl_nvm/README.md:472` | Document the exact-prefix sanitizer checks and the 109-mutant campaign. |

No RTL, constraint, configuration, generated-RTL, builder or workflow file
changed. The diff touches 26 files, all under `sw/firmware/`. Neither the
shipping bare-metal image nor the default all-fabric build compiles
`sw/firmware/ctrl` or `sw/firmware/ctrl_nvm`. The only mention of the codec in
`sw/firmware/milan_baremetal/milan_baremetal.c` (line 606) is a comment.
Per-file sizes, SHA-256 and git blob IDs at the head are in `candidate-files.json`.

## New tests and the planted defects they catch

| Test and source | Required behavior | Planted defect caught |
|---|---|---|
| `AdpReentry.AdvertiseInlineExpiry`, `test_adp_reentry.cpp:147` | An inline ADVERTISE expiry asserts in debug and is counted/refused in release; a valid deferred expiry advances later | `reentry-guard-removed` in both modes; `reentry-uncounted` and `reentry-not-ignored` in release |
| `AdpReentry.DelayInlineExpiryOnGmChange`, `test_adp_reentry.cpp:174` | An inline DELAY expiry asserts or is counted/refused; the deferred expiry reaches WAITING | `reentry-guard-removed` in both modes |
| `AllPorts/AdpPortEntry.RefusesBeforeTouchingState`, `test_adp_reentry.cpp:201` | 6 ports x 10 entries x same/other instance = 120 cases per mode; real assertion, or unchanged state/output and exactly one count | `reentry-not-ignored`, `reentry-uncounted`; guard removal also fails the matrix |
| `NvmCodec.codec_erased_loaded_prefix`, `test_nvm_prefix.cpp:18` | Exact allocated lengths 40/47/48 refuse safely; the final payload is accepted at exactly its end and refused one byte short | `erased_payload_end_bound` (ASan heap-buffer-overflow), `erased_payload_guard_early`, `erased_payload_guard_late` |

At this head the campaign reported (`logs/ctrl.log`):
- `reentry-guard-removed`: 2650 failed checks, first `AdpReentry.AdvertiseInlineExpiry: inline ADVERTISE expiry asserts`.
- `reentry-uncounted`: 122 failed checks.
- `reentry-not-ignored`: 1083 failed checks.

`logs/nvm-batch-1-20.log` shows all three erased-payload defects caught by
`codec_erased_loaded_prefix`. `logs/erased-end-asan.log` is a separate witness
at this head: it plants the restored `end` bound and runs the named test. The
log shows `AddressSanitizer: heap-buffer-overflow`, a 1-byte READ in
`nvm_all_erased` reached from `nvm_klj2_record` (lines 115 and 301 of the
planted copy), and `[FAIL] NvmCodec.codec_erased_loaded_prefix`.

No test filter is applied to positive controls. The debug child keeps the real
assertion diagnostic and exits on SIGABRT; it flushes gcov only in coverage
builds. Deferred positive controls run outside the failing child.

All 106 NVM mutants at the base are retained, including the 102 store defects
the assignment names, and three are added (109). All 76 previous
control-firmware mutants are retained, and three are added (79). No existing
test, mutant or acceptance check is weakened.

## Results at the head

- Control firmware: 423 host checks pass (model 14, port 30, ADP 26, unit 21,
  MMIO 2, walk 41, entity 5x9, debug re-entry 122, release re-entry 122). The
  RV32I freestanding build passes (9 objects). Mutants: 79 of 79 caught.
- Tally listener: 18 of 18 listener defects caught.
- NVM store: 435 tests across 5 shapes, with all five RV32 builds. Mutants:
  109 of 109 caught. `nvm-campaign.json` lists every repository mutant exactly
  once, with no finding.
- Coverage: `--selftest` and `--check` pass. The check includes the pinned
  optional lwSRP arm.
- Builder bank: all 100 functions of `sw/builder/test_builder.py`. Function 13
  ran as census slices: 358 mutations in six slices and 43 disconnected
  identity controls in four slices. Each case ran exactly once, and 53/53 RTL
  mutation variants were elaborated before counting.
- Docs and tooling bank: 47 commands, all return 0.
- Optional controls: the lwSRP arm and both lwSRP pin defects pass. The
  mailbox firmware co-simulation passes (13 checks: firmware on the RTL and
  on the model; RTL unchanged).

## Coverage

Coverage after the existing documented exclusions, measured at the head by
`fw_coverage.py --check`. All 14 files are at 100% lines and branches; 0/0
means the file has no branch.

| File | Covered lines | Covered branches |
|---|---|---|
| `sw/firmware/ctrl/adp/adp.c` | 204/204 | 95/95 |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/38 |
| `sw/firmware/ctrl/app/ctrl_app.c` | 12/12 | 6/6 |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 93/93 | 54/54 |
| `sw/firmware/ctrl/mbx/mbx.c` | 162/162 | 60/60 |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 198/198 | 106/106 |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/259 |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/63 |

Raw ADP counts are 204/206 lines and 95/102 arcs; raw codec counts are 198/199
lines and 106/110 arcs. The exclusion table has 15 rows at the base and 15 at
the head, with the same file and item columns. The five ADP rows changed only
their proof text, which now cites the `adp.h` rule. No exclusion was added or
expanded. The gate verifies that every excluded arc is still uncovered and
refuses stale rows.

## Validation method

The lane checkout is clean at the head, and its tree diff from the base is
byte-identical to the validated patch. The firmware gates and the docs bank ran
there, with every build directory in scratch outside the checkout; the tree was
clean after each run. The builder bank and the co-simulation ran in disposable
clones at the head. Their submodules were cloned at the pinned commits
(protocol-processor `ead80360`, gptp-processor `5dce647a`, verilog-axis
`48ff7a7e`). Batches that ran at the same time each used their own clone.
Those submodule clones are standalone, which git reports as uninitialized
(`-`). CONTRIBUTING's pin-proving gates refuse such clones, so `xvlog_gate.py`,
`lint_rtl.py` and the rest of the bank ran in the lane checkout instead, where
`git submodule status` shows the three registered pins initialized. No builder
function refused or skipped on submodule state; its only skip is gate 11 below.

Each gate ran in the foreground under a 590-second watchdog that records the
return code, the duration and the peak cgroup memory. Campaign drivers used at
most four workers. The co-simulation used `make -j8` with Verilator `-j 2`.
No hardware was used.

Three suites exceed one foreground window unsharded, so they ran in bounded
pieces using the repository's own functions:

- **NVM campaign.** `nvm_batch.py` calls the repository's `prepare`,
  `build`, `suite_tests`, `unnamed_checks` and `plant_and_grade` functions. It
  runs six disjoint slices of `nvm_mutants.MUTANTS`. Each batch first repeats
  the named-test audit, then plants every defect into its own complete build.
  `nvm_aggregate.py` requires exactly the 109 repository names, each once, and
  no finding.
- **Control campaign.** The full `--self-test` ran unsharded (553.9 s).
- **Builder bank.** `builder_batch.py` reads the 100-function list directly
  from `test_builder.py`. Batches 1-35 (excluding function 13), 36-65 and
  66-100 run the functions unchanged.
  - Function 13 (`test_baremetal_profile_contract`) is run in census slices.
  - A prefix slice runs the function through its mutation loop over one
    disjoint slice. It then applies the same elaboration accounting the
    function asserts after that loop: Verilator present, and elaborated ==
    requested. Then it returns.
  - A suffix slice skips the mutation loop and runs the rest of the function,
    with one disjoint slice of the disconnected identity controls.
  - Every assertion inside both loops is unchanged. `builder-census.json` shows
    that the slices partition both catalogs exactly once and that every
    selected case completed.
  - The function's closing summary prints catalog-wide totals even inside a
    slice. Only the per-slice manifests and return codes count as evidence.
    This is bounded execution, not an alternate pass criterion.
  - Only the compiler executable is redirected to the repository-pinned SDK
    (`scripts/ci_rv32_sdk.py`; the CI workflows install the same SDK at the
    path the builder names). Its flags and every verdict are kept. The SDK
    archive SHA-256 is
    `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`
    (102,597,892 bytes).

The attached helpers are the same as the executed ones, except that they read
their work directory from `VALIDATION_WORK` (outside the checkout and this
directory); the builder helper also requires `RV32_SDK`. `builder_batch.py` is
the exact file that ran. Run the helpers from a disposable checkout at the
head. The standard full-driver commands are in PR-BODY.md.

## Gate table

Every entry ran at head `6c94e9f5`. Each normalized log is in `logs/<gate>.log`.
The raw log's size and SHA-256 are in `evidence.json`. Memory is the peak of
the service cgroup's `memory.current`, which includes page cache.

| Gate | Exact command (scratch locations normalized) | rc | Seconds | Peak GB |
|---|---|---|---|---|
| tally | `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 0 | 60.0 | 1.9 |
| ctrl | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --jobs 4 --build-dir <scratch>/ctrl-full` | 0 | 553.9 | 1.9 |
| nvm-controls | `python3 -u sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | 96.6 | 3.3 |
| nvm-batch-1-20 | `python3 -u <scratch>/nvm_batch.py 1 20` | 0 | 355.8 | 3.3 |
| nvm-batch-21-40 | `python3 -u <scratch>/nvm_batch.py 21 40` | 0 | 396.8 | 7.2 |
| nvm-batch-41-60 | `python3 -u <scratch>/nvm_batch.py 41 60` | 0 | 395.9 | 7.2 |
| nvm-batch-61-80 | `python3 -u <scratch>/nvm_batch.py 61 80` | 0 | 393.8 | 8.9 |
| nvm-batch-81-95 | `python3 -u <scratch>/nvm_batch.py 81 95` | 0 | 328.1 | 8.9 |
| nvm-batch-96-109 | `python3 -u <scratch>/nvm_batch.py 96 109` | 0 | 278.7 | 9.4 |
| erased-end-asan | `python3 <scratch>/asan_witness.py` | 0 | 32.0 | 2.0 |
| coverage-selftest | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | 0.5 | 7.1 |
| coverage-check | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4 --lwsrp <lwSRP> --keep <scratch>/coverage-check` | 0 | 130.6 | 1.8 |
| lwsrp | `python3 <scratch>/lwsrp.py <lwSRP>` | 0 | 4.5 | 1.1 |
| mbx-cosim | `python3 <scratch>/cosim.py` | 0 | 7.0 | 1.6 |
| builder-1-35 | `python3 -u <evidence>/builder_batch.py 1 35 --without-census --require-rv32` | 0 | 54.5 | 1.1 |
| builder-1-35-isolated | `python3 -u <evidence>/builder_batch.py 1 35 --without-census --require-rv32` | 0 | 56.0 | 1.2 |
| builder-36-65 | `python3 -u <evidence>/builder_batch.py 36 65 --require-rv32` | 0 | 56.0 | 1.2 |
| builder-66-100 | `python3 -u <evidence>/builder_batch.py 66 100 --require-rv32` | 0 | 89.6 | 1.2 |
| census-prefix-0-of-6 | `python3 -u <evidence>/builder_batch.py 13 13 --require-rv32 --census-shard 0/6 --census-phase prefix` | 0 | 375.2 | 1.4 |
| census-prefix-1-of-6 | `... --census-shard 1/6 --census-phase prefix` | 0 | 402.3 | 2.0 |
| census-prefix-2-of-6 | `... --census-shard 2/6 --census-phase prefix` | 0 | 406.9 | 2.0 |
| census-prefix-3-of-6 | `... --census-shard 3/6 --census-phase prefix` | 0 | 391.3 | 2.0 |
| census-prefix-4-of-6 | `... --census-shard 4/6 --census-phase prefix` | 0 | 391.8 | 2.0 |
| census-prefix-5-of-6 | `... --census-shard 5/6 --census-phase prefix` | 0 | 389.3 | 1.6 |
| census-suffix-0-of-4 | `python3 -u <evidence>/builder_batch.py 13 13 --require-rv32 --census-shard 0/4 --census-phase suffix` | 0 | 346.7 | 1.6 |
| census-suffix-1-of-4 | `... --census-shard 1/4 --census-phase suffix` | 0 | 353.7 | 1.2 |
| census-suffix-2-of-4 | `... --census-shard 2/4 --census-phase suffix` | 0 | 351.2 | 1.2 |
| census-suffix-3-of-4 | `... --census-shard 3/4 --census-phase suffix` | 0 | 355.3 | 8.9 |
| bank-01 | `python3 avdecc/gen_aem_store.py --self-test` | 0 | 0.5 | 0.9 |
| bank-02 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | 0.5 | 0.9 |
| bank-03 | `python3 scripts/lint_rtl.py --check --self-test` | 0 | 10.0 | 8.9 |
| bank-04 | `python3 scripts/suite_shards.py --selftest` | 0 | 0.5 | 0.9 |
| bank-05 | `python3 scripts/ci_events.py --check` | 0 | 1.5 | 4.9 |
| bank-06 | `python3 scripts/ci_scope.py --selftest` | 0 | 9.0 | 9.0 |
| bank-07 | `python3 scripts/ci_events.py --selftest` | 0 | 23.5 | 9.0 |
| bank-08 | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | 3.5 | 9.0 |
| bank-09 | `python3 scripts/check_feature_status.py` | 0 | 1.5 | 1.6 |
| bank-10 | `python3 scripts/check_submodule_docs.py` | 0 | 1.0 | 1.6 |
| bank-11 | `python3 scripts/check_cpp_idiom.py` | 0 | 2.0 | 1.5 |
| bank-12 | `python3 scripts/check_py_idiom.py` | 0 | 5.0 | 1.2 |
| bank-13 | `python3 scripts/docs_check.py` | 0 | 6.5 | 1.2 |
| bank-14 | `python3 scripts/check_doc_style.py` | 0 | 0.5 | 1.1 |
| bank-15 | `python3 scripts/check_doc_style.py --selftest` | 0 | 0.5 | 1.1 |
| bank-16 | `python3 scripts/check_solution_docs.py` | 0 | 0.5 | 1.1 |
| bank-17 | `python3 scripts/check_doc_paths.py` | 0 | 0.5 | 1.1 |
| bank-18 | `python3 scripts/check_archive.py` | 0 | 0.5 | 1.2 |
| bank-19 | `python3 scripts/gen_toc.py --verify-anchors` | 0 | 3.5 | 1.2 |
| bank-20 | `python3 scripts/gen_toc.py --check` | 0 | 5.5 | 1.1 |
| bank-21 | `python3 scripts/check_hygiene.py --check` | 0 | 0.5 | 1.1 |
| bank-22 | `python3 scripts/check_todo_ownership.py` | 0 | 2.0 | 1.1 |
| bank-23 | `python3 scripts/check_sv_idiom.py` | 0 | 1.0 | 1.1 |
| bank-24 | `python3 scripts/check_sh_idiom.py` | 0 | 0.5 | 1.1 |
| bank-25 | `python3 scripts/check_rtl_source_lists.py` | 0 | 2.0 | 1.1 |
| bank-26 | `python3 scripts/check_soc_sources.py` | 0 | 0.5 | 1.1 |
| bank-27 | `python3 scripts/check_port_contracts.py` | 0 | 3.0 | 1.1 |
| bank-28 | `python3 scripts/check_nvm_record_space.py` | 0 | 3.0 | 1.1 |
| bank-29 | `python3 scripts/check_baremetal_only.py --check` | 0 | 20.5 | 1.2 |
| bank-30 | `python3 scripts/check_baremetal_only.py --selftest` | 0 | 7.5 | 1.1 |
| bank-31 | `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | 80.6 | 1.2 |
| bank-32 | `python3 scripts/check_sweep_shape.py --self-test` | 0 | 16.5 | 1.2 |
| bank-33 | `python3 scripts/xvlog_gate.py --check` | 0 | 158.6 | 1.3 |
| bank-34 | `python3 scripts/measure_control_flow.py --selftest` | 0 | 0.5 | 1.1 |
| bank-35 | `python3 scripts/measure_cohesion.py --selftest` | 0 | 0.5 | 1.1 |
| bank-36 | `python3 scripts/check_em_dash.py --base 6714181d0c8a16e2983f85b724f4d688f5111835` | 0 | 3.5 | 1.2 |
| bank-37 | `python3 scripts/measure_fail_fast.py --check` | 0 | 2.0 | 1.2 |
| bank-38 | `python3 scripts/measure_test_evidence.py --check` | 0 | 7.5 | 1.2 |
| bank-39 | `python3 scripts/measure_naming.py --check` | 0 | 1.0 | 1.2 |
| bank-40 | `python3 scripts/measure_test_evidence.py --selftest` | 0 | 7.5 | 1.2 |
| bank-41 | `python3 scripts/gen_toc.py --selftest` | 0 | 1.0 | 1.2 |
| bank-42 | `python3 scripts/check_em_dash.py --selftest` | 0 | 3.5 | 1.2 |
| bank-43 | `python3 scripts/docs_check.py --selftest` | 0 | 0.5 | 1.1 |
| bank-44 | `git diff --check 6714181d0c8a16e2983f85b724f4d688f5111835` (clean tree at the head) | 0 | 0.5 | 1.2 |
| bank-45 | `python3 scripts/check_wire_accountability.py --self-test` | 0 | 0.5 | 1.2 |
| bank-46 | `python3 scripts/check_entity_shape.py --self-test` | 0 | 57.1 | 1.2 |
| bank-47 | `python3 scripts/check_deploy_shape.py --self-test` | 0 | 0.5 | 1.2 |

The bank ran with the documentation dependencies from the repository's hashed
requirements first on `PATH` and the pinned Verilator 5.050 next.

One builder arm is NOT RUN, and the test registers it as a skip. The resource
calibration (gate 11) needs a historical mf48 placement report that is not on
this host. No calibration data was invented. A return code of 0 does not turn
that skip into a pass.

### Runs that do not count

- **Earlier receipts.** The previous session's receipts were recorded before
  the commit existed. They are superseded by the exact-head runs above and are
  not cited.
- **First builder 1-35 attempt.** It failed during setup: the first head clone
  carried submodule files without their git metadata, and the builder found
  "no tracked .sv files". The submodules were then cloned at their pins.
- **First builder 36-65 attempt.** It failed in
  `test_build_sh_grades_its_own_bindings`: the dry run refused because
  regenerating `configs/endstation_arty_current.yaml` would rewrite
  `hdl/common/csr/gen/lwsrp_csr_defaults.svh`.
  - That attempt shared one clone with the concurrent 1-35 batch, and the clone
    was clean afterwards.
  - Rerun in a clone of its own, 36-65 passed. 1-35 was also rerun alone
    (`builder-1-35-isolated`) and passed.
  - My attribution of the failure to the shared clone is an inference; I did
    not isolate the exact cause.

The receipts above for both labels are the reruns.

## Environment and execution limits

- Host toolchain: GCC/gcov 16.2.1; GoogleTest/GoogleMock 1.18.0.
- Firmware RV32 builds: GCC 14.3.0, freestanding RV32I/ilp32.
- Builder census: the pinned riscv32-ilp32d stable-2025.08-1 SDK.
- Verilator: 5.050.
- lwSRP pin: `19f5796b63652eb1151906de73cb827d4980a53f`; that checkout was
  clean and at the pin afterwards.

The cgroup's `memory.current` peaked at 9.42 GB. Gate peaks reached 9.36 GB
during the last NVM batch and about 9.0 GB during three bank checks. That is
above the 9 GB target and under the 12 GB cap. In a sample taken shortly after
the NVM batches, 7.65 of 8.08 GB was inactive page cache and 0.19 GB was
anonymous memory. Removing the completed build products dropped it to 0.38 GB.
`memory.events` records no OOM or high/max event.

Free space on `/data` stayed at or above 154 GB (floor: 30 GB). This directory
contains no toolchain, package installation, tree export, or file over 200 KB.

## Remaining responsibilities

- **Executor limits.** No push, PR creation or edit, merge, rebase, bench
  access or flashing. Only TAKEN and this REVIEW READY are posted on #677.
- **Evidence limits.**
  - The RV32 gates prove freestanding object compilation and the symbol
    inventory (`__assert_fail` is listed as undefined). They do not prove a
    linked target image or a target assertion handler.
  - The shared guard is not a concurrency lock.
  - No target timing or board claim is made.
- **Not run.** Hosted CI and the local hosted-workflow replica (`act_ci.py
  --pr`) need a published PR head, which the assignment does not allow.
- **Owed, not run.** `scripts/ci_scope.py` classifies any change under `sw/`
  as RTL/tooling-relevant. CONTRIBUTING therefore also requires the two long
  local gates before the PR is marked validated: `scripts/run_all_suites.sh`
  and `syn/yosys/run.sh`. The assignment's gate list does not include them,
  and this lane did not run them. The RTL is unchanged, but those results are
  still owed.
- **Pending with reviewers.** Both independent reviews, reviewer-owned lens
  coverage, candidate-merge validation and post-merge containment. The
  executor supplies no approval verdict.

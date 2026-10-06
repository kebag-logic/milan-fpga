[A557]

# First-round record

Historical record, superseded by public ruling 6022358702.

Status: STOP. Implementation committed; required local validation is blocked at builder gate 1b.
Branch: `679-rv32-sdk` -> `dev`.
Base: `6714181d0c8a16e2983f85b724f4d688f5111835`.
Head: `0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe`.
Executor: [A557]. Internal reviewer: [R526]. External reviewer: [R527].
Assignment: https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6021510923
Takeover: https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6021534259

## Scope and decision

The existing RV32 arms compile objects; they do not link an image. Retain that boundary and the pinned ILP32D SDK. Compile RV32I/ILP32 with `-ffreestanding`, isolated compiler-provided standard headers and declarations for the existing memory/format interfaces. No alternate SDK, glibc stub, OS, heap, runtime implementation or shipping-source change is introduced. `-nostdlib` is a link option; no new link is claimed. The existing shipping runtime is selected through its generated build environment and does not provide the ctrl formatter interface as a standalone validation runtime.

The assignment's linked-image sizes and whole-program stack wording therefore remains an evidence limitation: the figures here are object sizes and individual static frames. Firmware-unit is wired to require both RV32 arms. Hosted and supported act evidence cannot be produced before a separately authorized publication, which this session forbids.

## Changes

| File:line | Change |
|---|---|
| `.github/workflows/rtl-fast.yml:273` | Install the SDK before both required RV32 arms; execute the build self-test. |
| `scripts/ci_events.py:2344` | Pin the updated workflow sequence and reject removal of either required-RV32 flag. |
| `sw/firmware/gtest/fw_rv32.py:1` | Shared compiler selection, isolated freestanding includes, named arithmetic dependencies, ISA/ABI and stack-frame checks. |
| `sw/firmware/gtest/rv32_include/string.h:1` | Test-only declarations for existing memory interfaces. |
| `sw/firmware/gtest/rv32_include/stdio.h:1` | Test-only bounded formatter declaration. |
| `sw/firmware/gtest/fw_rv32_selftest.py:1` | Fifteen controls for headers, types, ABI, ISA, absent compiler, stack report and forbidden dependencies. |
| `sw/firmware/ctrl/test/ctrl_arms.py:156` | Apply shared checks and report static frames with explicit limits. |
| `sw/firmware/ctrl/test/ctrl_build.py:42` | Collect static stack usage; use shared compiler selection. |
| `sw/firmware/ctrl/test/test_ctrl_firmware.py:32` | Describe the freestanding object boundary. |
| `sw/firmware/ctrl_nvm/test/nvm_rv32.py:26` | Apply shared checks and disable SDK-added stack protection in validation objects. |
| `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py:149` | Report the largest static frame. |
| `sw/firmware/ctrl/README.md:110` | Explain pinned SDK and required CI arm. |
| `sw/firmware/ctrl_nvm/README.md:335` | Update object-size table and state stack evidence limits. |
| `sw/firmware/gtest/README.md:345` | Document headers, ABI, dependencies and the absence of linked/runtime proof. |
| `docs/testing/CI_WORKFLOWS.md:42` | Document both required RV32 arms and remaining local-only campaigns. |

## Validation progress

Ctrl's complete campaign passed all 76 mutants. Its final normal run also passed with the pinned SDK. The store's original full campaign timed out at 580 seconds after successful positive suites. Two bounded batches passed, then the full original driver passed in 392.3 seconds with physical mutant-directory reuse: all five shapes, 434 tests and all 106 mutants. No inventory, seam, compiler flag, cache key or grading assertion changed. Of the 100 builder-bank functions, 99 returned successfully (with the area-calibration arm explicitly not run); gate 1b timed out twice at 580 seconds. The incomplete builder bank is not claimed green.

The fifteen new RV32 controls, CI event contract (1741 items), its mutation self-test (2361 arms), CI scope self-test, SDK self-test (25 cases), tally controls (18 cases and 18 mutants), coverage self-test (28 cases), and documentation/style/generated-document gates have passed. Final and baseline coverage pass at 100 percent adjusted line and branch coverage for all 14 files, with the existing exclusions unchanged.

## Object sizes and stack evidence

| Subject | Text before -> after | Data | BSS | Largest static frame |
|---|---:|---:|---:|---:|
| ctrl | 11520 -> 11520 | 0 | 170 | 112 -> 112 |
| store arty_current | 12352 -> 12112 | 24 | 3160 | 128 -> 128 |
| store ax7101_1x1_tdm8 | 12368 -> 12128 | 24 | 4048 | 128 -> 128 |
| store arty_4x4 | 12360 -> 12120 | 24 | 5452 | 128 -> 128 |
| store arty_8ch | 12360 -> 12120 | 24 | 8012 | 128 -> 128 |
| store ax7101_8x8 | 12372 -> 12132 | 24 | 14408 | 128 -> 128 |

All units are bytes. Baseline ctrl cannot build on the pinned SDK; its before figures use the available matching-ABI SDK. Store before/after figures use the pinned SDK. Its 240-byte reduction removes compiler-injected stack-protector calls from validation objects; no firmware C behavior source changes. No linked image was produced, no firmware was flashed, and individual static frames are not a call-chain bound.

## Coverage table

Before and after use the same host compiler and coverage utility (16.2.1) and host test libraries (1.18.0). Raw covered/total values are identical. All 14 files retain 100 percent adjusted line and branch coverage. No budget or exclusion changed; the pre-existing ADP exclusions retain their #678 premise.

| File | Raw lines before = after | Raw branches before = after | Adjusted lines / branches before -> after |
|---|---:|---:|---|
| `sw/firmware/ctrl/adp/adp.c` | 168/170 | 73/80 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl/adp/adp_mbx.c` | 83/83 | 38/40 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl/app/ctrl_app.c` | 12/13 | 6/8 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl/loop/ctrl_loop.c` | 93/93 | 54/54 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl/mbx/mbx.c` | 162/162 | 60/60 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl/mbx/mbx_wire.h` | 15/15 | 12/12 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl/plat/mbx_plat_mmio.c` | 10/10 | 0/0 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl/port/ctrl_debug.c` | 19/19 | 6/6 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl/port/ctrl_pool.c` | 99/99 | 60/60 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl/port/shlan_port.c` | 22/22 | 6/6 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl/wire/wire.h` | 10/10 | 2/2 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl_nvm/nvm_klj2.c` | 195/196 | 104/108 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl_nvm/nvm_store.c` | 434/434 | 259/266 | 100% / 100% -> 100% / 100% |
| `sw/firmware/ctrl_nvm/plat/nvm_flash_litespi.c` | 100/100 | 63/64 | 100% / 100% -> 100% / 100% |

## Gate table

Commands run from the candidate checkout. `SDK_CC` below denotes the disposable pinned SDK compiler selected with `MILAN_RV32_CC`; `SCRATCH` denotes this lane's disk-backed scratch directory. Firmware commands used four jobs or fewer. All outputs were captured directly, without shell pipelines. The recorder enforces 580 seconds per invocation; 124 means that deadline, never a passing gate.

| Gate | Command or exact selection | Exit | Evidence |
|---|---|---:|---|
| Pinned SDK installer | `python3 scripts/ci_rv32_sdk.py --destination "$SCRATCH/sdk" --archive "$SDK_ARCHIVE"`; final `--verify-only` | 0 | Pinned archive verified; existing shared SDK untouched |
| SDK self-test | `python3 scripts/ci_rv32_sdk_selftest.py` | 0 | 25 tests |
| RV32 planted controls | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | 15 controls, exact pinned SDK |
| Ctrl positive suites | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --build-dir "$SCRATCH/ctrl-final-build"` | 0 | All default arms, RV32 included |
| Ctrl full campaign | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --build-dir "$SCRATCH/ctrl-campaign-build"` | 0 | All 76 mutants caught |
| Store positive suites | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --jobs 4` | 0 | Five shapes, 434 tests, each RV32 arm ran |
| Store initial full campaign | `python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` | 124 | Timed out; not a complete verdict |
| Store bounded batch | `python3 nvm_batch.py 0 20 "$SCRATCH/nvm-batches"` | 0 | Original inventory entries 0 through 19 caught |
| Store full campaign with directory reuse | `python3 nvm_foreground.py` invokes the original driver with `--require-rv32 --self-test --jobs 4` | 0 | Five shapes, 434 tests, all 106 mutants; 392.3 seconds |
| Store second bounded batch | `python3 nvm_batch.py 20 40 "$SCRATCH/nvm-batches"` | 0 | Inventory entries 20 through 39 caught |
| Tally | `python3 sw/firmware/gtest/tally_selftest.py --mutants` | 0 | 18 cases and 18 planted listener defects |
| Coverage refusal controls | `python3 sw/firmware/gtest/fw_coverage.py --selftest` | 0 | 28 cases |
| Coverage baseline and final | `python3 sw/firmware/gtest/fw_coverage.py --check --jobs 4` | 0 / 0 | Identical 14-file table above |
| CI contract | `python3 scripts/ci_events.py --check` | 0 | 1741 contract items |
| CI contract self-test | `python3 scripts/ci_events.py --selftest` | 0 | 2361 mutation arms |
| CI scope | `python3 scripts/ci_scope.py --selftest` | 0 | Scope contract passed |
| Builder bank except function 12 | `python3 builder_bank.py START STOP` for `[0:12]`, `[13:52]`, `[52:59]`, `[59:78]`, `[78:100]`, original `--require-rv32` | 0 each | 99 functions returned successfully; area-calibration arm explicitly NOT RUN without a route report |
| Builder gate 1b | `python3 builder_bank.py 12 13` twice | 124 / 124 | Both reached the 580-second limit; no complete builder-bank pass |
| Shipping-source comparison | `git diff --exit-code 6714181d..HEAD` restricted to RTL, configs, shipping build, SoC, SDK installer and both firmware C/header trees | 0 | No change to protected inputs |
| Hosted firmware-unit | Publication and PR required | Not run | Session forbids push and PR operations |
| Supported act replica | Trusted validation-base runner needs the published PR/head | Not run | No candidate host orchestrator executed |
| docs | `python3 scripts/docs_check.py` | 0 | `docs-staged.log` |
| em-dash | `python3 scripts/check_em_dash.py --base 6714181d` | 0 | `em-dash-final.log` |
| doc-style | `python3 scripts/check_doc_style.py` | 0 | `doc-style.log` |
| doc-style-selftest | `python3 scripts/check_doc_style.py --selftest` | 0 | `doc-style-selftest.log` |
| gptp-docs | `python3 scripts/check_gptp_docs.py --with-submodule` | 0 | `gptp-docs.log` |
| doc-map | `python3 docs/DOC_MAP.gen.py --check` | 0 | `doc-map.log` |
| solution-docs | `python3 scripts/check_solution_docs.py` | 0 | `solution-docs.log` |
| submodule-docs | `python3 scripts/check_submodule_docs.py` | 0 | `submodule-docs.log` |
| diagram-pngs | `python3 scripts/check_diagram_pngs.py` | 0 | `diagram-pngs.log` |
| feature-status | `python3 scripts/check_feature_status.py --self-test` | 0 | `feature-status.log` |
| module-matrix | `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `module-matrix.log` |
| baremetal | `python3 scripts/check_baremetal_only.py --check` | 0 | `baremetal.log` |
| baremetal-selftest | `python3 scripts/check_baremetal_only.py --selftest` | 0 | `baremetal-selftest.log` |
| python-idioms | `python3 scripts/check_py_idiom.py` | 0 | `python-idioms-staged.log` |
| cpp-idioms | `python3 scripts/check_cpp_idiom.py` | 0 | `cpp-idioms-staged.log` |
| shell-idioms | `python3 scripts/check_sh_idiom.py` | 0 | `shell-idioms.log` |
| code-hygiene | `python3 scripts/check_hygiene.py` | 0 | `code-hygiene.log` |
| todo | `python3 scripts/check_todo_ownership.py` | 0 | `todo.log` |
| test-evidence | `python3 scripts/measure_test_evidence.py --check` | 0 | `test-evidence-staged.log` |
| doc-paths | `python3 scripts/check_doc_paths.py` | 0 | `doc-paths.log` |
| archive | `python3 scripts/check_archive.py` | 0 | `archive.log` |
| toc | `python3 scripts/gen_toc.py --check` | 0 | `toc.log` |
| toc-anchors | `python3 scripts/gen_toc.py --verify-anchors` | 0 | `toc-anchors.log` |
| toc-selftest | `python3 scripts/gen_toc.py --selftest` | 0 | `toc-selftest.log` |

## Reproduction and retained evidence

`PR-BODY.md` contains the candidate description and standard commands. `builder_bank.py` reads the original 100-function bank from its syntax tree and calls each selected original function; it does not replace assertions. `nvm_batch.py` uses the original inventory, builders and named failure oracles. `nvm_foreground.py` calls the complete original driver with all 106 mutants, mapping only `work / mutant.name` to one physical directory per worker. Firmware C is rebuilt on every mutant. The original full-flags and preprocessed-content cache still determines test-object reuse, so a changed header cannot reuse an incompatible test object. The successful run is reproduced with `MILAN_RV32_CC="$SDK_CC" python3 "$SCRATCH/run.py" nvm-full-reuse python3 "$SCRATCH/nvm_foreground.py"` after placing both drivers in the scratch directory and running from the candidate checkout. `run.py` records direct output and exit status while bounding each foreground invocation. Set the scratch directory and required documented environments before running these small drivers.

The selected small logs are retained beside this document. `EVIDENCE.md` records raw-log sizes and SHA-256 values, including timeouts. Large artifacts, the SDK, installed dependencies and build trees are excluded from this output directory.

The SDK archive is 102597892 bytes. The pinned SDK archive SHA-256 is `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`; the unchanged installer SHA-256 is `ffcc5433d97209b00cac5155c61bc464a43a60fec49bce0330d81279e1df7cb4`.

Builder gate 1b used the existing shared matching-ABI SDK selected by its own unchanged selector; its version was 14.3.0, build 2026.05. Both firmware arms and the new build controls used the exact disposable CI-pinned SDK. No complete pinned-SDK builder result is claimed.

Ctrl campaign timing: the 76-mutant run preceded the final architecture-attribute check. The final positive ctrl run and 15-case build self-test exercise that final checker; all firmware sources and original mutation oracles are unchanged. The full merge validation bar remains incomplete.

## Completion limits and next steps

The assignment is not complete. Gate 1b could not finish within the foreground limit, and therefore the complete builder bank is unverified. Hosted/act evidence requires later authorized publication. No independent verdict, merge readiness, linked-image size proof or whole-program stack proof is claimed. The working tree is clean and contains no generated scratch. No push, PR operation, merge or hardware access occurred. Preserve the commit for review; do not interpret successful partial tests as approval.

Resource observations: service memory peak 8490868736 bytes, below the 9 GB ceiling; disk free space remained above the 30 GB floor. Repository-generated scratch was removed.

## Tests and planted defects

| Control | Planted defect or positive control | Result |
|---|---|---|
| Explicit compiler selection | An explicitly absent executable must not fall back or skip a required ctrl build | PASS |
| Freestanding header/type control | Poisoned hosted sysroot; real RV32 sizes and existing memory/format declarations must compile | PASS |
| Header isolation | Restore hosted include lookup; require the poison error | PASS |
| Freestanding flag | Remove -ffreestanding; require hosted include_next failure | PASS |
| ELF width | Compile a real RV64 object; require rejection | PASS |
| Floating-point ABI | Compile an ILP32D object; require rejection | PASS |
| Compressed ISA | Compile an RV32IC object; require rejection | PASS |
| Multiply ISA | Compile an RV32IM object; require rejection | PASS |
| Object format | Replace the object with non-ELF bytes; require rejection | PASS |
| Static frame evidence | Replace the report with dynamic stack usage; require rejection | PASS |
| Ctrl heap dependency | Replace the pool call with malloc; require named undefined-symbol failure | PASS |
| Ctrl unknown service | Replace the pool call with __unexpected_service; require named failure | PASS |
| Store heap dependency | Add a malloc call; require named failure | PASS |
| Store unknown service | Add an __unexpected_service call; require named failure | PASS |
| Store stack protection | Enable stack-protector instrumentation; require __stack_chk_fail rejection | PASS |

### Ctrl campaign

| Planted defect | Source | Named oracle(s) | Result |
|---|---|---|---|
| `departing-keeps-index` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/` | PASS |
| `departing-sends-zero` | `adp/adp.c` | `adp: AdpCore.A10toA14DepartingIndex` | PASS |
| `available-replaces-owed-departing` | `adp/adp.c` | `adp: AdpCore.A15OwedDepartingAcrossARestart` | PASS |
| `available-passes-owed-departing` | `adp/adp.c` | `adp: AdpCore.A17RoomBackBeforeAPoll` | PASS |
| `second-departing-dropped` | `adp/adp.c` | `adp: AdpCore.A16SecondShutdownQueuesItsOwn` | PASS |
| `second-shutdown-overwrites-index` | `adp/adp.c` | `adp: AdpCore.A16SecondShutdownQueuesItsOwn` | PASS |
| `link-loss-drops-owed-departing` | `adp/adp.c` | `adp: AdpCore.A18LinkLossKeepsTheOwedDeparting` | PASS |
| `gm-change-drops-owed-available` | `adp/adp.c` | `adp: AdpCore.A19IgnoredInputsKeepTheOwedAvailable` | PASS |
| `discover-drops-owed-available` | `adp/adp.c` | `adp: AdpCore.A19IgnoredInputsKeepTheOwedAvailable` | PASS |
| `stray-expiry-drops-owed-available` | `adp/adp.c` | `adp: AdpCore.A19IgnoredInputsKeepTheOwedAvailable` | PASS |
| `link-loss-keeps-owed-available` | `adp/adp.c` | `adp: AdpCore.A20LinkLossDropsTheOwedAvailable` | PASS |
| `departing-queue-unbounded` | `adp/adp.c` | `adp: Shutdowns/AdpOwedBound.E5CommittedInPassKPlusOne/` | PASS |
| `coalesced-departing-uncounted` | `adp/adp.c` | `adp: AdpCore.A21DepartingCapacity` | PASS |
| `coalesce-drops-queued-departing` | `adp/adp.c` | `adp: AdpCore.A21DepartingCapacity` | PASS |
| `coalesce-overwrites-oldest-index` | `adp/adp.c` | `adp: AdpCore.A21DepartingCapacity` | PASS |
| `own-discover-discarded` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_own_eid_x_WAITING` | PASS |
| `down-answers-discover` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/RCV_ADP_DISCOVER_eid_0_x_DOWN` | PASS |
| `link-down-departs` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/LINK_DOWN_x_WAITING` | PASS |
| `gm-change-ignored` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/GM_CHANGE_x_WAITING` | PASS |
| `delay-ignores-link-down` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/LINK_DOWN_x_DELAY_timer_armed` | PASS |
| `shutdown-in-down-departs` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/SHUTDOWN_x_DOWN` | PASS |
| `advertise-expiry-skips-delay` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/TMR_ADVERTISE_x_WAITING` | PASS |
| `advertise-period-wrong` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/TMR_DELAY_x_DELAY_timer_armed` | PASS |
| `link-up-draws-startup-kind` | `adp/adp.c` | `walk: Table551/AdpWalkCell.Graded/LINK_UP_x_DOWN` | PASS |
| `draw-kinds-merged` | `adp/adp.c` | `adp: AdpCore.A9DrawKinds` | PASS |
| `foreign-discover-answered` | `adp/adp.c` | `adp: AdpCore.A3toA5DiscoverAndDiscard` | PASS |
| `frame-misses-config-index` | `adp/adp.c` | `walk: AdpWalk.P11ConfigurationIndexBytes` | PASS |
| `stale-tag-accepted` | `adp/adp_mbx.c` | `adp: AdpAdapter.B1StaleTagDiscarded` | PASS |
| `latency-extra-read` | `adp/adp_mbx.c` | `adp: AdpLatency.C0toC6EveryResponsePath` | PASS |
| `pool-free-leaks` | `port/ctrl_pool.c` | `port: Pool.P2ReleaseAndBadFrees` | PASS |
| `calloc-overflow-unchecked` | `port/ctrl_pool.c` | `port: Pool.P3CallocZeroesAndRefusesAWrap` | PASS |
| `pool-double-free-accepted` | `port/ctrl_pool.c` | `port: Pool.P2ReleaseAndBadFrees` | PASS |
| `debug-truncation-uncounted` | `port/ctrl_debug.c` | `port: DebugSink.S2TruncatedToTheLine` | PASS |
| `tick-count-ignored` | `loop/ctrl_loop.c` | `port: Loop.L4TickFanOut` | PASS |
| `rx-pass-unbounded` | `loop/ctrl_loop.c` | `port: Loop.L2PerPassRxBound` | PASS |
| `poll-owes-nothing` | `adp/adp_mbx.c` | `adp: AdpOwed.E0toE3PendingWake` | PASS |
| `events-halved` | `loop/ctrl_loop.c` | `adp: AdpBacklog.F0toF7FullBacklogs` | PASS |
| `rx-before-events` | `loop/ctrl_loop.c` | `adp: AdpBacklog.F0toF7FullBacklogs` | PASS |
| `carried-ticks-overwritten` | `loop/ctrl_loop.c` | `port: Loop.L8TickRecordWhileCarried` | PASS |
| `tick-slice-unbounded` | `loop/ctrl_loop.c` | `port: Loop.L7TickSlices` | PASS |
| `owed-ticks-let-it-sleep` | `loop/ctrl_loop.c` | `port: Loop.L7TickSlices` | PASS |
| `filter-opened-before-eid` | `loop/ctrl_loop.c` | `port: LoopBring.L1OpenOrder` | PASS |
| `rx-no-resync` | `mbx/mbx.c` | `port: Driver.D1MalformedRecordResynchronises; unit: Records/DriverMalformed.D7RefusedAndResynchronised/` | PASS |
| `tx-overfills` | `mbx/mbx.c` | `port: Driver.D3HeldMergeFillsAndOrderAcrossChannels` | PASS |
| `lanes-big-endian` | `mbx/mbx_wire.h` | `model: Suite/MbxModelGroup.PassesOnTheModel/` | PASS |
| `frame-sources-from-sinks` | `adp/adp.c` | `entity: Fabric/EntityField.MatchesTheFabric/talker_stream_sources` | PASS |
| `pool-falls-back-to-heap` | `port/shlan_port.c` | `port: Pool.P4ShlanFunctionsDrawOnTheBoundPool; rv32: ` | PASS |
| `model-rate-unlimited` | `host/mbx_model.c` | `model: Suite/MbxModelGroup.PassesOnTheModel/RateLimit` | PASS |
| `seq-not-stamped` | `mbx/mbx.c` | `port: Driver.D3HeldMergeFillsAndOrderAcrossChannels` | PASS |
| `model-round-robin` | `host/mbx_model.c` | `model: Suite/MbxModelGroup.PassesOnTheModel/TxCommitOrder` | PASS |
| `model-gm-hi-live` | `host/mbx_model.c` | `model: Suite/MbxModelGroup.PassesOnTheModel/GmSnapshot` | PASS |
| `zero-byte-class-accepted` | `port/ctrl_pool.c` | `port: Pool.P5ClassTablesAndArenasRefused` | PASS |
| `zero-size-refusal-uncounted` | `port/ctrl_pool.c` | `port: Pool.P6CallocOfNothingAndOnAnExhaustedPool` | PASS |
| `foreign-free-uncounted` | `port/ctrl_pool.c` | `port: Pool.P7FreeBelowTheArenaRefused` | PASS |
| `port-pool-unreported` | `port/shlan_port.c` | `port: Pool.P8PortLayerUnbound` | PASS |
| `pool-follows-a-cut-free-list` | `port/ctrl_pool.c` | `port: Pool.P9AFreeListShorterThanItsCountIsExhausted` | PASS |
| `pool-cut-list-refuses-outright` | `port/ctrl_pool.c` | `port: Pool.P9AFreeListShorterThanItsCountIsExhausted` | PASS |
| `encoding-failure-swallowed` | `port/ctrl_debug.c` | `port: DebugSink.S3UnencodablePrintDiscarded` | PASS |
| `rx-binds-no-function` | `loop/ctrl_loop.c` | `port: LoopBring.L9TablesRefuseNullAndOverflow` | PASS |
| `seed-left-at-zero` | `adp/adp.c` | `adp: AdpCore.A22GeneratorNeverStuckAtZero` | PASS |
| `enable-not-idempotent` | `adp/adp.c` | `adp: AdpCore.A23RepeatedEnableOrDisableChangesNothing` | PASS |
| `other-subtype-accepted` | `adp/adp.c` | `adp: AdpCore.A24OtherEtherTypeOrSubtypeDiscarded` | PASS |
| `app-binds-pool-after-the-mailbox` | `app/ctrl_app.c` | `unit: AppComposition.U1BindsTheAppPoolBehindLwsrpBeforeTheMailbox` | PASS |
| `app-starts-on-an-uncarved-pool` | `app/ctrl_app.c` | `unit: AppComposition.U1AnUncarvablePoolStartsNothing` | PASS |
| `major-unchecked` | `mbx/mbx.c` | `unit: AppComposition.U1AnotherContractOpensNothing; unit: IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/major` | PASS |
| `evt-words-unchecked` | `mbx/mbx.c` | `unit: IdAndCaps/ContractField.U2RefusedAndNothingMoreRead/evt_words` | PASS |
| `step-waits-twice` | `loop/ctrl_loop.c` | `unit: LoopRun.U3TurnsForEverAndSleepsWhenNothingIsOwed` | PASS |
| `maap-base-shifted` | `mbx/mbx.c` | `unit: DriverUnit.D6MaapRangeWritten` | PASS |
| `tx-negative-fill` | `mbx/mbx.c` | `unit: DriverUnit.D8TransmitRefusals` | PASS |
| `unknown-event-decoded-as-tick` | `mbx/mbx.c` | `unit: DriverUnit.D9UnknownEventTypeGrandmasterAndInterrupt` | PASS |
| `whole-field-loses-its-top-bit` | `mbx/mbx_wire.h` | `unit: DriverUnit.D10LanesAndFieldsAtTheirBounds` | PASS |
| `slots-past-the-bank` | `adp/adp_mbx.c` | `unit: AdpAdapterUnit.B2SlotsPastTheTimerBankRefused` | PASS |
| `foreign-frame-uncounted` | `adp/adp_mbx.c` | `unit: AdpAdapterUnit.B3ForeignInterfaceCounted` | PASS |
| `attach-ignores-poll-room` | `adp/adp_mbx.c` | `unit: AdpAdapterUnit.B4LoopWithNoRoomRefused` | PASS |
| `mmio-offset-as-index` | `plat/mbx_plat_mmio.c` | `unit: MmioPlatform.M1OneWordAtBasePlusOffset` | PASS |
| `wait-without-wfi` | `plat/mbx_plat_mmio.c` | `unit: MmioPlatform.M2WaitIsThePlatformWfi` | PASS |

### Store campaign

All 106 entries below were caught in the successful complete-driver run.

| Index | Planted defect | Source(s) | Named oracle(s) |
|---:|---|---|---|
| 0 | `no_crc_check` | `nvm_store.c` | `torn_falls_back, verdict_parity` |
| 1 | `no_crc_anywhere` | `nvm_klj2.c, nvm_store.c` | `powercut` |
| 2 | `pick_older` | `nvm_store.c` | `newer_wins` |
| 3 | `pick_no_wrap` | `nvm_store.c` | `newer_wins` |
| 4 | `tie_picks_b` | `nvm_store.c` | `newer_wins` |
| 5 | `erased_header_only` | `nvm_klj2.c` | `verdict_parity, codec_parity` |
| 6 | `no_ascending` | `nvm_klj2.c` | `verdict_parity, codec_parity` |
| 7 | `overrun_as_rec` | `nvm_klj2.c` | `verdict_parity, codec_parity` |
| 8 | `incomplete_accepted` | `nvm_klj2.c` | `verdict_parity, codec_parity` |
| 9 | `room_unchecked` | `nvm_klj2.c` | `codec_room` |
| 10 | `short_prefix_read_on` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 11 | `short_prefix_as_len` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 12 | `header_guard_early` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 13 | `header_guard_late` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 14 | `payload_guard_early` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 15 | `payload_guard_late` | `nvm_klj2.c` | `codec_loaded_prefix` |
| 16 | `lookup_index_unbounded` | `nvm_klj2.c` | `codec_lookups` |
| 17 | `long_crc_unchecked` | `nvm_store.c` | `long_container_reads` |
| 18 | `unread_not_counted` | `nvm_store.c` | `long_container_reads` |
| 19 | `no_version_check` | `nvm_klj2.c` | `wrong_version_falls_back` |
| 20 | `no_blank_verdict` | `nvm_klj2.c` | `blank_boot` |
| 21 | `pad_not_zero` | `nvm_klj2.c` | `blank_boot` |
| 22 | `header_n_rec` | `nvm_klj2.c` | `blank_boot, first_commit_bytes` |
| 23 | `frame_crc_init` | `nvm_klj2.c` | `vector_round_trip, change_commit_bytes` |
| 24 | `no_blank_stage` | `nvm_store.c` | `blank_boot` |
| 25 | `verdict_not_named` | `nvm_store.c` | `both_torn_blank` |
| 26 | `stage_not_rechecked` | `nvm_store.c` | `read_flip_at_stage` |
| 27 | `stage_seq_unchecked` | `nvm_store.c` | `read_alias_at_stage` |
| 28 | `select_on_unchecked_reread` | `nvm_store.c` | `read_flip_boot` |
| 29 | `slot_read_fail_ignored` | `nvm_store.c` | `read_fail_boot` |
| 30 | `unread_not_held` | `nvm_store.c` | `authority_unknown, fallback_restage, read_disagreement` |
| 31 | `read_not_retried` | `nvm_store.c` | `read_fail_boot, authority_unknown` |
| 32 | `refusal_unconfirmed` | `nvm_store.c` | `authority_unknown, read_disagreement, reads_differ_in_verdict, reads_agree_in_digest_not_length` |
| 33 | `blank_unconfirmed` | `nvm_store.c` | `authority_unknown` |
| 34 | `refusal_by_verdict` | `nvm_store.c` | `read_disagreement` |
| 35 | `agreement_by_digest` | `nvm_store.c` | `reads_agree_in_digest_not_length` |
| 36 | `disagreement_not_counted` | `nvm_store.c` | `reads_differ_in_verdict, reads_agree_in_digest_not_length` |
| 37 | `restage_not_retried` | `nvm_store.c` | `read_flip_at_stage, read_alias_at_stage, read_fail_boot` |
| 38 | `fallback_restage_unchecked` | `nvm_store.c` | `fallback_restage` |
| 39 | `no_rollback` | `nvm_store.c` | `apply_fault_rolls_back, settle_fault_rolls_back` |
| 40 | `rollback_failure_ignored` | `nvm_store.c` | `rollback_fault_closes` |
| 41 | `release_on_closed` | `nvm_store.c` | `rollback_fault_closes` |
| 42 | `fault_as_refusal` | `nvm_store.c` | `apply_fault_rolls_back, binding_walk` |
| 43 | `refusal_aborts` | `nvm_store.c` | `refused_keeps_default` |
| 44 | `settle_fault_ignored` | `nvm_store.c` | `settle_fault_rolls_back` |
| 45 | `settle_after_names` | `nvm_store.c` | `golden_restore` |
| 46 | `no_settle_without_names` | `nvm_store.c` | `settle_after_the_last_record` |
| 47 | `shape_not_checked` | `nvm_store.c` | `shape_mismatch_disables_persistence` |
| 48 | `shape_mismatch_released_unproven` | `nvm_store.c` | `shape_mismatch_disables_persistence` |
| 49 | `release_before_apply` | `nvm_store.c` | `golden_restore` |
| 50 | `apply_erased` | `nvm_store.c` | `erased_records` |
| 51 | `model_ready_ignored` | `nvm_store.c` | `model_unproven_closes` |
| 52 | `bindings_skipped_unproven` | `nvm_store.c` | `model_unproven_closes` |
| 53 | `d3_rollback_takes_bindings` | `nvm_store.c` | `apply_fault_rolls_back, settle_fault_rolls_back` |
| 54 | `bindings_in_d3_walk` | `nvm_store.c` | `binding_walk, golden_restore` |
| 55 | `binding_fault_aborts_d3` | `nvm_store.c` | `binding_walk` |
| 56 | `binding_fault_keeps_preloads` | `nvm_store.c` | `binding_walk` |
| 57 | `quiet_period` | `nvm_store.c` | `debounce` |
| 58 | `no_debounce` | `nvm_store.c` | `debounce` |
| 59 | `capture_leaves_window_armed` | `nvm_store.c` | `debounce` |
| 60 | `taken_off_by_one` | `nvm_store.c` | `debounce` |
| 61 | `taken_while_capturing` | `nvm_store.c` | `capture_window_edges` |
| 62 | `taken_after_last_latch` | `nvm_store.c` | `capture_window_edges` |
| 63 | `change_of_no_record` | `nvm_store.c` | `change_unknown_record` |
| 64 | `nothing_to_save_framed` | `nvm_store.c` | `nothing_to_save` |
| 65 | `dr2b_ignores_durability` | `nvm_store.c` | `failed_commit_not_skipped` |
| 66 | `no_dr2b` | `nvm_store.c` | `unchanged_no_erase` |
| 67 | `console_force_ignored` | `nvm_store.c` | `console_commit_unchanged` |
| 68 | `no_backoff` | `nvm_store.c` | `media_failures` |
| 69 | `unbounded_attempts` | `nvm_store.c` | `media_failures` |
| 70 | `budget_rearmed_by_change` | `nvm_store.c` | `dr2c_unchanged_set` |
| 71 | `budget_rearmed_by_capture` | `nvm_store.c` | `dr2c_unchanged_set` |
| 72 | `commit_now_overrides_exhaustion` | `nvm_store.c` | `dr2c_console` |
| 73 | `commit_now_ignores_backoff` | `nvm_store.c` | `dr2c_console` |
| 74 | `success_forgives_exhaustion` | `nvm_store.c` | `recovers_after_failure, dr2c_unchanged_set` |
| 75 | `stale_kept` | `nvm_store.c` | `recovers_after_failure` |
| 76 | `dr2b_keeps_stale` | `nvm_store.c` | `recovers_after_failure` |
| 77 | `no_blankcheck` | `nvm_store.c` | `media_failures` |
| 78 | `blankcheck_first_stretch_only` | `nvm_store.c` | `blankcheck_tail` |
| 79 | `blankcheck_read_fail_ignored` | `nvm_store.c` | `media_verdicts` |
| 80 | `no_verify` | `nvm_store.c` | `media_failures, failed_commit_not_skipped` |
| 81 | `verify_skips_last_stretch` | `nvm_store.c` | `verify_tail` |
| 82 | `verify_read_fail_ignored` | `nvm_store.c` | `media_verdicts` |
| 83 | `program_refusal_ignored` | `nvm_store.c` | `media_verdicts` |
| 84 | `no_timeout` | `nvm_store.c` | `media_failures` |
| 85 | `same_sequence` | `nvm_store.c` | `change_commit_bytes` |
| 86 | `refused_slot_overwritten` | `nvm_store.c` | `refused_slot_kept` |
| 87 | `no_blank_slot_takes_b` | `nvm_store.c` | `first_commit_no_blank_slot` |
| 88 | `erase_authoritative` | `nvm_store.c` | `change_commit_bytes, powercut` |
| 89 | `descending_pages` | `nvm_store.c` | `first_commit_bytes` |
| 90 | `capture_in_one_step` | `nvm_store.c` | `service_bound` |
| 91 | `spin_wait` | `nvm_store.c` | `service_bound` |
| 92 | `litespi_no_wren` | `plat/nvm_flash_litespi.c` | `first_commit_bytes` |
| 93 | `litespi_status_ignored` | `plat/nvm_flash_litespi.c` | `first_commit_bytes` |
| 94 | `litespi_no_guard` | `plat/nvm_flash_litespi.c` | `port_guard` |
| 95 | `phc_time` | `plat/nvm_flash_litespi.c` | `time_base` |
| 96 | `clock_not_accumulated` | `plat/nvm_flash_litespi.c` | `time_base` |
| 97 | `ticks_per_us_truncated` | `plat/nvm_flash_litespi.c` | `port_clock, time_base` |
| 98 | `xfer_unbounded` | `plat/nvm_flash_litespi.c` | `port_stall` |
| 99 | `open_unbounded` | `plat/nvm_flash_litespi.c` | `port_stall` |
| 100 | `call_deadline_ignored` | `plat/nvm_flash_litespi.c` | `port_deadline, port_drain_deadline` |
| 101 | `drain_deadline_ignored` | `plat/nvm_flash_litespi.c` | `port_drain_deadline` |
| 102 | `read_runs_past_device` | `plat/nvm_flash_litespi.c` | `port_read_range` |
| 103 | `program_across_page` | `plat/nvm_flash_litespi.c` | `port_write_refusals` |
| 104 | `deadline_per_wait` | `plat/nvm_flash_litespi.c` | `port_deadline` |
| 105 | `stall_ignored` | `plat/nvm_flash_litespi.c` | `port_stall` |

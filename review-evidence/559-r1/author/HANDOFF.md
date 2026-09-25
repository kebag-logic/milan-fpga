# [A307] Issue #559 handoff

Status: implementation and requested local validation complete; ready for independent review.
Head: `32076148acb0b9122e8c92a44f8e2ebbc8169280` (local and unpublished).
Lane: `559-capture-copy`.
Base: `a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4`.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5828771434
Takeover: https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5828914729

## Measurement and remedy

The product CPU simulation route works using the installed environment, without
toolchain downloads. The selected remedy is the assignment's first branch:
**50 ms is enough under the assigned simulation route.** The worst observed 8x8
capture is 19.00433 ms, below the 25 ms acceptance limit, with a
2.6310x hold margin. No product firmware, RTL, hold parameter or
builder census list changed.

| Shape | Captures | CPU/system MHz | System timer ticks | Elapsed ms | 50 ms / maximum |
|---|---|---|---|---|---|
| `endstation_ax7101_1x1_tdm8` | 16 | 50/100 | 654,490 to 655,479 | 6.54490 to 6.55479 | 7.6280x |
| `endstation_ax7101_8x8` | 16 | 100/100 | 1,899,012 to 1,900,433 | 18.99012 to 19.00433 | 2.6310x |

Every capture has successful attestation, zero open ownership bits and zero byte
mismatches. All allocated records are closed after the real boot/RELOAD. The
whole copy is 3,218 bytes / 53 records at 1x1 and 12,634 / 156 at 8x8, including
4,672 output-map bytes. Materialization does not reduce it.

The firmware reads the 100 MHz system downcounter before ARM and after successful
ATTEST. The interval includes ownership reads, every `nvm_rec_after()` walk, byte
loads/stores, fence, attestation and probe overhead. Prefill and byte poisoning
are outside the interval. Poisoning live XOR 255 into every destination byte
makes an omitted copy observable. Each capture is released; no flash commit runs.

Traffic is continuous 60-byte AEM READ_DESCRIPTOR ENTITY 0 at the MAC AXIS face,
with backpressure respected, TX always ready and no line-rate/IFG throttle.
Counters cover only the record walk/copy: accepted complete input frames,
successful descriptor responses, and real shared descriptor-memory read ACKs.

| Shape | Accepted frames per copy | Successful responses per copy | Descriptor read ACKs per copy |
|---|---|---|---|
| 1x1 | 40,823 to 40,885 | 41 to 42 | 1,600 to 1,638 |
| 8x8 | 237,254 to 237,432 | 146 to 147 | 5,694 to 5,726 |

All raw rows, commands and input hashes are in the committed
`tb/verilator/nvm_capture_cpu/measurements.json` and this packet's `measurements.json`.
Complete UART logs are `final-1x1-uart.log` and `final-8x8-uart.log`.

## Exact commands

From the lane, each measurement was run in the foreground with `rtk proxy`:

```sh
timeout 10800 unshare --user --map-current-user --net env COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=riscv32-linux PATH="$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin:$WORKSPACE_HOME/litex-milan/venv/bin:$PATH" $WORKSPACE_HOME/litex-milan/venv/bin/python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_8x8 --captures 16 --build-dir $VALIDATION_STORAGE/559-a307-final-8x8
timeout 10800 unshare --user --map-current-user --net env COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true LITEX_ENV_CC_TRIPLE=riscv32-linux PATH="$VALIDATION_STORAGE/504-manager-r1/sdk-install/bin:$WORKSPACE_HOME/litex-milan/venv/bin:$PATH" $WORKSPACE_HOME/litex-milan/venv/bin/python3 tb/verilator/nvm_capture_cpu/run.py --shape endstation_ax7101_1x1_tdm8 --captures 16 --build-dir $VALIDATION_STORAGE/559-a307-final-1x1
```

Both commands returned 0; logs are `final-8x8.log` and `final-1x1.log`.
The final grader was reapplied by `python3 -B collect_measurements.py`, including
the explicit shape census added while these simulations were running. That
addition affects acceptance only; native source and firmware bytes did not change.

Both negative commands use the same environment prefix, 1x1 shape and
`--captures 2`, with `--mutation skip-copy --build-dir $VALIDATION_STORAGE/559-a307-final-mut-skip-copy`
or `--mutation no-traffic --build-dir $VALIDATION_STORAGE/559-a307-final-mut-no-traffic`.
Both wrappers return 0 only after detecting their named defect.

| Negative control | Captures | Timer ticks / ms | Copy and traffic evidence |
|---|---|---|---|
| Skip copy | 2, 1x1 | 604,386 / 6.04386; 603,436 / 6.03436 | All 3,218 bytes mismatch in both; requests 37,692 / 37,634; successful replies 40 / 40; reads 1,560 / 1,566. Native rc 1 is required. |
| No traffic | 2, 1x1 | 655,196 / 6.55196; 655,072 / 6.55072 | Copy and attestation pass; requests, replies and reads all zero. Positive acceptance would refuse these rows. |

Logs: `final-mut-*-uart.log`, `final-mut-*.log`, and corresponding rc files.

Recipe reproducibility is recorded in `environment-revisions.json` and the
committed receipt. The launches inherited an unset Python hash seed. A separate
offline `--build-only` 8x8 run with `PYTHONHASHSEED=0` returned 0 and produced
byte-identical CPU, BIOS, instrumented firmware, shape and gPTP program inputs.
Generated SoC RTL differs only in date comments and its scratch path. The two
measured CPU netlists differ only in their top module names. See
`seed0-comparison.json` and `seed0-8x8.log`. The run guide uses the board's fixed seed.

## Changes

| File and line | Change |
|---|---|
| `tb/verilator/nvm_capture_cpu/soc.py:101` | Actual board SoC, shape generation and simulated physical devices. |
| `tb/verilator/nvm_capture_cpu/probe.py:10` | Passive descriptor-memory observation and firmware traffic markers. |
| `tb/verilator/nvm_capture_cpu/firmware.py:68` | Scratch-only firmware instrumentation and named negative controls. |
| `tb/verilator/nvm_capture_cpu/sim_main.cpp:39` | Concurrent descriptor traffic and successful response accounting. |
| `tb/verilator/nvm_capture_cpu/sim_main.cpp:122` | Rational clocks, monotonic-time refusal and UART capture. |
| `tb/verilator/nvm_capture_cpu/run.py:31` | Every-capture census, copy, attestation, traffic and timing grading. |
| `tb/verilator/nvm_capture_cpu/README.md:9` | Reproduction commands, boundaries and negative-control contract. |
| `tb/verilator/nvm_capture_cpu/measurements.json:26` | All 32 measured rows and recipe/input hashes. |
| `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1557` | Section 18 replaces the derived model with measured timing. |
| `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1702` | UNRESOLVED 6 records the simulation result and remaining physical claims. |

The retired factors are six instructions per byte, fifty per record, ten cycles
per instruction, two DDR accesses per byte, thirty cycles per access, the blanket
50 MHz clock and the twofold pessimism multiplier. Actual execution and bus
latencies are included in the measured interval. The clock comes from each
shape's board recipe: 8x8 is 100 MHz; shipping 1x1 is 50 MHz.

## Gates

All commands ran in the foreground, with generous timeouts and no output pipes.
The Markdown gates use `PYTHONPATH=$VALIDATION_STORAGE/559-a307-markdown`, installed
from the repository's hash-locked requirements outside this output directory.

| Gate command | rc | Log |
|---|---|---|
| Full builder, pinned RV32 compiler; `python3 full-builder-sdk.py` | 0 | `gate-builder-sdk.log` |
| Full builder, compiler absent; `python3 full-builder-absent.py` | 0 | `gate-builder-absent.log` |
| `make -C tb/verilator/nvm_cosim` | 0 | `gate-nvm-cosim.log` |
| `make -C tb/verilator/nvm_backend` | 0 | `gate-nvm-backend.log` |
| `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` | 0 | `gate-nvm-hosttest.log` |
| `python3 scripts/check_baremetal_only.py --check` | 0 | `gate-baremetal-only.log` |
| `python3 -B scripts/docs_check.py` | 0 | `gate-docs-git.log` |
| `env GIT_DIR=/dev/null python3 -B scripts/docs_check.py` | 0 | `gate-docs-no-git.log` |
| `python3 scripts/check_em_dash.py --base a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4` | 0 | `gate-em-dash.log` |
| `python3 scripts/check_doc_style.py` | 0 | `gate-doc-style.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `gate-toc.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `gate-anchors.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `gate-doc-paths.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `gate-matrix.log` |
| `python3 scripts/xvlog_gate.py --check` | 0 | `gate-xvlog.log` |
| `python3 scripts/check_sv_idiom.py` | 0 | `gate-sv-idiom.log` |
| `python3 scripts/check_cpp_idiom.py` | 0 | `gate-cpp-idiom.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `gate-py-idiom.log` |
| `python3 scripts/check_port_contracts.py` | 0 | `gate-port-contracts.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `gate-naming.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `gate-test-evidence.log` |
| `git diff --check` | 0 | `gate-diff.log` |
| `git diff --cached --check` | 0 | `gate-diff-staged.log` |
| Product OOC recipe | N/A | No product RTL change |

The compiler-present builder wrapper is the specified reference driver with only
its audit destination changed. It invokes `sw/builder/test_builder.py --require-rv32`
through `runpy`, redirects only the expected compiler argv[0] to the pinned SDK,
and audits 535 compiler calls. The log records 232 RV32 census compiles. The
compiler-absent wrapper hides only the three compiler candidates, delegates all
other commands unchanged and visibly stands down the compiled census arm.
Both full builder modes report the historical gate 11 placement calibration arm
NOT RUN because its report is absent. Their rc 0 does not cover that arm.

The co-simulation suite records 465 PASS and all 39 mutants killed. The RTL parser
has zero first-party findings and the same four pinned-donor findings as its
ratchet. No budget or acceptance criterion was weakened.

Initial gate failures are retained in `initial-gate-*.log` and
`initial-static-driver.*`: missing locked Markdown dependencies and one README
compiler-prefix wording hit. The repaired gates returned 0. Only documentation
and inventory checks were rerun after final documentation/receipt edits; the
other logs cover their unchanged inputs.

## Scope and limitations

The harness retains the actual board CPU variant, bus fabric, memory CDC, PP
bridges, DDR controller, configured audio domains and product firmware. It
replaces physical clocks, memory devices and MAC transport. The DDR model retains
the board PHY's controller-facing phases/latencies, without physical leveling.
BIOS boot CRC, delays and startup DDR test are skipped outside the timed interval.
These results establish the assigned simulation margin under the specified
traffic. Silicon timing, physical memory ordering and debounce measurement remain
open in UNRESOLVED 6. No hardware was used.

## Development evidence excluded from acceptance

The original CPU boot preflight reached its prompt; its first matcher missed ANSI
escapes. An initial root-mapped offline namespace failed because Java sought the
root home. Both were corrected without downloads.

The original 8x8 fixtures accidentally mixed the 8x8 firmware with the tracked
1x1 RTL shape include. Their timing figures are invalid for acceptance:

| Commands | Requested shape / count | Traffic | Diagnostic figure and evidence |
|---|---|---|---|
| `product_soc_preflight.py --compile`, `compile_native.py`, `../native/Vsim` in preflight gateware | 8x8 / 1 | None; wrong flash byte order disabled the entity | 1,978,750 ticks / 19.78750 ms; `native-capture-preflight.log` |
| `run.py --shape endstation_ax7101_8x8 --captures 2 --build-dir $VALIDATION_STORAGE/559-a307-capture-8x8` with the offline prefix | 8x8 / 2 | READ_DESCRIPTOR returned BAD_ARGUMENTS, no successful responses; 14,463 / 14,466 read ACKs | 1,946,394 / 1,946,465 ticks, 19.46394 / 19.46465 ms; `capture-8x8-smoke-2-uart.log`; full runner rc 1 |
| `compile_debug.py`, then `../native/Vsim` in the same gateware directory, two diagnostic replays | 8x8 / 2 per replay | Same traffic; the second replay identifies name capacity 38 against requested 99 | Same two figures; `capture-8x8-debug-uart.log`, `capture-8x8-debug-2-uart.log`. Bare native rc 0 is not acceptance. |

The first corrected-shape 16-capture runs were deliberately terminated after the
native scheduler's edge-count multiplication overflowed near 0.184 simulated
seconds. Their partial rows are retained in `measure-8x8-uart.log` and
`measure-1x1-uart.log`; commands were the final measurement commands with build
directories named `559-a307-measure-8x8` and `559-a307-measure-1x1`.
They are not acceptance evidence. The final scheduler divides before multiplying,
checks monotonic time and completed all 16 captures at each shape. Initial
two-capture mutations in `mut-*-uart.log` reproduce the same rows as the final
negative-control table; they were rerun with the final scheduler.

| Excluded partial run / capture index | System ticks / ms | Accepted frames / successful replies / reads |
|---|---|---|
| 8x8, 0 of 4 completed / 16 requested | 1,899,620 / 18.99620 | 237,330 / 146 / 5,694 |
| 8x8, 1 of 4 completed / 16 requested | 1,899,932 / 18.99932 | 237,369 / 147 / 5,704 |
| 8x8, 2 of 4 completed / 16 requested | 1,900,385 / 19.00385 | 237,426 / 146 / 5,709 |
| 8x8, 3 of 4 completed / 16 requested | 1,900,330 / 19.00330 | 237,419 / 146 / 5,694 |
| 1x1, 0 of 2 completed / 16 requested | 654,490 / 6.54490 | 40,823 / 42 / 1,630 |
| 1x1, 1 of 2 completed / 16 requested | 655,102 / 6.55102 | 40,862 / 42 / 1,633 |

## Handoff state

No push, PR creation/edit, merge, other checkout, donor edit or sub-agent was used.
The local commit and `PR-BODY.md` are ready for the assigned independent reviewers.
`REVIEW-READY.md` contains the final public issue comment. Required hosted checks,
independent review and merge remain outside this author assignment.

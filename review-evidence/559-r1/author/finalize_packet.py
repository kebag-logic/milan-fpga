import json
from pathlib import Path
import re
import subprocess

root = Path('$LANES/559-capture-copy')
out = Path(__file__).parent
receipt = json.loads((out / 'measurements.json').read_text())
large, small = receipt['measurements']
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()

def interval(rows, key):
    values = [row[key] for row in rows]
    return f'{min(values):,} to {max(values):,}'

def line(path, marker):
    lines = (root / path).read_text().splitlines()
    return next(i for i, value in enumerate(lines, 1) if marker in value)

gate_names = [
 ('builder-sdk', 'Full builder, pinned RV32 compiler; `python3 full-builder-sdk.py`'),
 ('builder-absent', 'Full builder, compiler absent; `python3 full-builder-absent.py`'),
 ('nvm-cosim', '`make -C tb/verilator/nvm_cosim`'),
 ('nvm-backend', '`make -C tb/verilator/nvm_backend`'),
 ('nvm-hosttest', '`python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`'),
 ('baremetal-only', '`python3 scripts/check_baremetal_only.py --check`'),
 ('docs-git', '`python3 -B scripts/docs_check.py`'),
 ('docs-no-git', '`env GIT_DIR=/dev/null python3 -B scripts/docs_check.py`'),
 ('em-dash', '`python3 scripts/check_em_dash.py --base a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4`'),
 ('doc-style', '`python3 scripts/check_doc_style.py`'),
 ('toc', '`python3 scripts/gen_toc.py --check`'),
 ('anchors', '`python3 scripts/gen_toc.py --verify-anchors`'),
 ('doc-paths', '`python3 scripts/check_doc_paths.py`'),
 ('matrix', '`python3 docs/traceability/gen_module_matrix.py --check`'),
 ('xvlog', '`python3 scripts/xvlog_gate.py --check`'),
 ('sv-idiom', '`python3 scripts/check_sv_idiom.py`'),
 ('cpp-idiom', '`python3 scripts/check_cpp_idiom.py`'),
 ('py-idiom', '`python3 scripts/check_py_idiom.py`'),
 ('port-contracts', '`python3 scripts/check_port_contracts.py`'),
 ('naming', '`python3 scripts/measure_naming.py --check`'),
 ('test-evidence', '`python3 scripts/measure_test_evidence.py --check`'),
 ('diff', '`git diff --check`'),
 ('diff-staged', '`git diff --cached --check`'),
]
gates = []
for name, command in gate_names:
    rc = int((out / ('gate-' + name + '.rc')).read_text())
    assert rc == 0, (name, rc)
    gates.append(f'| {command} | 0 | `gate-{name}.log` |')

changes = [
 ('tb/verilator/nvm_capture_cpu/soc.py', 'def build(', 'Actual board SoC, shape generation and simulated physical devices.'),
 ('tb/verilator/nvm_capture_cpu/probe.py', 'class CaptureProbe', 'Passive descriptor-memory observation and firmware traffic markers.'),
 ('tb/verilator/nvm_capture_cpu/firmware.py', 'def prepare(', 'Scratch-only firmware instrumentation and named negative controls.'),
 ('tb/verilator/nvm_capture_cpu/sim_main.cpp', 'class Controller', 'Concurrent descriptor traffic and successful response accounting.'),
 ('tb/verilator/nvm_capture_cpu/sim_main.cpp', 'std::string simulate(', 'Rational clocks, monotonic-time refusal and UART capture.'),
 ('tb/verilator/nvm_capture_cpu/run.py', 'def _grade(', 'Every-capture census, copy, attestation, traffic and timing grading.'),
 ('tb/verilator/nvm_capture_cpu/README.md', '## Run', 'Reproduction commands, boundaries and negative-control contract.'),
 ('tb/verilator/nvm_capture_cpu/measurements.json', '"measurements"', 'All 32 measured rows and recipe/input hashes.'),
 ('docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md', 'Timing. MEASURED', 'Section 18 replaces the derived model with measured timing.'),
 ('docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md', '6. Physical timing', 'UNRESOLVED 6 records the simulation result and remaining physical claims.'),
]
change_rows = [f'| `{path}:{line(path, marker)}` | {description} |'
               for path, marker, description in changes]

timing_rows = []
for m in (small, large):
    timing_rows.append(f'| `{m["shape"]}` | {m["captures"]} | {m["cpu_hz"] // 1000000}/{m["sys_hz"] // 1000000} | '
                       f'{interval(m["rows"], "sys_cycles")} | {m["minimum_ms"]:.5f} to {m["maximum_ms"]:.5f} | {m["margin"]:.4f}x |')

partial_rows = []
for shape in ('8x8', '1x1'):
    log = (out / ('measure-' + shape + '-uart.log')).read_text()
    rows = [dict((key, int(value)) for key, value in re.findall(r'(\w+)=(\d+)', text))
            for text in log.splitlines() if text.startswith('CAPTURE index=')]
    for row in rows:
        partial_rows.append(f'| {shape}, {row["index"]} of {len(rows)} completed / 16 requested | '
                            f'{row["sys_cycles"]:,} / {row["sys_cycles"] / 100000:.5f} | '
                            f'{row["requests"]:,} / {row["responses"]} / {row["reads"]:,} |')

text = f'''# [A307] Issue #559 handoff

Status: implementation and requested local validation complete; ready for independent review.
Head: `{head}` (local and unpublished).
Lane: `559-capture-copy`.
Base: `a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4`.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5828771434
Takeover: https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5828914729

## Measurement and remedy

The product CPU simulation route works using the installed environment, without
toolchain downloads. The selected remedy is the assignment's first branch:
**50 ms is enough under the assigned simulation route.** The worst observed 8x8
capture is {large['maximum_ms']:.5f} ms, below the 25 ms acceptance limit, with a
{large['margin']:.4f}x hold margin. No product firmware, RTL, hold parameter or
builder census list changed.

| Shape | Captures | CPU/system MHz | System timer ticks | Elapsed ms | 50 ms / maximum |
|---|---|---|---|---|---|
{chr(10).join(timing_rows)}

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
| 1x1 | {interval(small['rows'], 'requests')} | {interval(small['rows'], 'responses')} | {interval(small['rows'], 'reads')} |
| 8x8 | {interval(large['rows'], 'requests')} | {interval(large['rows'], 'responses')} | {interval(large['rows'], 'reads')} |

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
{chr(10).join(change_rows)}

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
{chr(10).join(gates)}
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
{chr(10).join(partial_rows)}

## Handoff state

No push, PR creation/edit, merge, other checkout, donor edit or sub-agent was used.
The local commit and `PR-BODY.md` are ready for the assigned independent reviewers.
`REVIEW-READY.md` contains the final public issue comment. Required hosted checks,
independent review and merge remain outside this author assignment.
'''
(out / 'HANDOFF.md').write_text(text)

pr = f'''[A307]

Closes #559

Status: ready for independent review.

Description: measure the complete saved-state capture on the product CPU and SoC buses under continuous controller descriptor traffic. Across 16 captures per shape, the worst 8x8 result is {large['maximum_ms']:.5f} ms, giving {large['margin']:.4f}x margin against the unchanged 50 ms hold. The 1x1 maximum is {small['maximum_ms']:.5f} ms. The first assigned remedy applies: 50 ms is enough for this simulation route; firmware and hold settings are unchanged.

How to reproduce: use the commands and environment links in [snapshot ownership section 18](docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md#18-cost). Its linked measurement receipt contains all 32 rows and input hashes. Each capture checks the complete closed-record copy, attestation, ownership and traffic during the copy.

How to validate: all requested local gate commands returned zero, including both builder modes, the backend and firmware suites, and both documentation inventory modes. Both named negative controls are detected. The compiler-absent run explicitly skips its compiled census; both builder modes lack the historical placement calibration report.

DoD: the runnable harness, measured remedy, section 18 and UNRESOLVED 6 are updated. Physical timing and memory-ordering claims remain open. Independent review and hosted checks remain to be completed.
'''
(out / 'PR-BODY.md').write_text(pr)

public_commands = '\n'.join(command.strip('`') for _, command in gate_names[2:])
comment = f'''[A307] REVIEW READY

Commit: `{head}` (local, unpublished; branch `559-capture-copy`).

Changed: runnable product-CPU capture harness and full measurement receipt; snapshot-ownership section 18 and UNRESOLVED 6 now use measurements instead of the cost model. No product firmware, RTL, hold parameter or builder census list changed.

Measurement: 16 full closed-record captures at each shape under continuous READ_DESCRIPTOR ENTITY traffic at the MAC AXIS boundary. Firmware brackets ARM through successful ATTEST, including ownership reads, `nvm_rec_after()`, byte copy and fence. Every capture passes byte equality, attestation, closed ownership, successful controller responses and shared-memory read activity during the copy.

| Shape | Raw bytes / records | CPU/system MHz | Worst ms | 50 ms hold margin |
|---|---|---|---|---|
| 8x8 | 12,634 / 156 | 100/100 | {large['maximum_ms']:.5f} | {large['margin']:.4f}x |
| 1x1 | 3,218 / 53 | 50/100 | {small['maximum_ms']:.5f} | {small['margin']:.4f}x |

Acceptance: the 8x8 maximum is below 25 ms. The first assigned remedy applies: 50 ms is enough under the specified simulation route. All 32 rows and input hashes are in `tb/verilator/nvm_capture_cpu/measurements.json`; commands are in its adjacent README. Both missing-copy and missing-traffic negative controls are detected.

Validation: full builder with the pinned compiler and without a compiler; `make -C tb/verilator/nvm_cosim` (465 PASS, 39/39 mutants); `make -C tb/verilator/nvm_backend`; `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test`; all requested baremetal, documentation, style, Contents/anchor, path, module-matrix, parser, idiom, port-contract, naming, evidence and diff gates return 0. The compiler-present census ran; the compiler-absent census intentionally stands down. Both builder modes report the historical placement calibration arm NOT RUN because its report is absent. OOC is inapplicable without a product RTL change.

Exact gate commands below (all rc 0). The full builder additionally ran through the prescribed compiler argv mapping with `--require-rv32`, and through a wrapper hiding only its three compiler candidates in default mode. Both execute `sw/builder/test_builder.py` unchanged. Documentation renderer dependencies are the repository's locked versions.

```sh
{public_commands}
```

Limits: simulated physical devices and MAC-boundary traffic; this does not close silicon timing, physical memory-ordering or debounce claims. Independent review and hosted checks remain. HANDOFF.md and PR-BODY.md are in the assigned output directory. No push or PR mutation was performed.
'''
(out / 'REVIEW-READY.md').write_text(comment)

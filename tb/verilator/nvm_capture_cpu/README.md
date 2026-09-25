# Product CPU capture measurement

This harness measures the product firmware's complete `nvm_capture()` interval.
Its contract is the [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5831090112).
Both traffic arms contribute to the published maximum.
The 8x8 maximum must remain at or below 24.5 ms.
This is half the unchanged hold's guaranteed 49 ms floor.
The free-running tick makes the effective hold 49-50 ms.

## Contents

- **[Run](#run)** -- Commands, clocks, prerequisites and simulation controls.
- **[What is measured](#what-is-measured)** -- Product paths, timer boundaries and substituted device models.
- **[Hosted input gate](#hosted-input-gate)** -- Receipt checks and named controls without compilation or simulation.

## Run

Use the existing product LiteX tree with its
[product patches](../../../sw/litex/patches/README.md), pinned CPU netlist and
pinned RV32 SDK. A cached, matching CPU netlist is required.
An offline-generated netlist from the pinned generator also works.
Nothing here installs dependencies.
Set `LITEX_ENV_CC_TRIPLE` to the compiler prefix, without `-gcc`.
Put the SDK's `bin` directory first on `PATH`.
Set `PYTHONHASHSEED=0`, as the board launcher does.

Run from the repository root, using external build directories:

```sh
for traffic in on off; do
  python3 tb/verilator/nvm_capture_cpu/run.py \
    --shape endstation_ax7101_8x8 --cpu-hz 50000000 --captures 16 \
    --traffic "$traffic" --build-dir "/tmp/nvm-capture-8x8-50-$traffic"
  python3 tb/verilator/nvm_capture_cpu/run.py \
    --shape endstation_ax7101_1x1_tdm8 --cpu-hz 50000000 --captures 16 \
    --traffic "$traffic" --build-dir "/tmp/nvm-capture-1x1-50-$traffic"
  python3 tb/verilator/nvm_capture_cpu/run.py \
    --shape endstation_ax7101_8x8 --cpu-hz 100000000 --captures 16 \
    --traffic "$traffic" --build-dir "/tmp/nvm-capture-8x8-100-$traffic"
done
```

The 100 MHz runs are labelled non-contract comparisons.
The explicit override defaults to the contract's 50 MHz.
It leaves shape configurations untouched; [#565](https://github.com/kebag-logic/milan-fpga/issues/565) owns reconciliation.
Run inside a network namespace with networking disabled.
Set `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.
Missing prerequisites are environment failures, never permission to download.
Keep commands in the foreground with generous wall-clock timeouts.
The native runner bounds simulated time at 30 seconds.
It refuses nonmonotonic edges and avoids edge-count multiplication overflow.

`capture.log` holds boot output and every capture row.
`measurement.json` holds clocks, rows, extrema and floor-based margins.
`run.py` grades every row, including traffic OFF timing.
It checks the census, attestation, ownership and byte equality.
Traffic ON requires positive request, response and shared-read counters.
Traffic OFF requires all three counters to remain zero.
A bare native exit is insufficient evidence.
`--build-only` compiles without measuring.

The negative controls retain the product build and driver:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py \
  --shape endstation_ax7101_1x1_tdm8 --captures 2 --mutation skip-copy \
  --build-dir /tmp/nvm-capture-skip-copy
python3 tb/verilator/nvm_capture_cpu/run.py \
  --shape endstation_ax7101_1x1_tdm8 --captures 2 --mutation no-traffic \
  --build-dir /tmp/nvm-capture-no-traffic
```

Each returns zero only when its named defect is detected.
Skipping stores must leave every raw byte poisoned.
Disabling traffic must preserve copying while zeroing all traffic counters.
That control also grades the copy's elapsed time.

## What is measured

`soc.py` instantiates the board's cacheless RV32I VexiiRiscv variant.
It retains the product memory CDC, buses and PP bridges.
The DDR controller and SPI controller remain present.
The product builder generates shape constants and AEM flash contents.
Audio domains and configured audio geometry remain present.
No tracked generated files or donor files are changed.

`firmware.py` instruments a scratch copy at unique, checked anchors.
The product compiler builds that file and the real BIOS.
The 100 MHz system timer brackets ARM through successful ATTEST.
This includes ownership reads, every `nvm_rec_after()` walk and copying.
The fence, attestation and instrumentation overhead are included.
Flash prefill and destination poisoning happen before timing.

Accepted RELOAD closes every allocated record before measurement.
Every destination byte is poisoned using its live value XOR 255.
The byte oracle therefore detects copying omitted from unchanged images.
The full 8x8 copy covers 12,634 bytes and 156 records.
That includes 4,672 output-map bytes.
The 1x1 copy covers 3,218 bytes and 53 records.
Materialization does not reduce either copy.
Each iteration releases the capture without committing to flash.

Traffic uses continuous 60-byte AEM READ_DESCRIPTOR ENTITY 0 requests.
It enters the MAC AXIS boundary and respects backpressure.
TX stays ready; no line-rate throttle or inter-frame gap applies.
Traffic continues between captures; sequence identifiers wrap naturally.
Dropped requests never count as successful responses.
Counters span the record walk and copy, ending before ATTEST.
They count accepted frames, successful responses and descriptor-memory read ACKs.
The first five TX frames support response-header inspection.
The offered load is not an established worst-case stressor.
[Section 18](../../../docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md#18-cost) quantifies both arms.

Substitutions and limits:

- Clocks use ideal signals instead of board PLL primitives.
  CPU rising edges align with system rising edges.
  At 50/100 MHz, the CPU phase offset is 5 ns.
  At 100/100 MHz, that offset is zero.
  Audio clocks first rise after their respective half-periods.
  These deterministic phases are not a phase sweep.
- `SDRAMPHYModel` replaces `A7DDRPHY`, retaining controller-facing phases and latencies.
  Physical leveling and board DDR signal effects are absent.
- MAC transport uses direct AXIS injection and always-ready TX.
  Physical Ethernet transport is absent.
- `LiteSPIPHYModel` substitutes the flash device, retaining its controller.
  Flash prefill occurs before the timed interval.
- The simulated UART console has no baud-rate backpressure.
- BIOS delays, boot CRC and startup DDR testing are disabled.
  These all precede measurement.

The [receipt](measurements.json) identifies simulator version and input hashes.
The round-2 measurements use Verilator 5.052.
These are simulation measurements, with physical timing still unmeasured.
They do not establish silicon memory ordering.

## Hosted input gate

This directory is an environment-dependent measurement outside suite sweeps.
It is the documented exception to the suite Makefile rule.
Hosted CI runs a separate, compiler-free input gate:

```sh
python3 scripts/check_nvm_capture.py
```

The gate regenerates each shape's tables into temporary storage.
It recomputes framed closed-record bytes and record count.
It checks the explicit CPU clock and configured clocks.
Any difference from `measurements.json` requires new measurements.
The product firmware hash also prevents carrying timing across edits.
Harness hashes prevent carrying evidence across measurement-path changes.
The gate imports neither LiteX nor a simulator.

Named controls change bytes, records, CPU and configured clocks.
Timing controls check half-floor equality and one tick beyond it.
A slower OFF fixture must determine the published maximum.
A planted grader excluding OFF must fail that fixture.
All controls execute before the ordinary gate verdict.
These explicit mutations must each exit nonzero:

```sh
python3 scripts/check_nvm_capture.py --mutation bytes
python3 scripts/check_nvm_capture.py --mutation records
python3 scripts/check_nvm_capture.py --mutation clock
python3 scripts/check_nvm_capture.py --mutation ignore-off-timing
```

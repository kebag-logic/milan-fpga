# Product CPU capture measurement

This harness measures the shipping `nvm_capture()` on the product CPU and
memory buses for [issue #559](https://github.com/kebag-logic/milan-fpga/issues/559).
Its acceptance contract is the
[assignment](https://github.com/kebag-logic/milan-fpga/issues/559#issuecomment-5828771434).
The maximum observed 8x8 capture must fit within 25 ms of the unchanged 50 ms hold.

## Run

Use the existing product LiteX environment with its
[product patches](../../../sw/litex/patches/README.md), pinned CPU generator and
pinned RV32 SDK. Nothing here installs dependencies.
Set `LITEX_ENV_CC_TRIPLE` to the prefix of `riscv32-linux-gcc`, without `-gcc`.
Put the SDK's `bin` directory first on `PATH`.
Set `PYTHONHASHSEED=0`, as the board launcher does.
Run from the repository root, with an external scratch directory:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py \
  --shape endstation_ax7101_8x8 --captures 16 \
  --build-dir /tmp/nvm-capture-8x8
python3 tb/verilator/nvm_capture_cpu/run.py \
  --shape endstation_ax7101_1x1_tdm8 --captures 16 \
  --build-dir /tmp/nvm-capture-1x1
```

Run both commands in a network namespace with networking disabled,
`COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`. A missing generator or
compiler is an environment failure, not permission to download one. Keep the
commands in the foreground and allow a generous wall-clock timeout. The native
runner bounds simulated time at 30 seconds and refuses nonmonotonic clock edges.
It schedules rational clock periods without multiplying the full edge count by
half a trillion, which would overflow during a repeated run.
Each clock starts low and first rises at half its configured period.
The measurement uses these deterministic phases; it does not sweep clock phase.

`capture.log` contains boot output and one firmware measurement per capture.
`measurement.json` records every row, the selected clocks, extrema and hold
margin. Only `run.py` is the acceptance gate: it checks every row, all requested
captures, the expected shape census and traffic. A bare native exit is insufficient.
`--build-only` compiles without measuring.

The two negative controls use the same product build and driver:

```sh
python3 tb/verilator/nvm_capture_cpu/run.py \
  --shape endstation_ax7101_1x1_tdm8 --captures 2 --mutation skip-copy \
  --build-dir /tmp/nvm-capture-skip-copy
python3 tb/verilator/nvm_capture_cpu/run.py \
  --shape endstation_ax7101_1x1_tdm8 --captures 2 --mutation no-traffic \
  --build-dir /tmp/nvm-capture-no-traffic
```

These commands return zero only when their named oracle detects the defect.
Skipping the store must leave all raw bytes poisoned while traffic still runs.
Disabling traffic must leave the copy correct and all three traffic counters zero.

## What is measured

`soc.py` subclasses the board's `MilanSoC`, including its cacheless RV32I
VexiiRiscv variant, DMA port, CPU memory CDC, Wishbone fabric, PP bridges,
DDR controller and SPI controller. Shape constants and the AEM flash image come
from the product builder. The shape include is emitted under `gen/`, matching
the product include path. No tracked generated files or donor files are changed.
The configured CPU/system clocks are 100/100 MHz at 8x8 and 50/100 MHz at 1x1.
Audio domains and configured audio geometry remain present.

`firmware.py` copies the shipping C file into scratch and inserts instrumentation
at unique anchors. The product compiler builds that file and the real BIOS.
The firmware reads the 100 MHz system timer immediately before ARM and after
successful ATTEST. The interval includes ownership reads, every `nvm_rec_after()`
walk, byte loads and stores, the fence, attestation and instrumentation overhead.
Flash prefill and destination poisoning happen before timing.

The real boot and accepted RELOAD leave all allocated records closed. Every
capture checks the entire ownership vector, successful attestation and equality
of every raw destination byte with the live image. Before ARM, every destination
byte is poisoned with its live value XOR 255. This makes a skipped copy observable
even when live content has not changed. The full closed-record copy is 12,634
bytes across 156 records at 8x8, including 4,672 output-map bytes; it is 3,218
bytes across 53 records at 1x1. Materialization does not reduce that copy.
Each iteration releases the capture and repeats; it does not commit to flash.

`sim_main.cpp` offers continuous 60-byte AEM READ_DESCRIPTOR ENTITY 0 requests at
the MAC AXIS boundary, respecting backpressure. Traffic starts before capture
and continues between captures. TX is always ready. The offered load has no
Ethernet inter-frame gap or line-rate throttle. Sequence IDs wrap naturally;
requests that the PP drops under load are not counted as successful responses.

Three counters reset at the start of the record walk and stop before ATTEST:
completed input frames, successful READ_DESCRIPTOR responses, and read
acknowledgements on the real shared descriptor-memory Wishbone port. Every
capture must have positive counts for all three. Thus traffic is evidenced
during the copy, not inferred from a controller enabled before or after it.
The first five TX frames are logged for response-header inspection.

Board clock primitives and physical memory devices are replaced by simulation
models. The DDR model uses the board PHY's controller-facing phases and latencies;
physical leveling is disabled. The MAC, wire transport and board signal integrity
are outside the model. BIOS delays, boot CRC and the startup DDR test are disabled;
the timed capture code and its buses remain present. This is cycle-accurate SoC
evidence under the stated traffic, not a silicon timing or memory-ordering proof.
The measured remedy and figures belong in
[snapshot ownership section 18](../../../docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md#18-cost).
The [measurement receipt](measurements.json) records all 32 captures and input hashes.

# Firmware service-budget measurement

This is the product-CPU measurement for [issue #397](https://github.com/kebag-logic/milan-fpga/issues/397).
It imports the existing capture SoC read-only and links the unchanged product
firmware. The hart runs at 50 MHz, the system at 100 MHz, with aligned rising
edges. The [findings](../../../docs/findings/397_SERVICE_BUDGET.md) state the
measured scenarios, deadlines and remaining proof limits.

## Run and reproduce

`make -C tb/verilator/fw_service_budget` runs the portable measurement-oracle
and flash-device controls, including a planted duty one system tick beyond
its budget and a delayed UART response in the recorded 1x1 trace. The latter
must trigger the command's budget check, not merely its heartbeat check.
It does not claim a fresh product-CPU measurement. Full simulation
requires the same LiteX dependencies, cached shipping CPU netlist and RV32
SDK as the [capture harness](../nvm_capture_cpu/README.md). Keep builds outside
the checkout. The selected Python environment must also supply the `python3`
used by the BIOS build; put system build utilities ahead of SDK utilities.

```sh
python3 -B tb/verilator/fw_service_budget/run.py --self-test
python3 -B tb/verilator/fw_service_budget/run.py \
  --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/service-1x1 --build-only
python3 -B tb/verilator/fw_service_budget/run.py \
  --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/service-1x1 --reuse-build
python3 -B tb/verilator/fw_service_budget/run.py \
  --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/service-1x1 --reuse-build --populated
```

Repeat with `endstation_ax7101_8x8` and a separate build directory. Add
`--device-wait-us 1000` to exercise WIP polling with a one-millisecond device
delay for each erase and page program. This is a scenario input, not a flash
datasheet maximum. `--reuse-build` refuses changed compiled inputs or binary
contents. Commands run in the foreground; any build, device or marker failure
returns nonzero. The default also refuses a budget overrun, after writing its
receipt. For the issue's measurement-only scope, `--record-budget-findings`
records and prints every strict budget refusal while returning success for
valid evidence. This mode does not claim that those budgets passed or change
their thresholds. `--regrade` checks a previously bound log's hash and build
identity, then regenerates its analysis without executing the simulation again.
The build directory receives raw UART/event logs,
integer-cycle JSON receipts, generated fixtures, and build products.

## Measurement contract

`build.py` replaces only the simulated flash device boundary and adds passive
Wishbone and NVM-backend observation pads. The real CPU, firmware, DDR model,
CDC, bus adapters, NVM backend and LiteSPI controller remain instantiated.
The capture harness's BIOS CRC/delay/memory-test exclusions remain in effect;
there is no firmware source instrumentation. No physical boot-time claim
includes those excluded BIOS operations.

The external device accepts single-width serial transfers at eight system
cycles per bit plus one completion cycle, corresponding to 12.5 MHz SCK.
It implements flash reads, WREN, RDSR, sector erase and page program. It checks
WEL, WIP, journal bounds and page boundaries. Initial media is either erased
or two equal-sequence, valid KLJ2 containers covering every allocated record.
Their deterministic payloads exercise the restore traversal; they do not
represent a live network configuration. No external packet traffic is injected.

An event's cycle is the system rising edge at which its handshake occurs.
CPU cycles are the elapsed system cycles divided by two, rounded upward;
they are elapsed clock units, not retired instructions. Milliseconds use the
unrounded system count. Measurements include modeled bus/DDR stalls, serial
transport and CPU polling. Only the configured WIP spans are subtracted for
the separate service column. The CPU executes polling during those spans;
that subtraction is a wall-time decomposition, not CPU utilization.

Boot starts when reset is released and ends at the entity-enable write.
This also encloses AEM copy and CRC, which have no narrower marker. Restore
starts and ends at the existing restore-control writes and must contain
successful NVM-backend request/response handshakes. UART starts at the first
accepted input byte and ends after the returned console prompt. Every command
registered in the product translation unit is checked against the command
plan. Repeated commits visit both slots; wipe, status, numeric boundaries and
invalid arguments are exercised. UART has immediate byte handshakes, so these
are service intervals without the board's baud-rate and host pacing delays.

The commit bracket runs from START to ACK. The erase envelope runs from the
accepted erase to the first accepted page program; it also includes erase
verification and the first page's transmission. It is deliberately wider than
the erase poll loop. Flash command counts must match the generated image's
length and page count. No entity enable, missing commands, failed commits,
absent restore traffic, or excess flash operations can yield a measurement.

The 500 ms ordinary-command budget is a conservative service-window comparison
with the maximum heartbeat period, not a normative UART response deadline.
The measured heartbeat gap is reported separately, including the interval
from the last heartbeat to the final command's end. Clock-setting commands
change the firmware's PHC while the measurement clock remains monotonic.
The maximum gap is itself graded against 500 ms and retained as a named
finding if it exceeds that limit.
Commit and erase are compared with their existing 8,000 ms and 3,500 ms
limits; restore uses 3,000 ms. No boot deadline is inferred from ADP valid time.
Wipe has no single commit deadline: its two erase envelopes end at the second
erase and the returned prompt, respectively, and each uses the erase limit.
The whole wipe is reported without an invented deadline. Page-program work
is enclosed by the commit bracket, without an isolated polling-loop margin.
Device maxima and their conditional projections belong in the findings.

# Firmware service-budget measurement

This is the measurement harness for [issue #397](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5855879265).
It runs unchanged firmware on the shipping cacheless CPU.
The CPU runs at 50 MHz; the system runs at 100 MHz.
[Findings](../../../docs/findings/397_SERVICE_BUDGET.md) separate duties, schedules and liveness.
The service checks cover [#590](https://github.com/kebag-logic/milan-fpga/issues/590) and PHY publication under [#599](https://github.com/kebag-logic/milan-fpga/issues/599).

## Contents

- **[Run and reproduce](#run-and-reproduce)** -- Build prerequisites, named command plans, supported device waits and receipt handling.
- **[Markers and heartbeat opportunities](#markers-and-heartbeat-opportunities)** -- External duty boundaries, passive tick observation and schedule-dependent liveness evidence.
- **[Timing limits and controls](#timing-limits-and-controls)** -- Clock conversion, deadlines, substitution bias and mutation-sensitive controls.
- **[PHY publication and firmware controls](#phy-publication-and-firmware-controls)** -- Clause-22 pin transactions, real status readback, fabric counters and mutation-sensitive service controls.

## Run and reproduce

The portable gate requires Python and a C++17 compiler:

```sh
make -C tb/verilator/fw_service_budget
python3 -B tb/verilator/fw_service_budget/run.py --self-test
```

It does not regenerate product-CPU measurements.
Full simulation uses the [capture prerequisites](../nvm_capture_cpu/README.md#run).
Keep build directories under temporary storage, outside the checkout.
Put system build utilities ahead of SDK utilities.
The selected environment must provide the BIOS build's Python.
Set the compiler prefix through `LITEX_ENV_CC_TRIPLE`.
Use `PYTHONHASHSEED=0` and `PYTHONDONTWRITEBYTECODE=1`.
The inherited builder also writes ignored generated ROMs inside the checkout.
They are not measurement receipts or tracked source changes.

```sh
python3 -B tb/verilator/fw_service_budget/run.py \
  --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/service-1x1 --build-only
python3 -B tb/verilator/fw_service_budget/run.py \
  --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/service-1x1 \
  --reuse-build --populated --record-budget-findings
```

Repeat using `endstation_ax7101_8x8` and a separate build directory.
The named plans are:

| Plan | Input and purpose |
| --- | --- |
| `all` | Immediate UART handshakes; all 17 command cases, two commits and wipe |
| `uart-paced` | Same cases; both UART directions use 115,200 baud, 8N1 spacing |
| `queued-input` | Twelve NVM status commands, then status: 133 bytes on both shapes |
| `queued-short` | 350 consecutive status commands; isolates dispatch service from inner walks |
| `queued-builtins` | Repeated bounded `mem_read`, empty and unknown lines; final status |
| `device-wait` | One commit, then status; isolates erase/page WIP behavior |

`queued-input` models continuously available input at each returned prompt.
It does not inject an entire paste simultaneously into the RX ring.
The BIOS idle hook is consequently suppressed between these commands.
`uart-paced` permits idle service between received characters.
It adds no operator think time or host latency.
Frame spacing rounds upward to 8,681 system cycles.
The unchanged public pacing probe uses 8,680; its result is reported separately.
The final character's transmission completes at its modeled handshake boundary.

```sh
python3 -B tb/verilator/fw_service_budget/run.py \
  --build-dir /tmp/service-1x1 --reuse-build --populated \
  --plan uart-paced --record-budget-findings
python3 -B tb/verilator/fw_service_budget/run.py \
  --build-dir /tmp/service-1x1 --reuse-build --populated \
  --plan queued-input --record-budget-findings
python3 -B tb/verilator/fw_service_budget/run.py \
  --build-dir /tmp/service-1x1 --reuse-build --populated \
  --plan device-wait --device-wait-us 3000000 --program-wait-us 5000 \
  --record-budget-findings
```

`--device-wait-us` sets erase WIP; `--program-wait-us` sets page WIP.
They accept 0..3,000,000 and 0..5,000 microseconds, respectively.
These include the documented device maxima.
Values outside those ranges fail before building or simulating.
The largest plan has four erases and 100 pages.
Its maximum WIP is 12.5 seconds, below the 30-second guard.
Measured no-WIP work leaves additional room inside that guard.
This is a supported-scenario limit, not an arbitrary-stall guarantee.

Build reuse checks compiled inputs, generated files, ELF, BIOS and executable.
Each run emits its raw UART/event log and JSON receipt.
The receipt includes raw text, its digest and input hashes.
No manual receipt-assembly step is needed.
Raw per-run receipts belong in the public evidence packet.
The repository retains summary tables and portable oracle fixtures only.
`--regrade` checks the bound log and build before regenerating analysis.
Use identical scenario arguments with `--regrade`.

Use `--enforce-service` for the firmware lane's required verdict.
It checks each duty's tick allowance and actual deadlines.
Long-running BIOS built-ins remain outside these measured duty bounds.
`mem_test` and large `mem_read` ranges lack internal service.
They can exceed heartbeat and PHY publication bounds until returning.
The BIOS dispatch hook covers their boundaries, including queued input.

PHY publication reserves a 125 ms trigger phase plus the duty stretch,
UART allowance and a conservative poll charge within 250 ms.
The charge adds nine maximum measured transactions to the measured complete poll.
Nine reads cover discovery and the longest negotiation fallback.
This deliberately counts observed transaction time twice.
Startup AEM and restore report isolated service-plus-poll costs without a trigger phase.
Those costs exclude intervening startup work.
Observed gaps between status readbacks independently grade startup and runtime within 250 ms.
It also requires continuous backing after the first armed cycle.
Ordinary UART response duration remains a reported historical comparison.
A long handler can satisfy service through its internal ticks.

The default retains the original measurement-only duration comparisons.
`--record-budget-findings` prints every refusal and permits measurement completion.
Its success never approves a missed budget.
Commands run in the foreground; malformed evidence always fails.

## Markers and heartbeat opportunities

The capture SoC is imported read-only; product firmware is linked unchanged.
Passive bus pads observe CSR writes and backend handshakes.
SPI reads at offset `0x400000` begin the AEM interval.
The entity-enable write ends both AEM and boot intervals.
Boot begins at reset release, system cycle 64.
Restore uses control writes enclosing matching, successful backend handshakes.
Commands span their first input byte through the returned prompt.
Commit spans START through ACK; erase extends through first page acceptance.
Wipe has two erase envelopes, not a single commit timer.

Actual heartbeat writes use `PP_NVM_STAT <- 1`.
They differ from calls to the rate-limited heartbeat function.
A passive committed-PC observer measures those function-entry opportunities.
The linked ELF supplies the function address; missing symbols are refused.
The CPU's existing commit-valid and commit-PC signals qualify every observation.
Speculative fetches and stalled instructions do not count.
No firmware, CPU netlist or capture-harness file is modified.
Dense calls are compressed between external boundaries.
Each block preserves first/last calls, count and maximum internal gap.
The grader reconstructs duty-edge, cross-block and internal gaps.

The resulting opportunity-free span includes both duty-edge tails.
For isolated duties, compare 250 ms plus that span and TX blocking.
Receipts conservatively allow serialization of the containing command's entire output.
Paced observations already include UART blocking; adding it again is conservative.
Boot's pre-heartbeat prefix precedes writer liveness arming.
The boot row must not be interpreted as an armed-writer gap.

The plan-dependent heartbeat row includes the final, right-censored tail.
Receipts name its start, end, plan and both deadline margins.
It is not a per-duty worst-case bound.
UART `backed` and `PP_STAT[6]` observations retain liveness evidence.
The native observer also samples the backend's backing register every cycle.
It counts any loss after that register first asserts.
`--enforce-service` requires zero such cycles and all-positive console samples.

## Timing limits and controls

CPU cycles are system cycles divided by two, rounded upward.
Milliseconds retain the unrounded 100 MHz count.
These are elapsed clock units, not retired-instruction counts.
The comparison limits are 500 ms heartbeat and 2,000 ms liveness.
Restore, erase and commit use 3,000, 3,500 and 8,000 ms.
Boot uses the assignment's 20-second ADP validity comparison.
Milan v1.2 sections 5.6.2/5.6.3 supply that validity window.
Excluded BIOS CRC, delays and memory testing remain unmeasured.
A positive simulated margin cannot establish physical boot inside that window.

The independent flash model checks WEL, WIP, journal bounds and pages.
It retains the real controller but substitutes the serial PHY/device boundary.
The substitution is optimistic: 65 versus 67 cycles per byte.
A 32-bit transfer costs 257 versus 259 cycles.
CS reassertion omits another 11 cycles relative to steady transfers.
These are boundary costs, not a uniform correction for every duty.
DDR uses the existing simulation model; packet traffic is absent.
One deterministic clock phase is exercised.

Service time subtracts configured WIP from measured elapsed time.
Polling consumes CPU during WIP; subtraction does not measure spare capacity.
Future update writing, fault logging and temperature remain unmeasured.
Physical timing, the architecture decision and bench torture remain open.

The self-test pins complete rows and findings from three fixed traces:
both immediate `all` shapes and paced 1x1.
It also pins clock conversion, markers, deadlines and tick-span reconstruction.
An exact-budget duty passes; one extra system cycle fails.
A delayed final response must fail that command's budget specifically.
A combined control word must not become a standalone heartbeat marker.
The paced trace checks UART reconstruction across interleaved observations.
Device controls separately exercise busy refusal with WEL already true.
That predicate control deliberately uses explicit nonmonotonic test times.
It is not presented as a physical flash command sequence.

## PHY publication and firmware controls

The harness provides a Clause-22 peer at simulated MDIO pins.
The firmware performs every bit-bang transaction and status publication.
Both peers follow IEEE 802.3 section 22.3.4 output timing.
Rising edge k launches bit k+1 for subsequent sampling.
The firmware samples before the data rising edge.
A late-sample control must fail initial negotiated-status publication.
Simulation CSRs reproduce the product register and synchronizer semantics.
The product datapath receives the existing link-status inputs.
A separate bus reader reads the real MAC_STATUS register.
The observer reads actual fabric LINK_UP and LINK_DOWN counters.
Every published link transition must increment its corresponding counter once.
Repeated publications must leave both counters unchanged.
The peer drops link from 1.5 through 1.8 seconds.
At 2.4 seconds it changes negotiation to 100 Mb/s.
All queued plans and `device-wait` require one completed down/up cycle.
Host tests separately cover discovery, errors and speed/duplex modes.
They require a latched brief loss and its recovered state to publish in one poll.
A mutation restoring the old second-poll delay must fail that current-state check.

Target timestamps cover each transaction and the complete poll.
The poll envelope begins at the retired heartbeat entry.
It includes clock acquisition, MDIO, resolution and publication bookkeeping.
The console and NVM duties therefore include PHY polling cost.
The pin boundary replaces physical Ethernet transport and PHY timing.
It cannot establish the deferred board acceptance.

Explicit controls use scratch firmware with checked substitution anchors:

```sh
python3 -B tb/verilator/fw_service_budget/run.py \
  --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/service-no-dispatch \
  --populated --plan queued-builtins --enforce-service --mutation remove-dispatch
python3 -B tb/verilator/fw_service_budget/run.py \
  --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/service-no-publish \
  --populated --plan all --enforce-service --mutation no-publish
```

Dispatch removal must fail the continuous-backing check.
Every normal built-in, unknown and empty line requires an observed tick.
The built-in queue exceeds the required 133 input bytes.
`--mutation late-sample` must fail the negotiated-status check.
Publication removal must fail the target publication-evidence check.
The ordinary firmware serves as each control's positive arm.
Portable fixtures reject one-cycle service overruns and duplicate link edges.

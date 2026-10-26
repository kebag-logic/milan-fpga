# Split CPU service budget

This harness measures the Mark II split firmware's service paths on the shipping cacheless core.
Its contract is the [S2 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409745905) on #665, which re-opens [#397](https://github.com/kebag-logic/milan-fpga/issues/397).
The image is `ctrl_srp_image.py --with-aecp --layout split`, linked unmodified.
Every figure is a measured clock count at the CPU's 50 MHz, never an estimate.
Each is compared with T_svc = 10 ms and its ceiling in [FR_NFR.md 3.4.1](../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing).

## Contents

- **[Run and reproduce](#run-and-reproduce)** -- Prerequisites, the two points, the labelled arms, the controls, reuse and the regrade.
- **[The test SoC](#the-test-soc)** -- What is the shipping CPU and memory, what is test-only, and where each device sits.
- **[Markers and grading](#markers-and-grading)** -- The start and end of each path, the clock conversion, the pass bound, the defined load, its service and the verdicts.
- **[Results](#results)** -- Per access, per pass, every response path, the fan-outs, the backlog rows and the load's service.
- **[Findings](#findings)** -- The decision input for D4, D5 and D3, and the defects the measurement exposed.
- **[Controls and self-test](#controls-and-self-test)** -- The planted over-budget paths, the region-decode control and the grader mutants.
- **[Limits](#limits)** -- What is not measured, and why.

## Run and reproduce

Use the [capture prerequisites](../nvm_capture_cpu/README.md#run): the product LiteX tree, the pinned RV32 SDK and Verilator.
The CPU netlist is generated offline from the pinned generator; set `COURSIER_MODE=offline` and `SBT_OPTS=-Dsbt.offline=true`.
The tsn-c-stack and lwSRP submodules must be initialised.
Keep build directories outside the checkout.
The portable self-test needs Python and PyYAML only:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
```

Each point builds the runtime, the image, the SoC and the native model, then runs every group:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 \
  --build-dir /tmp/budget-8x8 --record-budget-findings
```

`1x1` is `endstation_ax7101_1x1_tdm8` with one AVB interface.
`8x8` is `endstation_ax7101_8x8` with two.
Without `--record-budget-findings` a path over T_svc fails the run.
With it, the misses are recorded and the run still fails on any probe that was not measured.
`--groups` selects groups and `--jobs` sets how many run at once.

`--reuse-build` reuses a build only if every input recorded in its `build.json` still has its digest.
The inputs are the checkout's testbench and mailbox sources, every file of the firmware source trees the image is compiled from, the image, its runtime archives, the ROM `.init` files the model reads when it runs, the exported SoC Verilog, the generated two-interface mailbox and the CPU netlist and RAM models.
A changed or missing input, a ROM file that was never recorded, or a recorded key that does not resolve is refused, and the run exits 1.
`--regrade --out DIR` grades the logs already in `DIR`, on a reused build.
Every selected group must have its script and its log there, and its script must be the one the scenario now generates.
Otherwise that group is refused by name and the run exits 1; a partial regrade selects its groups with `--groups`.
So a group whose script is unchanged, on a build that still attests, is regraded from its log rather than run again.

Two labelled arms change test code only, each in a scratch copy of the fixture, and are never the formal measurement:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-1x1-ports --variant answering-ports \
  --groups acmp-cmd,acmp-noresp,acmp-notk,acmp-disc,backlog,backlog-adp,backlog-owed,aecp-fanout \
  --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-1x1-shutdown --variant shutdown-entry --record-budget-findings
```

- `answering-ports` (arm B) makes the fixture's four observation callbacks answer.
- `shutdown-entry` adds the SHUTDOWN path's only input: a poll that calls `adp_mbx_set_enable(false)` once, at NOW_MS 2,500.
  It runs the `adp-shutdown` and `control-shutdown` groups only.

The directory has no Makefile on purpose.
The serial sweep discovers every Makefile, and `scripts/suite_shards.py` must then register the suite.
That is a CI change, outside this lane.

## The test SoC

[`split_soc.py`](split_soc.py) builds it; [`build.py`](build.py) links the image and compiles the model.

- **The CPU** is MilanSoC's own VexiiRiscv path: cacheless RV32I, one hart, the CPU at the 50 MHz Milan clock, the bus at 100 MHz.
  The DMA port the shipping image has is kept, idle.
- **The firmware memory** is `milan_soc.add_ctrl_memory`, the split placement's, built from the linked image.
- **The mailbox** is this harness's own instance of `KL_mbx` behind `KL_mbx_wb`, with CtrlMailbox's hookup.
  Its datapath side is on pads that [`sim_main.cpp`](sim_main.cpp) drives.
  `milan_soc.CtrlMailbox` and its idle tie-offs are not used.
  At two interfaces the RTL is `gen_mailbox.py`'s variant, written into the build directory.
- **The flash** keeps LiteSPI's crossbar, memory-mapped reader and command master.
  The serial device is [`fw_service_budget/flash.hpp`](../fw_service_budget/flash.hpp) with that harness's byte timing.
- **timer0** is LiteX's timer.

The linked image is a size fixture with placeholder bus addresses.
The SoC puts each device where the unmodified image addresses it, read from the fixture's own sources:

| Device | The image addresses it at | The product SoC maps it at |
|---|---|---|
| Mailbox window | `0x8000_0000` (`ctrl_build.py`, `CTRL_MBX_BASE`) | `0x9010_0000` (`CTRL_MBX_BASE`, `milan_soc.py`) |
| LiteSPI command master | `0xf000_3000` (`ctrl_nvm/test/rv32/generated/csr.h`) | `0xf000_2810` |
| timer0 | `0xf000_3800` | `0xf000_3000` |
| Flash window | `0x2000_0000` (`generated/mem.h`) | `0x0100_0000` |

Each reaches the same kind of device over the same peripheral bus in both maps, so the address does not change an access's cost.
`--ctrl-mailbox` leaves the CSR map unchanged ([split control memory](../../../docs/design/SPLIT_CONTROL_MEMORY.md#4-boot-console-and-diagnostics)).

The CPU generator is handed each region at its power-of-two cover (256 KiB for `rom` and `sram`).
Generated from the 224 KiB regions, its region check excludes every `rom` address with bit 15 set, and the image faults ([#791](https://github.com/kebag-logic/milan-fpga/issues/791)).
The two netlists differ only in address-decode lines, so the cover changes no timing.
`--cpu-regions as-built` builds the regions unchanged and reproduces the fault.

## Markers and grading

[`scenario.py`](scenario.py) writes each group's script.
Every probe is a `mark`, its stimulus and a bounded wait.
[`grade.py`](grade.py) reads its start and end off the log, as [FR_NFR.md 3.4.1](../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing) defines them:

- A received frame starts at its receive commit, `KL_mbx_rx`'s header write (RX_HEAD).
  The probe's frame carries a tag, so other frames on the ring are not mistaken for it.
- A commit belongs to the frame whose last byte it follows.
  `KL_mbx_rx` takes no byte of a frame until the previous frame's verdict (`rx_ready_o` only in `RECV_S`), and every commit measured follows its frame's last byte by 4 bus cycles.
  An older frame left without a commit was refused by the filter.
- A link or grandmaster event starts when its level changes at the mailbox input.
- A timer path starts at its armed deadline: the tick on which NOW_MS reaches it, not the record's posting.
- The test-only SHUTDOWN input starts at the commit of `adp_mbx_set_enable`'s entry.
- A path ends when its last required output is committed: an accepted TX_HEAD write, a TMR_CMD arm or cancel, a publication write or the record's RX_TAIL release.
- A response is matched by its sequence_id and its interface.
- A notification fan-out ends at the last required recipient's commit.
  Each recipient is a controller registered for unsolicited notifications on an interface (IEEE 1722.1-2021 7.5.2).
  Each must receive the unsolicited response of the probe's command type and descriptor.
  A missing recipient is refused, and so is the change notified to a controller outside the set; other unsolicited responses do not count.
  Every fan-out is measured with the firmware's registration capacity on every interface (`AECP_REGISTRATIONS`, 16, in `aecp.h`), from a requester outside them, so every registration is a recipient.
  The per-recipient cost is the last recipient's commit less the first's, over the gaps between them.
- A response with frames owed ahead of it requires exactly those responses, by sequence_id and in order, between its input and its own.
- A command the core may take and drop under the load (one behind the owed input) is a path too: a response that never comes is reported as **never answered**, a measured finding with no bound, not a refusal.

Every conversion is one `Grader` method: CPU cycles from bus cycles (times 50/100, rounded up), bus cycles from CPU cycles, and milliseconds from either.
A pass runs from one committed entry of `ctrl_loop_service` to the next.
The script's end cuts the pass in progress short, so the run of idle passes it flushes is no idle pass's figure.
A mailbox access is timed at the CPU's load/store bus, from command to response.
Instruction fetches are counted at the cacheless fetch bus, by region.

One phase is one sample.
So each probe also reports a measured bound.
It runs from the start of the pass that was running when the input arrived, or the longest idle pass before it, to the end of the pass that committed the output.
Whatever the input's phase, it is taken by the next pass at the latest, so with the same passes the interval cannot exceed the bound.
Each probe also reports the records ahead of its input: those on its ring (or in the event ring) committed before it and not yet released.

A backlog group's composed window, between its `composed` and `composed_end` marks, carries its row's defined load.
`grade.defined_load` derives that load from the mailbox contract alone, never from the stimulus: each channel's records one instant admits, at the size of the load's frame.
The grader counts the records each receive channel committed in the window, and the GM and LINK events posted.
It refuses the group unless that population is exactly the defined load, so a record the filter refused, a channel left out or one record too many fails the run.
The self-test counts every window's stimulus against the same loads, restated, so a scenario that drops a channel from its stimulus and from its own declaration together still fails.

The window must also service its load.
For each loaded channel, the window's first and last record are graded from their receive commit to the end of the pass that released them, as the SRP rows end: the handler runs after the release, inside that pass (`ctrl_loop.c`, `service_rx`).
A record no release reached is **never released**: its row carries the time it had waited by the run's end, a lower bound, and fits neither T_svc nor its ceiling.
The window's longest pass is the composed maximum only if the window released its whole load; otherwise the record names what was left, and that pass is a lower bound of a load the firmware did not finish.

The ceilings are 3.4.1's: ADP 200 ms, a discovery input's ACMP action and ACMP 20 ms, AECP 24 ms, a notification 24 ms, MAAP 50 ms, MRP 18 ms.
A path with a normative wait W, such as SRP's JoinTime, is bounded by W + T_svc, and its ceiling by W plus the ceiling.

## Results

Arm A is the image as linked, the formal measurement.
Arm B is the labelled second arm, whose fixture callbacks answer.
The SHUTDOWN row comes from the labelled `shutdown-entry` arm.
In the path tables a cell is a path's worst measured instance across the groups that measure it, "ms (the pass bound)"; **miss** is over T_svc, **over ceiling** over the 3.4.1 ceiling as well.
A record never released or a command never answered is worse than any time measured, and its cell gives the time it had waited, at least.
Each run writes every path's worst instance, every probe, every composed window and every timed-out wait to its `table.md`, and all of it to `results.json`.

Arm labels: A is arm A, B is arm B, S is the `shutdown-entry` arm; 1 is 1x1 and 8 is 8x8.
T_svc misses, counted per path and per probe instance (a path several groups measure is one path, at its worst; at 8x8 each interface's instance is its own path):

| Arm | Groups | Paths missing T_svc | Probe instances missing T_svc |
|---|---:|---:|---:|
| A1 | 18 | 22 of 81 | 58 of 141 |
| A8 | 17 | 60 of 129 | 102 of 182 |
| B1 | 8 | 18 of 44 | 41 of 68 |
| B8 | 8 | 36 of 68 | 60 of 92 |
| S1 | 2 | 0 of 1 | 0 of 2 |
| S8 | 2 | 0 of 2 | 0 of 3 |

### Per access and per instruction

| Point | CPU cycles per instruction | Fetches per instruction | Mailbox read / write, CPU cycles | BRAM fetch, CPU cycles (max) | sram load/store | CSR | Flash window load | Code fetched, boot / service (largest run) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 | 9.52 | 1.69 | 9 / 9 | 9.09 (303) | 9-10 / 9-10 | 9-10 / 9 | 262.9 mean (138-303) | 11,160 / 42,080 B |
| 8x8 | 9.49 | 1.68 | 9 / 9 | 9.13 (303) | 9-10 / 9-10 | 9-10 / 9 | 262.5 mean (138-303) | 11,396 / 43,060 B |

Every access is timed at the CPU, command to response, in CPU cycles at 50 MHz.
A mailbox access is 9 cycles, 0.18 us; `KL_mbx` itself answers in one bus cycle, and the rest is the clock crossing and the bus.
A fetch waits behind a slow flash read, hence the 303-cycle maximum.
Instruction fetches are 85 to 89 % of the CPU's bus transactions in every taking pass.
Their waits sum to 1.59 to 1.64 times each pass's cycles, so more than one fetch is outstanding on average: the cacheless core is fetch-bound.

### Passes

| Point, arm | Idle pass, CPU cycles (ms) | Worst pass, CPU cycles (ms), group | Composed maximum, CPU cycles (ms), group | Longest pass under a load left unreleased (lower bound) |
|---|---:|---:|---:|---:|
| 1x1, A | 65,703 to 72,632 (1.31 to 1.45) | 1,565,803 (31.32), backlog-adp | 740,260 (14.81), backlog | 1,565,803 (31.32), backlog-adp |
| 1x1, B | 65,703 to 232,901 (1.31 to 4.66) | 740,260 (14.81), backlog | 740,260 (14.81), backlog | - |
| 8x8, A | 157,133 to 185,315 (3.14 to 3.71) | 2,989,496 (59.79), acmp-notk | 1,392,016 (27.84), backlog | 2,209,308 (44.19), backlog-adp-refill |
| 8x8, B | 157,133 to 293,468 (3.14 to 5.87) | 2,004,666 (40.09), acmp-notk | 1,392,016 (27.84), backlog | - |

The composed maximum is the longest pass of a window that released its whole load.
In arm A's two bound-talker windows SRP's 32 records are never released (see [the load's service](#the-loads-service)), so their longest passes are lower bounds, in the last column.
An idle pass's largest consumers are AECP's two modules, `aecp` 26,497 and `aecp_nvm` 20,254 cycles at 1x1, 73,883 and 20,254 at 8x8, mostly their polls.
The idle range excludes the pass the script's end cuts short; at 8x8 it is 3.14 to 3.71 ms (157,133 to 185,315 cycles) in arm A.
The 8x8 link-up pass, 2,004,666 cycles, is lwSRP's `mrp_mad` 473,950, `memset` 361,053, `memcpy` 244,102, the mailbox driver 119,790 and software multiply and divide (`__mulsi3` 111,201, `__udivsi3` 89,954).
The composed maximum at both points is the `backlog` group's: at 1x1, 740,260 cycles of `memset` 278,637, the mailbox driver 141,995, `memcpy` 66,719, AECP 41,029 and ACMP 36,377; at 8x8, 1,392,016 cycles of `memset` 477,042, the mailbox driver 134,267, `memcpy` 132,197, AECP 111,084, ACMP 89,857 and `__mulsi3` 67,272.
The 1x1 worst pass, `backlog-adp`'s 1,565,803 cycles, is `memset` 984,728, AECP 173,531, the mailbox driver 127,547, ACMP 49,350 and `memcpy` 46,964: after the bind, AECP's retry (see [Findings](#findings)).

### ADP

| Path ([`MAILBOX_SPLIT.md:495-502`](../../../docs/design/MAILBOX_SPLIT.md#service-latency)) | 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses in the taking pass, 1x1 / 8x8 (model) |
|---|---:|---:|---:|
| RCV_ADP_DISCOVER -> TMR_DELAY armed | 0.29 (1.63) | 2.57 (9.27) / 2.86 (9.27) | 38 / 73 (31) |
| TMR_DELAY expiry -> ENTITY_AVAILABLE, TMR_ADVERTISE armed | 0.87 (3.57) | 2.64 (9.09) / 3.70 (10.87) | 46 / 47 (39) |
| TMR_ADVERTISE expiry -> TMR_DELAY armed | 0.13 (1.99) | 1.06 (8.28) / 1.37 (4.60) | 9 / 25 (11) |
| GM_CHANGE -> TMR_DELAY armed | 0.10 (1.46) | 2.38 (8.95) / 2.50 (8.95) | 18 / 34 (11) |
| LINK_UP -> TMR_DELAY armed | 0.11 (4.97) | 32.51 (73.31) **miss** / 41.69 (73.31) **miss** | 88 / 345 (11) |
| LINK_DOWN -> timer stopped | 0.08 (5.48) | 18.35 (42.60) **miss** / 26.84 (42.60) **miss** | 33 / 70 (9) |
| SHUTDOWN -> ENTITY_DEPARTING (test-only entry, `shutdown-entry` arm) | 0.58 (1.94) | 0.58 (5.14) / 1.17 (5.14) | 39 / 75 (29) |

### ACMP

| Path ([`MAILBOX_SPLIT.md:645-657`](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency)) | A: 1x1 ms (bound) | A: 8x8 if0 / if1 | B: 1x1 | B: 8x8 if0 / if1 | Accesses, A 1x1 / 8x8 (model) |
|---|---:|---:|---:|---:|---:|
| BIND_RX | 1.62 (3.96) | 4.51 (13.22) / 11.36 (31.60) **miss** | 1.62 (3.96) | 4.51 (13.22) / 4.22 (12.59) | 82 / 90 (77) |
| UNBIND_RX | 6.56 (26.86) | 6.75 (27.03) / 19.80 (40.08) **miss** | 1.07 (3.22) | 3.99 (10.46) / 3.95 (12.55) | 119 / 176 (50) |
| GET_RX_STATE | 3.34 (23.10) | 10.96 (30.77) **miss** / 19.79 (39.60) **miss** | 0.96 (2.79) | 4.15 (12.47) / 3.46 (10.05) | 113 / 114 (47) |
| PROBE_TX_RESPONSE | 12.02 (29.87) **miss** | 19.40 (35.12) **miss** / 15.99 (39.22) **miss** | 0.37 (2.46) | 2.95 (11.41) / 3.41 (11.87) | 104 / 102 (32) |
| PROBE_TX | 3.48 (23.02) | 11.17 (30.68) **miss** / 21.02 (54.45) **over ceiling** | 1.51 (3.25) | 1.54 (9.89) / 4.11 (12.26) | 115 / 116 (48) |
| GET_TX_STATE | 6.37 (26.36) | 10.67 (30.66) **miss** / 27.60 (87.09) **over ceiling** | 1.00 (2.72) | 3.52 (11.65) / 3.53 (9.89) | 117 / 115 (48) |
| DISCONNECT_TX | 24.77 (44.77) **over ceiling** | 10.62 (30.62) **miss** / 20.18 (32.59) **over ceiling** | 0.95 (2.67) | 0.96 (6.62) / 4.19 (12.34) | 117 / 115 (48) |
| GET_TX_CONNECTION | 11.08 (26.31) **miss** | 10.63 (30.63) **miss** / 19.70 (39.52) **miss** | 0.95 (2.67) | 3.45 (9.84) / 3.48 (9.85) | 117 / 115 (48) |
| the first TMR_NO_RESP | 5.48 (47.98) | 14.19 (70.11) **miss** / 12.89 (70.11) **miss** | 0.86 (3.03) | 2.53 (13.06) / 1.14 (9.12) | 124 / 113 (35) |
| the second TMR_NO_RESP | 1.64 (21.79) | 4.43 (24.89) / 5.24 (24.89) | 1.19 (3.89) | 1.46 (12.60) / 0.54 (8.12) | 72 / 67 (14) |
| TMR_RETRY | 7.99 (46.72) | 27.14 (76.55) **over ceiling** / 26.21 (76.55) **over ceiling** | 0.19 (3.79) | 3.17 (16.68) / 3.15 (14.68) | 73 / 68 (14) |
| TMR_DELAY | 2.90 (44.04) | 5.69 (38.79) / 8.58 (38.80) | 1.94 (5.06) | 1.70 (9.80) / 1.08 (6.57) | 95 / 93 (35) |
| TMR_NO_TK | 4.57 (22.15) | 15.23 (75.59) **miss** / 5.43 (38.64) | 0.19 (2.31) | 3.63 (9.89) / 3.24 (11.86) | 74 / 93 (14) |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 10.37 (25.92) **miss** | 27.41 (41.44) **over ceiling** / 29.72 (41.44) **over ceiling** | 0.90 (2.79) | 3.45 (14.07) / 5.76 (14.07) | 104 / 129 (35) |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 25.17 (50.78) **over ceiling** | 45.45 (83.13) **over ceiling** / 47.73 (83.13) **over ceiling** | 0.35 (2.24) | 1.18 (11.76) / 3.46 (11.75) | 98 / 177 (29) |
| TMR_NO_ADP (H-DISC) | 1.91 (22.31) | 8.51 (37.51) / 5.66 (31.48) | 0.99 (3.04) | 4.84 (15.30) / 2.25 (11.98) | 95 / 67 (12) |

The ACMP groups bind a sink, and from then on arm A's AECP retries its change notices every millisecond.
Those groups also run lane F1's first saved-state commit: one erase and 14 page programs (3,336 B) at 1x1, up to 52 (13,256 B) at 8x8, with zero device wait.
The 1x1 first TMR_NO_RESP and ENTITY_DEPARTING cells are the `fixture` group's instances, the worst of their paths.

### AECP

Each row ends at the command's solicited response (H-AECP).
The notification a setter's change causes is the fan-out below.

| AECP path | 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses, 1x1 / 8x8 |
|---|---:|---:|---:|
| READ_DESCRIPTOR type 0, 312 B | 5.14 (6.28) | 6.17 (12.33) / 6.19 (12.34) | 124 / 125 |
| READ_DESCRIPTOR type 1, 106 B | 4.33 (5.47) | 6.09 (11.91) / 6.12 (11.93) | 73 / 80 |
| READ_DESCRIPTOR type 2, 148 B | 4.49 (5.63) | 6.21 (12.03) / 5.54 (11.36) | 83 / 121 |
| READ_DESCRIPTOR type 5, 146 B | 4.49 (5.63) | 6.94 (11.69) / - | 82 / 83 |
| READ_DESCRIPTOR type 6, 146 B | 5.01 (6.15) | 6.28 (12.10) / - | 89 / 90 |
| READ_DESCRIPTOR type 9, 102 B | 4.84 (5.98) | 5.38 (11.20) / - | 78 / 72 |
| READ_DESCRIPTOR type 10, 86 B | 4.79 (5.93) | 6.08 (11.50) / - | 74 / 69 |
| READ_DESCRIPTOR type 12, 72 B | 4.73 (5.87) | 5.30 (11.12) / - | 71 / 65 |
| READ_DESCRIPTOR type 13, 452 B | 6.21 (7.35) | 7.50 (12.92) / - | 166 / 160 |
| READ_DESCRIPTOR type 14, 20 B | 4.03 (5.17) | 5.77 (11.59) / - | 52 / 59 |
| READ_DESCRIPTOR type 15, 20 B | 4.02 (5.16) | 5.09 (10.91) / - | 51 / 52 |
| READ_DESCRIPTOR type 20, 90 B | 4.86 (6.01) | 6.23 (11.69) / - | 75 / 70 |
| READ_DESCRIPTOR type 26, 113 B | 4.95 (6.09) | 5.59 (11.41) / - | 81 / 75 |
| READ_DESCRIPTOR type 36, 82 B | 4.84 (5.98) | 6.26 (11.72) / - | 73 / 71 |
| entity_available | 4.49 (5.63) | 5.00 (11.16) / 5.77 (11.59) | 57 / 51 |
| get_avb_info | 4.51 (5.66) | 5.92 (11.35) / 5.21 (11.03) | 53 / 48 |
| get_configuration | 4.42 (5.56) | 14.82 (27.43) **miss** / 5.69 (11.10) | 53 / 60 |
| get_counters | 4.92 (6.06) | 6.57 (12.39) / 6.21 (12.03) | 86 / 80 |
| get_name | 4.69 (5.83) | 7.05 (12.87) / 5.21 (11.36) | 70 / 99 |
| lock_entity | 3.96 (5.41) | 8.32 (14.50) / 8.19 (14.64) | 66 / 73 |
| MVU GET_MILAN_INFO | 2.50 (3.64) | 3.52 (9.68) / 3.53 (9.35) | 50 / 52 |
| register_unsolicited | 2.48 (3.61) | 5.91 (11.72) / 4.87 (10.68) | 46 / 54 |
| set_name | 4.81 (6.90) | 7.47 (15.08) / 7.52 (15.20) | 106 / 114 |
| unknown_command | 4.42 (5.56) | 5.65 (11.47) / 5.69 (11.50) | 53 / 54 |
| unlock_entity | 3.95 (5.40) | 5.61 (11.51) / 6.12 (12.56) | 65 / 66 |

### Notification fan-out

The `aecp-fanout` group registers 16 controllers on every interface, the firmware's capacity, and a controller outside them sends each state-changing command the image notifies.
Every fan-out ends at the last of the 16 (1x1) or 32 (8x8) recipients' commits.
Only the first SET of a value notifies, so the sampling rate (the image has one) and the configuration are measured once, on interface 0.

| Fan-out (H-NOTIFY), to the last of every registration | A: 1x1 ms (bound) | A: 8x8 if0 / if1 | B: 1x1 | B: 8x8 if0 / if1 | CPU cycles a recipient, 1x1 / 8x8 if0 |
|---|---:|---:|---:|---:|---:|
| SET_NAME (ENTITY name) | 11.33 (12.98) **miss** | 20.68 (27.82) **miss** / 22.98 (29.45) **miss** | 11.33 (12.98) **miss** | 20.68 (27.82) **miss** / 22.72 (29.51) **miss** | 20,358 / 20,486 |
| SET_CLOCK_SOURCE (CLOCK_DOMAIN 0) | 8.05 (8.92) | 15.09 (19.86) **miss** / 14.79 (19.93) **miss** | 8.05 (8.92) | 15.09 (19.86) **miss** / 14.79 (19.94) **miss** | 12,355 / 12,352 |
| SET_CONTROL (IDENTIFY on, then off) | 7.79 (8.94) | 14.62 (20.46) **miss** / 15.43 (21.29) **miss** | 7.79 (8.94) | 14.62 (20.46) **miss** / 15.64 (19.02) **miss** | 11,859 / 11,870 |
| REMOVE_AUDIO_MAPPINGS (STREAM_PORT_INPUT 0) | 8.58 (9.79) | - / - | 8.58 (9.79) | - / - | 13,396 / - |
| ADD_AUDIO_MAPPINGS (STREAM_PORT_INPUT 0) | 8.57 (9.78) | - / - | 8.57 (9.78) | - / - | 13,274 / - |
| SET_SAMPLING_RATE (AUDIO_UNIT 0) | 7.97 (8.81) | 15.08 (18.86) **miss** / - | 7.94 (8.78) | 12.58 (19.55) **miss** / - | 12,352 / 12,403 |
| LOCK_ENTITY, acquired | 8.20 (9.35) | 16.07 (21.92) **miss** / 16.39 (22.25) **miss** | 8.23 (9.38) | 13.60 (16.54) **miss** / 13.58 (16.52) **miss** | 13,271 / 13,376 |
| LOCK_ENTITY, released | 8.21 (9.36) | 15.64 (21.49) **miss** / 15.74 (21.59) **miss** | 8.20 (9.35) | 15.68 (19.74) **miss** / 15.66 (21.51) **miss** | 13,307 / 13,335 |
| SET_CONFIGURATION | - | - / - | 9.23 (10.02) | 19.79 (27.04) **miss** / - | 11,874 (B) / 11,786 (B) |
| SET_STREAM_INFO (STREAM_OUTPUT 0, its latency) | - | - / - | 11.68 (12.83) **miss** | 22.56 (28.81) **miss** / 32.78 (52.42) **over ceiling** | 21,875 (B) / 22,030 (B) |
| REMOVE_AUDIO_MAPPINGS (STREAM_PORT_OUTPUT 0) | - | - / - | 8.74 (10.00) | 16.80 (21.65) **miss** / 16.73 (23.34) **miss** | 13,364 (B) / 13,415 (B) |
| ADD_AUDIO_MAPPINGS (STREAM_PORT_OUTPUT 0) | - | - / - | 8.75 (10.00) | 15.08 (22.40) **miss** / 15.02 (22.34) **miss** | 13,271 (B) / 13,376 (B) |
| BIND_RX -> its GET_STREAM_INFO notice | - | - / - | 14.80 (15.95) **miss** | 25.79 (29.12) **over ceiling** / 28.92 (34.78) **over ceiling** | 18,358 (B) / 18,359 (B) |

- In arm A, the fixture's stream observation reports unavailable, so the image refuses SET_CONFIGURATION and SET_STREAM_INFO (ENTITY_MISBEHAVING), and an output map edit, and never sends BIND_RX's GET_STREAM_INFO notice: AECP retries it every millisecond.
  Those paths are arm B's.
- At 8x8 the image's input maps have capacity 0, so only an output map edit can change a map, in arm B.
- SET_NAME's notice carries the 64-byte name, and costs about 20,400 CPU cycles a recipient; the others cost 11,800 to 13,400.

### SRP and MAAP

| SRP and MAAP path | 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses, 1x1 / 8x8 |
|---|---:|---:|---:|
| SRP startup declarations (LINK_UP) | 4.44 (4.97) | 15.79 (18.01) **miss** / 13.25 (33.17) **miss** | 88 / 124 |
| SRP Listener Ready RX (registrar; the fixture grants no licence) | 2.77 (2.77) | 9.11 (12.34) / 8.33 (9.56) | 29 / 36 |
| SRP malformed MRPDU discard | 2.15 (2.15) | 7.70 (11.04) / 5.69 (9.17) | 35 / 36 |
| SRP Domain RX -> declarations (W = JoinTime 200 ms) | 4.93 (7.07) | 14.28 (20.31) / 8.17 (21.00) | 78 / 142 |
| MAAP first PROBE (LINK_UP) | 0.90 (4.97) | 18.49 (38.98) **miss** / 17.04 (39.82) **miss** | 88 / 178 |
| MAAP PROBE retransmission (the worse of two) | 1.86 (3.92) | 3.78 (10.89) / 2.96 (9.41) | 37 / 44 |
| MAAP last PROBE retransmission | 1.24 (4.23) | 3.92 (8.86) / 2.64 (9.41) | 64 / 65 |
| MAAP ANNOUNCE | 1.50 (4.23) | 4.17 (8.86) / 2.90 (9.41) | 64 / 65 |
| MAAP conflicting PROBE -> DEFEND | 0.71 (2.02) | 1.72 (8.05) / 1.97 (8.23) | 47 / 48 |

### Backlog rows

Every backlog group's composed window carries every receive channel's admitted burst at once and fifteen grandmaster changes, alternating the interfaces.
The row's own channel carries the row's records: ACMP 12 in `backlog` and `backlog-owed`, ADP 8, or 11 with the refill leg, which fills the ADP ring's room.
Each row's input is the last of its own channel's records but the owed row's, which has the rest of the ACMP ring's admitted burst behind it.

- ADP: ENTITY_DISCOVERs; ACMP: GET_RX_STATEs to sink 0; AECP: READ_DESCRIPTORs; SRP: a bridge's Listener Ready.
- MAAP: a bridge's PROBE of each interface's announced range, so the range filter passes it and the entity DEFENDs it (IEEE 1722-2016 B.3.6.6).
  The groups wait for MAAP's ANNOUNCE first.

What arrives at once is bounded by each channel's token bucket and ring (`KL_mbx_rx.sv`): the bucket starts full, passes its burst back to back and then refills one record per period, and the ring holds a fixed number of records of each size.

| Channel | Burst | Refill | Ring room, records of the load's frame | Offered at once | Bound? |
|---|---:|---:|---:|---:|---|
| adp | 8 | 1 per 10 ms | 11 (23 words each) | 8 | no: observed at the burst |
| aecp | 16 | 1 per 5 ms | 30 (17 words each) | 16 | no: observed at the burst |
| maap | 8 | 1 per 20 ms | 7 (17 words each) | 7 | yes: the ring is full |
| srp | 32 | 1 per 2 ms | 60 (17 words each) | 32 | no: observed at the burst |
| acmp | 16 | 1 per 5 ms | 12 (20 words each) | 12 | yes: the ring is full |

So the event ring, the ACMP ring and the MAAP ring are at their room: a bound.
The ADP, AECP and SRP rings are offered their burst, which is fewer records than they hold.
Under sustained arrivals the bucket keeps admitting one record per period, so those rings can hold more: their rows are observed at the burst, not bounded by it.
`backlog-adp-refill` measures that for the bound-talker row: the burst, then one more ENTITY_DISCOVER per refill period, up to the ring's room, then the input.

| Backlog row ([`MAILBOX_SPLIT.md:753-758`](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency)) | Desk bound, accesses IF=1 / IF=2 | A: 1x1 ms (bound) [records ahead] | A: 8x8 | B: 1x1 | B: 8x8 |
|---|---:|---:|---:|---:|---:|
| an event behind 15 others | 10,569 / 13,287 | 15.49 (29.11) **miss** [15 ahead] | 44.65 (73.70) **miss** [16 ahead] | 15.49 (29.11) **miss** [15 ahead] | 44.65 (73.70) **miss** [16 ahead] |
| an ACMP command behind a full acmp ring | 38,753 / 48,719 | 63.30 (70.05) **over ceiling** [11 ahead] | 108.71 (120.30) **over ceiling** [11 ahead] | 63.30 (70.05) **over ceiling** [11 ahead] | 108.71 (120.30) **over ceiling** [11 ahead] |
| an ENTITY_AVAILABLE behind the adp ring at its burst (observed) | 77,506 / 97,438 | 67.93 (81.83) **over ceiling** [7 ahead] | 83.51 (107.83) **over ceiling** [7 ahead] | 36.72 (47.10) **over ceiling** [7 ahead] | 55.79 (76.28) **over ceiling** [7 ahead] |
| the same, its bucket refilling up to the ring's room (observed) | - | 88.33 (107.65) **over ceiling** [4 ahead] | 118.81 (156.29) **over ceiling** [6 ahead] | - | - |
| a response with 7 frames owed ahead of it | 31,707 / 39,861 | 126.29 (130.31) **over ceiling** [7 ahead] | 161.10 (170.62) **over ceiling** [7 ahead] | 126.28 (130.30) **over ceiling** [7 ahead] | 161.10 (170.62) **over ceiling** [7 ahead] |
| an ACMP command behind the owed input, the worst of four | - | at least 363.98, **never answered** [8 ahead] | at least 860.00, **never answered** [9 ahead] | at least 363.98, **never answered** [8 ahead] | at least 860.00, **never answered** [9 ahead] |
| the same, from the moment the room returns | - | 66.29 | 101.10 | 66.28 | 101.10 |

The desk bounds charge every pass with every term at once, at a full ring of the smallest records.
"Records ahead" is the backlog in the input's own ring (for the event row, the event ring) when it arrived.
At 8x8 the event ring was full (16 records) when the LINK change occurred, so the event waited for room, which 3.4.1 counts.
The owed-frame row fills the ACMP transmit ring with the egress held, then owes eight more responses while the load arrives: seven commands, the probe and four more behind it.
Its response follows exactly the seven owed responses, 0x7380 to 0x7386 in order, at both points and in both arms.
The four commands behind it are each a path: at 1x1 none is ever answered, in either arm (at least 363.98 ms by the run's end); at 8x8 0x7390 and 0x7392 are answered after 176.52 and 188.27 ms, and 0x7391 and 0x7393 never are (at least 860.00 ms).
On the `backlog` group's interface 0 the event row's LINK_DOWN arrives with the load, so MAAP and SRP on that interface take their records with the link down.

### The load's service

Each loaded channel's first and last record of a composed window, from its commit to the end of the pass that released it, at its worst over the groups [records ahead of it]:

| Record released under the composed load (commit to the end of its releasing pass) | A: 1x1 ms | A: 8x8 if0 / if1 | B: 1x1 | B: 8x8 if0 / if1 |
|---|---:|---:|---:|---:|
| ADP, first record | 18.69 **miss** [0 ahead] | 27.41 **miss** [0 ahead] / - | 14.80 **miss** [0 ahead] | 27.41 **miss** [0 ahead] / - |
| ADP, last record | 101.25 **miss** [4 ahead] | 137.94 **miss** [6 ahead] / 88.96 **miss** [7 ahead] | 51.03 **miss** [7 ahead] | 72.71 **miss** [7 ahead] / 88.96 **miss** [7 ahead] |
| ACMP, first record | 18.70 **miss** [0 ahead] | 27.36 **over ceiling** [0 ahead] / - | 14.76 **miss** [0 ahead] | 27.36 **over ceiling** [0 ahead] / - |
| ACMP, last record | 141.21 **over ceiling** [11 ahead] | 177.90 **over ceiling** [11 ahead] / - | 69.99 **over ceiling** [11 ahead] | 118.96 **over ceiling** [11 ahead] / - |
| AECP, first record | 18.73 **miss** [0 ahead] | 27.40 **over ceiling** [0 ahead] / - | 14.80 **miss** [0 ahead] | 27.40 **over ceiling** [0 ahead] / - |
| AECP, last record | 417.50 **over ceiling** [15 ahead] | - / 510.22 **over ceiling** [15 ahead] | 155.13 **over ceiling** [15 ahead] | - / 224.97 **over ceiling** [15 ahead] |
| MAAP, first record | 18.72 **miss** [0 ahead] | 27.39 **miss** [0 ahead] / - | 14.79 **miss** [0 ahead] | 27.39 **miss** [0 ahead] / - |
| MAAP, last record | 81.55 **over ceiling** [6 ahead] | 103.71 **over ceiling** [6 ahead] / - | 51.01 **over ceiling** [6 ahead] | 88.94 **over ceiling** [6 ahead] / - |
| SRP, first record | at least 628.32, **never released** [0 ahead] | at least 658.79, **never released** [0 ahead] / - | 84.11 **over ceiling** [0 ahead] | 143.91 **over ceiling** [0 ahead] / - |
| SRP, last record | at least 628.30, **never released** [31 ahead] | - / at least 658.77, **never released** [31 ahead] | 186.48 **over ceiling** [31 ahead] | - / 340.85 **over ceiling** [31 ahead] |

SRP's records, per window:

| Arm, group | SRP first record ms | SRP last record ms |
|---|---:|---:|
| A1 backlog | 84.11 | 158.92 |
| A1 backlog-adp | at least 567.97, never released | at least 567.95, never released |
| A1 backlog-adp-refill | at least 628.32, never released | at least 628.30, never released |
| A1 backlog-owed | 65.97 | 182.69 |
| A8 backlog | 131.25 | 278.54 |
| A8 backlog-adp | at least 583.54, never released | at least 583.52, never released |
| A8 backlog-adp-refill | at least 658.79, never released | at least 658.77, never released |
| A8 backlog-owed | 143.91 | 340.85 |
| B1 backlog | 84.11 | 158.91 |
| B1 backlog-adp | 67.68 | 186.48 |
| B1 backlog-owed | 65.96 | 182.68 |
| B8 backlog | 131.25 | 278.54 |
| B8 backlog-adp | 131.11 | 334.69 |
| B8 backlog-owed | 143.91 | 340.85 |

Every window committed exactly its defined load (the run refuses one that did not), and these released it:

| Arm, group | Composed population committed (records; events) | Window, ms | Load released | Longest pass in it, CPU cycles (ms) |
|---|---|---:|---|---:|
| A1 backlog | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15, LINK 1 | 162.91 | yes | 740,260 (14.81) |
| A1 backlog-adp | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 567.99 | no: srp 32 never | 1,565,803 (31.32), a lower bound |
| A1 backlog-adp-refill | adp 11, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 628.34 | no: srp 32 never | 1,531,355 (30.63), a lower bound |
| A1 backlog-owed | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 364.03 | yes | 582,677 (11.65) |
| A8 backlog | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15, LINK 1 | 608.76 | yes | 1,392,016 (27.84) |
| A8 backlog-adp | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 583.56 | no: srp 32 never | 2,208,710 (44.17), a lower bound |
| A8 backlog-adp-refill | adp 11, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 658.81 | no: srp 32 never | 2,209,308 (44.19), a lower bound |
| A8 backlog-owed | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 860.05 | yes | 1,111,766 (22.24) |
| B1 backlog | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15, LINK 1 | 162.91 | yes | 740,260 (14.81) |
| B1 backlog-adp | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 195.37 | yes | 645,058 (12.90) |
| B1 backlog-owed | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 364.03 | yes | 582,392 (11.65) |
| B8 backlog | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15, LINK 1 | 608.76 | yes | 1,392,016 (27.84) |
| B8 backlog-adp | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 555.84 | yes | 1,111,647 (22.23) |
| B8 backlog-owed | adp 8, acmp 12, aecp 16, maap 7, srp 32, GM 15 | 860.05 | yes | 1,111,766 (22.24) |

## Findings

**The rows miss T_svc, so this lane stops** ([owner decision D4](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409738976)).

- Per-pass CPU work, not mailbox accesses, sets the time.
  The 1x1 worst pass makes 365 mailbox accesses, about 3,300 of its 1,565,803 cycles.
  [`MAILBOX_SPLIT.md:753-758`](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency) allows each row 0.10 to 0.94 us an access to fit T_svc.
  The measured access is 0.18 us, inside every allowance but the full-ADP-ring row's; the passes around the accesses are 1.3 to 60 ms.
- The single passes break the [#397 one-hart rule](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5857491046).
  A pass is the loop's only opportunity to take an input, and the smallest deadline every duty shares is T_svc.
  The composed maximum is 14.81 ms at 1x1 and 27.84 ms at 8x8, in both arms; arm A's windows that never finish their load run passes of 31.32 and 44.19 ms, and the 8x8 link-up pass is 40.09 ms.
- An input waits for the pass that is running and then for the pass that takes it.
  So T_svc needs every pass well under 5 ms.
  At 8x8 the idle pass is already 3.1 to 3.7 ms, and LINK_UP, LINK_DOWN, SRP's startup and MAAP's first PROBE miss outright.
- **SRP is starved while the passes are longer than the TICK.**
  `srp_mbx.c:441-451` (`rx_order_ready`) lets SRP take a record only when no tick is owed and no event is pending.
  The mailbox posts a TICK every 10 ms, so a pass longer than 10 ms always leaves one pending, and SRP takes nothing.
  In arm A's `backlog-adp` and `backlog-adp-refill`, after the bind, every pass is over 10 ms: none of SRP's 32 records is released in windows of 568 to 659 ms, at both points.
  Where SRP is served its first record waits 66 to 144 ms and its 32nd up to 341 ms, against MRP's 18 ms ceiling, in both arms.
- **The ACMP core drops the commands it cannot owe.**
  The ring admits 12 GET_RX_STATEs, but the core holds at most `ACMP_OWED_MAX` = 8 responses (tsn-c-stack `acmp.h`; `room()` counts a busy drop).
  With the egress held and eight responses owed, the core takes the commands behind and never answers them.
  At 1x1 none of the four commands behind the owed input is ever answered, in either arm; at 8x8 two of the four are, after 176.52 and 188.27 ms, and two are not. Their controller sees no response, and its 200 ms ACMP timeout (Milan v1.2 Table 5.26) expires.
- **Notification fan-out costs a recipient 11,800 to 20,400 CPU cycles**, so 16 registrations take 7.8 to 11.3 ms at 1x1 and 32 take 12.4 to 23.0 ms at 8x8.
  SET_NAME misses T_svc at both points, every fan-out misses it at 8x8, and at 8x8 BIND_RX's GET_STREAM_INFO notice (25.79 and 28.92 ms) and SET_STREAM_INFO on interface 1 (32.78 ms) are over the 24 ms ceiling (arm B).
- **For D4 (a), a per-pass cap**, the measured consumers are, in order:
  - `memset` and `memcpy`, byte loops on RV32I: each AECP response zeroes its 1,514-byte frame (`aecp.c:58`) and the 1,476-byte payload in it (`aecp_commands.c:555`), and a 1x1 READ_DESCRIPTOR pass spends 153,929 to 156,240 cycles (3.1 ms) in `memset`;
  - lwSRP's link reset and declarations (`mrp_mad`), 474,000 cycles in the 8x8 link-up pass and 430,000 in the 8x8 composed passes;
  - AECP's two modules (mostly their polls), about 47,000 cycles of every 1x1 pass and 94,000 at 8x8;
  - each fan-out's notices, one a recipient in one pass (`aecp.c`, `transmit`), 11,800 to 20,400 cycles each;
  - software multiply and divide, the RV32I core having no M extension.
  A cap that keeps passes under the TICK also ends SRP's starvation.
- **For D4 (b), the admitted backlog** ([Backlog rows](#backlog-rows)):
  - The event ring (16 records), the ACMP ring (12 GET_RX_STATEs) and the MAAP ring (7 MAAPDUs) take their room at once, so those backlogs are bounds.
  - The ADP, AECP and SRP buckets admit 8, 16 and 32 records at once, of the 11, 30 and 60 their rings hold, and then one more every 10, 5 and 2 ms.
    Their backlog under sustained arrivals is not bounded by the burst; the rows measured at the burst are observations.
  - The loop takes at most two records of a channel a pass (`ctrl_loop.c`, `service_rx`): the composed windows release two ADP, ACMP and MAAP records a pass, one AECP record, and two SRP records only in the passes where SRP is ready for them.
    Each record ahead of an input therefore costs up to a whole pass, and the last record of every loaded channel misses T_svc (the load's service).
  - So a smaller ring or bucket removes whole passes from the ring rows, but no row fits T_svc while one pass can exceed it.
    The refill leg shows the other side: its input arrives behind 4 records instead of 7, but during the longest passes, and takes 88.33 ms against 67.93.
  - The ACMP ring's room (12) exceeds the core's owed responses (8): with the egress held, the difference is dropped.
- **The fixture's AECP retries every millisecond.**
  For each pending change notice, `aecp.c:461-495` builds the response and, when the observation port reports unavailable, sets `retry_at = a->now + 1u`.
  The fixture's ports always report unavailable, so after a bind every pass rebuilds the notices: up to 1.57 M cycles, 31 ms, at 1x1.
  Arm B, whose callbacks answer, takes the same H-DISC paths in 0.35 to 0.99 ms at 1x1, its bound-talker row in 36.72 ms against arm A's 67.93, and serves SRP in every window.
  The retry has no backoff, so a real port that reports unavailable would do the same.

**D5, the smaller core** (deferred until after the flip): the shipping core already misses at both points, so a slower core would miss by more until S2b's per-pass cap lands.

**D3, the hybrid XIP split:**

- A fetch from block RAM costs 9.1 CPU cycles.
  A read through the flash window costs 138 to 303, 263 on average: about 15 to 29 times a block RAM fetch, on the 1x SPI the product configures.
  The low end is a burst continuation, the nearest to straight-line fetch from flash.
- The core is fetch-bound, so code executing from flash would run roughly that much slower: no path inside T_svc can be fetched from flash.
- The image fetches 11,160 B of code before the mailbox opens (11,396 B at 8x8) and at least 42,080 B after it (43,060 B at 8x8), of 85,912 and 87,596 B of `.text`.
  The service figure is the largest single run, so it is a lower bound for the hot set S14 must keep in block RAM.

**Defects the measurement found**, each for its own issue:

1. **The split image cannot run on the CPU the split SoC builds** ([#791](https://github.com/kebag-logic/milan-fpga/issues/791)).
   The generator decodes a region whose size is not a power of two wrongly.
   For the 224 KiB `rom` at 0 its fetch and load checks are `(address & 0xfffc8000) == 0`, which excludes every address with bit 15 set.
   The image's first call above 0x8000 (`jal aecp_image_load`, 0x6880 to 0xb1ec) takes an instruction access fault, cause 1, traps to 0 and restarts, forever.
2. **The linked image addresses placeholders**, not the split SoC (the address table above).
   S3's target firmware owns the real addresses.
3. **#723 is open**: the runtime recipe builds without `-fno-stack-protector` and the image does not link.
   [`runtime_ssp.py`](runtime_ssp.py) runs it unchanged with that one flag.

## Controls and self-test

`run.py --self-test` regrades the committed trace [`fixture.log`](fixture.log), which the `fixture` group recorded at 1x1, against [`oracle.json`](oracle.json).
The fixture has a short composed window: one record on every receive channel and two GM events.
Its checks:

- the fixture's digest, each of its seven rows with its pass bound and the records ahead, each loaded channel's first and last record served in its window, its worst pass and its composed maximum with the window's population and its release;
- a planted over-budget path (the recorded BIND_RX response moved past T_svc) must miss; the window with its MAAP record's commit deleted, and with that record also left out of its declaration, must be refused by name, and so must the window against a defined load one record smaller; with SRP's release deleted, SRP must be reported never released and the window no composed maximum;
- every clock conversion; the ceilings and T_svc, restated in [`selftest.py`](selftest.py) so a changed table fails;
- an exact-budget path passes and one bus cycle more misses; W + T_svc passes, one cycle more misses within W plus the ceiling, and past that it is over the ceiling;
- the probe's own tagged frame starts it; a commit after a refused frame is the next frame's; a commit that follows no frame is refused;
- a response to another sequence_id, or on the other interface, does not end it; the last required output ends it; the expected response is checked;
- a timer path starts at its armed deadline; a test-only entry at its own function's entry; the pass bound runs from the running pass at the bus ratio;
- a notification over two recipients ends at the last; a late recipient misses; a missing one, a duplicate standing in for another, and a controller outside the set are refused; unrelated unsolicited responses do not end it;
- the composed maximum is a window's longest pass even when that pass is neither its first nor its last, and the worst pass includes the run's last pass; the pass the script's end cuts is no idle pass;
- the responses owed ahead are exactly the owed ones, in order; a command that may be dropped and is never answered is reported, unbounded, and one that may not is refused;
- the defined loads, restated; every composed window of the real scenario, at one and two interfaces, sends and declares exactly its defined load; the owed row has its seven owed and its four behind;
- the real fan-out group registers the firmware's capacity (read from `aecp.h`) on every interface, every registration is each fan-out's recipient, and no requester is registered;
- a control probe is an instance of its functional path; repeated instances count as one path, at their worst, with every miss;
- the records ahead of an input; each path's worst instance, a starved one first, and the misses per path and per instance;
- the run's exit status for a miss, a refusal and an empty run; a regrade's refusal of an absent log, an absent script and a stale script; a trap's refusal;
- reuse refuses a changed image, ROM file, SoC Verilog, CPU netlist and firmware source, a deleted or unrecorded ROM file, a changed native model and an unresolved key, and reuses an unchanged build.

Then [`selftest_mutants.py`](selftest_mutants.py) replaces each rule in turn, and a named check must fail:

| Mutant | Caught by |
|---|---|
| marker: the frame tag is ignored | tagged start |
| marker: a timer path starts when its record is posted | fixture row fixture.tmr_no_resp1.if0 |
| marker: a timer path starts one millisecond after its deadline | fixture row fixture.tmr_no_resp1.if0 |
| marker: an entry start takes any function entry | an entry start is its own function's |
| marker: any response on the channel ends the path | sequence and interface |
| marker: the interface is ignored | sequence and interface |
| marker: the first required output ends the path | fixture row fixture.set_name.if0 |
| marker: a receive commit goes to the oldest pending frame (earlier rule) | a receive commit belongs to the frame it follows |
| marker: the expected-response check is skipped | the expected response is checked |
| notify: the first recipient's commit ends the fan-out | two recipients across interfaces end at the last |
| notify: the first unsolicited response on any interface ends it (earlier rule) | two recipients across interfaces end at the last |
| notify: any unsolicited response counts as the change | unrelated unsolicited responses do not end it |
| notify: a missing recipient is not refused | a missing recipient is refused |
| notify: a recipient outside the set is not refused | a notification to a controller outside the set is refused |
| clock ratio: CPU cycles equal bus cycles | fixture row fixture.link_up.if0 |
| clock ratio: inverted | fixture row fixture.link_up.if0 |
| clock ratio: CPU cycles rounded down | fixture row fixture.malformed.if0 |
| clock ratio: milliseconds from the CPU clock | fixture row fixture.link_up.if0 |
| clock ratio: a pass's milliseconds from the bus clock | fixture passes: worst pass and composed maximum |
| clock ratio: a pass's bus cycles equal its CPU cycles | fixture row fixture.link_up.if0 |
| pass bound: it starts at the input, not at the running pass | fixture row fixture.malformed.if0 |
| composition: the window's population is not checked | a composed load missing one channel is refused |
| composition: the composed maximum is the run's worst pass | fixture passes: worst pass and composed maximum |
| composition: the composed maximum is the window's first pass | fixture passes: worst pass and composed maximum |
| worst pass: the run's last pass is dropped | the pass bound runs from the running pass at the bus ratio |
| passes: the pass the script's end cuts counts as idle (earlier rule) | the pass the script's end cuts is no idle pass |
| composition: a window that committed more than its load is accepted | a composed window that committed more than its load is refused |
| composition: the load is the stimulus's own declaration (earlier rule) | a window short of its defined load is refused although it declares it |
| composition: the backlog stimulus omits SRP | every composed window's stimulus is its defined load |
| composition: the backlog stimulus omits MAAP | every composed window's stimulus is its defined load |
| composition: the owed row omits the ACMP commands behind its input (earlier rule) | every composed window's stimulus is its defined load |
| service: a record never released is omitted | a starved channel is reported by name, and its window is no composed maximum |
| service: a window that left its load unreleased is the composed maximum (earlier rule) | a starved channel is reported by name, and its window is no composed maximum |
| service: a record's service ends at its release, not at its pass's end | fixture row fixture.service.adp.first.if0 |
| owed: the responses ahead are not checked | the responses owed ahead are checked: ['31'] |
| owed: a command never answered fits | a command never answered is reported, unbounded, where it may be dropped |
| notify: the fan-out registers one controller an interface (earlier rule) | the fan-out group registers the firmware's capacity, every registration a recipient |
| deadline: T_svc 20 ms | fixture row fixture.service.srp.first.if0 |
| deadline: strictly below the budget | exact budget passes |
| deadline: the normative wait is not added | W + T_svc passes |
| deadline: the ceiling drops the normative wait | W + T_svc passes |
| deadline: the ACMP ceiling is the transaction timeout | ceilings pinned |
| run: a CPU trap is not refused | a CPU trap is refused |
| run: a T_svc miss never fails the run | a T_svc miss fails the run unless recorded |
| run: a refusal does not fail the run | a refusal fails the run, recorded or not |
| regrade: a selected group without its log is dropped (earlier rule) | a regrade refuses each absent log or script, and a stale script, by name |
| reuse: an input outside the checkout is not rechecked (earlier rule) | reuse refuses the image |
| reuse: the ROM files are not attested | reuse refuses a ROM file |
| tables: a path's first instance is reported, not its worst (earlier rule) | each path reports its worst instance |
| tables: misses are counted per probe instance only (earlier rule) | misses are counted per path and per probe instance |
| tables: a control instance is its own path (earlier rule) | a control instance is its functional path |
| tables: a starved instance is not its path's worst | a starved instance is its path's worst |

A mutant whose name ends in "(earlier rule)" restores a rule this harness had before these checks, so its check is the test that fails on that rule.

Regenerate the fixture only through its generator, from a fresh 1x1 run of the `fixture` group:

```sh
python3 -B tb/verilator/ctrl_service_budget/selftest.py --write-fixture RESULTS/fixture.log BUILD/build.json
```

Three controls run the full harness:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-slow-adp --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-slow-shutdown --variant shutdown-entry --mutation slow-adp-shutdown
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-as-built --cpu-regions as-built
```

`slow-adp-rx` builds a scratch copy of the firmware whose ADP receive handler spins first.
The `control` group's RCV_ADP_DISCOVER must miss T_svc: it measures 24.614 ms, and the run prints `CONTROL slow-adp-rx caught`.
The ordinary image measures the same path at 0.294 ms.
`slow-adp-shutdown` makes disabling ADP spin before its ENTITY_DEPARTINGs, in the `shutdown-entry` arm.
The `control-shutdown` group's SHUTDOWN, an instance of the same path, must miss T_svc: it measures 24.903 ms against 0.582 ms unplanted, and the run prints `CONTROL slow-adp-shutdown caught`.
`as-built` hands the generator the SoC's regions unchanged.
The run must refuse the boot with an instruction access fault, cause 1, and prints `CONTROL as-built caught`.

## Limits

- One phase is measured per probe; the pass bound covers any phase under the same passes, not other loads.
- The ADP, AECP and SRP backlog rows are observed at their bucket's burst; the refill leg is one sample of sustained arrivals, not a bound.
- A composed window closes three quiet passes, or 500 ms, after its row's input is served; a record still unreleased then is reported with the time it had waited by the run's end, a lower bound of a wait the measurement does not see end.
- A record's service ends at the end of the pass that released it; lwSRP may keep a record for replay (`pending_rx`) and finish it in a later pass.
- SHUTDOWN is measured through a test-only entry, because the linked image never disables ADP.
- START_STREAMING calls a port the fixture leaves empty, so it is not run.
- The lock expiry's notice (60 s after a LOCK_ENTITY) and the counter pushes are not run: the first is beyond the simulation's length, and the fixture changes no counter.
- The fixture's sources are never allocated, so a Listener Ready grants no licence; that path ends at the record's release.
- Ends are mailbox commits; wire departure, ingress, egress and the network (H-ACMP's round trip) are not measured.
- The flash's erase and program waits are zero, so F1's commit is measured as CPU work only; S4 owns the target port.
- There is no datapath, no DDR3 and no packet traffic besides the stimulus; the CPU's DMA port is idle.
- The firmware polls (`CTRL_MBX_WFI` undefined), as the fixture is linked.
- The two-interface fixture gives both interfaces the same MAC, as `ctrl_aecp_image.c` does.

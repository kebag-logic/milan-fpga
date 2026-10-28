# Split CPU service budget

This harness measures the Mark II split firmware's service paths on the split placement's core.
That is the shipping VexiiRiscv with the split CPU's instruction cache ([#665 S2c](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6421463860)), or without it (`--fetch-l1 none`), the cacheless core S2 measured.
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
- **[The instruction cache](#the-instruction-cache)** -- The split CPU's fetch L1: the size sweep at both points, the hybrid-XIP arm, its block RAM and logic, and the T_svc gap it leaves.
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
`--fetch-l1` selects the CPU's instruction cache: `split`, the split placement's own (the default); `none`, the cacheless core; or `SETSxWAYS`, a test-only sweep point of 64-byte lines.
So the two commands above give the split cache's arms in [The instruction cache](#the-instruction-cache).
S2's figures in [Results](#results) are the cacheless core's, and their commands add `--fetch-l1 none`.

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
  It runs three of the four backlog rows, `backlog`, `backlog-adp` and `backlog-owed`, without `backlog-adp-refill`, so its composed maximum is partial.
- `shutdown-entry` adds the SHUTDOWN path's only input: a poll that calls `adp_mbx_set_enable(false)` once, at NOW_MS 2,500.
  It runs the `adp-shutdown` and `control-shutdown` groups only.

As written, both arms build the split's cache, the arms B and S of [The instruction cache](#the-instruction-cache).
With `--fetch-l1 none` they are S2's arms in [Results](#results).

`--xip` is the labelled hybrid-XIP arm (D3, lane S14): the image's own objects, relinked so that every function past the reset entry executes from the flash window behind the instruction cache.
`rom` keeps the reset entry, F1's flash driver (`nvm_flash_litespi.c`), `.rodata` and the initial values of `.data`.
The driver stays in block RAM, as D3 requires: a CPU fetching from the flash cannot also hold the flash's command master.
The code sits at the first erase block past the product's AEM slot, and the flash device's image is preloaded with it:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-1x1-xip --xip --record-budget-findings
```

The directory has no Makefile on purpose.
The serial sweep discovers every Makefile, and `scripts/suite_shards.py` must then register the suite.
That is a CI change, outside this lane.

## The test SoC

[`split_soc.py`](split_soc.py) builds it; [`build.py`](build.py) links the image and compiles the model.

- **The CPU** is MilanSoC's own VexiiRiscv path: RV32I, one hart, the CPU at the 50 MHz Milan clock, the bus at 100 MHz.
  It has the split placement's instruction cache (`milan_soc.ctrl_cpu_args`), or the `--fetch-l1` selection; its data side is cacheless.
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
Instruction fetches are counted at the CPU's fetch bus, by region.
Without the cache a fetch is one word; with it, one 64-byte line refill, whose wait runs to its last beat.
With the split CPU's data cache, loads and stores are counted at its IO bus, which carries every uncached access and so every mailbox access; cached accesses and refills never reach it and are not counted.

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
A served record's records ahead are its channel's earlier records not yet released at its commit.
A window that left records unreleased names them, and its passes ran without that work, so its longest pass is a lower bound of a load the firmware did not finish.
The composed maximum is the longest pass over every backlog row's window, each of which committed its defined load (`run.composed_maximum`).
While any of those windows left its load unreleased, the composed maximum is a lower bound.
A run that did not include every backlog row names the rows not run, and its figure is labelled partial: the longest pass of the windows it ran, not the composed maximum.
The longest pass of the windows that released their whole load is reported beside it, labelled as such: it leaves out the windows the firmware never finished, so it is not the composed maximum.

The ceilings are 3.4.1's: ADP 200 ms, a discovery input's ACMP action and ACMP 20 ms, AECP 24 ms, a notification 24 ms, MAAP 50 ms, MRP 18 ms.
A path with a normative wait W, such as SRP's JoinTime, is bounded by W + T_svc, and its ceiling by W plus the ceiling.

## Results

These are S2's results, on the cacheless core:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-1x1-none --fetch-l1 none --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 \
  --build-dir /tmp/budget-8x8-none --fetch-l1 none --record-budget-findings
```

Arms B and S add `--fetch-l1 none` to their commands in [Run and reproduce](#run-and-reproduce) in the same way.
[The instruction cache](#the-instruction-cache) gives the same groups on the split CPU's cache.
Arm A is the image as linked, the formal measurement.
Arm B is the labelled second arm, whose fixture callbacks answer.
The SHUTDOWN row comes from the labelled `shutdown-entry` arm.
In the path tables a cell is a path's worst measured instance across the groups that measure it, "ms (the pass bound)"; **miss** is over T_svc, **over ceiling** over the 3.4.1 ceiling as well.
A record never released or a command never answered is worse than any time measured, and its cell gives the time it had waited, at least.
Each run writes every path's worst instance, every probe, every composed window, the composed maximum (labelled partial where the run left out a backlog row) and every timed-out wait to its `table.md`, and all of it to `results.json`.

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

| Point, arm | Idle pass, CPU cycles (ms) | Worst pass, CPU cycles (ms), group | Composed maximum, every backlog window, CPU cycles (ms), group | Over the windows that released their whole load only |
|---|---:|---:|---:|---:|
| 1x1, A | 65,703 to 72,632 (1.31 to 1.45) | 1,565,803 (31.32), backlog-adp | at least 1,565,803 (31.32), backlog-adp, a lower bound | 740,260 (14.81), backlog |
| 1x1, B | 65,703 to 232,901 (1.31 to 4.66) | 740,260 (14.81), backlog | partial, 3 of 4 windows (`backlog-adp-refill` not run): 740,260 (14.81), backlog | 740,260 (14.81), backlog |
| 8x8, A | 157,133 to 185,315 (3.14 to 3.71) | 2,989,496 (59.79), acmp-notk | at least 2,209,308 (44.19), backlog-adp-refill, a lower bound | 1,392,016 (27.84), backlog |
| 8x8, B | 157,133 to 293,468 (3.14 to 5.87) | 2,004,666 (40.09), acmp-notk | partial, 3 of 4 windows (`backlog-adp-refill` not run): 1,392,016 (27.84), backlog | 1,392,016 (27.84), backlog |

The composed maximum is the longest pass over every backlog window, each of which committed its row's defined load.
In arm A, the formal measurement, the two bound-talker windows never release SRP's 32 records (see [the load's service](#the-loads-service)), so their passes ran without SRP's work and the composed maximum is a lower bound: at least 31.32 ms at 1x1 and at least 44.19 ms at 8x8.
The last column leaves those windows out; it is labelled, and it is not the composed maximum.
Arm B runs three of the four backlog rows, `backlog`, `backlog-adp` and `backlog-owed`, without `backlog-adp-refill`.
So its figure is partial, over 3 of 4 backlog windows, and is not the composed maximum; each of those three windows released its load, so its two figures are the same.
An idle pass's largest consumers are AECP's two modules, `aecp` 26,497 and `aecp_nvm` 20,254 cycles at 1x1, 73,883 and 20,254 at 8x8, mostly their polls.
The idle range excludes the pass the script's end cuts short; at 8x8 it is 3.14 to 3.71 ms (157,133 to 185,315 cycles) in arm A.
The 8x8 link-up pass, 2,004,666 cycles, is lwSRP's `mrp_mad` 473,950, `memset` 361,053, `memcpy` 244,102, the mailbox driver 119,790 and software multiply and divide (`__mulsi3` 111,201, `__udivsi3` 89,954).
In arm B's three backlog windows, and over arm A's windows that released their load, the longest pass at both points is the `backlog` group's: at 1x1, 740,260 cycles of `memset` 278,637, the mailbox driver 141,995, `memcpy` 66,719, AECP 41,029 and ACMP 36,377; at 8x8, 1,392,016 cycles of `memset` 477,042, the mailbox driver 134,267, `memcpy` 132,197, AECP 111,084, ACMP 89,857 and `__mulsi3` 67,272.
Arm A's 1x1 composed maximum and worst pass, `backlog-adp`'s 1,565,803 cycles, is `memset` 984,728, AECP 173,531, the mailbox driver 127,547, ACMP 49,350 and `memcpy` 46,964: after the bind, AECP's retry (see [Findings](#findings)).
Arm A's 8x8 composed maximum, `backlog-adp-refill`'s 2,209,308 cycles, is `memset` 827,831, lwSRP's `mrp_mad` 429,626, AECP 350,539, the mailbox driver 150,636 and `memcpy` 140,364.

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
- Over every fan-out measured, on every interface, a recipient costs 11,786 to 22,030 CPU cycles (11,818 to 20,486 in arm A).
  SET_NAME's notice carries the 64-byte name and costs 20,358 to 20,486; in arm B SET_STREAM_INFO's costs 21,875 to 22,030 and BIND_RX's GET_STREAM_INFO notice 18,358 to 18,475; every other fan-out costs 11,786 to 13,440 (11,818 to 13,440 in arm A).
- The 16 recipients at 1x1 take 7.77 to 14.80 ms (7.77 to 11.33 in arm A), and the 32 at 8x8 take 12.39 to 32.78 ms (12.39 to 22.98 in arm A).
  A SET_CONTROL cell is the worse of its two fan-outs, identify on and identify off; the better ones, 7.77 ms at 1x1 and 12.39 ms on 8x8 interface 0, set the low ends.

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
| the owed response, from the moment the room returns | - | 66.29 | 101.10 | 66.28 | 101.10 |

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
  In arm A, the formal measurement, the composed maximum is at least 31.32 ms at 1x1 and at least 44.19 ms at 8x8: a lower bound, because those passes ran in windows whose SRP load is never released.
  Arm B runs three of the four backlog rows, `backlog`, `backlog-adp` and `backlog-owed`, without `backlog-adp-refill`, and each released its load.
  Over those three windows its longest pass is 14.81 and 27.84 ms, the same as over arm A's released windows only: a partial figure, not the composed maximum.
  Its 8x8 link-up pass is 40.09 ms.
- **The baseline for S2b and S2c** is arm A's composed maximum over every backlog window: at least 1,565,803 cycles (31.32 ms) at 1x1 and at least 2,209,308 (44.19 ms) at 8x8, compared window by window in [the load's service](#the-loads-service).
  The figure over the released windows only is no baseline: a change that lets SRP be served in `backlog-adp` adds that window to it, so its before and after would cover different windows.
  Nor is a partial figure: a re-measure that leaves out a backlog row names it, and its figure covers fewer windows than the baseline.
  The [later owner decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6421463860) puts the instruction cache (S2c) before firmware-only tuning (S2b).
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
- **Notification fan-out costs a recipient 11,786 to 22,030 CPU cycles** (11,818 to 20,486 in arm A), so 16 registrations take 7.77 to 14.80 ms at 1x1 (7.77 to 11.33 in arm A) and 32 take 12.39 to 32.78 ms at 8x8 (12.39 to 22.98 in arm A).
  SET_NAME misses T_svc at both points, and at 1x1 so do arm B's SET_STREAM_INFO (11.68 ms) and BIND_RX's GET_STREAM_INFO notice (14.80 ms).
  Every fan-out misses it at 8x8, and there BIND_RX's GET_STREAM_INFO notice (25.79 and 28.92 ms) and SET_STREAM_INFO on interface 1 (32.78 ms) are over the 24 ms ceiling (arm B).
- **For D4 (a), a per-pass cap**, the measured consumers are, in order:
  - `memset` and `memcpy`, byte loops on RV32I: each AECP response zeroes its 1,514-byte frame (`aecp.c:58`) and the 1,476-byte payload in it (`aecp_commands.c:555`), and a 1x1 READ_DESCRIPTOR pass spends 153,929 to 156,240 cycles (3.1 ms) in `memset`;
  - lwSRP's link reset and declarations (`mrp_mad`), 474,000 cycles in the 8x8 link-up pass and 430,000 in the 8x8 composed passes;
  - AECP's two modules (mostly their polls), about 47,000 cycles of every 1x1 pass and 94,000 at 8x8;
  - each fan-out's notices, one a recipient in one pass (`aecp.c`, `transmit`), 11,786 to 22,030 cycles each (11,818 to 20,486 in arm A);
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

## The instruction cache

The [S2c assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6421463860) gives the split CPU an L1 instruction cache, VexiiRiscv's fetch L1, through the pinned generator's own options (`milan_soc.ctrl_cpu_args`).
The split CPU's cache is 4 KiB, direct-mapped, of 64-byte lines; its data side stays cacheless.
[Split placement control memory](../../../docs/design/SPLIT_CONTROL_MEMORY.md#7-the-cpus-instruction-cache) states the parameters and why, and debits the block RAM.
This section runs the same groups as [Results](#results) on the cached CPU, at the split's size and at the sweep's other sizes, at both points, graded as Results are.
Every run's `table.md` lists every path's worst instance and every probe, in CPU cycles and ms.

### The sweep

| Instruction cache | Tiles, out of context (difference) | 1x1: composed maximum, every backlog window, ms | 1x1: over the windows that released their whole load only, ms | 1x1: paths (instances) missing T_svc | 8x8: composed maximum, every backlog window, ms | 8x8: over the windows that released their whole load only, ms | 8x8: paths (instances) missing T_svc |
|---|---:|---:|---:|---:|---:|---:|---:|
| none (S2) | 4.5 (+0) | at least 31.32 | 14.81 | 22 of 81 (58 of 141) | at least 44.19 | 27.84 | 60 of 129 (102 of 182) |
| 2 KiB, 1 way | 5.5 (+1) | at least 18.82 | 8.99 | 16 of 81 (41 of 141) | at least 29.73 | 14.58 | 37 of 129 (65 of 182) |
| 4 KiB, 1 way (split) | 6 (+1.5) | at least 19.32 | 8.60 | 13 of 81 (34 of 141) | at least 29.12 | 14.03 | 34 of 129 (66 of 182) |
| 8 KiB, 1 way | 7 (+2.5) | at least 18.96 | 8.40 | 13 of 81 (34 of 141) | at least 28.79 | 13.76 | 31 of 129 (59 of 182) |
| 8 KiB, 2 ways | 7.5 (+3) | at least 18.01 | 8.19 | 12 of 81 (33 of 141) | at least 28.35 | 13.63 | 29 of 129 (61 of 182) |
| 16 KiB, 1 way | 9 (+4.5) | at least 17.98 | 8.17 | 12 of 81 (33 of 141) | at least 28.17 | 13.53 | 29 of 129 (61 of 182) |

The tiles are Vivado's out-of-context mapping of each netlist the harness ran, the cacheless one included; [block RAM and logic](#block-ram-and-logic) has the full figures.
The composed maximum is taken as [Passes](#passes) takes it, over every backlog window.
At every size, as without the cache, the two bound-talker windows, `backlog-adp` and `backlog-adp-refill`, never release SRP's 32 records, so the composed maximum is a lower bound.
It falls from at least 31.32 to at least 19.32 ms at 1x1, and from at least 44.19 to at least 29.12 ms at 8x8.
Those lower bounds come from loads the firmware never finished, and they do not rank the sizes: at 1x1, 2 KiB's 18.82 ms is below 4 KiB's 19.32.
The windows that released their whole load are the same two at every size and without the cache, `backlog` and `backlog-owed`, so their longest pass compares like with like.
That figure is labelled, and it is not the composed maximum.
On it, the first 4 KiB takes most of the gain: from 14.81 to 8.60 ms at 1x1 (42 %) and from 27.84 to 14.03 ms at 8x8 (50 %).
2 KiB is 4 to 5 % slower than 4 KiB and leaves three more paths missing T_svc at each point, for half a tile less.
8 and 16 KiB, with one way or two, are 2 to 5 % faster than 4 KiB for one to three tiles more.
So the split takes 4 KiB with one way.

[Findings](#findings) compares S2's baseline window by window, so here is arm A's longest pass in each backlog window, in ms:

| Backlog window, arm A | 1x1, none | 1x1, 4 KiB | 8x8, none | 8x8, 4 KiB |
|---|---:|---:|---:|---:|
| `backlog` | 14.81 | 8.60 | 27.84 | 14.03 |
| `backlog-adp` | at least 31.32, SRP unreleased | at least 18.98, SRP unreleased | at least 44.17, SRP unreleased | at least 29.12, SRP unreleased |
| `backlog-adp-refill` | at least 30.63, SRP unreleased | at least 19.32, SRP unreleased | at least 44.19, SRP unreleased | at least 29.12, SRP unreleased |
| `backlog-owed` | 11.65 | 7.48 | 22.24 | 12.46 |

The cache shortens the released windows' longest passes by 36 to 50 %, and the measured passes of the unreleased windows by 34 to 39 %.
It releases no window that the cacheless core left unreleased.

Every arm on the split's cache, against S2's cacheless figures above:

| Arm, with the 4 KiB cache | Groups | Paths missing T_svc | Probe instances missing T_svc | Without the cache (S2), paths / instances |
|---|---:|---:|---:|---:|
| A1 | 18 | 13 of 81 | 34 of 141 | 22 of 81 / 58 of 141 |
| A8 | 17 | 34 of 129 | 66 of 182 | 60 of 129 / 102 of 182 |
| B1 | 8 | 10 of 44 | 25 of 68 | 18 of 44 / 41 of 68 |
| B8 | 8 | 26 of 68 | 44 of 92 | 36 of 68 / 60 of 92 |
| S1 | 2 | 0 of 1 | 0 of 2 | 0 of 1 / 0 of 2 |
| S8 | 2 | 0 of 2 | 0 of 3 | 0 of 2 / 0 of 3 |

Arm B runs three of the four backlog rows, as S2's arm B does, without `backlog-adp-refill`.
So its figure is partial, over 3 of 4 backlog windows, and is not the composed maximum: 8.61 ms at 1x1 and 14.07 ms at 8x8 with the cache, against S2's 14.81 and 27.84 ms.

### What the cache changes

| Point, instruction cache | CPU cycles per instruction | Fetch commands per 1,000 instructions | Mean fetch wait, CPU cycles | Fetch waits / cycles | Data waits / cycles |
|---|---:|---:|---:|---:|---:|
| 1x1, none | 9.52 | 1687.6 | 9.1 | 1.611 | 0.226 |
| 1x1, 4 KiB | 5.83 | 15.5 | 42.3 | 0.112 | 0.390 |
| 1x1, 8 KiB | 5.68 | 10.8 | 42.3 | 0.081 | 0.394 |
| 8x8, none | 9.49 | 1676.7 | 9.1 | 1.614 | 0.233 |
| 8x8, 4 KiB | 5.65 | 10.1 | 42.2 | 0.075 | 0.403 |
| 8x8, 8 KiB | 5.58 | 8.1 | 42.2 | 0.061 | 0.405 |

Without the cache every instruction word is a bus transaction of about 9 CPU cycles, and those waits add up to 1.6 times the run's cycles: more than one fetch is outstanding at a time.
With 4 KiB a fetch command is a 64-byte line refill of 42 cycles, 10 to 16 of them every 1,000 instructions, and refill waits fall to 7 to 11 % of the cycles.
The CPU then waits on its data side: a load or store to `sram`, the mailbox or a CSR stays 9 to 10 cycles, and those waits are 39 to 40 % of the cycles.
The composed maximum is `backlog-adp-refill`'s at both points, after the bind and so under AECP's change-notice retry (see [Findings](#findings)).
At 1x1 it is also the worst pass: at least 966,218 cycles, of `memset` 609,416 (63 %), AECP 141,656 and the mailbox driver 71,268.
At 8x8 it is at least 1,455,957 cycles, of `memset` 541,525 (37 %), AECP 305,284 and lwSRP's `mrp_mad` 254,640.
Over the windows that released their load, the longest pass is `backlog`'s, 429,838 cycles at 1x1 and 701,553 at 8x8.
Its largest consumer is still `memset`, a byte loop on RV32I: 31 % at both points (133,859 and 219,287 cycles).
The mailbox driver takes 21 % and 12 % of it, and `memcpy` 9 % and 11 %.
The 8x8 worst pass, `acmp-cmd`'s 1,894,336 cycles, is 49 % `memset`, again under the retry.

### Backlog rows and notification fan-out

| Backlog row | A 1x1, none | A 1x1, 4 KiB | A 8x8, none | A 8x8, 4 KiB | B 1x1, 4 KiB | B 8x8, 4 KiB |
|---|---:|---:|---:|---:|---:|---:|
| an event behind 15 others | 15.49 (29.11) **miss** | 8.99 (16.94) | 44.65 (73.70) **miss** | 14.45 (28.05) **miss** | 9.02 (16.97) | 14.49 (28.12) **miss** |
| an ACMP command behind a full acmp ring | 63.30 (70.05) **over ceiling** | 36.41 (40.22) **over ceiling** | 108.71 (120.30) **over ceiling** | 57.96 (63.77) **over ceiling** | 36.41 (40.22) **over ceiling** | 58.13 (63.97) **over ceiling** |
| an ENTITY_AVAILABLE behind the adp ring at its burst (observed) | 67.93 (81.83) **over ceiling** | 37.07 (50.09) **over ceiling** | 83.51 (107.83) **over ceiling** | 46.43 (66.02) **over ceiling** | 22.21 (29.60) **over ceiling** | 33.61 (43.29) **over ceiling** |
| the same, its bucket refilling up to the ring's room (observed) | 88.33 (107.65) **over ceiling** | 34.33 (55.30) **over ceiling** | 118.81 (156.29) **over ceiling** | 52.00 (65.59) **over ceiling** | - | - |
| a response with 7 frames owed ahead of it | 126.29 (130.31) **over ceiling** | 93.51 (95.48) **over ceiling** | 161.10 (170.62) **over ceiling** | 122.32 (128.00) **over ceiling** | 94.03 (96.47) **over ceiling** | 118.52 (124.19) **over ceiling** |

The cache shortens every backlog row by a quarter to two thirds, but only the 1x1 event row then fits T_svc.
The ring and owed rows still span several passes of 14 to 21 ms each.
Arm B, without the retry passes, gives the same event, ACMP-ring and owed rows within 3 %, and an ADP-ring row of 22.21 ms at 1x1 and 33.61 ms at 8x8.

| Fan-out at registration capacity, arm A | Interface | 1x1, none | 1x1, 4 KiB | 8x8, none | 8x8, 4 KiB |
|---|---:|---:|---:|---:|---:|
| `add_audio_mappings` | 0 | 8.57 (9.78) | 4.91 (5.71) | - | - |
| `lock_entity` | 0 | 8.20 (9.35) | 4.66 (5.43) | 16.07 (21.92) **miss** | 8.38 (10.02) |
| `lock_entity` | 1 | - | - | 16.39 (22.25) **miss** | 10.01 (13.67) **miss** |
| `remove_audio_mappings` | 0 | 8.58 (9.79) | 4.93 (5.72) | - | - |
| `set_clock_source` | 0 | 8.05 (8.92) | 4.61 (5.22) | 15.09 (19.86) **miss** | 9.07 (12.56) |
| `set_clock_source` | 1 | - | - | 14.79 (19.93) **miss** | 8.25 (9.73) |
| `set_control` | 0 | 7.79 (8.94) | 4.45 (5.22) | 14.62 (20.46) **miss** | 9.64 (13.29) |
| `set_control` | 1 | - | - | 15.43 (21.29) **miss** | 9.64 (13.29) |
| `set_name` | 0 | 11.33 (12.98) **miss** | 6.45 (7.47) | 20.68 (27.82) **miss** | 12.81 (17.15) **miss** |
| `set_name` | 1 | - | - | 22.98 (29.45) **miss** | 13.56 (17.73) **miss** |
| `set_sampling_rate` | 0 | 7.97 (8.81) | 4.57 (5.15) | 15.08 (18.86) **miss** | 8.51 (9.97) |
| `unlock_entity` | 0 | 8.21 (9.36) | 4.67 (5.44) | 15.64 (21.49) **miss** | 10.02 (13.67) **miss** |
| `unlock_entity` | 1 | - | - | 15.74 (21.59) **miss** | 10.03 (13.68) **miss** |

A SET_CONTROL cell is the worse of its two fan-outs, identify on and identify off.
With the 4 KiB cache, over every fan-out measured, on every interface and in both arms:

- A recipient costs 7,054 to 15,334 CPU cycles (7,144 to 13,114 in arm A), against S2's 11,786 to 22,030 (11,818 to 20,486).
  SET_NAME's notice costs 11,796 to 14,488; in arm B SET_STREAM_INFO's costs 12,635 to 15,334 and BIND_RX's GET_STREAM_INFO notice 10,686 to 13,374; every other fan-out costs 7,054 to 10,571.
- The 16 recipients at 1x1 take 4.42 to 8.70 ms (4.43 to 6.45 in arm A), against S2's 7.77 to 14.80 (7.77 to 11.33).
  The 32 at 8x8 take 8.25 to 18.19 ms (8.25 to 13.56 in arm A), against S2's 12.39 to 32.78 (12.39 to 22.98).
- At the firmware's registration capacity, 16 controllers on every interface, every fan-out now fits T_svc at 1x1, in both arms.
  SET_NAME takes 6.45 ms in arm A, from 11.33, and arm B's BIND_RX GET_STREAM_INFO notice 8.70 ms, from 14.80.
- At 8x8, 5 of arm A's 13 fan-outs still miss: SET_NAME, LOCK_ENTITY and UNLOCK_ENTITY, at 10.01 to 13.56 ms.
  So do 10 of arm B's 22, at 10.45 to 18.19 ms: BIND_RX's GET_STREAM_INFO notice (the longest), SET_STREAM_INFO, SET_NAME, SET_CONFIGURATION, an output map removal and one SET_CONTROL.
  None is over the 24 ms ceiling, where S2 had three in arm B.

Each group's graded JSON carries every fan-out it measured, with its recipients and its cost a recipient (`fanout`).

### Paths that still miss T_svc

A cell is a path's worst measured instance, as in [Results](#results).
A command never answered or a record never released is worse than any time measured, and its cells give the time it had waited by the run's end, at least.
Those figures are lower bounds of waits that never ended, with and without the cache, so they do not measure what the cache saves.

| 1x1: path missing T_svc with the 4 KiB cache | Interface | none, ms (bound) | 4 KiB, ms (bound) | 4 KiB, CPU cycles |
|---|---:|---:|---:|---:|
| PROBE_TX_RESPONSE | 0 | 12.02 (29.87) **miss** | 11.35 (30.26) **miss** | 567,383 |
| UNBIND_RX | 0 | 6.56 (26.86) | 10.29 (15.85) **miss** | 514,510 |
| an ACMP command behind a full acmp ring | 0 | 63.30 (70.05) **over ceiling** | 36.41 (40.22) **over ceiling** | 1,820,497 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | 67.93 (81.83) **over ceiling** | 37.07 (50.09) **over ceiling** | 1,853,704 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | 88.33 (107.65) **over ceiling** | 34.33 (55.30) **over ceiling** | 1,716,699 |
| a response with 7 frames owed ahead of it | 0 | 126.29 (130.31) **over ceiling** | 93.51 (95.48) **over ceiling** | 4,675,270 |
| an ACMP command behind the owed input | 0 | at least 363.98, **never answered** | at least 363.69, **never answered** | at least 18,184,318, **never answered** |
| ACMP record released under the composed load, last | 0 | 141.21 **over ceiling** | 81.43 **over ceiling** | 4,071,644 |
| ADP record released under the composed load, last | 0 | 101.25 **miss** | 44.63 **miss** | 2,231,449 |
| AECP record released under the composed load, last | 0 | 417.50 **over ceiling** | 244.70 **over ceiling** | 12,235,196 |
| MAAP record released under the composed load, last | 0 | 81.55 **over ceiling** | 44.67 **miss** | 2,233,287 |
| SRP record released under the composed load, first | 0 | at least 628.32, **never released** | at least 574.32, **never released** | at least 28,715,962, **never released** |
| SRP record released under the composed load, last | 0 | at least 628.30, **never released** | at least 574.30, **never released** | at least 28,714,955, **never released** |

| 8x8: path missing T_svc with the 4 KiB cache | Interface | none, ms (bound) | 4 KiB, ms (bound) | 4 KiB, CPU cycles |
|---|---:|---:|---:|---:|
| DISCONNECT_TX | 0 | 10.62 (30.62) **miss** | 16.30 (36.30) **miss** | 814,999 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 0 | 27.41 (41.44) **over ceiling** | 21.38 (53.20) **over ceiling** | 1,069,241 |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 1 | 29.72 (41.44) **over ceiling** | 22.66 (53.20) **over ceiling** | 1,133,183 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 0 | 45.45 (83.13) **over ceiling** | 21.22 (29.72) **over ceiling** | 1,061,066 |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 1 | 47.73 (83.13) **over ceiling** | 22.47 (29.72) **over ceiling** | 1,123,367 |
| GET_RX_STATE | 0 | 10.96 (30.77) **miss** | 18.68 (38.55) **miss** | 933,947 |
| GET_TX_CONNECTION | 0 | 10.63 (30.63) **miss** | 16.29 (36.29) **miss** | 814,715 |
| GET_TX_STATE | 0 | 10.67 (30.66) **miss** | 16.32 (36.31) **miss** | 816,003 |
| PROBE_TX | 0 | 11.17 (30.68) **miss** | 18.80 (38.48) **miss** | 939,974 |
| PROBE_TX | 1 | 21.02 (54.45) **over ceiling** | 13.46 (24.91) **miss** | 672,826 |
| TMR_DELAY, or the first TMR_NO_RESP | 1 | 12.89 (70.11) **miss** | 10.46 (45.03) **miss** | 523,060 |
| UNBIND_RX | 0 | 6.75 (27.03) | 12.11 (32.32) **miss** | 605,716 |
| lock_entity | 1 | 16.39 (22.25) **miss** | 10.01 (13.67) **miss** | 500,717 |
| set_name | 0 | 20.68 (27.82) **miss** | 12.81 (17.15) **miss** | 640,708 |
| set_name | 1 | 22.98 (29.45) **miss** | 13.56 (17.73) **miss** | 678,100 |
| unlock_entity | 0 | 15.64 (21.49) **miss** | 10.02 (13.67) **miss** | 500,843 |
| unlock_entity | 1 | 15.74 (21.59) **miss** | 10.03 (13.68) **miss** | 501,625 |
| an ACMP command behind a full acmp ring | 0 | 108.71 (120.30) **over ceiling** | 57.96 (63.77) **over ceiling** | 2,897,982 |
| an ENTITY_AVAILABLE behind a full adp ring | 0 | 83.51 (107.83) **over ceiling** | 46.43 (66.02) **over ceiling** | 2,321,442 |
| an ENTITY_AVAILABLE behind the adp ring, its bucket refilling (observed) | 0 | 118.81 (156.29) **over ceiling** | 52.00 (65.59) **over ceiling** | 2,600,153 |
| an event behind 15 others | 0 | 44.65 (73.70) **miss** | 14.45 (28.05) **miss** | 722,398 |
| a response with 7 frames owed ahead of it | 0 | 161.10 (170.62) **over ceiling** | 122.32 (128.00) **over ceiling** | 6,115,798 |
| an ACMP command behind the owed input | 0 | at least 860.00, **never answered** | at least 369.84, **never answered** | at least 18,492,065, **never answered** |
| ACMP record released under the composed load, first | 0 | 27.36 **over ceiling** | 13.99 **miss** | 699,320 |
| ACMP record released under the composed load, last | 0 | 177.90 **over ceiling** | 102.46 **over ceiling** | 5,123,204 |
| ADP record released under the composed load, first | 0 | 27.41 **miss** | 14.03 **miss** | 701,449 |
| ADP record released under the composed load, last | 0 | 137.94 **miss** | 62.51 **miss** | 3,125,398 |
| ADP record released under the composed load, last | 1 | 88.96 **miss** | 47.30 **miss** | 2,364,755 |
| AECP record released under the composed load, first | 0 | 27.40 **over ceiling** | 14.02 **miss** | 701,112 |
| AECP record released under the composed load, last | 1 | 510.22 **over ceiling** | 312.35 **over ceiling** | 15,617,522 |
| MAAP record released under the composed load, first | 0 | 27.39 **miss** | 14.01 **miss** | 700,592 |
| MAAP record released under the composed load, last | 0 | 103.71 **over ceiling** | 57.56 **over ceiling** | 2,877,773 |
| SRP record released under the composed load, first | 0 | at least 658.79, **never released** | at least 591.99, **never released** | at least 29,599,416, **never released** |
| SRP record released under the composed load, last | 1 | at least 658.77, **never released** | at least 591.97, **never released** | at least 29,598,409, **never released** |

A probe measures one phase, so a path can measure longer with the cache than without it.
In arm A's ACMP groups the change-notice retry makes every pass 14 to 16 ms at 1x1 and 19 to 21 ms at 8x8 with the cache, against 27 to 31 ms without it.
At 8x8, seven ACMP inputs arrive after their pass took its records, so each waits for the next pass and spans two cached passes where it spanned one cacheless pass; their pass bounds rise by 5 to 20 ms.
At 1x1 a few ADP and ACMP inputs land later in their pass: the ADP paths stay within 1.04 ms, and UNBIND_RX's 10.29 ms has a pass bound of 15.85 ms against 26.86 ms without the cache.
Arm B, whose callbacks answer, has no retry passes.

### The hybrid-XIP arm

| Point, instruction cache, code | Planned block RAM, tiles | CPU cycles per instruction | Mean refill, CPU cycles | Groups graded, probes refused | Paths (instances) missing T_svc | Composed maximum, every backlog window, ms | Over the windows that released their whole load only, ms | Worst pass, ms |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, 4 KiB, block RAM | 35.5 | 5.83 | 42 | 18, 0 | 13 of 81 (34 of 141) | at least 19.32 | 8.60 | 19.32 |
| 1x1, 4 KiB, flash | 15 | 33.95 | 2,143 | 18, 3 | 71 of 78 (120 of 138) | at least 94.91 | none | 94.91 |
| 1x1, 32 KiB, flash | 15 | 10.19 | 2,145 | 18, 0 | 19 of 81 (62 of 141) | at least 28.08 | 23.42 | 28.08 |
| 8x8, 4 KiB, block RAM | 56 | 5.65 | 42 | 17, 0 | 34 of 129 (66 of 182) | at least 29.12 | 14.03 | 37.89 |
| 8x8, 4 KiB, flash | 35 | 21.75 | 2,161 | 17, 4 | 111 of 125 (151 of 178) | at least 98.76 | none | 112.79 |
| 8x8, 32 KiB, flash | 35 | 8.92 | 2,094 | 17, 0 | 50 of 129 (83 of 182) | at least 41.78 | 30.99 | 50.75 |

With the code in flash, a 64-byte refill takes 2,100 to 2,160 CPU cycles on the product's single-lane read (the model's 12.5 MHz serial clock), against 42 from block RAM.
A 4 KiB cache does not hide that: the CPU runs at 34 cycles an instruction at 1x1 and 22 at 8x8, waiting on refills for most of them.
71 of 78 paths miss T_svc at 1x1 and 111 of 125 at 8x8; no composed window releases its load, and three probes' bounded waits (four at 8x8) expire before their outputs.
A 32 KiB cache, on a CPU of 13 tiles out of context, brings the CPU to 10 cycles an instruction at 1x1 and 9 at 8x8, near the cacheless block-RAM core's 9.5.
It still leaves 19 of 81 and 50 of 129 paths missing T_svc.
Its composed maxima, at least 28.08 and 41.78 ms, are lower bounds, as the cacheless core's at least 31.32 and 44.19 ms are.
Over the windows that released their whole load, the same windows in both, it takes 23.42 and 30.99 ms, longer than the cacheless core's 14.81 and 27.84 ms.
Against the split's 4 KiB cache with its code in block RAM, it would save about 14 tiles at either point (a CPU of 13 tiles against 6, and 20.5 or 21 tiles of `rom`), for two to three times the longest pass of the windows that released their load.
So the T_svc service paths stay in block RAM behind the split's cache, or behind one eight times its size, as D3 rules.
Moving the code out of block RAM would free 20.5 tiles at 1x1 with one interface (35.5 to 15.0, planned) and 21 at 8x8 with two (56.0 to 35.0); F1's flash driver, `.rodata` and the initial values of `.data` stay.

A first run also put F1's flash driver in flash.
The CPU then stalled in the driver's `ls_window` while the command master held the flash's chip select, and took an illegal-instruction trap (cause 2) in the three ACMP groups that read saved state.
That is D3's rule that the driver stays in block RAM, and the arm now keeps it there.

### Block RAM and logic

| Instruction cache | Vivado LUT / FF | Vivado RAMB36 / RAMB18 (tiles) | Routed WNS / WHS at 20 / 10 ns, ns | Yosys LUT (with LUTRAM) / FF | Yosys RAMB36 / RAMB18 |
|---|---:|---:|---:|---:|---:|
| none (S2) | 2,525 / 3,021 | 2 / 5 (4.5) | +0.980 / +0.089 | 7,198 / 6,552 | 0 / 0 |
| 2 KiB, 1 way | 2,537 / 3,192 | 2 / 7 (5.5) | +0.566 / +0.078 | 7,386 / 6,936 | 0 / 2 |
| 4 KiB, 1 way (split) | 2,534 / 3,194 | 3 / 6 (6) | +0.931 / +0.075 | 7,194 / 6,938 | 2 / 0 |
| 8 KiB, 1 way | 2,548 / 3,196 | 4 / 6 (7) | +0.821 / +0.081 | 7,328 / 6,940 | 4 / 0 |
| 8 KiB, 2 ways | 2,587 / 3,242 | 4 / 7 (7.5) | +0.324 / +0.077 | 7,398 / 7,078 | 4 / 0 |
| 16 KiB, 1 way | 2,549 / 3,198 | 6 / 6 (9) | +0.846 / +0.066 | 7,196 / 6,902 | 8 / 2 |
| 16 KiB, 2 ways | 2,597 / 3,245 | 6 / 7 (9.5) | +0.537 / +0.094 | 7,584 / 7,080 | 8 / 0 |
| 32 KiB, 1 way | 2,551 / 3,200 | 10 / 6 (13) | +0.708 / +0.084 | 7,190 / 6,906 | 16 / 2 |

Each netlist is the harness's CPU, with the power-of-two region cover.
Vivado runs out of context with `AreaOptimized_high` on `xc7a100t-fgg484-2`; the timing column places and routes the same synthesis at the shipping clocks, the CPU at 20 ns and its bus at 10 ns.
Yosys maps with `synth_xilinx -family xc7 -flatten`, as `syn/yosys/ooc.sh` prices a top; it keeps the cacheless core's FIFOs in logic, where Vivado uses 4.5 tiles.
The cache costs about 170 to 220 FF and under 75 LUTs at every size, and, in Vivado, one tile for each 4 KiB of data and half a tile of tags for each way.
The product split CPU's figures are in [split placement control memory](../../../docs/design/SPLIT_CONTROL_MEMORY.md#7-the-cpus-instruction-cache).

### The T_svc gap

The cache alone does not close T_svc at either point.

- **1x1, one interface.** The composed maximum is at least 19.32 ms, a lower bound, and 13 of 81 paths (34 of 141 instances) still miss.
  Over the windows that released their load the longest pass is 8.60 ms, within T_svc; that figure leaves out the two bound-talker windows, which never release SRP's 32 records, after at least 574 ms.
  The ACMP-ring, ADP-ring and owed rows take 34 to 94 ms.
  The worst pass is the composed maximum's, 19.32 ms, so #397's one-hart rule, every pass well under T_svc, still fails.
- **8x8, two interfaces.** The composed maximum is at least 29.12 ms, a lower bound, and 34 of 129 paths (66 of 182 instances) miss.
  Over the windows that released their load the longest pass is 14.03 ms.
  The event row is 14.45 ms, the ring and owed rows 46 to 122 ms, and the fan-outs that miss at registration capacity 10.01 to 13.56 ms in arm A (10.45 to 18.19 ms in arm B); the worst pass is 37.89 ms.

The residual is the data side's, and in order of size:

- `memset` and `memcpy`, byte loops: 65 % of the composed maximum's pass at 1x1 and 43 % at 8x8, and 40 % and 42 % of the longest pass of the windows that released their load. Word-wide copies and zeroing only the bytes a response sends are S2b's first item.
- AECP's change-notice retry every millisecond (`aecp.c`, `retry_at = now + 1`), which sets every worst pass in arm A and the composed maximum at both points. S2b's backoff answers it.
- AECP, ACMP and lwSRP's `mrp_mad`, together 18 % of the composed maximum's pass at 1x1 and 39 % at 8x8 (15 % and 21 % of the released windows' longest), and the mailbox driver, 7 % and 6 % (21 % and 12 %). S2b's per-pass cap bounds them.
- Software multiply, divide and shift, 3 % of the composed maximum's pass at both points (7 % of the released windows' longest). The M extension removes them; that is an owner decision.

With the instruction cache in, the core's own lever left is its data side: loads and stores wait 39 to 40 % of the cycles.
A data cache is the owner's option, with the coherent interconnect it needs (see [split placement control memory](../../../docs/design/SPLIT_CONTROL_MEMORY.md#7-the-cpus-instruction-cache)); the clock stays the owner's too.

### Controls with the cache

The three controls run again on the cached CPU, and each is caught.
Their commands are those in [Controls and self-test](#controls-and-self-test), with `--fetch-l1 64x1`, the split's geometry, in place of `--fetch-l1 none`:

- `slow-adp-rx`: the planted RCV_ADP_DISCOVER measures 16.556 ms against 0.513 ms unplanted. The planted loop now runs from the cache, so it is shorter than the cacheless 24.614 ms, and still over T_svc.
- `slow-adp-shutdown`: SHUTDOWN measures 16.328 ms against 0.333 ms unplanted. The `shutdown-entry` arm's SHUTDOWN is 0.33 ms at 1x1 and 0.32 / 0.64 ms at 8x8.
- `as-built`: handed the SoC's regions, the cached CPU takes the same instruction access fault, cause 1, at the same call (`0x6880`). The cache does not change #791's decode.

## Controls and self-test

`run.py --self-test` regrades the committed trace [`fixture.log`](fixture.log), which the `fixture` group recorded at 1x1, against [`oracle.json`](oracle.json).
The fixture has a short composed window: one record on every receive channel and two GM events.
Its checks:

- the fixture's digest, each of its seven rows with its pass bound and the records ahead, each loaded channel's first and last record served in its window, its worst pass and its composed maximum with the window's population and its release;
- a planted over-budget path (the recorded BIND_RX response moved past T_svc) must miss; the window with its MAAP record's commit deleted, and with that record also left out of its declaration, must be refused by name, and so must the window against a defined load one record smaller; with SRP's release deleted, SRP must be reported never released and the window must report its load unreleased;
- every clock conversion; the ceilings and T_svc, restated in [`selftest.py`](selftest.py) so a changed table fails;
- an exact-budget path passes and one bus cycle more misses; W + T_svc passes, one cycle more misses within W plus the ceiling, and past that it is over the ceiling;
- the probe's own tagged frame starts it; a commit after a refused frame is the next frame's; a commit that follows no frame is refused;
- a response to another sequence_id, or on the other interface, does not end it; the last required output ends it; the expected response is checked;
- a timer path starts at its armed deadline; a test-only entry at its own function's entry; the pass bound runs from the running pass at the bus ratio;
- a notification over two recipients ends at the last; a late recipient misses; a missing one, a duplicate standing in for another, and a controller outside the set are refused; unrelated unsolicited responses do not end it; over three recipients, the cost a recipient is the first to last commit over the two gaps;
- the composed maximum is a window's longest pass even when that pass is neither its first nor its last, and the worst pass includes the run's last pass; the pass the script's end cuts is no idle pass;
- the composed maximum is the longest pass of every backlog window, the fixture's excluded, and a lower bound while one left its load unreleased, with the released windows' longest beside it; it is still a lower bound when the longest window released its load and a shorter one did not;
- a run without every backlog row names the rows not run, and its composed maximum is partial: arm B's three rows, and one row alone;
- `results.json`'s composed maximum is the record the table renders, its line checked word for word: a lower bound over every window, a partial figure, and both at once;
- the responses owed ahead are exactly the owed ones, in order; a command that may be dropped and is never answered is reported, unbounded, and one that may not is refused;
- the defined loads, restated; every composed window of the real scenario, at one and two interfaces, sends and declares exactly its defined load; the owed row has its seven owed and its four behind;
- the real fan-out group registers the firmware's capacity (read from `aecp.h`) on every interface, every registration is each fan-out's recipient, and no requester is registered;
- a control probe is an instance of its functional path; repeated instances count as one path, at their worst, with every miss;
- the records ahead of an input; a served record's: an earlier record released after its commit is ahead of it, one released before is not; each path's worst instance, a starved one first, and the misses per path and per instance;
- the run's exit status for a miss, a refusal and an empty run; a regrade's refusal of an absent log, an absent script and a stale script; a trap's refusal;
- reuse refuses a changed image, ROM file, SoC Verilog, CPU netlist and firmware source, a deleted or unrecorded ROM file, a changed native model and an unresolved key, and reuses an unchanged build;
- the fetch observers follow the CPU's fetch plugin, a refill's 16 beats are read off the netlist's line-aligned refill address, and a cached netlist without that address is refused;
- the load/store observers follow the data cache's IO bus, without ids, an instruction cache without a data cache keeps the cacheless load/store observers, and a cached netlist with neither or both of the two load/store plugins is refused;
- `run.main` builds and records the fetch L1 and the arm it selected, on temporary files with the build's toolchain steps replaced;
- `run.main` refuses a reused build of another fetch L1 or arm, reuses the selected one, and takes a build that records no fetch L1 as the cacheless one;
- the XIP arm's link script keeps the reset entry and the flash driver in `rom` and puts every other function in the flash window.

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
| worst pass: the run's last pass is dropped | refused: synthetic.service.acmp.last.if0: the release at 2050 belongs to no work pass |
| passes: the pass the script's end cuts counts as idle (earlier rule) | the pass the script's end cuts is no idle pass |
| composition: a window that committed more than its load is accepted | a composed window that committed more than its load is refused |
| composition: the load is the stimulus's own declaration (earlier rule) | refused: synthetic: the composed window committed two ACMP records, its declared load none |
| composition: the backlog stimulus omits SRP | every composed window's stimulus is its defined load |
| composition: the backlog stimulus omits MAAP | every composed window's stimulus is its defined load |
| composition: the owed row omits the ACMP commands behind its input (earlier rule) | every composed window's stimulus is its defined load |
| service: a record never released is omitted | a starved channel is reported by name, and its window reports its load unreleased |
| service: a window that left its load unreleased reports it released (earlier rule) | a starved channel is reported by name, and its window reports its load unreleased |
| composition: the composed maximum is taken over the windows that released their load (earlier rule) | the composed maximum is the longest pass of every backlog window, a lower bound while one left its load unreleased |
| composition: the composed maximum is no lower bound where a window left its load unreleased | the composed maximum is the longest pass of every backlog window, a lower bound while one left its load unreleased |
| composition: the composed maximum includes the fixture's short window | the composed maximum is the longest pass of every backlog window, a lower bound while one left its load unreleased |
| composition: the composed maximum is a lower bound only where its own window left its load unreleased | the composed maximum is a lower bound while a window shorter than the longest left its load unreleased |
| composition: the composed maximum does not name the backlog rows a run did not include | a run without every backlog row names the rows not run, and its composed maximum is partial |
| tables: results.json omits the composed maximum | results.json's composed maximum is the record the table renders, with its lower-bound and partial labels |
| tables: the composed maximum line drops its lower-bound label | results.json's composed maximum is the record the table renders, with its lower-bound and partial labels |
| tables: the composed maximum line drops its partial label | results.json's composed maximum is the record the table renders, with its lower-bound and partial labels |
| service: the records ahead count only those never released | a served record's records ahead are those not yet released at its commit |
| notify: the cost a recipient divides by the recipients, not the gaps | a fan-out's cost a recipient is its first to last commit over the gaps between them |
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
| fetch bus: the cacheless observers on a cached CPU | the fetch observers follow the CPU's fetch plugin |
| fetch bus: one beat a refill | a refill's beats are read off the netlist |
| lsu bus: the cacheless observers on a data-cached CPU | the load/store observers follow the data cache's IO bus, without ids |
| reuse: the fetch L1 and the arm are not compared | the run refuses a reused build of another fetch L1 or arm and reuses the selected one; a build with no fetch L1 is cacheless |
| reuse: a reused build is not compared with the selection | the run refuses a reused build of another fetch L1 or arm and reuses the selected one; a build with no fetch L1 is cacheless |
| build: an XIP build records the block-RAM arm | the run builds and records the fetch L1 and the arm it selected |
| build: the CPU is built with the split's cache whatever the selection | the run builds and records the fetch L1 and the arm it selected |
| xip: the reset entry moves to flash with the other code | the XIP arm keeps the reset entry and the flash driver in rom and moves the other code to flash |
| xip: the flash driver moves to flash with the other code | the XIP arm keeps the reset entry and the flash driver in rom and moves the other code to flash |

A mutant whose name ends in "(earlier rule)" restores a rule this harness had before these checks, so its check is the test that fails on that rule.
Under two mutants the synthetic window of the records-ahead check is refused, and a refusal anywhere counts as caught, so those two rows name the refusal.

Regenerate the fixture only through its generator, from a fresh 1x1 run of the `fixture` group.
The committed fixture and its oracle were recorded on the cacheless core, so the run selects it:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-fixture --fetch-l1 none --groups fixture --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/selftest.py --write-fixture \
  /tmp/budget-fixture/results/fixture.log /tmp/budget-fixture/build.json
```

Three controls run the full harness, here on the cacheless core S2 measured them on:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-slow-adp --fetch-l1 none --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-slow-shutdown --fetch-l1 none --variant shutdown-entry --mutation slow-adp-shutdown
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-as-built --fetch-l1 none --cpu-regions as-built
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
- SET_STREAM_FORMAT is refused in both arms, whose format port answers unsupported (`ctrl_aecp_image.c`, `a_format`), so its fan-out is not run.
- The lock expiry's notice (60 s after a LOCK_ENTITY) and the counter pushes are not run: the first is beyond the simulation's length, and the fixture changes no counter.
- The fixture's sources are never allocated, so a Listener Ready grants no licence; that path ends at the record's release.
- Ends are mailbox commits; wire departure, ingress, egress and the network (H-ACMP's round trip) are not measured.
- The flash's erase and program waits are zero, so F1's commit is measured as CPU work only; S4 owns the target port.
- There is no datapath, no DDR3 and no packet traffic besides the stimulus; the CPU's DMA port is idle.
- The firmware polls (`CTRL_MBX_WFI` undefined), as the fixture is linked.
- The two-interface fixture gives both interfaces the same MAC, as `ctrl_aecp_image.c` does.
- With the instruction cache, a fetch is observed as a line refill on the cache's bus; hits are on no bus and are not counted.
- The self-test's build check replaces the SoC export, which needs LiteX, with a recorder of the selection it is handed; `split_soc.build`'s own record (`soc.json`) is attested by each run's `build.json`, not by the portable self-test.
- The XIP arm runs every function but the reset entry and F1's flash driver from flash.
  The model's erase and program waits are zero, so it does not see a real part's read stall while it programs.

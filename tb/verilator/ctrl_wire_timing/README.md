<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Wire timing in the split simulation (#665 S8)

This harness runs the split placement's platform image on the split CPU, cycle by cycle, with the datapath connected, and grades what leaves and enters the datapath's MAC boundary.
Its contract is [#868](https://github.com/kebag-logic/milan-fpga/issues/868), the plan's section S8 of #665, with the ruling on its points and load ([issuecomment-6755260058](https://github.com/kebag-logic/milan-fpga/issues/868#issuecomment-6755260058)) and the ruling on its reviews ([issuecomment-6788719673](https://github.com/kebag-logic/milan-fpga/issues/868#issuecomment-6788719673)).
The grader works offline, on the log a run leaves.

It grades, at the shipping 1x1 shape and at 8x8 with two interfaces, without load and with the composed load:

- the ACMP round trips under Milan v1.2 Table 5.26's 200 ms, each bind with the PROBE_TX it causes (#868 item 1);
- every MAAP probe and announce interval strictly inside IEEE 1722-2016 B.3.4.2 and B.3.4.1, and each frame's egress under the 11 ms reserve (item 2);
- the ADP advertise period inside Milan v1.2 Table 5.50, and the AECP response time under 240 ms, every response with the status its scenario states (item 3);
- its planted controls: an egress delay past the reserve, and a grader with a shifted clock (item 4).

The 1x1 short paths run in CI (item 5); the announce interval and the advertise periods run in a [local campaign](#the-local-campaign).

## Contents

- **[Run](#run)** -- The prerequisites, the build once and its reuse, the CI step, the campaign unit, the regrade and the self-test.
- **[The composition](#the-composition)** -- The CPU half, the split top at each point, and what the testbench models between them.
- **[The stimulus and the load](#the-stimulus-and-the-load)** -- Each draw, the seeds, and the composed load with its three stated differences.
- **[What is graded](#what-is-graded)** -- The clock check, the commits, and each path with its clause and bound.
- **[Results](#results)** -- Every distribution at both points, without and with the load.
- **[The local campaign](#the-local-campaign)** -- Four units to the second ANNOUNCE: the command, the seeds, the wall time and every distribution, with the announce interval and the advertise periods.
- **[Controls and self-test](#controls-and-self-test)** -- The grader's controls and the plants on every real log, each refused or found by its own words.
- **[Limits](#limits)** -- What the simulation leaves out, and what the points share.

## Run

Use the [CPU budget harness's prerequisites](../ctrl_service_budget/README.md#run-and-reproduce): the product LiteX tree, the pinned RV32 SDK, Verilator and the offline CPU generator (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`).
The tsn-c-stack and lwSRP submodules must be initialised.
Keep build and output directories outside the checkout.
The grader's self-test needs Python only:

```sh
python3 -B tb/verilator/ctrl_wire_timing/run.py --self-test
python3 -B tb/verilator/ctrl_wire_timing/run.py --ci --build-dir /tmp/wire-ci
python3 -B tb/verilator/ctrl_wire_timing/run.py --point 8x8 --build-dir /tmp/wire-8x8 --draws 16 --load composed
python3 -B tb/verilator/ctrl_wire_timing/run.py --build-dir /tmp/wire-8x8 --reuse-build --draws 16 --load none
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir /tmp/wire-ci --seed 1 --load none --out /tmp/camp0
python3 -B tb/verilator/ctrl_wire_timing/run.py --build-dir /tmp/wire-8x8 --regrade --out /tmp/wire-8x8/results/none-s0
```

A first run at a point builds once ([`wire_build.py`](wire_build.py)); `--reuse-build` runs again on that build, and refuses it when any recorded input changed.
The record is every input the model is built from or reads when it runs: the image, the ROM files and the generated headers; this harness's model, export and build; the build's tools elsewhere, milan_dp's split recipe (its `Makefile`) among them; the recipe's own source list (`make print-split-srcs`: the datapath's, `KL_mbx`'s and `tb_split_top`'s); every file a Verilator run or the native compile read, from the dependency lists they leave; the checkout's modules the CPU half's export imported; the shape's config; and the firmware's source trees, the TSN stack's and lwSRP's among them, by one digest.
So a build is reused only at the tree it was built from.
`--ci` is the CI step: the self-test, the 1x1 build, and its two runs at once, without and with the load ([CI](../../../docs/testing/CI_WORKFLOWS.md)).
`--campaign` is one unit of the [local campaign](#the-local-campaign).
A run writes its stimulus (`wire.txt`), the testbench's lines (`wire.log`), `run.json`, `results.json` and `table.md` into its output directory, `results/<load>-s<seed>` under the build directory unless `--out` names one.
`--regrade` grades the log a run left.
Every grade is followed by its two plants on the same log ([Controls](#controls-and-self-test)).
Exit 0 is a pass, 1 a finding or an escaped plant, and 2 a refusal.
`WIRE_JOBS` sets the build's parallel jobs (16 by default).

The split top's model is built by milan_dp's own split recipe (`make build-split`), its object directory in the build directory.
That recipe writes the suite's generated ROM and header files into `tb/verilator/milan_dp`, as every milan_dp leg does, and git ignores them.
The directory has no Makefile, for the [CPU budget harness's reason](../ctrl_service_budget/README.md#run-and-reproduce): the serial sweep discovers every Makefile.

## The composition

Two models run in lockstep on one bus clock, and no new simulation top is written:

- **The CPU half** ([`wire_soc.py`](wire_soc.py)) is the [CPU budget harness's](../ctrl_service_budget/README.md#the-test-soc) split SoC, built from its parts read only, with the [split boot simulation's](../ctrl_split_boot/README.md#the-soc-and-the-testbench) CSR window and UART pads.
  The CPU is the shipping VexiiRiscv with the split instruction cache, at the 100 MHz product clock (the owner's decision of 2026-10-30 on #665), on this base's own CPU clock input.
  Its firmware memory holds the platform image, linked unmodified and twice, as the split boot simulation links it.
  The one difference from those SoCs is the mailbox: only `KL_mbx_wb` is built, and its host port is on pads.
- **The split top** is milan_dp's [`tb_split_top.sv`](../milan_dp/tb_split_top.sv): `KL_mbx`, `KL_mbx_cdc`, the two byte crossings and `milan_datapath` with `CTRL_SPLIT_P = 1`, built by its own recipe at the point's shape, streams and interfaces ([its page](../milan_dp/README.md#the-split-placements-control-path-obj_split-665)).

| Point | Shape | Interfaces | Datapath streams |
|---|---|---:|---:|
| `1x1` | `endstation_ax7101_1x1_tdm8` | 1 | 1 |
| `8x8` | `endstation_ax7101_8x8` | 2 | 8 |

At 8x8 both halves build `KL_mbx` and `KL_mbx_wb` from the contract generator's two-interface variant, and the build refuses two variants that differ.
Interface 0 is the datapath's, through `KL_mbx_cdc`.
Interface 1 is not a second datapath: the split top gives it to the bench, which drives it as the CPU budget harness drives `KL_mbx`.
That is its link level and its frames at the mailbox's own byte boundary, between interface 0's frames.
Its commit is acknowledged at the contract's bound, and its windows, grandmaster and face events are idle.
The platform image at 8x8 with two interfaces is the planner's one ledgered point, `platform-8x8-two-interfaces` (59.0 RAMB36, [SPLIT_CONTROL_MEMORY.md section 5](../../../docs/design/SPLIT_CONTROL_MEMORY.md)), so its link and the CPU half's memory plan name that ledger.

The testbench, [`wire_main.cpp`](wire_main.cpp), joins them and models what neither holds:

- the host port: before each bus edge the CPU half's request reaches the split top and its answer comes back, until neither moves, so each model samples the other's settled outputs;
- `KL_mbx`'s millisecond: one pulse every 100,000 bus cycles, as `milan_soc.CtrlMailbox` counts it;
- the CSR window: each of the CPU's Wishbone accesses becomes one AXI4-Lite access on the datapath's port, on the 50 MHz datapath clock;
- the MAC boundary at 1 Gb/s: received beats are offered and sent beats taken at 2.5 bytes a datapath cycle, 24 bytes apart between frames, a short frame counted as 60;
- interface 1 at 8x8: one byte a bus cycle in, every byte KL_mbx sends on it taken at once;
- the flash, the CPU budget harness's device model, blank; the UART, read only.

Every line it prints is a bus cycle count: `MS` each millisecond, `RXW` and `TXW` each frame's first and last beat at the MAC boundary, `RXB` and `TXB` the same on interface 1, `MTX` each frame's last byte leaving `KL_mbx`, `TXC` each mailbox transmit commit, `TMR` each timer command, `LOAD` each load queued (the cycle it was queued and its frames may go from, the timer slot whose arm queued it or `-` for a script step, its frames and its echoes skipped per interface), `CSRW` and `CSRR` each CSR access.
Each load frame carries the tag `load-<name>-<n>`, its load's n-th offer, so the grader counts the frames of each offer that reached the MAC.
`WIRE_HOST_LOG=<from>:<to>` adds, between those bus cycles, every host access and flash operation, for diagnosis; no grade reads them.

## The stimulus and the load

The stimulus ([`wire_scenario.py`](wire_scenario.py)) uses the CPU budget harness's frames and identities.
Every link is raised before the boot, so MAAP acquires on interface 0 (IEEE 1722-2016 B.3) and ADP advertises (Milan v1.2 5.6.3.5) while the draws run.
Each draw takes 100 ms:

- a controller's BIND_RX (IEEE 1722.1-2021 CONNECT_RX_COMMAND, Milan v1.2 5.5.2) to STREAM_INPUT 0;
- the PROBE_TX it causes, answered by the talker's PROBE_TX_RESPONSE after a turnaround under 1 ms;
- an UNBIND_RX 60 ms later;
- 20 ms on, one AEM command, in turn READ_DESCRIPTOR (ENTITY), GET_CONFIGURATION, GET_COUNTERS on AVB_INTERFACE 0, GET_AVB_INFO (0x0027) on AVB_INTERFACE 0, GET_NAME and the MVU GET_MILAN_INFO, the CPU budget harness's AECP rows; each final response must carry SUCCESS, the status `AECP_COMMANDS` states for each.
  GET_AVB_INFO's command is IEEE 1722.1-2021 7.4.40.1's: a descriptor_type, AVB_INTERFACE, and a descriptor_index, 0.

For seed 0 each draw's bind arrives 7,919 bus cycles later in a millisecond than the last, and the talker answers 6,007 cycles later, both modulo one millisecond; another seed draws both from its own generator.
A run ends 250 ms after both its last draw and its last required ANNOUNCE, the longest response bound it grades, so every command's answer, or its absence, falls inside the log.

**The load** (the ruling on the points and load, its item 3) is the CPU budget harness's composed load (`scenario.composed_load`): every receive channel's admitted burst at once, but the measured path's own, alternating the interfaces as that harness does.
It is offered right before each bind (ACMP's path) and each AEM command (AECP's), and 200 us before every deadline the firmware arms on interface 0's MAAP and ADP timer slots, so the burst is in the loop when the timer expires.
A burst carries about 60 records: 8 ADP, 16 AECP, 7 MAAP, 32 SRP and 12 ACMP, less the measured channel's; `KL_mbx_rx`'s token buckets admit what they admit.
Three parts differ from that harness's load, each stated:

- its ADP records are ENTITY_DISCOVERs for another entity: a global one restarts this entity's advertise cycle at every burst (Milan v1.2 5.6.3.5.4), so no advertise period would ever complete under load; the frame, its channel and its parse up to the target check are the same;
- its MAAP records echo their interface's last ANNOUNCE as a conflicting PROBE, as that harness's do: a conflicting PROBE while probing restarts the acquisition (B.3.6.5) whose intervals are measured, so before an interface's first ANNOUNCE its echoes are skipped (the `LOAD` line counts them per interface).
  `wire_main.cpp` keeps each echo's newest match as each frame is sent, so the ANNOUNCE is found whenever one has been sent, whatever traffic followed it; that harness keeps a history per channel, and here the MAAP channel itself carries the DEFENDs the echoes cause.
  The grader finds an echo skipped after its interface's first ANNOUNCE left;
- a deadline's burst leaves out the ACMP and AECP records, the channels whose received records the draws measure; the draws' own bursts are whole.
  That harness never loads a measured path's own channel, and a deadline's burst can land with a draw's command.
  The first campaign, at `79997664d5`, measured it twice: an ADP deadline's 12 GET_RX_STATEs filled ACMP's ring (room 12) 56 us before a BIND_RX (seed 3) and 0.26 us before a PROBE_TX_RESPONSE (seed 4), and `KL_mbx` dropped each.
  A MAAP deadline's burst is therefore ADP's and SRP's records and an ADP deadline's is MAAP's and SRP's, so no ACMP or AECP record is in the loop at a MAAP or ADP deadline.
  `run.py` refuses a stimulus whose deadline load reaches either channel.

The grandmaster changes of that harness's other rows are not part of the composed load; interface 0's would need the gPTP plane `tb_split_top` builds off.

## What is graded

[`wire_grade.py`](wire_grade.py) converts nothing before it has checked its clock: consecutive `MS` lines must be exactly `sys_hz / 1000` cycles apart.
A grader given another clock, or a log whose milliseconds drifted, is refused.
The n-th transmit commit on a channel is the n-th frame of that channel to leave `KL_mbx` (`MTX`); interface 0's, in order, are that protocol's frames at the MAC.
A count that disagrees, a frame before its commit, or an interface 0 frame that never reaches the MAC is refused.
Every figure is interface 0's.

| Path | From | To | Bound |
|---|---|---|---|
| `acmp.bind_rx` | the BIND_RX's first byte in | the BIND_RX_RESPONSE's last byte out | 200 ms (Milan v1.2 5.5.2.3, Table 5.26) |
| `acmp.probe_tx` | the PROBE_TX's transmit commit, where the listener's transaction starts | the handling of the PROBE_TX_RESPONSE | 200 ms (Table 5.26) |
| `aecp.response` | an AEM or MVU command's first byte in | its final response's last byte out | 240 ms (IEEE 1722.1-2021 9.2.1, as #868 names it; the bound is [FR_NFR.md 3.4.1](../../../docs/reference/FR_NFR.md)'s, from 9.3.2.6 and Milan v1.2 5.4.3.4) |
| `maap.egress` | a timer-driven PROBE's or ANNOUNCE's millisecond | its first byte out | 11 ms, the reserve ([the MAAP firmware's page](../../../sw/firmware/ctrl/maap/README.md)) |
| `maap.probe_interval` | a PROBE's first byte out | the next PROBE's | strictly 500 to 600 ms (IEEE 1722-2016 B.3.4.2) |
| `maap.announce_interval` | an ANNOUNCE's first byte out | the next ANNOUNCE's | strictly 30 to 32 s (B.3.4.1) |
| `maap.interval_error` | an interval at the wire | less its drawn value, in magnitude | 11 ms, the reserve |
| `adp.egress` | an ENTITY_AVAILABLE's delay millisecond | its first byte out | 400 ms, 200 ms at startup ([FR_NFR.md 3.4.1](../../../docs/reference/FR_NFR.md)) |
| `adp.advertise_period` | an ENTITY_AVAILABLE's first byte out | the next one's | 5 to 9 s (Milan v1.2 Table 5.50), graded inside 4,998 to 9,400 ms: 2 ms of phase below, [FR_NFR.md 3.4.1](../../../docs/reference/FR_NFR.md)'s 400 ms ceiling above; the margin to the strict 9,000 ms is published beside it |
| `egress.<protocol>.first`, `.last` | a frame's transmit commit | its first, last byte out | reported |

Reported beside them: the bind to the PROBE_TX it causes, the PROBE_TX's legs (its egress, the talker's turnaround, the response's ingress to its handling), and each AEM command's own row.

A bind's PROBE_TX is the first one out after the bind's own BIND_RX_RESPONSE and before the next draw's bind; every draw binds the same stream, so the stream's identity cannot tell the draws apart.
A bind without one is a finding, and so is a count of graded PROBE_TX transactions other than the draws.
A BIND_RX_RESPONSE whose status is not SUCCESS (IEEE 1722.1-2021 Table 8-3) is a finding, and so is an AEM or MVU final response whose status is not the one `wire_scenario.AECP_COMMANDS` states for its command, SUCCESS for every one (Table 7-170).

The PROBE_TX's handling is the arm of the interface's ACMP timer slot (`ctrl_app.h`) that follows both the response's last byte and the arm the PROBE_TX made for its own timeout, before the next PROBE_TX.
A timer-driven frame left on its slot's latest expiry by its commit: an arm expires when no later write of the slot came before its millisecond, or at once when its deadline had already come (a zero ADP delay).
The firmware draws MAAP's intervals inside 511 to 589 ms and 30,011 to 31,989 ms, so each drawn value is checked against that range, each interval against its clause, and each frame's egress and each interval's error against the 11 ms reserve.
ADP's advertise timer must be armed for exactly 5,000 ms after each ENTITY_AVAILABLE, and each delay drawn inside 0 to 4,000 ms, or 0 to 2,000 ms at startup.
A run to its second ANNOUNCE must sample an advertise period, and a log that runs on 9,400 ms past its last ENTITY_AVAILABLE has stopped advertising: both are findings.
A command without its answer is a finding, but for one the log ends within the bound of, which is reported as censored.
An AECP IN_PROGRESS answer to a getter is a finding.

Each load is counted three ways, kept apart in `results.json` and the table:

- **queued**: each `LOAD` line, an offer queued by a script step or by a timer slot's arm (an armed trigger), with its frames and the echoes skipped;
- **delivered**: the offers whose every frame, and the frames, that reached the MAC or the bench's `KL_mbx` boundary inside the run, by their tags;
- **expiries met**: for a load a timer's arm queued, the arms that expired with their burst delivered.

A deadline past the run's end is queued and never delivered, and a burst whose arm a later write cancelled is delivered and meets no expiry.
Every frame received is a draw's, four a draw, or a delivered load frame, so their sum must be the model's own count, `SUMMARY`'s `rx_frames` and `bench_rx`; another sum is a finding.

## Results

At `267fc9815d`, whose model, build and stimulus the head keeps: 16 draws a run, seed 0, each run to its first ANNOUNCE and 250 ms on, at both points without and with the composed load.
Each cell is N: min / mean / max, in ms unless marked us; every bound is in ms:

| Path (N: min / mean / max ms) | bound ms | 1x1 none | 1x1 composed | 8x8/2if none | 8x8/2if composed |
|---|---:|---|---|---|---|
| `acmp.bind_rx` | 200.0 | 16: 0.396 / 0.673 / 0.966 | 16: 0.728 / 1.339 / 3.423 | 16: 0.401 / 0.920 / 1.727 | 16: 0.758 / 11.940 / 18.277 |
| `acmp.bind_to_probe_tx` | - | 16: 0.585 / 0.862 / 1.155 | 16: 0.917 / 1.528 / 3.613 | 16: 0.607 / 1.127 / 1.933 | 16: 0.965 / 12.147 / 18.483 |
| `acmp.probe_tx` | 200.0 | 16: 0.399 / 0.909 / 1.080 | 16: 0.399 / 2.946 / 5.263 | 16: 0.841 / 1.175 / 2.177 | 16: 0.841 / 1.921 / 5.763 |
| `acmp.probe_tx.entity` | - | 16: 0.177 / 0.458 / 0.839 | 16: 0.219 / 2.495 / 4.539 | 16: 0.180 / 0.725 / 1.456 | 16: 0.180 / 1.470 / 5.043 |
| `aecp.response` | 240.0 | 16: 0.964 / 1.708 / 2.264 | 16: 3.003 / 3.710 / 4.151 | 16: 1.550 / 2.234 / 3.178 | 16: 4.053 / 9.820 / 24.504 |
| `aecp.response.get_avb_info` | - | 3: 1.528 / 1.593 / 1.639 | 3: 3.296 / 3.550 / 3.746 | 3: 1.611 / 2.139 / 2.877 | 3: 8.543 / 15.044 / 24.504 |
| `maap.egress` | 11.0 | 4: 0.410 / 0.787 / 1.008 | 4: 1.147 / 1.546 / 1.972 | 4: 0.961 / 1.250 / 1.479 | 4: 1.771 / 2.036 / 2.472 |
| `maap.probe_interval` | 600.0 | 3: 513.505 / 530.413 / 559.139 | 3: 514.340 / 531.270 / 560.297 | 3: 515.482 / 539.817 / 582.696 | 3: 516.571 / 540.663 / 583.689 |
| `maap.interval_error` | 11.0 | 3: 0.139 / 0.349 / 0.505 | 3: 0.174 / 0.937 / 1.340 | 3: 0.274 / 0.484 / 0.696 | 3: 0.728 / 1.329 / 1.689 |
| `adp.egress` | 400.0 | 1: 0.838 / 0.838 / 0.838 | 1: 1.550 / 1.550 / 1.550 | 1: 0.911 / 0.911 / 0.911 | 1: 2.207 / 2.207 / 2.207 |
| `egress.acmp.first` | - | 48: 0.36 / 0.37 / 0.37 us | 240: 0.36 / 0.36 / 0.37 us | 48: 0.36 / 0.36 / 0.37 us | 240: 0.36 / 0.37 / 0.37 us |
| `egress.maap.first` | - | 5: 0.36 / 0.37 / 0.37 us | 12: 0.36 / 0.37 / 0.37 us | 5: 0.36 / 0.37 / 0.37 us | 9: 0.36 / 0.36 / 0.37 us |

Each run's load, in the grader's three counts (see [What is graded](#what-is-graded)): queued, as offers (those a timer's arm queued) / frames / echoes skipped; delivered inside the run, as offers whole (in part) / frames; and the expiries met.
The two loaded runs carry the same load:

| Run | findings | censored | simulated ms | ready ms | queued | delivered | expiries met |
|---|---:|---|---:|---:|---|---|---|
| 1x1 none | 0 | none | 1935 | 49.102 | none | none | - |
| 1x1 composed | 0 | none | 1935 | 49.102 | acmp 16 (0) / 896 / 112, adp 2 (2) / 64 / 14, aecp 16 (0) / 839 / 105, maap 5 (5) / 200 / 0 | acmp 16 (0) / 896, adp 1 (0) / 32, aecp 16 (0) / 839, maap 3 (0) / 120 | adp 1, maap 3 |
| 8x8/2if none | 0 | none | 2001 | 115.271 | none | none | - |
| 8x8/2if composed | 0 | none | 2001 | 115.271 | the same as 1x1 composed | the same as 1x1 composed | adp 1, maap 3 |

So a loaded 16-draw run has 3 MAAP and 1 ADP deadline bursts in the loop at an expiry, of the 5 and 2 its arms queued.
At 1x1 the other three deadlines fall past the log's 1,935 ms: the probe deadline the final probe expiry's pass arms and cancels (2,210 ms), the announce deadline (33,590 ms) and the advertise timer's (5,405 ms).
In every run the delivered load frames and four a draw are the frames the model received: 1,887 and 64 are 1,951, the loaded 1x1's `rx_frames` and the loaded 8x8's 1,104 `rx_frames` and 847 `bench_rx`; 64 for each unloaded run.
Every echo skipped was queued before its interface's first ANNOUNCE left.

Every graded path is inside its bound at both points, without and with the load:

- The slowest ACMP transaction is the loaded 8x8 bind at 18.3 ms, 181.7 ms inside Table 5.26's 200 ms; without load every one ends within 2.2 ms.
- The slowest AEM response is the loaded 8x8's GET_AVB_INFO at 24.5 ms, 215.5 ms inside 240 ms; every AEM and MVU response carries SUCCESS.
- MAAP's egress, from each timer's millisecond to the frame's first byte at the MAC, is at most 2.5 ms, and every probe interval is within 1.7 ms of its draw: both inside the 11 ms reserve.
- A frame's first byte leaves 0.36 to 0.37 us after its commit; its last follows at line rate.

The platform image boots to ready at 49.1 ms at 1x1 and 115.3 ms at 8x8.
On four CPUs of a shared host the CI step took 693 s: the build 85 s (the CPU netlist from the local generator's cache), then both 1x1 runs at once, 608 s each.
The 8x8 runs took 707 s and 661 s for 2,001 ms of simulated time each, on one shared core.

## The local campaign

The campaign grades what one CI-sized run cannot reach: the IEEE 1722-2016 B.3.4.1 announce interval (30 to 32 s), and the Milan v1.2 Table 5.50 advertise periods inside it.
It is four units at the shipping 1x1 shape, each its own process on the same build, each with its own draw seed, each to its second ANNOUNCE.
There is no time compression: every unit runs cycle by cycle for about 34.7 s of simulated time.
Each unit is 342 draws, enough to keep the stimulus running past the latest second ANNOUNCE the firmware can draw, then the 250 ms tail.

| Unit | Seed | Load |
|---|---:|---|
| 0 | 1 | none |
| 1 | 2 | none |
| 2 | 3 | composed |
| 3 | 4 | composed |

Each unit is one command, here unit 0's, from a checkout with its 1x1 build at `/tmp/wire-ci`:

```sh
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir /tmp/wire-ci --seed 1 --load none --out /tmp/camp0
```

Each unit grades every path above, and adds one announce interval and the advertise periods inside it.
At `267fc9815d`, whose model, build, stimulus and grader the head keeps, the four units ran side by side on one build, each one single-threaded process on a shared host, in 2.45 to 2.77 h each, 3.5 to 3.9 ms of simulated time a second:

| Path (N: min / mean / max ms) | bound ms | unit 0, seed 1, none | unit 1, seed 2, none | unit 2, seed 3, composed | unit 3, seed 4, composed |
|---|---:|---|---|---|---|
| `acmp.bind_rx` | 200.0 | 342: 0.358 / 0.734 / 2.694 | 342: 0.355 / 0.733 / 2.650 | 342: 0.389 / 1.288 / 5.024 | 342: 0.384 / 1.296 / 6.728 |
| `acmp.bind_to_probe_tx` | - | 342: 0.548 / 0.923 / 2.883 | 342: 0.545 / 0.923 / 2.839 | 342: 0.579 / 1.477 / 5.213 | 342: 0.573 / 1.485 / 6.918 |
| `acmp.probe_tx` | 200.0 | 342: 0.399 / 1.045 / 4.487 | 342: 0.399 / 1.167 / 4.490 | 342: 0.399 / 2.959 / 5.593 | 342: 0.399 / 3.039 / 5.591 |
| `acmp.probe_tx.entity` | - | 342: 0.166 / 0.570 / 3.528 | 342: 0.171 / 0.643 / 3.534 | 342: 0.163 / 2.462 / 5.298 | 342: 0.164 / 2.546 / 5.245 |
| `aecp.response` | 240.0 | 342: 0.834 / 1.756 / 3.902 | 342: 0.834 / 1.709 / 3.550 | 342: 2.202 / 3.997 / 7.251 | 342: 2.328 / 4.037 / 6.882 |
| `aecp.response.get_avb_info` | - | 57: 1.353 / 1.731 / 3.716 | 57: 1.362 / 1.672 / 3.550 | 57: 2.825 / 3.964 / 6.214 | 57: 2.831 / 4.032 / 6.637 |
| `maap.egress` | 11.0 | 5: 0.323 / 0.556 / 0.856 | 5: 0.302 / 0.641 / 0.800 | 5: 0.981 / 1.639 / 2.457 | 5: 0.957 / 1.346 / 2.083 |
| `maap.probe_interval` | 600.0 | 3: 513.174 / 530.274 / 558.840 | 3: 513.086 / 530.344 / 559.099 | 3: 513.730 / 531.435 / 559.756 | 3: 513.386 / 531.094 / 560.408 |
| `maap.interval_error` | 11.0 | 4: 0.160 / 0.199 / 0.267 | 4: 0.086 / 0.209 / 0.498 | 4: 0.730 / 1.172 / 1.819 | 4: 0.021 / 0.576 / 1.408 |
| `maap.announce_interval` | 32000.0 | 1: 31957.267 / 31957.267 / 31957.267 | 1: 31956.502 / 31956.502 / 31956.502 | 1: 31958.383 / 31958.383 / 31958.383 | 1: 31957.021 / 31957.021 / 31957.021 |
| `adp.egress` | 400.0 | 6: 0.415 / 0.608 / 0.834 | 6: 0.355 / 0.494 / 0.839 | 6: 0.233 / 0.897 / 1.304 | 6: 0.281 / 1.229 / 2.637 |
| `adp.advertise_period` | 9400.0 | 5: 5362.581 / 6820.423 / 8387.053 | 5: 5363.114 / 6820.105 / 8385.816 | 5: 5362.966 / 6820.604 / 8385.438 | 5: 5364.705 / 6821.437 / 8387.356 |
| `egress.acmp.first` | - | 1026: 0.36 / 0.36 / 0.37 us | 1026: 0.36 / 0.36 / 0.37 us | 5130: 0.36 / 0.36 / 0.37 us | 5130: 0.36 / 0.36 / 0.37 us |
| `egress.maap.first` | - | 6: 0.36 / 0.36 / 0.37 us | 6: 0.36 / 0.36 / 0.37 us | 1656: 0.36 / 0.36 / 0.37 us | 1656: 0.36 / 0.36 / 0.37 us |

The load columns are the grader's three counts, as in [Results](#results): queued, as offers (those a timer's arm queued) / frames / echoes skipped; delivered inside the run, as offers whole (in part) / frames; and the expiries met:

| Run | findings | censored | simulated ms | ready ms | queued | delivered | expiries met |
|---|---:|---|---:|---:|---|---|---|
| unit 0, seed 1, none | 0 | none | 34703 | 49.102 | none | none | - |
| unit 1, seed 2, none | 0 | none | 34706 | 49.102 | none | none | - |
| unit 2, seed 3, composed | 0 | none | 34705 | 49.102 | acmp 342 (0) / 21434 / 112, adp 12 (12) / 454 / 14, aecp 342 (0) / 20073 / 105, maap 6 (6) / 240 / 0 | acmp 342 (0) / 21434, adp 11 (0) / 415, aecp 342 (0) / 20073, maap 5 (0) / 200 | adp 11, maap 4 |
| unit 3, seed 4, composed | 0 | none | 34690 | 49.102 | the same as unit 2 | the same as unit 2 | adp 11, maap 4 |

Every unit passes with no finding and nothing censored, and both plants are caught on each log:

- Each announce interval is 31,956.5 to 31,958.4 ms, strictly inside B.3.4.1's 30 to 32 s, 41.6 ms or more below its ceiling.
- Every probe and announce interval is within 1.82 ms of its draw, and MAAP's egress is at most 2.46 ms on all 20 timer-driven frames: both inside the 11 ms reserve.
- Each advertise period is 5,362.6 to 8,387.4 ms, inside Table 5.50's 5 to 9 s, 612.6 ms or more inside the strict 9,000 ms (1,012.6 ms inside the graded 9,400 ms), and each ENTITY_AVAILABLE leaves within 2.7 ms of its delay.
- Over the 1,368 draws the slowest transaction is an AEM response at 7.3 ms, and the slowest ACMP one 6.7 ms; every bind has its own PROBE_TX, and every ACMP frame the entity sends and every AEM and MVU response carries SUCCESS.
- In each loaded unit every MAAP echo after the first ANNOUNCE is found: 664 offers queued after it, 663 of them with echoes, 4,641 echoes found and none skipped; the 231 skipped were all queued before it. The entity answers them with 1,650 DEFENDs on the MAAP channel, which is why each echo keeps its own match rather than a window of that channel.
- Of a loaded unit's 6 MAAP and 12 ADP deadline bursts, 5 and 11 are delivered and 4 and 11 meet an expiry: the probe deadline the final probe expiry's pass arms and cancels is delivered and meets none, and the next announce deadline and the last advertise timer fall past the log.
- The delivered load frames and four a draw are the frames the model received: 42,122 and 1,368 are 43,490 in each loaded unit, and 1,368 in each unloaded one.

## Controls and self-test

`--self-test` first checks the stimulus: a loaded script's deadline loads reach no draw's channel (`clean-loaded-script`), and one planted with a GET_RX_STATE in ADP's deadline load is refused (`deadline-load-on-a-draw-channel`, words `the deadline load adp reaches the acmp channel`).

It then checks the reuse guard on a stand-in build directory, recorded by `wire_build.inputs` itself, with no build: the record as made is accepted (`clean-reuse`), and each of five recorded sources, its digest changed as an edit after the build leaves it, is refused by its own name.

| Control | Source edited after the build | Words |
|---|---|---|
| `reuse-after-an-edit-of-tb_split_top.sv` | the split top | `'tb/verilator/milan_dp/tb_split_top.sv'` |
| `reuse-after-an-edit-of-milan_datapath.sv` | the datapath | `'hdl/milan/milan_datapath.sv'` |
| `reuse-after-an-edit-of-KL_mbx.sv` | the split top's `KL_mbx` | `'hdl/milan/mailbox/KL_mbx.sv'` |
| `reuse-after-an-edit-of-Makefile` | milan_dp's split recipe | `'tb/verilator/milan_dp/Makefile'` |
| `reuse-after-an-edit-of-tree:firmware` | any file of the firmware's source trees, the TSN stack's among them | `'tree:firmware'` |

It then grades synthetic logs of two draws, MAAP's acquisition and ADP's startup advertisement, a 37 s log with a second ANNOUNCE and ADP's periodic advertising, and a loaded log.
Each clean log must pass, and each control must be refused or found by its own words.

The clean logs are `clean`, `clean-announce-interval` and `clean-two-interfaces`, with no finding.
The fourth, `clean-censored-at-the-end`, ends 49 ms after an unanswered command, which it must report as censored and not as a finding.
The fifth, `clean-loaded`, is `clean` under a load as the model logs it: an offer before each bind, its echo skipped before the ANNOUNCE; an offer at each of MAAP's five arms, the last one's deadline past the log's end, and one the same pass cancels before its deadline, as the firmware's final probe expiry arms a probe deadline and cancels it for the announce; then, after the ANNOUNCE, 70 unrelated frames sent, more than a 64-frame history of every protocol held, one more offer whose echo is found, and a last offer the log ends inside, one of its three frames received.
It must report its load exactly: 5 MAAP offers queued, 4 delivered and 3 expiries met (the cancelled arm's burst is delivered and meets none), and 2 AECP offers queued, 1 delivered whole and 1 in part.
So a grader that counted a cancelled arm's burst as meeting its expiry, or no offer as delivered in part, fails it.

| Control | What it changes | Words |
|---|---|---|
| `shifted-clock` | the clean log graded at 125 MHz (#868 item 4) | `the clock is shifted` |
| `drifted-milliseconds` | one millisecond one cycle late | `the clock is shifted` |
| `missing-response` | the first BIND_RX_RESPONSE gone | `has no BIND_RX_RESPONSE` |
| `bind-without-its-probe-tx` | the first bind causes no PROBE_TX; the second draw's follows | `the BIND_RX acmp-bind-0 caused no PROBE_TX after its response and before the next bind` |
| `probe-tx-transactions-not-the-draws` | the same log: one PROBE_TX for two binds | `1 PROBE_TX transactions graded (1 sent), the run asked for 2 draws` |
| `bind-refused` | the first BIND_RX_RESPONSE carries status 1, LISTENER_UNKNOWN_ID | `carries status 1, not SUCCESS` |
| `late-response` | each response 200 ms after its command | `acmp.bind_rx: 200.0 ms is not under 200.0 ms` |
| `unhandled-answer` | the handling's arm gone, the PROBE_TX's own arm kept after the answer | `was never handled` |
| `handled-on-another-slot` | the handling armed on another slot | `was never handled` |
| `frame-before-commit` | a commit moved past its frame's first byte | `before its commit` |
| `incomplete-model` | the model's tally gone | `did not complete` |
| `no-mailbox-egress` | every `MTX` line gone | `no KL_mbx egress` |
| `egress-without-commit` | a frame leaving `KL_mbx` with no commit | `frames left KL_mbx after` |
| `bench-frames-counted-as-interface-0` | at two interfaces, interface 1's frames logged as interface 0's | `never reached the MAC` |
| `missing-aecp-response` | the first AEM response gone | `has no final response` |
| `late-aecp-response` | each AEM response 240 ms after its command | `aecp.response: 240.0 ms is not under 240.0 ms` |
| `aecp-in-progress` | an IN_PROGRESS answer before each final response | `IN_PROGRESS answers` |
| `aem-refused` | the first AEM response carries status 2, NO_SUCH_DESCRIPTOR | `carries status 2, not the 0 its scenario states` |
| `mvu-refused` | the first draw's MVU GET_MILAN_INFO answered with status 1, NOT_IMPLEMENTED | `carries status 1, not the 0 its scenario states` |
| `unanswered-before-the-end` | a command 300 ms before the log ends, unanswered | `has no final response` |
| `egress-past-reserve` | the third PROBE 11 ms and one cycle late at the MAC (#868 item 4) | `maap.egress: 11.` |
| `interval-error-past-reserve` | the next deadline armed 11 ms after its PROBE left | `maap.interval_error: 11.` |
| `probe-draw-outside-reserve` | a probe interval drawn at 590 ms | `outside the reserved 511 to 589 ms` |
| `probe-interval-outside-clause` | the second PROBE 42 ms late, its interval 600.03 ms | `is not strictly inside 500 to 600 ms` |
| `maap-frame-on-no-expiry` | the first probe deadline's arm gone | `left on no expired timer` |
| `maap-expiry-cancelled` | that deadline cancelled before it came | `left on no expired timer` |
| `announce-interval-outside-clause` | the second ANNOUNCE 1,001 ms late | `is not strictly inside 30000 to 32000 ms` |
| `no-announce-interval` | the second ANNOUNCE gone | `ANNOUNCEs left the MAC, the run asked for 2` |
| `advertise-timer-not-5s` | every advertise timer armed for 4,999 ms | `not 5000 ms` |
| `adp-delay-outside-table` | a delay drawn at 4,001 ms | `outside 0 to 4000 ms` |
| `adp-egress-past-ceiling` | every ENTITY_AVAILABLE 400 ms after its delay | `adp.egress: 400.` |
| `available-sent-twice` | the same expiry's ENTITY_AVAILABLE sent twice, a millisecond apart | `adp.advertise_period: 1.000 ms` |
| `no-advertise-period` | the 37 s log with no advertising after the startup ENTITY_AVAILABLE | `adp.advertise_period: no sample in a run to its second ANNOUNCE` |
| `stopped-advertising` | the same log with advertising stopping after its second period | `the entity stopped advertising` |
| `echo-skipped-after-the-announce` | the loaded log's last offer with its echo skipped, as a history the unrelated frames filled leaves it | `echoes of load aecp skipped on interface 0 ... after its first ANNOUNCE left` |
| `received-frame-unaccounted` | one of that offer's frames received untagged | `17 delivered load frames and 4 a draw (2 draws) are not the 26 frames the model received` |
| `load-offer-over-delivered` | a fourth frame of the loaded log's first offer, of three, received under its tag | `LOAD: 4 frames of offer 0 of load acmp were received, 3 were queued` |

After every run's grade, `run.py` grades two plants on that run's own log, and each must be caught:

| Plant | What it changes | Words |
|---|---|---|
| `egress-past-reserve` | the first timer-driven PROBE moved 12 ms later at the MAC, past the 11 ms reserve | `maap.egress: ... is not under 11.0 ms` |
| `shifted-clock` | the log graded at 125 MHz | `the clock is shifted` |

## Limits

- The MAC core's and the PHY's own pipeline delays are outside the simulation; they add a fixed sub-microsecond each way.
- The CSR window's AXI4-Lite access is the testbench's, on the datapath clock; the product's Wishbone bridge and crossing are not modelled.
- The flash is blank and erases and programs at once, as in the CPU budget harness.
- The firmware polls the mailbox (`CTRL_MBX_WFI` undefined), as the platform is linked.
- MAAP draws its intervals from an xorshift32 seeded with the MAC plus NOW_MS at `maap_begin` (B.3.6.1), which the boot fixes in a cycle-true model. So every run at a point draws the same intervals; the seeds move the stimulus and its load against each expiry, which is what moves the egress.
- Interface 1 at 8x8 has no datapath; its figures are not graded.

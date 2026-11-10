<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Wire timing in the split simulation (#665 S8)

This harness runs the split placement's platform image on the split CPU, cycle by cycle, with the datapath connected, and grades what leaves and enters the datapath's MAC boundary.
Its contract is [#868](https://github.com/kebag-logic/milan-fpga/issues/868), the plan's section S8 of #665, with the round 2 ruling ([issuecomment-6755260058](https://github.com/kebag-logic/milan-fpga/issues/868#issuecomment-6755260058)).
The grader works offline, on the log a run leaves.

It grades, at the shipping 1x1 shape and at 8x8 with two interfaces, without load and with the composed load:

- the ACMP round trips under Milan v1.2 Table 5.26's 200 ms (#868 item 1);
- every MAAP probe and announce interval strictly inside IEEE 1722-2016 B.3.4.2 and B.3.4.1, and each frame's egress under the 11 ms reserve (item 2);
- the ADP advertise period inside Milan v1.2 Table 5.50, and the AECP response time under 240 ms (item 3);
- its planted controls: an egress delay past the reserve, and a grader with a shifted clock (item 4).

The 1x1 short paths run in CI (item 5); the announce interval and the advertise periods run in a [local campaign](#the-local-campaign).

## Contents

- **[Run](#run)** -- The prerequisites, the build once and its reuse, the CI step, the campaign unit, the regrade and the self-test.
- **[The composition](#the-composition)** -- The CPU half, the split top at each point, and what the testbench models between them.
- **[The stimulus and the load](#the-stimulus-and-the-load)** -- Each draw, the seeds, and the composed load with its two stated differences.
- **[What is graded](#what-is-graded)** -- The clock check, the commits, and each path with its clause and bound.
- **[Results](#results)** -- Every distribution at both points, without and with the load, and the campaign's intervals.
- **[The local campaign](#the-local-campaign)** -- Four units to the second ANNOUNCE: the command, the seeds, the wall time.
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

Every line it prints is a bus cycle count: `MS` each millisecond, `RXW` and `TXW` each frame's first and last beat at the MAC boundary, `RXB` and `TXB` the same on interface 1, `MTX` each frame's last byte leaving `KL_mbx`, `TXC` each mailbox transmit commit, `TMR` each timer command, `LOAD` each load offered, `CSRW` and `CSRR` each CSR access.
`WIRE_HOST_LOG=<from>:<to>` adds, between those bus cycles, every host access and flash operation, for diagnosis; no grade reads them.

## The stimulus and the load

The stimulus ([`wire_scenario.py`](wire_scenario.py)) uses the CPU budget harness's frames and identities.
Every link is raised before the boot, so MAAP acquires on interface 0 (IEEE 1722-2016 B.3) and ADP advertises (Milan v1.2 5.6.3.5) while the draws run.
Each draw takes 100 ms:

- a controller's BIND_RX (IEEE 1722.1-2021 CONNECT_RX_COMMAND, Milan v1.2 5.5.2) to STREAM_INPUT 0;
- the PROBE_TX it causes, answered by the talker's PROBE_TX_RESPONSE after a turnaround under 1 ms;
- an UNBIND_RX 60 ms later;
- 20 ms on, one AEM command, in turn READ_DESCRIPTOR (ENTITY), GET_CONFIGURATION, GET_COUNTERS, GET_AVB_INFO, GET_NAME and the MVU GET_MILAN_INFO, the CPU budget harness's AECP rows.

For seed 0 each draw's bind arrives 7,919 bus cycles later in a millisecond than the last, and the talker answers 6,007 cycles later, both modulo one millisecond; another seed draws both from its own generator.
A run ends 250 ms after both its last draw and its last required ANNOUNCE, the longest response bound it grades, so every command's answer, or its absence, falls inside the log.

**The load** (the round 2 ruling's item 3) is the CPU budget harness's composed load (`scenario.composed_load`): every receive channel's admitted burst at once, but the measured path's own, alternating the interfaces as that harness does.
It is offered right before each bind (ACMP's path) and each AEM command (AECP's), and 200 us before every deadline the firmware arms on interface 0's MAAP and ADP timer slots, so the burst is in the loop when the timer expires.
A burst carries about 60 records: 8 ADP, 16 AECP, 7 MAAP, 32 SRP and 12 ACMP, less the measured channel's; `KL_mbx_rx`'s token buckets admit what they admit.
Two parts differ from that harness's load, each stated:

- its ADP records are ENTITY_DISCOVERs for another entity: a global one restarts this entity's advertise cycle at every burst (Milan v1.2 5.6.3.5.4), so no advertise period would ever complete under load; the frame, its channel and its parse up to the target check are the same;
- its MAAP records echo interface 0's last ANNOUNCE as a conflicting PROBE, as that harness's do, so before the first ANNOUNCE they are skipped (the `LOAD` line counts them): a conflicting PROBE while probing restarts the acquisition (B.3.6.5) whose intervals are measured.

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
| `adp.advertise_period` | an ENTITY_AVAILABLE's first byte out | the next one's | 5 to 9 s (Milan v1.2 Table 5.50), widened by 2 ms below and the ceiling above |
| `egress.<protocol>.first`, `.last` | a frame's transmit commit | its first, last byte out | reported |

Reported beside them: the bind to the PROBE_TX it causes, the PROBE_TX's legs (its egress, the talker's turnaround, the response's ingress to its handling), and each AEM command's own row.

The PROBE_TX's handling is the arm of the interface's ACMP timer slot (`ctrl_app.h`) that follows both the response's last byte and the arm the PROBE_TX made for its own timeout, before the next PROBE_TX.
A timer-driven frame left on its slot's latest expiry by its commit: an arm expires when no later write of the slot came before its millisecond, or at once when its deadline had already come (a zero ADP delay).
The firmware draws MAAP's intervals inside 511 to 589 ms and 30,011 to 31,989 ms, so each drawn value is checked against that range, each interval against its clause, and each frame's egress and each interval's error against the 11 ms reserve.
ADP's advertise timer must be armed for exactly 5,000 ms after each ENTITY_AVAILABLE, and each delay drawn inside 0 to 4,000 ms, or 0 to 2,000 ms at startup.
A command without its answer is a finding, but for one the log ends within the bound of, which is reported as censored.
An AECP IN_PROGRESS answer to a getter is a finding.

## Results

At `6404b60ba1`: 16 draws a run, seed 0, each run to its first ANNOUNCE and 250 ms on, at both points without and with the composed load.
Each cell is N: min / mean / max, in ms unless marked us; every bound is in ms:

| Path (N: min / mean / max ms) | bound ms | 1x1 none | 1x1 composed | 8x8/2if none | 8x8/2if composed |
|---|---:|---|---|---|---|
| `acmp.bind_rx` | 200.0 | 16: 0.378 / 0.665 / 0.968 | 16: 0.594 / 1.026 / 1.762 | 16: 0.383 / 0.900 / 1.708 | 16: 0.758 / 13.168 / 19.212 |
| `acmp.probe_tx` | 200.0 | 16: 0.399 / 0.909 / 1.080 | 16: 0.399 / 2.944 / 5.264 | 16: 0.841 / 1.175 / 2.177 | 16: 0.841 / 2.006 / 5.124 |
| `acmp.probe_tx.entity` | - | 16: 0.177 / 0.458 / 0.839 | 16: 0.219 / 2.493 / 4.483 | 16: 0.180 / 0.725 / 1.456 | 16: 0.240 / 1.555 / 4.283 |
| `aecp.response` | 240.0 | 16: 0.872 / 1.611 / 2.248 | 16: 3.108 / 5.843 / 26.908 | 16: 1.518 / 2.211 / 3.178 | 16: 5.325 / 32.081 / 97.653 |
| `maap.egress` | 11.0 | 4: 0.744 / 0.815 / 0.872 | 4: 1.207 / 1.588 / 2.061 | 4: 0.927 / 1.222 / 1.460 | 4: 0.984 / 1.501 / 2.375 |
| `maap.probe_interval` | 600.0 | 3: 512.915 / 530.368 / 559.068 | 3: 514.289 / 531.273 / 560.385 | 3: 515.467 / 539.808 / 582.677 | 3: 516.799 / 540.400 / 582.793 |
| `maap.interval_error` | 11.0 | 3: 0.068 / 0.091 / 0.120 | 3: 0.146 / 0.940 / 1.385 | 3: 0.279 / 0.474 / 0.677 | 3: 0.609 / 1.067 / 1.799 |
| `adp.egress` | 400.0 | 1: 0.838 / 0.838 / 0.838 | 1: 1.550 / 1.550 / 1.550 | 1: 0.911 / 0.911 / 0.911 | 1: 2.207 / 2.207 / 2.207 |
| `egress.acmp.first` | - | 48: 0.36 / 0.37 / 0.37 us | 277: 0.36 / 0.36 / 0.37 us | 48: 0.36 / 0.36 / 0.37 us | 272: 0.36 / 0.36 / 0.37 us |
| `egress.maap.first` | - | 5: 0.36 / 0.36 / 0.37 us | 12: 0.36 / 0.37 / 0.37 us | 5: 0.36 / 0.36 / 0.37 us | 9: 0.36 / 0.36 / 0.37 us |

| Run | findings | censored | simulated ms | ready ms | load offers |
|---|---:|---|---:|---:|---|
| 1x1 none | 0 | none | 1935 | 49.102 | none |
| 1x1 composed | 0 | none | 1935 | 49.102 | acmp 16, adp 2, aecp 16, maap 5 |
| 8x8/2if none | 0 | none | 2001 | 115.271 | none |
| 8x8/2if composed | 0 | none | 2001 | 115.271 | acmp 16, adp 2, aecp 16, maap 5 |

Every graded path is inside its bound at both points, without and with the load:

- The slowest ACMP transaction is the loaded 8x8 bind at 19.2 ms, 180.8 ms inside Table 5.26's 200 ms; without load every one ends within 2.2 ms.
- The slowest AEM response is the loaded 8x8's at 97.7 ms, 142.3 ms inside 240 ms; the load's own 16 READ_DESCRIPTORs on each burst are what it waits behind.
- MAAP's egress, from each timer's millisecond to the frame's first byte at the MAC, is at most 2.4 ms, and every probe interval is within 1.8 ms of its draw: both inside the 11 ms reserve.
- A frame's first byte leaves 0.36 to 0.37 us after its commit; its last follows at line rate.

The platform image boots to ready at 49.1 ms at 1x1 and 115.3 ms at 8x8.
On four CPUs of a shared host the CI step took 565 s: the build 59 s (the CPU netlist from the local generator's cache), then both 1x1 runs at once.
Each 8x8 run took about 1,540 s for 2,001 ms of simulated time on one shared core.

## The local campaign

The campaign grades what one CI-sized run cannot reach: the IEEE 1722-2016 B.3.4.1 announce interval (30 to 32 s), and the Milan v1.2 Table 5.50 advertise periods inside it.
It is four units at the shipping 1x1 shape, each its own process on the same build, each with its own draw seed, each to its second ANNOUNCE.
There is no time compression: every unit runs cycle by cycle for about 34.3 s of simulated time.
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
At about 4 ms of simulated time a second on an unloaded core, a unit takes about 2.4 h; four run side by side.

## Controls and self-test

`--self-test` grades synthetic logs of two draws, MAAP's acquisition and ADP's startup advertisement, and a 37 s log with a second ANNOUNCE and ADP's periodic advertising.
Each clean log must pass, and each control must be refused or found by its own words:

The clean logs are `clean`, `clean-announce-interval` and `clean-two-interfaces`, with no finding.
The fourth, `clean-censored-at-the-end`, ends 49 ms after an unanswered command, which it must report as censored and not as a finding.

| Control | What it changes | Words |
|---|---|---|
| `shifted-clock` | the clean log graded at 125 MHz (#868 item 4) | `the clock is shifted` |
| `drifted-milliseconds` | one millisecond one cycle late | `the clock is shifted` |
| `missing-response` | the first BIND_RX_RESPONSE gone | `has no BIND_RX_RESPONSE` |
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

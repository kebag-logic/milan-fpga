<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# Wire timing in the split simulation (#665 S8)

This harness runs the split placement's platform image on the split CPU, cycle by cycle, with the datapath connected, and grades what leaves and enters the datapath's MAC boundary.
Its contract is [#868](https://github.com/kebag-logic/milan-fpga/issues/868), the plan's section S8 of #665.
The grader works offline, on the log a run leaves.

At this head it grades acceptance item 1 at the shipping shape: the ACMP round trips under Milan v1.2 Table 5.26's 200 ms.
The other points and items wait on the two decisions in [Limits](#limits).

## Contents

- **[Run](#run)** -- The prerequisites, the build once and its reuse, the regrade and the self-test.
- **[The composition](#the-composition)** -- The CPU half, the split top, and what the testbench models between them.
- **[What is graded](#what-is-graded)** -- The clock check, each draw's stimulus, and each ACMP path with its bound.
- **[Results](#results)** -- The ACMP round trips at the shipping shape, their margin to 200 ms, and the egress.
- **[Controls and self-test](#controls-and-self-test)** -- The grader's controls, each refused or found by its own words.
- **[Limits](#limits)** -- The two decisions items 1 to 5 wait on, and what the simulation leaves out.

## Run

Use the [CPU budget harness's prerequisites](../ctrl_service_budget/README.md#run-and-reproduce): the product LiteX tree, the pinned RV32 SDK, Verilator and the offline CPU generator (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`).
The tsn-c-stack and lwSRP submodules must be initialised.
Keep the build directory outside the checkout.
The grader's self-test needs Python only:

```sh
python3 -B tb/verilator/ctrl_wire_timing/run.py --self-test
python3 -B tb/verilator/ctrl_wire_timing/run.py --point 1x1 --build-dir /tmp/wire-1x1 --draws 16
python3 -B tb/verilator/ctrl_wire_timing/run.py --build-dir /tmp/wire-1x1 --reuse-build --draws 16
python3 -B tb/verilator/ctrl_wire_timing/run.py --build-dir /tmp/wire-1x1 --regrade --draws 16
```

The first run builds once ([`wire_build.py`](wire_build.py)); `--reuse-build` runs again on that build, and refuses it when any recorded input changed.
`--regrade` grades the log a run left.
The run writes `results/wire.txt` (the stimulus), `results/wire.log` (the testbench's lines), `results/results.json` and the table below.
Exit 0 is a pass, 1 a finding and 2 a refusal.

The split top's model is built by milan_dp's own split recipe (`make build-split`), its object directory in the build directory.
That recipe writes the suite's generated ROM and header files into `tb/verilator/milan_dp`, as every milan_dp leg does, and git ignores them.
The directory has no Makefile, for the [CPU budget harness's reason](../ctrl_service_budget/README.md#run-and-reproduce): the serial sweep discovers every Makefile.

## The composition

Two models run in lockstep on one bus clock, and no new simulation top is written:

- **The CPU half** ([`wire_soc.py`](wire_soc.py)) is the [CPU budget harness's](../ctrl_service_budget/README.md#the-test-soc) split SoC, built from its parts read only, with the [split boot simulation's](../ctrl_split_boot/README.md#the-soc-and-the-testbench) CSR window and UART pads.
  The CPU is the shipping VexiiRiscv with the split instruction cache, at the 100 MHz product clock (the owner's decision of 2026-10-30 on #665), on this base's own CPU clock input.
  Its firmware memory holds the platform image, linked unmodified and twice, as the split boot simulation links it.
  The one difference from those SoCs is the mailbox: only `KL_mbx_wb` is built, and its host port is on pads.
- **The split top** is milan_dp's [`tb_split_top.sv`](../milan_dp/tb_split_top.sv): `KL_mbx`, `KL_mbx_cdc`, the two byte crossings and `milan_datapath` with `CTRL_SPLIT_P = 1` at the shipping AX7101 shape, built by its own recipe.

The testbench, [`wire_main.cpp`](wire_main.cpp), joins them and models what neither holds:

- the host port: before each bus edge the CPU half's request reaches the split top and its answer comes back, until neither moves, so each model samples the other's settled outputs;
- `KL_mbx`'s millisecond: one pulse every 100,000 bus cycles, as `milan_soc.CtrlMailbox` counts it;
- the CSR window: each of the CPU's Wishbone accesses becomes one AXI4-Lite access on the datapath's port, on the 50 MHz datapath clock;
- the MAC boundary at 1 Gb/s: received beats are offered and sent beats taken at 2.5 bytes a datapath cycle, 24 bytes apart between frames, a short frame counted as 60;
- the flash, the CPU budget harness's device model, blank; the UART, read only.

Every line it prints is a bus cycle count: `MS` each millisecond, `RXW` and `TXW` each frame's first and last beat at the MAC boundary, `TXC` each mailbox transmit commit, `TMR` each timer command, `CSRW` and `CSRR` each CSR access.
`WIRE_HOST_LOG=<from>:<to>` adds, between those bus cycles, every host access and flash operation, for diagnosis; no grade reads them.

## What is graded

[`wire_grade.py`](wire_grade.py) converts nothing before it has checked its clock: consecutive `MS` lines must be exactly `sys_hz / 1000` cycles apart.
A grader given another clock, or a log whose milliseconds drifted, is refused.

The stimulus ([`wire_scenario.py`](wire_scenario.py)) uses the CPU budget harness's frames and identities.
Each draw is a controller's BIND_RX (IEEE 1722.1-2021 CONNECT_RX_COMMAND, Milan v1.2 5.5.2) to STREAM_INPUT 0, the PROBE_TX it causes, the talker's PROBE_TX_RESPONSE, and an UNBIND_RX 60 ms later.
Each draw's bind arrives 7,919 bus cycles later in a millisecond than the last, and the talker answers 6,007 cycles later, both modulo one millisecond, so the draws meet the loop at different phases.

| Path | From | To | Bound |
|---|---|---|---|
| `acmp.bind_rx` | the BIND_RX's first byte in | the BIND_RX_RESPONSE's last byte out | 200 ms (Milan v1.2 5.5.2.3, Table 5.26) |
| `acmp.bind_to_probe_tx` | the BIND_RX's first byte in | the PROBE_TX's last byte out | reported |
| `acmp.probe_tx` | the PROBE_TX's transmit commit, where the listener's transaction starts | the handling of the PROBE_TX_RESPONSE | 200 ms (Table 5.26) |
| `acmp.probe_tx.entity` | `acmp.probe_tx` | less the talker's turnaround | reported |
| `egress.<protocol>.first`, `.last` | a frame's transmit commit | its first, last byte out | reported |

The handling is the arm of the interface's ACMP timer slot (`ctrl_app.h`) that follows both the response's last byte and the arm the PROBE_TX made for its own timeout, before the next PROBE_TX.
That own arm is committed after the command in the same pass, so a prompt answer can arrive before it.
A command without its answer, an answer without its command, or a frame that leaves before its commit is graded.

## Results

At `1d6bf5556a`, `endstation_ax7101_1x1_tdm8` with one interface, 16 draws, no other load; the platform image boots to ready at 49.1 ms of simulated time.
The talker's turnaround runs from 0.02 to 0.90 ms:

| Path | N | min ms | mean ms | max ms | margin to 200 ms |
|---|---:|---:|---:|---:|---:|
| `acmp.bind_rx` | 16 | 0.3717 | 0.7023 | 0.9063 | 199.0937 |
| `acmp.bind_to_probe_tx` | 16 | 0.5612 | 0.8918 | 1.0958 | |
| `acmp.probe_tx` | 16 | 0.3990 | 0.9089 | 1.0796 | 198.9204 |
| `acmp.probe_tx.entity` | 16 | 0.1768 | 0.4584 | 0.8393 | |
| `egress.acmp.first` | 48 | 0.00036 | 0.00037 | 0.00037 | |
| `egress.acmp.last` | 48 | 0.00176 | 0.00177 | 0.00177 | |

Both ACMP transactions end within 1.1 ms, so 198.9 ms of Table 5.26's 200 ms is left for the network and the peer.
A frame's first byte leaves 0.36 to 0.37 us after its commit; its last byte follows at line rate.

The same run sent one MAAP acquisition: its probe gaps at the wire were 558.713, 519.341 and 513.012 ms, inside IEEE 1722-2016 B.3.4.2's 500 to 600 ms.
Those are observations, not yet a grade: item 2 is not graded here.

The run takes 418 s for 1,685 ms of simulated time, about 4.0 ms of simulated time a second, and 34 MB of memory.

## Controls and self-test

`--self-test` grades synthetic logs of two draws.
The clean log must pass, and each control must be refused or found by its own words:

| Control | What it changes | Words |
|---|---|---|
| `shifted-clock` | the clean log graded at 125 MHz | `the clock is shifted` |
| `drifted-milliseconds` | one millisecond one cycle late | `the clock is shifted` |
| `missing-response` | the first BIND_RX_RESPONSE gone | `has no BIND_RX_RESPONSE` |
| `late-response` | each response 200 ms after its command | `acmp.bind_rx: 200.0 ms is not under 200.0 ms` |
| `unhandled-answer` | the handling's arm gone, the PROBE_TX's own arm kept after the answer | `was never handled` |
| `handled-on-another-slot` | the handling armed on another slot | `was never handled` |
| `frame-before-commit` | a commit moved past its frame's first byte | `before its commit` |
| `incomplete-model` | the model's tally gone | `did not complete` |

## Limits

- **8x8 with two interfaces is not run.** `tb_split_top.sv`, the split recipe and `milan_soc.CtrlMailbox` connect one interface at the shipping shape, so no split composition joins a second interface to a datapath. Running it needs a decision on how that interface is connected.
- **The long intervals do not fit a 30-minute job.** At 4.0 ms of simulated time a second, the run above would reach its first IEEE 1722-2016 B.3.4.1 announce interval's end (the next ANNOUNCE's deadline, 33,587 ms) after about 2.3 hours, and its first Milan v1.2 Table 5.50 advertise period's end (the second ENTITY_AVAILABLE's deadline, 5,404 ms) after about 22 minutes. #868 items 2, 3 and 5 together need a decision on how those intervals are measured.
- The MAC core's and the PHY's own pipeline delays are outside the simulation; they add a fixed sub-microsecond each way.
- The CSR window's AXI4-Lite access is the testbench's, on the datapath clock; the product's Wishbone bridge and crossing are not modelled.
- The flash is blank and erases and programs at once, as in the CPU budget harness.
- The firmware polls the mailbox (`CTRL_MBX_WFI` undefined), as the platform is linked.

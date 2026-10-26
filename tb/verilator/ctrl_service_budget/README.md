# Split CPU service budget

This harness measures the Mark II split firmware's service paths on the shipping cacheless core.
Its contract is the [S2 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409745905) on #665, which re-opens [#397](https://github.com/kebag-logic/milan-fpga/issues/397).
The image is `ctrl_srp_image.py --with-aecp --layout split`, linked unmodified.
Every figure is a measured clock count at the CPU's 50 MHz, never an estimate.
Each is compared with T_svc = 10 ms and its ceiling in [FR_NFR.md 3.4.1](../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing).

## Contents

- **[Run and reproduce](#run-and-reproduce)** -- Prerequisites, the two points, the labelled second arm, the controls and the regrade.
- **[The test SoC](#the-test-soc)** -- What is the shipping CPU and memory, what is test-only, and where each device sits.
- **[Markers and grading](#markers-and-grading)** -- The start and end of each path, the clock conversion, the pass bound and the verdicts.
- **[Results](#results)** -- Per access, per pass, every response path, the backlog rows and the fetch share.
- **[Findings](#findings)** -- The decision input for D4, D5 and D3, and the defects the measurement exposed.
- **[Controls and self-test](#controls-and-self-test)** -- The planted over-budget path, the region-decode control and the grader mutants.
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
`--reuse-build --regrade --out DIR` grades the logs already in `DIR`.
It refuses a group whose recorded script the scenario no longer generates.

The labelled second arm builds the fixture with its four observation callbacks answering:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-1x1-ports --variant answering-ports \
  --groups acmp-cmd,acmp-noresp,acmp-notk,acmp-disc,backlog,backlog-adp --record-budget-findings
```

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
Generated from the 224 KiB regions, its region check excludes every `rom` address with bit 15 set, and the image faults (see [Findings](#findings)).
The two netlists differ only in address-decode lines, so the cover changes no timing.
`--cpu-regions as-built` builds the regions unchanged and reproduces the fault.

## Markers and grading

[`scenario.py`](scenario.py) writes each group's script.
Every probe is a `mark`, its stimulus and a bounded wait.
[`grade.py`](grade.py) reads its start and end off the log, as [FR_NFR.md 3.4.1](../../../docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing) defines them:

- A received frame starts at its receive commit, `KL_mbx_rx`'s header write (RX_HEAD).
  The probe's frame carries a tag, so other frames on the ring are not mistaken for it.
- A link or grandmaster event starts when its level changes at the mailbox input.
- A timer path starts at its armed deadline: the tick on which NOW_MS reaches it, not the record's posting.
- A path ends when its last required output is committed: an accepted TX_HEAD write, a TMR_CMD arm or cancel, a publication write or the record's RX_TAIL release.
- A response is matched by its sequence_id and its interface.

CPU cycles are bus cycles times 50/100, rounded up; milliseconds come from the bus count.
A pass runs from one committed entry of `ctrl_loop_service` to the next.
A mailbox access is timed at the CPU's load/store bus, from command to response.
Instruction fetches are counted at the cacheless fetch bus, by region.

One phase is one sample.
So each probe also reports a measured bound.
It runs from the start of the pass that was running when the input arrived, or the longest idle pass before it, to the end of the pass that committed the output.
Whatever the input's phase, it is taken by the next pass at the latest, so with the same passes the interval cannot exceed the bound.

The ceilings are 3.4.1's: ADP 200 ms, a discovery input's ACMP action and ACMP 20 ms, AECP 24 ms, a notification 24 ms, MAAP 50 ms, MRP 18 ms.
A path with a normative wait W, such as SRP's JoinTime, is bounded by W + T_svc.

## Results

Arm A is the image as linked, the formal measurement.
Arm B is the labelled second arm, whose fixture callbacks answer.
In the path tables a cell is "ms at this phase (the pass bound)"; **miss** is over T_svc, **over ceiling** over the 3.4.1 ceiling as well.
Each run writes every probe to its `table.md` and `results.json`.

### Per access and per instruction

| Point | CPU cycles per instruction | Fetches per instruction | Mailbox read / write, CPU cycles | BRAM fetch, CPU cycles (max) | sram load/store | CSR | Flash window load | Code fetched, boot / service (largest run) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 | 9.72 | 1.73 | 9 / 9 | 9.10 (303) | 9-10 / 9-10 | 9-10 / 9 | 263 mean (138-303) | 11,160 / 40,532 B |
| 8x8 | 9.62 | 1.70 | 9 / 9 | 9.15 (303) | 9-10 / 9-10 | 9-10 / 9 | 263 mean (138-303) | 11,396 / 43,060 B |

Every access is timed at the CPU, command to response, in CPU cycles at 50 MHz.
A mailbox access is 9 cycles, 0.18 us; `KL_mbx` itself answers in one bus cycle, and the rest is the clock crossing and the bus.
A fetch waits behind a slow flash read, hence the 303-cycle maximum.
Instruction fetches are 85 to 89 % of the CPU's bus transactions in every taking pass.
Their waits sum to 1.59 to 1.69 times each pass's cycles, so more than one fetch is outstanding on average: the cacheless core is fetch-bound.

### Passes

| Point, arm | Idle pass, CPU cycles (ms) | Worst pass, CPU cycles (ms), group | Composed maximum, worst pass (ms) |
|---|---:|---:|---:|
| 1x1, A | 65,703 to 72,358 (1.31 to 1.45) | 1,552,161 (31.04), acmp-disc | 1,391,312 (27.83) |
| 1x1, B | 65,703 to 232,901 (1.31 to 4.66) | 685,184 (13.70), backlog | 685,184 (13.70) |
| 8x8, A | 102,152 to 185,315 (2.04 to 3.71) | 2,989,496 (59.79), acmp-notk | 2,141,242 (42.82) |
| 8x8, B | 7,081 to 293,468 (0.14 to 5.87) | 2,004,666 (40.09), acmp-notk | 1,302,022 (26.04) |

The idle pass's largest consumers are AECP's two polls: `aecp_poll` 26,497 and `aecp_nvm_poll` 20,254 cycles at 1x1, 73,883 and 20,254 at 8x8.
The 8x8 link-up pass, 2,004,666 cycles, is lwSRP's `mrp_mad` 473,950, `memset` 361,053, `memcpy` 244,102, the mailbox driver 119,790 and software multiply and divide (`__mulsi3` 111,201, `__udivsi3` 89,954).
The 1x1 composed maximum, 685,184 cycles, is `memset` 268,495, the mailbox driver 111,947, `memcpy` 66,719, AECP 44,965 and ACMP 35,611.
Arm A's passes after a bind, 1.06 to 1.55 M cycles at 1x1, are mostly `memset` (1.1 M) and AECP (0.2 M): the retry described in [Findings](#findings).

### ADP

| Path ([`MAILBOX_SPLIT.md:495-502`](../../../docs/design/MAILBOX_SPLIT.md#service-latency)) | 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses in the taking pass, 1x1 / 8x8 (model) |
|---|---:|---:|---:|
| RCV_ADP_DISCOVER -> TMR_DELAY armed | 0.29 (1.63) | 2.57 (9.27) / 2.86 (9.27) | 38 / 73 (31) |
| TMR_DELAY expiry -> ENTITY_AVAILABLE, TMR_ADVERTISE armed | 0.87 (3.57) | 2.64 (9.09) / 3.70 (10.87) | 46 / 47 (39) |
| TMR_ADVERTISE expiry -> TMR_DELAY armed | 0.13 (1.99) | 1.06 (8.28) / 1.37 (4.60) | 9 / 25 (11) |
| GM_CHANGE -> TMR_DELAY armed | 0.10 (1.46) | 2.38 (8.95) / 2.50 (8.95) | 18 / 34 (11) |
| LINK_UP -> TMR_DELAY armed | 0.11 (4.97) | 32.51 (73.31) **miss** / 41.69 (73.31) **miss** | 88 / 345 (11) |
| LINK_DOWN -> timer stopped | 0.08 (5.48) | 18.35 (42.60) **miss** / 26.84 (42.60) **miss** | 33 / 70 (9) |
| SHUTDOWN -> ENTITY_DEPARTING | not reachable: the fixture has no shutdown input | - | - |

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
| the first TMR_NO_RESP | 3.36 (22.30) | 14.19 (70.11) **miss** / 12.89 (70.11) **miss** | 0.86 (3.03) | 2.53 (13.06) / 1.14 (9.12) | 95 / 113 (35) |
| the second TMR_NO_RESP | 1.64 (21.79) | 4.43 (24.89) / 5.24 (24.89) | 1.19 (3.89) | 1.46 (12.60) / 0.54 (8.12) | 72 / 67 (14) |
| TMR_RETRY | 7.99 (46.72) | 27.14 (76.55) **over ceiling** / 26.21 (76.55) **over ceiling** | 0.19 (3.79) | 3.17 (16.68) / 3.15 (14.68) | 73 / 68 (14) |
| TMR_DELAY | 2.90 (44.04) | 5.69 (38.79) / 8.58 (38.80) | 1.94 (5.06) | 1.70 (9.80) / 1.08 (6.57) | 95 / 93 (35) |
| TMR_NO_TK | 4.57 (22.15) | 15.23 (75.59) **miss** / 5.43 (38.64) | 0.19 (2.31) | 3.63 (9.89) / 3.24 (11.86) | 74 / 93 (14) |
| ENTITY_AVAILABLE from its RX_HEAD (H-DISC) | 10.37 (25.92) **miss** | 27.41 (41.44) **over ceiling** / 29.72 (41.44) **over ceiling** | 0.90 (2.79) | 3.45 (14.07) / 5.76 (14.07) | 104 / 129 (35) |
| ENTITY_DEPARTING from its RX_HEAD (H-DISC) | 14.42 (22.53) **miss** | 45.45 (83.13) **over ceiling** / 47.73 (83.13) **over ceiling** | 0.35 (2.24) | 1.18 (11.76) / 3.46 (11.75) | 95 / 177 (29) |
| TMR_NO_ADP (H-DISC) | 1.91 (22.31) | 8.51 (37.51) / 5.66 (31.48) | 0.99 (3.04) | 4.84 (15.30) / 2.25 (11.98) | 95 / 67 (12) |

The ACMP groups bind a sink, and from then on arm A's AECP retries its change notices every millisecond.
Those groups also run lane F1's first saved-state commit: one erase and 14 page programs (3,336 B) at 1x1, up to 52 (13,256 B) at 8x8, with zero device wait.

### AECP

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
| lock_entity | 3.96 (5.41) | 8.32 (14.50) / 4.68 (11.13) | 66 / 73 |
| MVU GET_MILAN_INFO | 2.50 (3.64) | 3.52 (9.68) / 3.53 (9.35) | 50 / 52 |
| register_unsolicited | 2.48 (3.61) | 5.91 (11.72) / 4.87 (10.68) | 46 / 54 |
| set_name | 5.22 (6.90) | 7.88 (15.08) / 7.93 (15.20) | 106 / 114 |
| unknown_command | 4.42 (5.56) | 5.65 (11.47) / 5.69 (11.50) | 53 / 54 |
| unlock_entity | 3.95 (5.40) | 5.61 (11.51) / 6.86 (11.77) | 65 / 66 |

### SRP and MAAP

| SRP and MAAP path | 1x1 ms (bound) | 8x8 if0 / if1 ms (bound) | Accesses, 1x1 / 8x8 |
|---|---:|---:|---:|
| SRP startup declarations (LINK_UP) | 4.44 (4.97) | 15.79 (18.01) **miss** / 13.25 (33.17) **miss** | 88 / 124 |
| SRP Listener Ready RX (registrar; the fixture grants no licence) | 2.77 (2.77) | 9.11 (12.34) / 8.33 (9.56) | 29 / 36 |
| SRP malformed MRPDU discard | 1.75 (1.75) | 7.70 (11.04) / 5.69 (9.17) | 29 / 36 |
| SRP Domain RX -> declarations (W = JoinTime 200 ms) | 4.93 (7.07) | 14.28 (20.31) / 8.17 (21.00) | 78 / 142 |
| MAAP first PROBE (LINK_UP) | 0.90 (4.97) | 18.49 (38.98) **miss** / 17.04 (39.82) **miss** | 88 / 178 |
| MAAP PROBE retransmission | 1.55 (4.26) | 3.78 (10.89) / 2.96 (9.41) | 37 / 44 |
| MAAP PROBE retransmission | 1.86 (3.92) | 1.40 (8.20) / 1.67 (5.08) | 37 / 38 |
| MAAP last PROBE | 1.24 (4.23) | 3.92 (8.86) / 2.64 (9.41) | 64 / 65 |
| MAAP ANNOUNCE | 1.50 (4.23) | 4.17 (8.86) / 2.90 (9.41) | 64 / 65 |
| MAAP conflicting PROBE -> DEFEND | 0.71 (2.02) | 1.72 (8.05) / 1.97 (8.23) | 47 / 48 |

### Backlog rows

| Backlog row ([`MAILBOX_SPLIT.md:753-758`](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency)) | Desk bound, accesses IF=1 / IF=2 | A: 1x1 ms (bound) | A: 8x8 ms (bound) | B: 1x1 | B: 8x8 |
|---|---:|---:|---:|---:|---:|
| an event behind 15 others | 10,569 / 13,287 | 14.12 (27.14) **miss** | 40.51 (67.64) **miss** | 14.12 (27.14) **miss** | 40.51 (67.64) **miss** |
| an ACMP command behind a full acmp ring | 38,753 / 48,719 | 60.35 (67.08) **over ceiling** | 101.98 (113.42) **over ceiling** | 60.36 (67.08) **over ceiling** | 101.98 (113.42) **over ceiling** |
| an ENTITY_AVAILABLE behind a full adp ring | 77,506 / 97,438 | 43.90 (52.85) **over ceiling** | 48.63 (65.42) **over ceiling** | 7.90 (9.79) | 15.28 (22.85) **miss** |
| a response with 7 frames owed ahead of it | 31,707 / 39,861 | 75.76 (78.70) **over ceiling** | 98.93 (106.92) **over ceiling** | 75.78 (78.72) **over ceiling** | 98.93 (106.92) **over ceiling** |
| the same, from the moment the room returns | - | 15.76 | 38.93 | - | - |

The desk bounds charge every pass with every term at once, at a full ring of the smallest records.
The fabric admits less: each channel's token-bucket burst or its ring's room, whichever is smaller (`scenario.admitted`).
That is 8 ADP records (the desk counts 42), 12 GET_RX_STATE commands (19), 16 AECP commands and 7 MAAP records.
Each row's input is the last of its channel's admitted burst, with 15 grandmaster changes in the event ring and every other channel's burst arriving too.
The owed-frame row fills the ACMP transmit ring with the egress held, then owes eight more responses.
Arm B equals arm A here except for the bound-talker row: the other rows bind no sink, so no retry runs.

## Findings

**The rows miss T_svc, so this lane stops** ([owner decision D4](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409738976)).

- Per-pass CPU work, not mailbox accesses, sets the time.
  A 1x1 pass that takes one event record makes 15 mailbox accesses, 135 of its 89,773 cycles.
  [`MAILBOX_SPLIT.md:753-758`](../../../docs/design/MAILBOX_SPLIT.md#acmp-service-latency) allows each row 0.10 to 0.94 us an access to fit T_svc.
  The measured access is 0.18 us, inside every allowance but the full-ADP-ring row's; the passes around the accesses are 1.3 to 60 ms.
- The single passes break the [#397 one-hart rule](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5857491046).
  A pass is the loop's only opportunity to take an input, and the smallest deadline every duty shares is T_svc.
  The composed maximum is 27.83 ms (arm A) and 13.70 ms (arm B) at 1x1, 42.82 and 26.04 ms at 8x8, and the 8x8 link-up pass is 40.09 ms.
- An input waits for the pass that is running and then for the pass that takes it.
  So T_svc needs every pass well under 5 ms.
  At 8x8 the idle pass is already 2.0 to 3.7 ms, and LINK_UP, LINK_DOWN, SRP's startup and MAAP's first PROBE miss outright.
- **For D4 (a), a per-pass cap**, the measured consumers are, in order:
  - `memset` and `memcpy`, byte loops on RV32I: each AECP response zeroes its 1,514-byte frame (`aecp.c:58`) and the 1,476-byte payload in it (`aecp_commands.c:555`), and a 1x1 READ_DESCRIPTOR pass spends 153,929 to 156,240 cycles (3.1 ms) in `memset`;
  - lwSRP's link reset and declarations (`mrp_mad`), 474,000 cycles in the 8x8 link-up pass;
  - AECP's two polls, about 47,000 cycles of every 1x1 pass and 94,000 at 8x8;
  - software multiply and divide, the RV32I core having no M extension.
- **For D4 (b), the admitted backlog**: the token buckets already admit 8, 12, 16 and 7 records, not the desk's full rings.
  Fewer would shorten the ring rows by whole passes, but no backlog change shortens a single 40 ms pass.
- **The fixture's AECP retries every millisecond.**
  For each pending change notice, `aecp.c:461-495` builds the response and, when the observation port reports unavailable, sets `retry_at = a->now + 1u`.
  The fixture's ports always report unavailable, so after a bind every pass rebuilds the notices: 1.06 to 1.55 M cycles, 21 to 31 ms.
  Arm B, whose callbacks answer, takes the same H-DISC paths in 0.35 to 0.99 ms at 1x1.
  The retry has no backoff, so a real port that reports unavailable would do the same.

**D5, the smaller core** (deferred until after the flip): the shipping core already misses at both points, so a slower core would miss by more until S2b's per-pass cap lands.

**D3, the hybrid XIP split:**

- A fetch from block RAM costs 9.1 CPU cycles.
  A read through the flash window costs 263 on average, about 29 times as much, on the 1x SPI the product configures.
- The core is fetch-bound, so code executing from flash would run roughly that much slower: no path inside T_svc can be fetched from flash.
- The image fetches 11,160 B of code before the mailbox opens (11,396 B at 8x8) and at least 40,532 B after it (43,060 B at 8x8), of 85,912 and 87,596 B of `.text`.
  The service figure is the largest single run, so it is a lower bound for the hot set S14 must keep in block RAM.

**Defects the measurement found**, each for its own issue:

1. **The split image cannot run on the CPU the split SoC builds.**
   The generator decodes a region whose size is not a power of two wrongly.
   For the 224 KiB `rom` at 0 its fetch and load checks are `(address & 0xfffc8000) == 0`, which excludes every address with bit 15 set.
   Generated from the shipping split region list it is the same.
   The image's first call above 0x8000 (`jal aecp_image_load`, 0x6880 to 0xb1ec) takes an instruction access fault, cause 1, traps to 0 and restarts, forever.
   M8a-2's boot needs `rom` and `sram` at a power-of-two size in the CPU's region list, or a generator fix.
2. **The linked image addresses placeholders**, not the split SoC (the address table above).
   S3's target firmware owns the real addresses.
3. **#723 is open**: the runtime recipe builds without `-fno-stack-protector` and the image does not link.
   [`runtime_ssp.py`](runtime_ssp.py) runs it unchanged with that one flag.

## Controls and self-test

`run.py --self-test` regrades the committed trace [`fixture.log`](fixture.log), which the `fixture` group recorded at 1x1, against [`oracle.json`](oracle.json).
Its checks:

- the fixture's digest and each of its seven rows;
- the clock conversion, 1,000,000 bus cycles being 500,000 CPU cycles and 10 ms;
- the ceilings and T_svc, restated in [`selftest.py`](selftest.py) so a changed table fails;
- an exact-budget path passes and one bus cycle more misses;
- the probe's own tagged frame starts it, not an earlier frame on the ring;
- a response to another sequence_id, or on the other interface, does not end it;
- the last required output ends a path;
- a timer path starts at its armed deadline, not when its record is posted;
- W + T_svc passes, and one cycle more misses;
- a planted over-budget path: the recorded BIND_RX response moved past T_svc must miss.

Then it mutates each grader rule and requires a named check to fail:

| Mutant | Caught by |
|---|---|
| marker: the frame tag is ignored | tagged start |
| marker: a timer path starts when its record is posted | fixture row `fixture.tmr_no_resp1.if0` |
| marker: any response on the channel ends the path | sequence and interface |
| marker: the interface is ignored | sequence and interface |
| marker: the first required output ends the path | fixture row `fixture.set_name.if0` |
| clock ratio: CPU cycles equal bus cycles | fixture row `fixture.link_up.if0` |
| clock ratio: inverted | fixture row `fixture.link_up.if0` |
| clock ratio: milliseconds from the CPU clock | fixture row `fixture.link_up.if0` |
| deadline: T_svc 20 ms | ceilings pinned |
| deadline: strictly below the budget | exact budget passes |
| deadline: the normative wait is not added | W + T_svc passes |
| deadline: the ACMP ceiling is the transaction timeout | ceilings pinned |

Regenerate the fixture only through its generator, from a fresh 1x1 run of the `fixture` group:

```sh
python3 -B tb/verilator/ctrl_service_budget/selftest.py --write-fixture RESULTS/fixture.log BUILD/build.json
```

Two controls run the full harness:

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-slow-adp --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 \
  --build-dir /tmp/budget-as-built --cpu-regions as-built
```

`slow-adp-rx` builds a scratch copy of the firmware whose ADP receive handler spins first.
The `control` group's RCV_ADP_DISCOVER must miss T_svc: it measures 24.614 ms, and the run prints `CONTROL slow-adp-rx caught`.
The ordinary image measures the same path at 0.294 ms.
`as-built` hands the generator the SoC's regions unchanged.
The run must refuse the boot with an instruction access fault, cause 1, and prints `CONTROL as-built caught`.

## Limits

- One phase is measured per probe; the pass bound covers any phase under the same passes, not other loads.
- SHUTDOWN has no input in the fixture, and START_STREAMING calls a port the fixture leaves empty, so neither is run.
- The fixture's sources are never allocated, so a Listener Ready grants no licence; that path ends at the record's release.
- Ends are mailbox commits; wire departure, ingress, egress and the network (H-ACMP's round trip) are not measured.
- The flash's erase and program waits are zero, so F1's commit is measured as CPU work only; S4 owns the target port.
- There is no datapath, no DDR3 and no packet traffic besides the stimulus; the CPU's DMA port is idle.
- The firmware polls (`CTRL_MBX_WFI` undefined), as the fixture is linked.
- The two-interface fixture gives both interfaces the same MAC, as `ctrl_aecp_image.c` does.

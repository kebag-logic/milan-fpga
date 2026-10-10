# Mark II area plan

Stage 1 of [#640](https://github.com/kebag-logic/milan-fpga/issues/640) plans the [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) redesign.
Round 1d uses records committed on dev `5603c353`.
It incorporates the [recorded decisions](#recorded-decisions).
The original 2026-10-05 inventory remains labelled measurement history.
This stage changes documentation only.
Milestone 12 precedes P3, with delivery planned by 2026-12-15.
The [#396](https://github.com/kebag-logic/milan-fpga/issues/396) release campaigns run on the qualified redesigned image.

## Contents

- **[Summary](#summary)** -- The recorded baseline, split estimate, remaining savings and qualification risk.
- **[Target](#target)** -- The LUT bar, accepted margin, timing requirements and delivery date.
- **[Baseline recorded on dev 5603c353](#baseline-recorded-on-dev-5603c353)** -- The committed endpoint records and their measured source revision.
- **[Baseline at dev e6172750](#baseline-at-dev-e6172750)** -- Historical measurements and hierarchy from the original plan.
- **[Inventory](#inventory)** -- Historical hierarchy functions, clauses, construction and implementation choices.
- **[Levers](#levers)** -- Twelve levers, each with its saving and basis, risk, verification cost and protocol-visible effect.
- **[Ledger](#ledger)** -- Disjoint split removal references, measured replacement cost and cumulative estimates.
- **[Lane sequence](#lane-sequence)** -- The ordered lanes to 2026-12-15, each with its LUT target, repository, verification, risks and dependencies.
- **[What holds throughout](#what-holds-throughout)** -- The suites and counts, ATDECC as the only source of state, the second port, the gate's re-record and timing.
- **[Recorded decisions](#recorded-decisions)** -- The accepted rulings and the later default-split decisions that supersede the initial plan.
- **[Method and receipts](#method-and-receipts)** -- The recipe, how a head the gate does not describe is mapped, the core pricing, and every run's exit status and log digest.

## Summary

- **Recorded start:** 50,267 routed LUTs, 12,227 above 38,040.
  The [#645](https://github.com/kebag-logic/milan-fpga/issues/645)/[#647](https://github.com/kebag-logic/milan-fpga/issues/647) record already includes the third processor adoption.
  Its +0.299/+0.031 ns setup/hold slacks meet the build gate.
- **Default split:** ADP, ACMP, MAAP, SRP and AECP move to firmware.
  F1 supplies saved-state read, apply and write-back.
  Shipping defaults wait for F2-F5 suites and bench acceptance.
- **Estimated saving:** L2 credits 14,000 LUTs, range 11,500-16,000.
  This includes the measured 3,102-LUT mailbox cost.
  The complete split has no integrated area measurement yet.
- **Estimated finish:** the [ledger](#ledger) reaches 31,667 LUTs centrally.
  Its conservative combined estimate is 35,867, below 38,040.
  These arithmetic scenarios are not fit or timing evidence.
- **No double counting:** M3/M10 receive zero default-image credit.
  Their AECP hardware leaves with F5.
  M4 is replaced by the split; diagnostics remain enabled.
- **Firmware allocation:** 224 KB, budgeted at about 50 RAMB36 tiles.
  The [memory ledger](#firmware-and-block-ram-ledger) preserves the 10 percent reserve.
  Its reuse and packing assumptions require routed confirmation.
- **Qualification risk:** F5, target service timing and bench acceptance remain.
  M8's smaller core must pass capture, boot and split-load bounds.
  Every function lacking qualification retains its fabric placement.

## Target

| Item | Value |
|---|---|
| [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) ([requirements](../reference/FR_NFR.md)) | At most 38,040 LUTs, 60 percent of 63,400 |
| Planning margin, D8 | At least 1 percent below the limit: <= 37,659 LUTs |
| Timing | Shipping 50 MHz datapath; every build-gate corner WNS >= +0.030 ns and WHS >= 0 |
| Gate comparison | At the current +0.114 ns WNS record, the +0.030 ns floor binds first, after a fall of 0.084 ns; the 0.25 ns fall limit is unchanged |
| Function | Equivalent PDUs and state transactions; suites and campaigns retain their counts |
| Delivery | Milestone 12 by 2026-12-15, before P3 |

The [owner retained the 60 percent target](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967924270).
D8 replaces the initial 5 percent planning margin.
The [resource policy](AREA_BUDGET.md#the-resource-gate) remains unchanged.

## Baseline recorded on dev `5603c353`

Source: [`pp_resource_baseline.json`](../../syn/ooc/pp_resource_baseline.json), all three `record` objects.
Each `measured` note identifies `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`.
That is [#645](https://github.com/kebag-logic/milan-fpga/issues/645)/[#647](https://github.com/kebag-logic/milan-fpga/issues/647)'s measured merge of dev `6aa25dec`.
It uses processor `2ad2f845dd583f8310075fa2380cb60a04fd091a`.
Dev `5603c353137e90c1fa95429f6d00ef7a2298d9ee` carries those records unchanged.
This names the stored baseline, not a measurement of `5603c353`.
No new Vivado measurement was made for Rounds 1b-1d.

| Endpoint | LUT | FF | Slice | RAMB36 | RAMB18 | BRAM tiles | DSP | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `route-1x1` | 50,267 | 54,413 | 15,779 | 74 | 27 | 87.5 | 14 | +0.299 / +0.031 |
| `ooc-1x1` | 23,179 | 19,779 | -- | 16 | 3 | 17.5 | 8 | -3.562 / +0.159 |
| `ooc-8x8` | 30,135 | 27,380 | -- | 21 | 5 | 23.5 | 8 | -2.278 / +0.159 |

The resource records omit LUTRAM; it is not zero.
The historical inventory below retains its separately measured LUTRAM column.
Standalone timing has unconstrained I/O and proves no integrated fit.
The 8x8 row is a scaling reference, not shipping acceptance.
The route leaves 71 slices and 47.5 physical BRAM tiles.
The 121.5-tile policy ceiling leaves 34 tiles of usable allowance.

[The source receipt](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-08-issues-645-and-647)
records the completed route and all four signoff corners.
Its source checkpoint is `alinx_ax7101_route.dcp` from that measurement.
The route log SHA-256 is
`94c0471debaa23a0fd20d9050298173facb997735ffa8bbf451f68cbd82de0ac`
(829,160 bytes).
The record's input SHA-256 values bind the measurement inputs:

| Endpoint | Input SHA-256 |
|---|---|
| `route-1x1` | `95a6cc95786fa743da28e2aa603d3a6af08200c86bf4bb7c452aeba7ec072c4c` |
| `ooc-1x1` | `2dd522bd12b3480a8817cf2bb3dd969ac7be6f3d80be70d13fe32ce5576011a5` |
| `ooc-8x8` | `5604984543f875b19f344900a8b183adf81281c02ba42517ff894502f7a07f0c` |

The recipe uses Vivado 2026.1 build 6511674, `xc7a100t-fgg484-2`.
Directives: `AreaOptimized_high`, `ExploreArea`, `ExtraPostPlacementOpt`, `AggressiveExplore`.
It uses the default seed, one synthesis worker, 32 general threads.
The standalone wrapper clock is 20 ns.
The historical route below predates this synthesis-worker recipe identity.
Its deltas therefore inform planning, not a comparable gate verdict.

### Current processor inventory

These are the source-scope references of the gate's current record, [#696](https://github.com/kebag-logic/milan-fpga/issues/696)'s [re-baseline of 2026-10-10](../findings/234_PP_SHADOW_AREA_BASELINE.md#re-baseline-of-2026-10-10-issue-696).
It measured merge result `0df48637` of dev `8b61b709`, with processor `2ad2f845`.
Against the baseline above, only the route figures changed; both standalone endpoints keep every figure.
The levers and the ledger keep the baseline's route figures.
The routed hierarchy is rebuilt and can absorb neighbouring logic.
Use standalone scopes to estimate removable source functionality.
Parent rows include descendants; never add both to a saving.
The [historical inventory](#inventory) supplies functions, clauses and construction.

| Scope relative to wrapper | Route LUT | OOC 1x1 LUT | OOC 8x8 LUT | Split disposition |
|---|---:|---:|---:|---|
| `wrapper` | 22,873 | 23,179 | 30,135 | Replaced after every control function qualifies |
| `u_pp` | 22,318 | 22,517 | 28,938 | Control functions move; retained fabric interfaces are reconnected |
| `u_pp/u_aecp` | 7,733 | 6,150 | 7,298 | F5; includes the following five children |
| `u_pp/u_aecp/u_d3` | 1,871 | 1,703 | 2,297 | F1/F5 saved-state ownership |
| `u_pp/u_aecp/u_dyn` | 1,054 | 134 | 497 | F5; fabric media state stays authoritative |
| `u_pp/u_aecp/u_store` | 979 | 1,026 | 1,119 | F5 validated image and names |
| `u_pp/u_aecp/u_ucpu` | 1,763 | 1,553 | 1,651 | F5; no second M10 credit |
| `u_pp/u_aecp/u_resp` | 339 | 432 | 416 | F5 response serving |
| `u_pp/u_notify` | 2,199 | 2,125 | 2,114 | F5 registry, notification and counter serving |
| `u_pp/u_srp` | 3,639 | 3,868 | 7,312 | F4; media admission enforcement remains in fabric |
| `u_pp/u_srp/u_encoder` | 1,355 | 1,479 | 1,466 | Included in SRP |
| `u_pp/u_srp/u_decoder` | 580 | 588 | 922 | Included in SRP |
| `u_pp/u_listener` | 1,451 | 1,560 | 1,681 | F3 ACMP listener |
| `u_pp/u_talker` | 664 | 823 | 1,472 | F3 ACMP talker |
| `u_pp/u_adp` | 384 | 523 | 696 | F0/F3 advertisement and discovery |
| `u_pp/u_originator` | 688 | 697 | 682 | F3/F5 originated transactions |
| `u_pp/u_nvm_shadow` | 791 | 808 | 780 | F1/F3 binding persistence |
| `u_pp/u_nvm_port` | 513 | 526 | 524 | F1 store and flash service |
| `u_nvm` | 488 | 581 | 1,116 | F1 replaces container backend |
| `u_pp/u_timer` | 881 | 906 | 1,631 | Hard deadlines remain fabric events; no saving credited |
| `u_pp/u_dispatch` | 666 | 887 | 908 | Replaced routing; no separate credit |
| `u_pp/u_trace` | 31 | 37 | 28 | Equivalent diagnostics retained; no credit |

The [#232](https://github.com/kebag-logic/milan-fpga/issues/232) registry, [#230](https://github.com/kebag-logic/milan-fpga/issues/230) SRP storage and [#639](https://github.com/kebag-logic/milan-fpga/issues/639) rings/listener changes
are already included; their savings cannot be subtracted again.
[#686](https://github.com/kebag-logic/milan-fpga/issues/686) also changed MAAP, before [#645](https://github.com/kebag-logic/milan-fpga/issues/645)/[#647](https://github.com/kebag-logic/milan-fpga/issues/647) refreshed the record.
[#696](https://github.com/kebag-logic/milan-fpga/issues/696) changed MAAP again before the current record.

## Baseline at dev `e6172750`

**Historical measurement, 2026-10-05.**
The tables in this section are not the Round 1b baseline.


### What changed since the gate's record

At `e6172750`, the gate's record described dev `54643724`.
The [budget](AREA_BUDGET.md#the-resource-gate) now holds a later record.
Since then dev changed one shipping-image input functionally: [`KL_crf_rx.sv`](../../hdl/ieee1722/crf/KL_crf_rx.sv) now scores a locked CRF input's unbind as one MEDIA_UNLOCKED ([#653](https://github.com/kebag-logic/milan-fpga/issues/653)).
[`KL_nvm_backend.sv`](../../hdl/milan/KL_nvm_backend.sv) gained a named constant with no logic, [`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv) a comment, the builder a generation-time refusal ([#652](https://github.com/kebag-logic/milan-fpga/issues/652)), and [`syn/ooc/pp_baseline.py`](../../syn/ooc/pp_baseline.py) the `--integrated-clock` option.
No routed checkpoint of this tree existed on the host: the checkpoints there were processor-lane scratch parents and the in-flight second pin adoption.
So the shipping image was routed again here with the [#234 recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md), and `KL_pp_shadow` was synthesized out of context at 1x1.

### The routed shipping image

| Measurement | LUT | LUTRAM | FF | Slice | RAMB36 | RAMB18 | BRAM tiles | DSP | CARRY4 | WNS ns | WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Gate record, dev `54643724` | 50,767 | - | 59,634 | 15,832 | 79 | 27 | 92.5 | 14 | 3,506 | +0.193 | +0.024 |
| This head, dev `e6172750` | 50,702 | 2,228 | 59,677 | 15,828 | 79 | 27 | 92.5 | 14 | 3,506 | +0.244 | +0.036 |
| This head minus the record | -65 | - | +43 | -4 | 0 | 0 | 0 | 0 | 0 | +0.051 | +0.012 |
| This head, percent of `xc7a100t` | 79.97 | - | 47.06 | 99.86 | 58.52 | 10.00 | 68.52 | 5.83 | - | - | - |

Against the gate's record the route exits 0 (`pp_resource_gate.py check --endpoint route-1x1`): 65 fewer LUTs, 43 more FFs and 4 fewer slices, block RAM and DSP unchanged, every routable net routed (106,639 of 106,639, none with a routing error).
All four signoff corners meet the [build gate](../integration/BUILDING.md#5-gates-before-a-build-is-good): the worst setup slack is +0.244 ns at the slow corners and the worst hold slack +0.036 ns at the fast corners.
The wrapper moved by +147 LUTs although no wrapper source changed: optimization moving with an unrelated change, which the gate prints without gating ([budget](AREA_BUDGET.md#the-resource-gate)).
The critical path starts at `u_pp/u_rx_validator/hdr_ctlr_eid_r_reg[11]` and ends at `u_pp/u_tx_arbiter`: 39 logic levels and 19.443 ns, 73 percent of it routing, inside the processor.
At `e6172750`, 22 slices were free.
Placement was the binding limit at that checkpoint.

### The routed hierarchy

The rebuilt hierarchy after cross-boundary optimization: its names describe placement, not source ownership, as the [#649 map](../findings/649_RESOURCE_MAP_AND_SENSITIVITY.md#the-map) explains.
LUT counts a LUT site that holds cells of two children once in each, so a parent can be smaller than the sum of its children.
Every row below is read from the map, which ties the image's totals to the route's own reports.
BRAM is in tiles, a RAMB36 counting one and a RAMB18 half.

| Scope | Block | LUT | LUTRAM | FF | RAMB36 | RAMB18 | BRAM tiles | DSP | LUT % of image |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| (image) | Whole image | 50,702 | 2,228 | 59,677 | 79 | 27 | 92.5 | 14 | 100.00 |
| `@own` | SoC: the LiteX top's own logic | 4,833 | 294 | 6,072 | 47 | 10 | 52 | 0 | 9.53 |
| `VexiiRiscvLitex_*` | SoC: the control hart | 3,522 | 122 | 4,736 | 2 | 5 | 4.5 | 0 | 6.95 |
| `KL_gptp_gmii_launch` | SoC: gPTP GMII launch | 186 | 0 | 317 | 0 | 0 | 0 | 0 | 0.37 |
| `KL_mac_rmon_events` | SoC: MAC event counters | 49 | 0 | 78 | 0 | 0 | 0 | 0 | 0.10 |
| `milan_datapath` | The datapath (non-CPU stack) | 42,138 | 1,812 | 48,474 | 30 | 12 | 36 | 14 | 83.11 |
| `milan_datapath/pp_shadow` | The protocol processor wrapper | 24,051 | 1,108 | 24,263 | 21 | 3 | 22.5 | 8 | 47.44 |
| `milan_datapath/pp_shadow/u_pp` | Processor top | 23,480 | 1,108 | 23,433 | 20 | 2 | 21 | 4 | 46.31 |
| `milan_datapath/pp_shadow/u_pp/u_srp` | SRP | 4,219 | 180 | 6,264 | 0 | 1 | 0.5 | 2 | 8.32 |
| `milan_datapath/pp_shadow/u_pp/u_srp/u_encoder` | SRP encoder | 1,320 | 168 | 1,062 | 0 | 0 | 0 | 0 | 2.60 |
| `milan_datapath/pp_shadow/u_pp/u_srp/@own` | SRP glue and timer FIFOs | 862 | 0 | 2,792 | 0 | 0 | 0 | 0 | 1.70 |
| `milan_datapath/pp_shadow/u_pp/u_srp/u_talker` | SRP talker FSMs | 612 | 0 | 672 | 0 | 0 | 0 | 0 | 1.21 |
| `milan_datapath/pp_shadow/u_pp/u_srp/u_decoder` | SRP decoder | 584 | 0 | 630 | 0 | 1 | 0.5 | 0 | 1.15 |
| `milan_datapath/pp_shadow/u_pp/u_srp/u_listener` | SRP listener FSMs | 419 | 0 | 667 | 0 | 0 | 0 | 0 | 0.83 |
| `milan_datapath/pp_shadow/u_pp/u_srp/u_admission` | SRP admission | 223 | 0 | 207 | 0 | 0 | 0 | 2 | 0.44 |
| `milan_datapath/pp_shadow/u_pp/u_aecp` | AECP engine | 7,451 | 218 | 3,500 | 6 | 0 | 6 | 1 | 14.70 |
| `milan_datapath/pp_shadow/u_pp/u_aecp/@own` | AECP dispatch and framing | 1,798 | 0 | 1,099 | 1 | 0 | 1 | 0 | 3.55 |
| `milan_datapath/pp_shadow/u_pp/u_aecp/u_ucpu` | AECP micro-coded engine | 1,720 | 132 | 495 | 3 | 0 | 3 | 0 | 3.39 |
| `milan_datapath/pp_shadow/u_pp/u_aecp/u_d3` | AECP saved-state writer | 1,405 | 0 | 485 | 0 | 0 | 0 | 0 | 2.77 |
| `milan_datapath/pp_shadow/u_pp/u_aecp/u_dyn` | AECP dynamic state | 1,265 | 0 | 467 | 0 | 0 | 0 | 0 | 2.49 |
| `milan_datapath/pp_shadow/u_pp/u_aecp/u_store` | AECP descriptor store | 974 | 86 | 694 | 2 | 0 | 2 | 1 | 1.92 |
| `milan_datapath/pp_shadow/u_pp/u_aecp/u_resp` | AECP response buffer | 334 | 0 | 260 | 0 | 0 | 0 | 0 | 0.66 |
| `milan_datapath/pp_shadow/u_pp/u_notify` | Notification, registry, lock | 3,118 | 96 | 3,299 | 0 | 0 | 0 | 0 | 6.15 |
| `milan_datapath/pp_shadow/u_pp/u_listener` | ACMP listener | 1,414 | 0 | 1,110 | 5 | 0 | 5 | 0 | 2.79 |
| `milan_datapath/pp_shadow/u_pp/u_talker` | ACMP talker | 689 | 56 | 517 | 0 | 0 | 0 | 0 | 1.36 |
| `milan_datapath/pp_shadow/u_pp/u_adp` | ADP | 442 | 48 | 471 | 0 | 0 | 0 | 1 | 0.87 |
| `milan_datapath/pp_shadow/u_pp/u_originator` | Originator | 721 | 20 | 885 | 0 | 0 | 0 | 0 | 1.42 |
| `milan_datapath/pp_shadow/u_pp/u_timer` | Timer service | 884 | 0 | 179 | 1 | 0 | 1 | 0 | 1.74 |
| `milan_datapath/pp_shadow/u_pp/u_dispatch` | Dispatch queues | 775 | 392 | 635 | 0 | 0 | 0 | 0 | 1.53 |
| `milan_datapath/pp_shadow/u_pp/u_nvm_shadow` | ACMP binding store | 790 | 98 | 1,118 | 0 | 0 | 0 | 0 | 1.56 |
| `milan_datapath/pp_shadow/u_pp/u_nvm_port` | NVM port | 439 | 0 | 127 | 0 | 0 | 0 | 0 | 0.87 |
| `milan_datapath/pp_shadow/u_pp/u_rx_validator` | RX validator | 543 | 0 | 751 | 0 | 1 | 0.5 | 0 | 1.07 |
| `milan_datapath/pp_shadow/u_pp/u_tx_slots` | TX slots | 341 | 0 | 135 | 1 | 0 | 1 | 0 | 0.67 |
| `milan_datapath/pp_shadow/u_pp/u_tx_arbiter` | TX arbiter | 200 | 0 | 182 | 0 | 0 | 0 | 0 | 0.39 |
| `milan_datapath/pp_shadow/u_pp/@own` | Processor top's own logic | 419 | 0 | 3,084 | 0 | 0 | 0 | 0 | 0.83 |
| `milan_datapath/pp_shadow/u_nvm` | Saved-state backend | 504 | 0 | 476 | 0 | 0 | 0 | 4 | 0.99 |
| `milan_datapath/g_gptp_plane.u_gptp_shadow` | gPTP plane | 4,999 | 508 | 5,899 | 3 | 3 | 4.5 | 4 | 9.86 |
| `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine` | gPTP engine | 3,804 | 464 | 3,638 | 1 | 1 | 1.5 | 4 | 7.50 |
| `milan_datapath/g_gptp_plane.u_gptp_shadow/u_engine/u_ucpu` | gPTP micro-coded engine | 2,083 | 132 | 728 | 1 | 1 | 1.5 | 4 | 4.11 |
| `milan_datapath/csr` | CSR plane | 2,907 | 0 | 2,141 | 0 | 2 | 1 | 0 | 5.73 |
| `milan_datapath/chan_map_capture` | Channel map, capture | 1,076 | 0 | 1,321 | 1 | 0 | 1 | 0 | 2.12 |
| `milan_datapath/g_mmcm_servo.mmcm_servo` | Media-clock servo | 899 | 0 | 814 | 0 | 0 | 0 | 0 | 1.77 |
| `milan_datapath/avtp_rx_monitor` | Stream Input counters | 942 | 0 | 1,353 | 0 | 1 | 0.5 | 0 | 1.86 |
| `milan_datapath/aaf_latency_tap_bank` | Latency taps (diagnostic) | 672 | 0 | 620 | 0 | 0 | 0 | 0 | 1.33 |
| `milan_datapath/aaf_packetizer` | AAF packetizer | 650 | 0 | 1,331 | 1 | 1 | 1.5 | 0 | 1.28 |
| `milan_datapath/@own` | Datapath's own logic | 562 | 0 | 2,850 | 0 | 0 | 0 | 0 | 1.11 |
| `milan_datapath/g_rx_filter.rx_filter` | RX address filter | 513 | 0 | 1,570 | 0 | 0 | 0 | 0 | 1.01 |
| `milan_datapath/avtp_rx_parser` | AVTP stream parser | 474 | 0 | 706 | 0 | 0 | 0 | 0 | 0.93 |
| `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render` | TDM render lane | 499 | 0 | 623 | 3 | 0 | 3 | 0 | 0.98 |
| `milan_datapath/g_aaf_meter.aaf_clock_meter` | AAF clock meter | 488 | 32 | 630 | 0 | 0 | 0 | 0 | 0.96 |
| `milan_datapath/g_maap.maap_engine` | MAAP | 519 | 0 | 267 | 0 | 0 | 0 | 0 | 1.02 |
| `milan_datapath/render_setpoint` | Render set-point | 356 | 128 | 137 | 0 | 0 | 0 | 0 | 0.70 |
| `milan_datapath/media_grid_align` | Media grid align | 370 | 0 | 107 | 0 | 0 | 0 | 0 | 0.73 |
| `milan_datapath/crf_tx` | CRF talker | 313 | 0 | 311 | 0 | 0 | 0 | 1 | 0.62 |
| `milan_datapath/crf_rx` | CRF listener | 241 | 0 | 542 | 0 | 1 | 0.5 | 0 | 0.48 |
| `milan_datapath/talker_diag` | Stream Output counters | 136 | 0 | 359 | 0 | 0 | 0 | 0 | 0.27 |

### `KL_pp_shadow` at 1x1, out of context

The standalone synthesis attributes the wrapper in source terms, at the build's 20 ns clock ([recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md#standalone-measurements)).

| Sub-block | Instances | LUT | LUTRAM | FF | RAMB36 | RAMB18 | DSP |
|---|---|---:|---:|---:|---:|---:|---:|
| Wrapper total | `wrapper` | 24,332 | 1,242 | 25,345 | 21 | 3 | 8 |
| SRP | `u_pp/u_srp` | 4,573 | 186 | 6,439 | 0 | 1 | 2 |
| SRP talker FSMs | `u_pp/u_srp/u_talker` | 662 | 0 | 714 | 0 | 0 | 0 |
| SRP listener FSMs | `u_pp/u_srp/u_listener` | 420 | 0 | 667 | 0 | 0 | 0 |
| SRP encoder | `u_pp/u_srp/u_encoder` | 1,461 | 174 | 1,086 | 0 | 0 | 0 |
| SRP decoder | `u_pp/u_srp/u_decoder` | 589 | 0 | 630 | 0 | 1 | 0 |
| SRP admission | `u_pp/u_srp/u_admission` | 337 | 0 | 271 | 0 | 0 | 2 |
| ADP | `u_pp/u_adp` | 628 | 48 | 479 | 0 | 0 | 1 |
| ACMP talker | `u_pp/u_talker` | 894 | 56 | 551 | 0 | 0 | 0 |
| ACMP listener | `u_pp/u_listener`, `u_pp/u_lsn_admit` | 1,441 | 0 | 1,111 | 5 | 0 | 0 |
| AECP engine, total | `u_pp/u_aecp` | 5,598 | 220 | 3,500 | 6 | 0 | 1 |
| AECP dispatch and framing (own logic) | `u_pp/u_aecp/@own` | 1,416 | 0 | 1,098 | 1 | 0 | 0 |
| AECP micro-coded engine | `u_pp/u_aecp/u_ucpu` | 1,608 | 132 | 495 | 3 | 0 | 0 |
| AECP saved-state writer | `u_pp/u_aecp/u_d3` | 1,066 | 0 | 485 | 0 | 0 | 0 |
| AECP dynamic state | `u_pp/u_aecp/u_dyn` | 152 | 0 | 468 | 0 | 0 | 0 |
| AECP descriptor store | `u_pp/u_aecp/u_store` | 1,030 | 88 | 694 | 2 | 0 | 1 |
| AECP response buffer | `u_pp/u_aecp/u_resp` | 346 | 0 | 260 | 0 | 0 | 0 |
| Notification, registry and lock | `u_pp/u_notify` | 3,175 | 96 | 3,299 | 0 | 0 | 0 |
| Originator | `u_pp/u_originator` | 782 | 20 | 885 | 0 | 0 | 0 |
| Timer service | `u_pp/u_timer` | 910 | 0 | 179 | 1 | 0 | 0 |
| Dispatch queues | `u_pp/u_dispatch` | 896 | 516 | 815 | 0 | 0 | 0 |
| RX validator | `u_pp/u_rx_validator` | 538 | 0 | 789 | 0 | 1 | 0 |
| NVM port | `u_pp/u_nvm_port` | 452 | 0 | 127 | 0 | 0 | 0 |
| NVM manager arbiter | `u_pp/u_nvm_arb` | 13 | 0 | 4 | 0 | 0 | 0 |
| ACMP binding store | `u_pp/u_nvm_shadow` | 815 | 100 | 1,118 | 0 | 0 | 0 |
| Saved-state backend (wrapper) | `u_nvm` | 592 | 0 | 476 | 0 | 0 | 4 |
| Packet storage: RX pools | `u_pp/g_rx_pool[*].u_rx_slots` | 252 | 0 | 206 | 5 | 0 | 0 |
| Packet storage: TX slots | `u_pp/u_tx_slots` | 347 | 0 | 138 | 1 | 0 | 0 |
| TX arbiter | `u_pp/u_tx_arbiter` | 208 | 0 | 187 | 0 | 0 | 0 |
| Trace ring (diagnostic) | `u_pp/u_trace` | 37 | 0 | 18 | 1 | 0 | 0 |
| Processor top's own logic | `u_pp/@own` | 432 | 0 | 3,170 | 0 | 0 | 0 |
| Control-frame FIFO (wrapper) | `ctl_fifo` | 79 | 0 | 33 | 1 | 1 | 0 |

The run equals the gate's `ooc-1x1` record in every gated figure (`check --endpoint ooc-1x1` exits 0 with no movement): no wrapper input changed since dev `54643724`, and its sub-blocks match the [#234](https://github.com/kebag-logic/milan-fpga/issues/234) page's combination C.
The historical routed wrapper was 0.988 of it (24,051 LUTs).
Round 1b does not reuse that ratio as a calibration.
The two hierarchies attribute differently: the AECP dynamic-state store is 152 LUTs here and 1,265 in the routed hierarchy, which places other AECP logic under its name.

### After the second pin adoption

The second pin adoption ([#661](https://github.com/kebag-logic/milan-fpga/issues/661)) moves the processor to `ead80360`, which carries [#232](https://github.com/kebag-logic/milan-fpga/issues/232), [#230](https://github.com/kebag-logic/milan-fpga/issues/230) and [#639](https://github.com/kebag-logic/milan-fpga/issues/639).
Its lane published its measured image on 2026-10-05 ([REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5990292142), head `42f65447`, on dev `506d91db`, which already carries [#653](https://github.com/kebag-logic/milan-fpga/issues/653)).
That evidence was under review when the original plan was written.
The later adopted records are in the current baseline above.

| Endpoint | LUT | FF | Slice | RAMB36 | WNS / WHS ns | Against the gate's record |
|---|---:|---:|---:|---:|---:|---|
| Route, second pin ([#661](https://github.com/kebag-logic/milan-fpga/issues/661)) | 50,318 | 54,214 | 15,789 | 74 | +0.108 / +0.036 | -449 LUT, -5,420 FF, -43 slices, -5 RAMB36 |
| Route, this head | 50,702 | 59,677 | 15,828 | 79 | +0.244 / +0.036 | -65 LUT, +43 FF, -4 slices |
| Standalone 1x1, second pin ([#661](https://github.com/kebag-logic/milan-fpga/issues/661)) | 23,178 | 19,776 | - | - | - | -1,154 LUT, -5,569 FF |
| Standalone 8x8, second pin ([#661](https://github.com/kebag-logic/milan-fpga/issues/661)) | 29,853 | 27,370 | - | - | - | -1,703 LUT, -6,567 FF |

So the adoption moves the route by -384 LUTs against this head and leaves 61 slices free.
The three area lanes' own routes, each measured against one base route with the C8, P2-P1 and C10 parent patches, explain most of it:

| Change | Base route LUT / FF | Head route LUT / FF | LUT change | FF change | Other |
|---|---:|---:|---:|---:|---|
| Processor `main` before the area lanes, with the parent patches, against the gate's record | 50,767 / 59,634 | 51,434 / 59,691 | +667 | +57 | C7, C8, P1, P2, [#143](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/143), C10 |
| [#232](https://github.com/kebag-logic/milan-fpga/issues/232), notification registry in distributed RAM (processor PR [#153](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/153)) | 51,434 / 59,691 | 50,671 / 57,660 | -763 | -2,031 | `u_notify` -927 LUT |
| [#230](https://github.com/kebag-logic/milan-fpga/issues/230), SRP timer FIFOs and walk storage (processor PR [#154](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/154)) | 51,434 / 59,691 | 51,005 / 57,262 | -429 | -2,429 | `u_srp` 4,340 to 3,711 LUT |
| [#639](https://github.com/kebag-logic/milan-fpga/issues/639), timer-arm rings and listener records (processor PR [#155](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/155)) | 51,434 / 59,691 | 51,152 / 58,598 | -282 | -1,093 | RAMB36 79 to 74 |
| The three added, as a projection | | 49,960 / 54,138 | -807 against the record | | |

The measured adoption is 358 LUTs and 76 FFs above that projection: the lanes' deltas do not add exactly, and processor PRs [#152](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/152) (tests) and [#157](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/pull/157) (one GET_DYNAMIC_INFO classifier hunk) were in none of those routes.
The original ledger started from 50,318.
The [current ledger](#ledger) starts from the committed 50,267 record.

## Inventory

**Historical source inventory at `e6172750`.**
The clauses and implementation choices remain reference material.
Current measured processor costs appear in the current baseline above.
The split changes ownership as recorded in L2; standards stay binding.

Every hierarchy of the routed image above 500 LUTs, in the rebuilt hierarchy's names; the image itself is left out, and a parent whose only large child is that child shares its row.
"Set by the standard" is the part of the cost a Milan or IEEE clause fixes: a state machine's existence, a field's width, a count's minimum.
"Implementation choice" is the part this design chose: how state is stored, how many copies of the logic exist, how wide an internal path is.
Clauses are IEEE 1722.1-2021, IEEE 1722-2016, IEEE 802.1Q-2018, IEEE 802.1AS-2011 and Milan v1.2.

**Protocol processor**

| Hierarchy | LUT | FF | Protocol function and clause | How it is built | Set by the standard | Implementation choice |
|---|---:|---:|---|---|---|---|
| `milan_datapath` | 42,138 | 48,474 | the whole fabric endpoint below the SoC: the protocol processor, the gPTP plane, AVTP/AAF/CRF media, the CSR plane | one module with the blocks below and its own per-stream registers | see the blocks | see the blocks |
| `milan_datapath/pp_shadow` | 24,051 | 24,263 | The ATDECC entity: ADP, ACMP, AECP, SRP, the saved-state backend (1722.1 clauses 6 to 9; Milan v1.2 Sections 4.2.7 and 5) | `KL_pp_shadow` around `protocol_processor_top`, the NVM backend and the control-frame FIFO | the protocols and their state | one engine per protocol, contexts per stream |
| `.../pp_shadow/u_pp` | 23,480 | 23,433 | `protocol_processor_top`: every engine below, the packet engine and the timer-arm queues | one engine per protocol around a shared RX parser, TX slot pool and timer service | the protocols | one engine per protocol; its own logic holds the timer-arm queues in flip-flops at this head ([#639](https://github.com/kebag-logic/milan-fpga/issues/639) moves them to distributed RAM) |
| `.../u_pp/u_aecp` | 7,451 | 3,500 | AECP AEM commands and responses (1722.1 clauses 7.4 and 9; Milan v1.2 Section 5.4) | a dispatch cone, the micro-coded engine, the dynamic-state store, the descriptor store over DRAM, the saved-state writer and the response-buffer DMA | the served command set, the response formats, the dynamic state Milan lets a controller set | the dispatch decode in logic, dynamic state in flip-flops |
| `.../u_aecp/@own` | 1,798 | 1,099 | command dispatch and AECPDU framing | a pop-time opcode decode feeding the microcode address, operand staging and the TX slot writer | the opcode set and PDU layout | the decode as a logic cone rather than a dispatch ROM |
| `.../u_aecp/u_ucpu` | 1,720 | 495 | executes every AEM command's microprogram | four-stage pipeline, 16 x 64 operand file in distributed RAM, 2,048 x 48 microcode in three RAMB36 | none | the engine itself: it is the time-multiplexed form L1 extends |
| `.../u_aecp/u_d3` | 1,405 | 485 | saving and restoring the non-binding dynamic state (Milan v1.2 Sections 5.3.5.1, 5.3.7.1, 5.3.8.1, 5.3.11.1) | a hardwired record writer per group with debounce, framing and restore transaction | which values survive power loss | a second record manager beside the binding manager, hardwired |
| `.../u_aecp/u_dyn` | 1,265 | 467 | the settable dynamic state (Milan v1.2 Sections 5.3.5, 5.3.7, 5.3.8, 5.3.11, 5.3.12) | flip-flop fields behind a read multiplexer addressed by field | the set of values and their widths | flip-flops rather than a RAM table |
| `.../u_aecp/u_store` | 974 | 694 | READ_DESCRIPTOR and the name table (1722.1 Section 7.4.5; Milan v1.2 Section 5.3.13) | index map in distributed RAM, line and names in block RAM, a DRAM read master | the descriptors and names served | the image in DRAM, the index in distributed RAM |
| `.../u_pp/u_notify` | 3,118 | 3,299 | registered controllers, the entity lock and unsolicited notifications (Milan v1.2 Sections 5.3.4.1, 5.3.4.2, 5.4.5; 1722.1 Sections 7.4.2, 7.4.37, 7.4.38) | at this head, a 16 x 128-bit registry in flip-flops with 16 parallel identity compares, pending-class vectors per controller, throttle stamps ([#232](https://github.com/kebag-logic/milan-fpga/issues/232) moves the registry to distributed RAM) | at least 16 controllers, each with its own sequence ID; 60 s lock | parallel compares and flop storage |
| `.../u_pp/u_listener` | 1,414 | 1,110 | the ACMP listener state machine (Milan v1.2 Section 5.5.3; 1722.1 clause 8) | already one event-at-a-time executor over per-sink records, a ROM transition matrix and hardwired action primitives, records in five RAMB36 at this head ([#639](https://github.com/kebag-logic/milan-fpga/issues/639) moves them to distributed RAM) | the state machine and the ACMPDU | hardwired actions and a 376-bit record |
| `.../u_pp/u_talker` | 689 | 517 | the stateless ACMP talker responder and the destination-MAC gate (Milan v1.2 Sections 5.5.2.7, 5.5.4) | response logic and one gate per source | the four responses | per-source gate replication |
| `.../u_pp/u_timer` | 884 | 179 | every protocol timer: MRP, ACMP and AECP timeouts, ADP valid time, the lock | prescalers, a millisecond timebase, a 61-slot deadline RAM swept one slot per cycle | the timers and their values | per-slot armed flip-flops and wide modular compares |
| `.../u_pp/u_dispatch` | 775 | 635 | per-protocol command queues between the parser and the engines | four queues of wide transaction records in distributed RAM (depths 4, 4, 4, 2) | none | one queue per protocol |
| `.../u_pp/u_nvm_shadow` | 790 | 1,118 | saving and restoring each sink's binding (Milan v1.2 Sections 5.3.8.1, 5.5.3) | capture of the listener's record writes, a preload face, a record serializer | which binding fields survive power loss | a hardwired manager of its own |
| `.../u_pp/u_originator` | 721 | 885 | entity-initiated commands: ACMP PROBE_TX, AECP CONTROLLER_AVAILABLE, their retries and timeouts | an in-flight table matched on key and sequence ID | sequence IDs, one retry, the timeouts | a separate table and matcher |
| `.../u_pp/u_rx_validator` | 543 | 751 | the shared receive front end: address and EtherType gates, subtype demux, common-header extraction, the MRP bypass | a beat-wise parser | the address, EtherType and header rules | one parser for every protocol, already shared |
| `.../u_pp/u_srp` | 4,219 | 6,264 | the MSRP and MVRP participant (802.1Q-2018 clauses 10, 11, 35; Milan v1.2 Section 4.2.7) | stream FSMs per context, a vector decoder, an encoder with pending tables, admission, VLAN and Domain | one applicant and registrar per declared attribute, the exact three-field match, the MRP timers | every context evaluated in parallel every cycle |
| `.../u_srp/u_encoder` | 1,320 | 1,062 | MRPDU vector encoding, one MRPDU per application per join tick (802.1Q-2018 Sections 10.8, 35.2.2) | two pending tables in distributed RAM, run detection, three- and four-packed coding | the PDU format and the aggregation rule | table storage and parallel run compares |
| `.../u_srp/@own` | 862 | 2,792 | SRP glue: the event merge, the service port and the timer-arm FIFOs | at this head the two FIFOs are one flop array ([#230](https://github.com/kebag-logic/milan-fpga/issues/230) moves them to distributed RAM) | none | the FIFO storage |
| `.../u_srp/u_talker` | 612 | 672 | the talker-side applicant and registrar per source (802.1Q-2018 Tables 10-3, 10-4; Milan v1.2 Section 4.2.7.2.2) | one FSM pair per context, evaluated in parallel | the state machines | parallel evaluation per context |
| `.../u_srp/u_decoder` | 584 | 630 | MRPDU vector decoding and its malformed-PDU tolerance (802.1Q-2018 Section 10.8.1.2; Milan v1.2 Section 4.2.7.1) | a byte-serial walker emitting one value per cycle | the PDU grammar | none of note |
| `.../pp_shadow/u_nvm` | 504 | 476 | the saved-state backend ([#70](https://github.com/kebag-logic/milan-fpga/issues/70)) | record framing and the KLJ2 container over the NVM port | which state is saved | a fabric backend |

**The rest of the datapath**

| Hierarchy | LUT | FF | Protocol function and clause | How it is built | Set by the standard | Implementation choice |
|---|---:|---:|---|---|---|---|
| `milan_datapath/g_gptp_plane.u_gptp_shadow` | 4,999 | 5,899 | gPTP (802.1AS-2011; Milan v1.2 Section 4.2.6), the product's time owner | a receive tap and FIFO, a byte-serial engine (parser, micro-coded handlers, TX slot, timer), egress timestamp return, the publication bank | the state machines, message formats, servo inputs | its own micro-coded engine, a 64-bit ALU |
| `.../g_gptp_plane.u_gptp_shadow/u_engine` | 3,804 | 3,638 | the gPTP engine (`KL_gptp_engine`, gPTP processor submodule) | parser, micro-coded handlers, TX slot, an 8-slot timer and the engine's state regions | as above | as above |
| `.../u_engine/u_ucpu` | 2,083 | 728 | the gPTP handlers | a superset of the AECP engine with 64-bit arithmetic | none | a second engine beside the AECP one |
| `.../u_engine/@own` | 852 | 2,158 | the engine's state regions | flip-flops and distributed RAM behind the engine's state port | the per-port state | storage form |
| `.../g_gptp_plane.u_gptp_shadow/@own` | 614 | 985 | the plane's integration: byte serializer, gear-up, publication | width converters and registers | none | the width conversion |
| `milan_datapath/csr` | 2,907 | 2,141 | the CSR plane (REQ-CSR-01, REQ-CSR-02) | inert RW words in a block RAM shadow; a live read multiplexer over every status face; snapshot registers | nothing in Milan; the register map is this product's ABI | the read multiplexer's shape |
| `milan_datapath/chan_map_capture` | 1,076 | 1,321 | talker channel mapping (Milan v1.2 Section 5.3.9) | a map RAM and one source multiplexer per pair slot | the mapping semantics | per-slot multiplexers |
| `milan_datapath/g_mmcm_servo.mmcm_servo` and its own logic | 899 | 814 | the media-clock actuator for CRF and AAF following (Milan v1.2 Section 7; 1722-2016 clause 10) | servo arithmetic and an MMCM reconfiguration port driver | the following behaviour | dedicated arithmetic |
| `milan_datapath/avtp_rx_monitor` | 942 | 1,353 | the Stream Input counters (Milan v1.2 Section 5.3.8, Table 5.6) | per-stream counters and their event logic in flip-flops | twelve 32-bit counters per stream input | flip-flop counters |
| `milan_datapath/aaf_latency_tap_bank` and its `g_ltap.aaf_latency_taps` | 672 | 620 | diagnostic stage-latency taps (no protocol function) | per-stage timestamp chains | none | the whole block (L6) |
| `milan_datapath/aaf_packetizer` | 650 | 1,331 | AAF talker framing (1722-2016 clause 7; Milan v1.2 Section 6) | a framer with pair injection | the PDU format | none of note |
| `milan_datapath/@own` | 562 | 2,850 | the datapath's own registers and glue | per-stream registers outside the blocks | none | registers kept at the top |
| `milan_datapath/g_maap.maap_engine` | 519 | 267 | MAAP, dynamic stream destination addresses (1722-2016 Annex B) | one hardwired state machine with its timers, random draw and PDU builder | probe, defend and announce, the address range | a dedicated engine (L2 would move it) |
| `milan_datapath/g_rx_filter.rx_filter` and its `mac_cam` | 513 | 1,570 | receive address filtering (REQ-MAC-02) | a ternary CAM in flip-flops | REQ-MAC-02 (a MUST) | the CAM in flip-flops |

**The SoC side**

| Hierarchy | LUT | FF | Function | How it is built | Set by the standard | Implementation choice |
|---|---:|---:|---|---|---|---|
| `@own` (the LiteX top) | 4,833 | 6,072 | DDR3 controller and PHY, the SoC bus and CSR banks, the management MAC, UART, SPI flash, the BIOS ROM and SRAM, generated FIFOs | one flat generated module | nothing in Milan | DDR3 main memory (L11a), the FIFO storage (L3) |
| `VexiiRiscvLitex_*` | 3,522 | 4,736 | the control hart (NFR-SCOUT-01: one cacheless RV32I) | the VexiiRiscv core and its bus bridges | nothing in Milan | the core choice (L11b) |
| `VexiiRiscvLitex_*/vexiis_0_logic_core` and its own logic | 1,148 | 1,041 | the RV32I pipeline itself | an in-order pipeline with its register file | nothing in Milan | the core |
| `VexiiRiscvLitex_*/@own` | 696 | 1,807 | the netlist's own glue: bus adapters, clock-domain FIFOs, the interrupt and timer blocks | generated interconnect | nothing in Milan | replaced with the core in L11b |

## Levers

The [ledger](#ledger) owns the current numerical estimates.
Historical measurements support estimates; none proves a redesigned image fits.
Every lane measures its actual delta before adopting a saving.
All implemented paths must preserve wire semantics and normative ordering.
D1/D3 permit bounded internal latency changes with reviewed equivalence evidence.

### L1 Shared sequencing in retained fabric control

ACMP/ADP sequencing and SRP L1b are superseded by F0-F5.
M3 retains only the AECP/notification/record-manager residual for fabric AECP.
Its estimate is 2,600 LUTs (1,500-3,600), zero in the default image.
The ledger derives it from current standalone scopes, less engine overhead.

**Risk: high.** Shared sequencing changes contention and internal latency.
Each response path needs a deterministic bound under maximum fan-out.
**Verification:** processor suites and campaigns at their recorded counts;
PDU/port-transaction differential checks; parent consumers, `pp_shadow`,
`nvm_cosim`, `milan_dp`, capture bounds and bench compliance.
Cycle-pinned tests are retargeted under review, never removed.
The interface index remains in all contexts.

### L2 Default control split

F0-F5 transfers ADP, ACMP, MAAP, SRP and AECP control ownership.
F1 supplies flash validation, boot apply and transactional write-back.
The [split contract](../ARCHITECTURE_HW_SW_SPLIT.md) keeps one owner per function.
The [mailbox contract](MAILBOX_SPLIT.md) provides filtered packet mailboxes and events.
The earlier CSR-only interface proposal is superseded.

**Saving:** estimated 14,000 LUTs, range 11,500-16,000.
The ledger shows disjoint removal references and all cost allowances.
The measured mailbox skeleton costs 3,102 LUTs and six BRAM tiles.
F0-F4 code is present at the assigned dev revision.
Presence does not establish integrated, bench-qualified operation.
The [SoC wiring](../../sw/litex/milan_soc.py) holds the mailbox datapath idle.
[`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv) still instantiates `KL_pp_shadow` unconditionally.
Consequently, enabling `--ctrl-mailbox` alone saves no processor logic.

**What leaves after qualification:** the selected protocol engines, their
private tables, notification and descriptor serving, and fabric NVM serialization.
The complete flip removes `KL_pp_shadow` from the default build.
Equivalent settings, counters, diagnostics and media controls must remain accessible.
Framing, timestamps, ingress filtering, hard-deadline event timers, gPTP,
AVTP/AAF/CRF, media admission and physical audio stay in fabric.
A software protocol owner must not become a software media path.

**Risk: high.** Target service time, ring backlog, flash interference,
firmware capacity and F5 qualification remain implementation obligations.
The [owner's memory decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413) replaces the earlier approximately 128 KB budget.
F5's limit is now 224 KB, including AECP.
Budget about 50 RAMB36 tiles for firmware.
The [memory ledger](#firmware-and-block-ram-ledger) includes the measured preflight and packing risk.
Measure linked code, data, stack, static pools and saved-state staging.
The current ROM parameter does not establish Mark II capacity.

**Verification:** F0 mailbox tests on both adapters, filter mutation campaigns,
F1 store tests, F2-F5 unit and differential protocol suites,
RV32 execution and the [service hooks](../reference/FR_NFR.md#342-control-service-test-hooks).
Prove 10 ms project service under bounded ingress, SRP churn,
full rings, all recipients, flash activity and delayed events.
Prove wire deadlines separately; mailbox commit is insufficient evidence.
Retain all-fabric suites and compare reused stimuli at unchanged counts.
Bench acceptance covers every stream, counters and audio soak.
Unqualified functions remain all-fabric until their acceptance passes.

### L3 RAM-friendly retained tables

M2 covers retained SoC FIFOs, identified below after D4.
**Saving:** 200 LUTs (100-400), reduced from the original 800.
The old inventory included processor tables removed by L2.
gPTP belongs to M7; media context tables belong to M6.
The historical RAM census motivates this target.
[#639](https://github.com/kebag-logic/milan-fpga/issues/639) illustrates storage tradeoffs, not these FIFOs' measured savings.
Budget up to two extra tiles, subject to measured primitive counts.

[The SoC wiring](../../sw/litex/milan_soc.py) names the surviving scope:

| Retained object | Purpose after D4 | M2 treatment |
|---|---|---|
| `MilanMAC.tx_sf` payload and parameter FIFOs | Gapless complete-frame transmission | Already synchronous block-RAM storage; no credit for its earlier conversion |
| `MilanMAC.mac_tx_cdc`, `MilanMAC.mac_rx_cdc` | MAC/datapath crossings at distinct clocks | Inspect residual storage and control; retain buffering and paired reset |
| `milan_axil_cdc` AW/W/B/AR/R FIFOs | CPU-to-datapath CSR crossing at distinct clocks | Inspect shallow storage and control; preserve AXI-Lite ordering and coherent snapshots |

D4 removes DDR3, not the MAC or CSR crossings.
The estimate is an aggregate target for this surviving scope.
It is not a measured per-FIFO saving.
Preserve widths, depths, throughput, reset behavior and clock-domain contracts.
The implemented conversion and its LUT saving still need proof.
Already inferred block RAM supplies no second conversion credit.

Exclude LiteDRAM bank-machine, command, read and write queues.
Exclude `memory_port_cdc*` and CPU-internal bridge FIFOs under M8.
Exclude `descmem_*`, `respmem_*` and `nvmmem_*` crossings under L2/M8.
Their retained-AECP variants remain those lanes' responsibility.
Mailbox rings belong to L2.
Media/gPTP tables belong to M6/M7.
Reconcile the actual post-D4 export before assigning any M2 saving.

**Risk: medium.** Same-cycle reads may prevent block RAM inference.
**Verification:** per-array lockstep and negative controls, owning suites,
both shapes, primitive mapping and integrated route.
Read latency changes require D3's deterministic bounds.

### L4 Entity-derived widths

Wire IDs, addresses, sequence numbers and counters retain standard widths.
Only implementation indices can narrow from the generated entity shape.
The historical 200-LUT estimate is included in M3's residual.
It receives zero default-split credit.
[#233](https://github.com/kebag-logic/milan-fpga/issues/233) already found shipping stream geometry fully derived.

**Risk: low. Verification:** boundary indices, all supported shapes,
refusals and owning suites; unchanged wire bytes.

### L5 Remaining specialization items

VLAN reference widths, descriptor lines and queue depths need measurement.
The original 30-100 LUT estimate remains reference material only.
SRP's work leaves with F4; AECP residue belongs to M3.
Neither adds another default-split credit.
Depth reductions require burst/backpressure evidence and protocol capacity.
GET_DYNAMIC_INFO still requires its 524-byte response capacity.

**Risk: low to medium. Verification:** owning SRP, notification,
dispatch and AECP suites, including worst-case backlog.

### L6 Diagnostics retained

D2 rejects diagnostic pruning from the shipping image.
The earlier 700-LUT opportunity is dropped, with zero saving.
Latency taps, probe information and equivalent control diagnostics remain.
Milan counter producers were never optional diagnostic prunes.
The split's integration allowance includes retained control observability.

**Verification:** diagnostic readback, counter coherence and builder presence checks.
No implementation lane is opened to disable them.

### L7 SRP shared evaluator

F4 replaces M4 and L1b/L7 in the default plan.
The historical 450-LUT estimate is not an additional saving.
A supported fabric SRP implementation may revisit it separately.

**Risk: medium.** Serialized event handling changes internal latency.
**Verification:** SRP suites/campaigns at both shapes, event stalls,
MRP timers and bench protocol checks under D3.

### L8 CSR read path

M5 restructures the existing live-status read mux and snapshots.
**Saving:** 600 LUTs (400-1,000), from the historical 2,907-LUT block
and [#649](https://github.com/kebag-logic/milan-fpga/issues/649)'s 2,893 fixed plus 211-per-stream OOC model.
New split-interface logic is charged to L2, not saved again here.

**Risk: medium.** Snapshot coherence and AXI-Lite latency must hold.
**Verification:** CSR, `tcam_csr`, `milan_dp`, firmware host tests,
register-map checks and boot readback in both placements.
Register addresses, widths and reset values remain unchanged by M5.

### L9 Media context tables

M6 owns listener/talker counters, channel-map capture and render set-point.
**Saving:** 600 LUTs (400-900), from the historical routed inventory
and [#649](https://github.com/kebag-logic/milan-fpga/issues/649)'s per-stream OOC marginals of 208, 317 and 205.
These datapath functions remain fabric-owned in the split.

**Risk: medium.** Read-modify-write hazards can break coherent counters.
**Verification:** `avtp_rxmon`, `tkdiag`, `chmap_capture`, `render_setpoint`,
`milan_dp`, GET_COUNTERS, wrap/reset and concurrent update cases.
No M2 table credit overlaps these arrays.

### L10 Fabric gPTP

M7 moves eligible gPTP tables into block RAM or narrows indices.
**Saving:** 500 LUTs (300-700), based on 464 historical LUTRAM LUTs.
Dual-read operand files remain where required.
M10 shares gPTP and AECP execution only in retained-fabric AECP builds.
Its estimated 1,200 LUTs (900-1,500) has zero default-image credit.
F5 already removes the AECP engine in the split.

**Risk:** medium for tables; high for shared execution and turnaround.
**Verification:** gPTP processor suites, `gptp_plane`, `gptp_shadow`,
`gptp_txts`, `milan_dp_gptp`, timestamp/CDC checks and [#117](https://github.com/kebag-logic/milan-fpga/issues/117) bench evidence.
M10 additionally proves arbitration and worst-case gPTP turnaround.
Audio and gPTP deadlines remain independent of firmware service.

### L11 The SoC side

D4 approves on-chip main memory instead of DDR3.
M8a sizes [#70](https://github.com/kebag-logic/milan-fpga/issues/70)/F1 staging to the selected shape's container.
**Saving:** 1,000 LUTs (400-1,500), repriced in Round 1c.
The [historical census](../findings/649_RESOURCE_MAP_AND_SENSITIVITY.md#the-soc-tops-own-logic) reports pre-packing LUT cells.
Its controller has 823; its PHY has 873.
The 1,696 cells do not identify packed LUT sites.
Another 3,231 anonymous LUT cells have no assigned owner.
Their DDR share is unknown and receives zero credit.

The estimate uses explicit packing and replacement assumptions:

| Case | Named cells retained as LUT sites | Replacement debit, LUT | Net calculation | Rounded saving |
|---|---:|---:|---|---:|
| Conservative | 50 percent | 400 | `1,696 * 0.50 - 400 = 448` | 400 |
| Central | 75 percent | 250 | `1,696 * 0.75 - 250 = 1,022` | 1,000 |
| Optimistic | 100 percent | 100 | `1,696 - 100 = 1,596` | 1,500 |

Each result rounds down to the preceding hundred LUTs.
The packing shares bracket paired and unpaired named cells.
Replacement allowances cover on-chip decode, arbitration and storage control.
These are planning assumptions, not measured conversion ratios or bounds.
Shared sites or larger replacement logic can erase that saving.
Anonymous DDR logic could instead increase the measured saving.
M8a must replace these assumptions with a routed delta.
M0s and M9 retain independent primitive and memory-capacity checks.
M8a replaces the existing CPU memory allocation within the 50-tile budget.
It must reconcile that reuse against the [memory ledger](#firmware-and-block-ram-ledger).
The lane owns its memory-map migration and both placement contracts.

D5 conditionally approves a smaller cacheless RV32I control hart.
**Saving:** 1,700 LUTs (1,300-2,200).
This includes 300-600 retained bridge LUTs.
The original same-part `AreaOptimized_high` OOC pricing was:

| Core/netlist | LUT | FF | BRAM tiles |
|---|---:|---:|---:|
| Shipping VexiiRiscv netlist, including bus bridges | 3,066 | 5,017 | 4.5 |
| VexRiscv Min | 843 | 791 | 1 |
| PicoRV32 minimal | 1,051 | 549 | 0 |

These are isolated netlists, not integrated replacement measurements.
**Risk: high.** CPU service and on-chip capacity can invalidate estimates.
Prove 8x8 capture <= 24.5 ms with [`check_nvm_capture.py`](../../scripts/check_nvm_capture.py).
Keep boot timing and recheck service under filtered SRP churn.
A smaller core failing those conditions is reverted.

**Verification:** firmware host tests, `nvm_cosim` and `nvm_capture_cpu`.
Also run builder/deploy gates and target service hooks.
Repeat bench boot and persistence checks.
The all-fabric option still needs its response and staging memory.
Neither 8x8 nor F5 memory fit is established.

### L12 Functional prunes excluded

RX filtering, loopback, media-clock servo, CRF and rendering remain.
Milan's 16-controller minimum remains in either placement.
MAAP's protocol remains required; F2 relocates its implementation.
No protocol surface is removed to achieve area savings.

## Ledger

### M0s step-1 intermediate status

The [step-1 assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6086604096) first requires integrated F0-F4 placement.
Inspection at assigned base `7c1b52be` fails that prerequisite.
The [mailbox adapter](../../sw/litex/milan_soc.py) holds packet and event inputs idle.
Its outgoing packet stream has no datapath consumer.
The [datapath](../../hdl/milan/milan_datapath.sv) still instantiates the wrapper unconditionally.
The [MAAP firmware contract](../../sw/firmware/ctrl/maap/README.md) leaves placement integration outstanding.
Firmware presence therefore earns no engine-removal credit.

| Intermediate checkpoint | LUT / FF / slices | RAMB36 / RAMB18 | WNS / WHS | Disposition |
|---|---|---|---|---|
| M0s step 1, F0-F4 with fabric AECP | Not measured | Not measured | Not measured | STOP: parent integration must connect the datapath |

No route was started; no new resource figure is claimed.
At that base the last accepted gate record was #645/#647's 50,267 LUTs and 74/27 RAM primitives.
[#696](https://github.com/kebag-logic/milan-fpga/issues/696) has since re-recorded it at 50,230 LUTs with 74/27 unchanged; that record is the comparison anchor, and the ledger keeps the baseline figures.
These are stored figures, not measurements of this lane.
The partial memory ledger still requires actual allocation and reconciliation.
Neither the 50-tile firmware estimate nor complete-wrapper reclamation proves fit.
The 121.5-tile ceiling and 10 percent reserve remain binding.

Step 2 supplies [selected-placement measurement support](../testing/PP_SHADOW_BASELINE_RECIPE.md#selected-placement-measurements).
It names `all-fabric`, `f0-f4` and `full-split` explicitly.
Split runs check retained engines before implementation and after routing.
The gate refuses mismatched placement or incomplete population evidence.
Whole-image comparisons retain the existing tool/flow identity and policy.
Both all-fabric standalone references remain independent and unchanged.
The acceptance schema, thresholds and records are unchanged.
Only M9 re-records acceptance.

The parent integration lane must connect ingress, egress and events.
It must select F0-F4 firmware and remove the corresponding engines.
Media controls, counters and saved-state ownership must remain connected.
Then repeat this prerequisite check and route the selected image.
That route must replace this missing measurement with actual figures.

### Default split saving basis

All savings below are estimates of the integrated 1x1 image.
The baseline's standalone rows avoid cross-boundary routed attribution.
The following rows are disjoint; AECP already includes its children.
Only the full qualified split receives the complete credit.

| Removed function | OOC 1x1 LUT basis | Ownership after flip |
|---|---:|---|
| ADP | 523 | F0/F3 |
| ACMP listener and listener admission | 1,561 | F3 |
| ACMP talker | 823 | F3 |
| Originator | 697 | F3/F5 |
| ACMP binding store | 808 | F1/F3 |
| SRP | 3,868 | F4; fabric admission cost reserved below |
| AECP, including microcode, descriptor and D3 stores | 6,150 | F5/F1 |
| Notification | 2,125 | F5; hardware counter producers stay |
| NVM port and arbiter | 542 | F1 |
| Wrapper NVM backend | 581 | F1 |
| **Disjoint wrapper subtotal** | **17,678** | Does not credit remaining wrapper logic |
| Parent MAAP | **429** | F2; measured [#686](https://github.com/kebag-logic/milan-fpga/issues/686) route reference |
| **Gross reference** | **18,107** | Mixed measurement contexts, not a routed delta |

MAAP's 429-LUT reference is recorded in [AREA_BUDGET](AREA_BUDGET.md#the-resource-gate).
It predates [#645](https://github.com/kebag-logic/milan-fpga/issues/645)/[#647](https://github.com/kebag-logic/milan-fpga/issues/647); its uncertainty is included below.
Processor MAAP is excluded; shipping uses parent MAAP.
Removing source instances does not guarantee their attributed routed saving.
AECP measures 8,084 routed and 6,150 standalone.
Its dynamic child measures 1,440 routed and 134 standalone.
The larger routed figures are deliberately not removal credits.

| Added or retained cost | Central LUT debit | Basis |
|---|---:|---|
| Packet mailboxes and Wishbone adapter | 3,102 | [Measured F3 round-3 skeleton](MAILBOX_SPLIT.md#measured-area): 2,946 FF, 1 RAMB36 + 10 RAMB18, no DSP, +0.402 ns WNS at 100 MHz |
| Remaining integration and retained interfaces | 1,000 | Estimate, 500-2,000: ingress/egress CDC, media settings/licences, admission enforcement, coherent counter/status faces and retained diagnostics |
| Mapping allowance | 0 | Estimate +/- 1,500 for source attribution, changed CPU region decode and integrated optimization |

The allowance includes SRP admission: 345 LUTs standalone.
It also includes the owner's 200-400-LUT control-register estimate.
Those are not independently subtracted elsewhere.
Mailbox timers, filter, rings and arbitration already cost 3,102.
No second cost is added for those same blocks.
Shared timers, trace, pools and dispatch receive no saving credit.
The remaining 5,501 wrapper LUTs receive no removal credit.
That residual includes processor MAAP, absent from shipping.
It is not a guaranteed reserve or an additional saving.

Central arithmetic: `18,107 - 3,102 - 1,000 = 14,005`.
Round down to **14,000 LUTs saved**.
Conservative arithmetic: `18,107 - 3,102 - 2,000 - 1,500 = 11,505`.
Optimistic arithmetic: `18,107 - 3,102 - 500 + 1,500 = 16,005`.
Use **11,500-16,000** as the rounded planning range.
The old 6,800-7,300 estimate covered fewer functions.
It assumed cheaper mailboxes.
It is superseded, not added to this estimate.

Credited source rows release 6.5 BRAM tiles before replacement.
The mailbox needs six; net credit is 0.5 tiles.
The wrapper's full 17.5 tiles require proven removal.
F5 needs an image, state and firmware memory census.
M8 must fit within the unchanged 121.5-tile ceiling.
The full route, primitive counts and service timing remain unmeasured.

### Firmware and block RAM ledger

The [owner decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413) allocates about 50 RAMB36 tiles to firmware.
The [F5 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916) sets its linked-image limit at 224 KB, AECP included.
This supersedes the approximately 128 KB figure.
The device still reserves 13.5 of its 135 tiles.
The usable ceiling remains 121.5 tiles.

The [F5 sizing preflight](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081556432) used dev `5603c353`.
It linked existing protocol code with the F1 store retained.
It contained neither AECP nor its descriptor image.

| Preflight shape | Linked span, bytes | Status |
|---|---:|---|
| Shipping 1x1, one interface | 94,688 | Size fixture; AECP absent |
| Largest supported shape, two interfaces | 147,360 | Size fixture; AECP absent |

The largest fixture has 56,948 text and 3,458 rodata bytes.
Data is zero; BSS is 78,744 bytes, including static pools.
Its stack reservation is 8,192 bytes.
Those sections total 147,342 bytes; link alignment adds 18.
Do not add the pools to BSS again.
These are measured link spans, not an irreducible minimum.
They establish neither F5 completion nor mapped RAMB36 counts.

The 50-tile figure uses approximately 4.5 KB per RAMB36.
That is raw capacity; mapping can expose less usable storage.
For example, 224 KiB needs 56 tiles at 4 KiB usable each.
That example is a packing check, not a new F5 threshold.
M8a must report actual usable bytes and allocated primitives.

This ledger first withholds the wrapper's remaining 11 tiles.
It credits only the same removed scopes as L2's LUT basis.
RAMB18 counts as half a tile; deltas carry their signs.
The firmware row replaces CPU memory, so replacement storage counts once.

| Item | RAMB36 delta | RAMB18 delta | Tile delta | Image tiles after |
|---|---:|---:|---:|---:|
| Recorded route at `a5ca6e51` | 74 | 27 | 87.5 | 87.5 |
| L2 credited removals: AECP and SRP storage | -6 | -1 | -6.5 | 81 |
| Measured mailbox replacement | +1 | +10 | +6 | 87 |
| M8a reuse of existing BIOS ROM and SRAM, estimate | -18 | -1 | -18.5 | 68.5 |
| Total firmware allocation, including reused CPU memory | +50 | 0 | +50 | 118.5 |
| M2 maximum additional allocation | +2 | 0 | +2 | 120.5 |
| Conditional release of remaining wrapper storage | -10 | -2 | -11 | 109.5 |

The base and wrapper counts come from the [route record](../../syn/ooc/pp_resource_baseline.json).
The [mailbox measurement](MAILBOX_SPLIT.md#measured-area) supplies its debit.
The reuse estimate comes from the [earlier SoC census](../findings/649_RESOURCE_MAP_AND_SENSITIVITY.md#the-soc-tops-own-logic).
That census reports BIOS ROM/SRAM at 18 RAMB36 and one RAMB18.
It is historical attribution, not a new census of `a5ca6e51`.
M8a must confirm the reusable count at its actual checkpoint.
Any retained boot memory outside the firmware allocation adds a debit.
The allocation must also contain stack, pools and shape-sized saved-state staging.
Any descriptor image or alignment space outside it adds a debit.
No separate smaller-core RAM saving is credited.

Arithmetic in tiles: `87.5 - 6.5 + 6 - 18.5 + 50 + 2 = 120.5`.
The conditional release subtracts eleven once, giving 109.5.
These memory entries grant no additional LUT saving.
The LUT estimates remain 31,667 central and 27,567-35,867 across the range.
They depend on fitting the credited RAM conversions within the ledger.

Before the conditional release, the estimate leaves one tile below 121.5.
After it, 109.5 tiles leaves twelve below that ceiling.
Both leave the separate 13.5-tile reserve untouched.
Neither number proves integrated fit.
Unpriced M6/M7 RAM conversions and integration buffers consume that allowance.
Each lane must debit them before accepting its LUT saving.
Without the estimated CPU-memory reuse, those totals become 139 and 128.
Both exceed the ceiling; reuse is a prerequisite, not free headroom.

**What gives way above 50 firmware tiles:** the remaining wrapper storage.
These disjoint scopes are outside the six AECP tiles and SRP half-tile:

| Released fabric scope, relative to wrapper | RAMB36 | RAMB18 | Tiles |
|---|---:|---:|---:|
| `u_pp/g_rx_pool[0,1,2,4,5].u_rx_slots`, five separate pools | 5 | 0 | 5 |
| `u_pp/u_mrp_strip` | 1 | 0 | 1 |
| `u_pp/u_tx_slots` | 1 | 0 | 1 |
| `u_pp/u_timer` | 1 | 0 | 1 |
| `u_pp/u_trace` | 1 | 0 | 1 |
| `u_pp/u_rx_validator` | 0 | 1 | 0.5 |
| `ctl_fifo` | 1 | 1 | 1.5 |
| Total | 10 | 2 | 11 |

Full-split integration must remove these stores before claiming their capacity.
Debit every replacement event, queue or diagnostic store separately.
Equivalent observability remains required by D2.
The measured mailbox already supplies its own queues and timers.
Do not credit its storage or these released stores twice.
At 56 firmware tiles, the conditional total becomes 115.5 tiles.
It leaves six below the ceiling, before other unpriced debits.
Beyond that allowance, defer M2's two-tile MAC/CSR FIFO conversion first.
Keep its existing storage and reprice the associated LUT saving.
Defer new M6/M7 block-RAM conversions next, with the same repricing.
No media buffer, diagnostic function or protocol capacity is pruned.
If these trades still exceed 121.5, the manager must commission further redesign.

Partial placement retains AECP's six tiles and any still-used wrapper stores.
With the same 50-tile hold, the pre-release estimate becomes 126.5.
That is five tiles over the ceiling, before extra fabric-AECP staging.
M0s must substitute measured firmware use and actual retained storage.
A partial route cannot borrow the full split's reclamation credits.
The all-fabric option needs its own complete memory reconciliation.

**Checkpoint evidence:** both M0s routes, the default flip and M9 report this ledger.
Record linked text, rodata, data, BSS, stack and static pools.
Count pools once; report alignment, descriptor images and staging separately.
Cover shipping and largest supported shapes, at one and two interfaces.
Report allocated RAMB36/RAMB18, usable bytes and unused firmware capacity.
Name the five largest BSS consumers and a reduction option each.
F5 implements no reductions outside AECP's own footprint.
Publish whole-image LUT, FF, RAMB36/RAMB18 and timing at each routed checkpoint.
Reconcile removals, replacement debits and actual firmware allocation against 121.5.
The default flip requires firmware resident in block RAM and the reserve intact.
Missing measurements or an exceeded ceiling cannot qualify the flip.

### Remaining levers without overlap

| Lane | Default saving, central (range) | Basis and overlap exclusion |
|---|---:|---|
| M2 / L3 | 200 (100-400) | Retained MAC and CSR FIFOs listed in L3; excludes DDR3, CPU/protocol-memory bridges and M6/M7 tables |
| M3 / L1a, L4, L5 | 0 | AECP/notification residual applies only where fabric AECP remains; ACMP/ADP work is replaced by F0-F5 |
| M5 / L8 | 600 (400-1,000) | Historical 2,907-LUT CSR read path; optimize existing status mux only, not split-interface growth |
| M6 / L9 | 600 (400-900) | Historical monitor, counter, channel-map and set-point contexts; retained media functions |
| M7 / L10a | 500 (300-700) | Historical gPTP plane tables; no overlap with M2 or M10 |
| M8a / L11a | 1,000 (400-1,500) | 1,696 named pre-packing cells, explicit packing/replacement assumptions in L11; 3,231 anonymous cells receive no credit |
| M8b / L11b | 1,700 (1,300-2,200) | Core OOC comparison in L11; conditional on capture, boot and split service under load |
| M10 / L10b | 0 | F5 removes fabric AECP's engine; sharing it cannot save twice |

M3 remains a priced fabric-AECP lane.
Its estimate is 2,600 LUTs (1,500-3,600).
Its basis uses these shares:

| Scope | LUT basis | Share |
|---|---:|---:|
| Notification | 2,125 | 60 percent |
| D3 and dynamic state | 1,703 + 134 | 70 percent |
| AECP own logic | 1,302 | 50 percent |
| AECP dispatch queue | 421 | 40 percent |

That displaces about 3,380 LUTs.
Engine and arbitration overhead costs about 1,000 LUTs.
Residual width work adds approximately 200 LUTs.
That brings the saving near 2,600.
This is a prototype target for retained fabric AECP only.
M10 remains planned there at 1,200 LUTs (900-1,500).
The routed AECP engine bounds sharing: 1,727 LUTs.
M3 must preserve that engine for M10 to remove.
If M3 consumes it, reprice M10 to zero.
Neither lane receives credit in the default-split total.

### Cumulative default-image estimates

Each row assumes every preceding row has landed and qualified.
Ranges describe all-low or all-high savings, not statistical confidence.

| Order | Lane | Saving | Central image | Conservative image | Optimistic image |
|---:|---|---:|---:|---:|---:|
| 0 | Recorded baseline | -- | 50,267 | 50,267 | 50,267 |
| 1 | F0-F5, complete qualified flip / L2 | 14,000 | 36,267 | 38,767 | 34,267 |
| 2 | M2 | 200 | 36,067 | 38,667 | 33,867 |
| 3 | M5 | 600 | 35,467 | 38,267 | 32,867 |
| 4 | M6 | 600 | 34,867 | 37,867 | 31,967 |
| 5 | M7 | 500 | 34,367 | 37,567 | 31,267 |
| 6 | M8a | 1,000 | 33,367 | 37,167 | 29,767 |
| 7 | M8b, conditional | 1,700 | 31,667 | 35,867 | 27,567 |
| 8 | M3 and M10 | 0 | 31,667 | 35,867 | 27,567 |
| 9 | M9 | No assumed saving | Measure | Measure | Measure |

Central headroom below 38,040 is 6,373 LUTs.
That is 16.75 percent.
The conservative estimate leaves 2,173, or 5.71 percent.
Both exceed D8's 1 percent planning margin.
Without M8b, the conservative image is 37,167.
It still clears the margin.
Timing cannot be inferred from these LUT calculations.

### No-split and partial-flip estimates

All scenarios retain required function, diagnostics and D7 policy.
Each assumes its credited levers qualify independently, including conditional M8b.
M3 must preserve a separate AECP engine for M10.
Their combined central credit is 3,800 LUTs.
The range is 2,400-5,100.
They receive no credit in the complete split.

**No split:** apply M2/M5/M6/M7/M8a/M8b first.
Those levers alone leave 45,667 LUTs centrally.
Adding M3 and M10 gives **41,867 LUTs**.
No F-lane removal or mailbox replacement is counted here.

**Partial flip:** F0-F4 qualify; F5 remains unqualified.
AECP, notification, originator and their NVM path remain in fabric.
That retains 10,095 LUTs from the full-split basis:
`6,150 + 2,125 + 697 + 542 + 581 = 10,095`.
F1/F3 owns moved binding persistence; fabric retains AECP persistence.
Each field still has one owner; integration must prove arbitration.
The ACMP binding store's 808-LUT removal is conditional on this.

The disjoint removal basis is **8,012 LUTs**:
`523 + 1,561 + 823 + 808 + 3,868 + 429 = 8,012`.
Debit the complete 3,102-LUT mailbox.
Do not assume fewer rings.
Use the complete split's integration and mapping allowances unchanged.
Retained shared timers, pools and dispatch receive no removal credit.

| Partial split case | Calculation | Estimated split saving |
|---|---|---:|
| Conservative | `8,012 - 3,102 - 2,000 - 1,500` | 1,410 |
| Central | `8,012 - 3,102 - 1,000` | 3,910 |
| Optimistic | `8,012 - 3,102 - 500 + 1,500` | 5,910 |

The remaining lanes are M2/M5/M6/M7/M8a/M8b.
Their central saving totals 4,600 LUTs.
Conservative savings total 2,900; optimistic savings total 6,700.
The partial scenario also credits M3/M10's retained-AECP work.
Thus: `50,267 - 3,910 - 4,600 - 3,800 = 37,957`.
Neither this arithmetic nor its range establishes measured savings.
M0s must verify retained ownership, integration cost and timing.

Positive headroom meets the stated LUT bar; negative headroom misses.
The two bars remain distinct; timing qualification remains mandatory.

| Placement | Case | Estimated image LUT | Headroom to 38,040 | Headroom to 37,659 |
|---|---|---:|---:|---:|
| Full split | Conservative | 35,867 | +2,173 | +1,792 |
| Full split | Central | 31,667 | +6,373 | +5,992 |
| Full split | Optimistic | 27,567 | +10,473 | +10,092 |
| No split, including M3/M10 | Conservative | 44,967 | -6,927 | -7,308 |
| No split, including M3/M10 | Central | 41,867 | -3,827 | -4,208 |
| No split, including M3/M10 | Optimistic | 38,467 | -427 | -808 |
| Partial, F5 unqualified | Conservative | 43,557 | -5,517 | -5,898 |
| Partial, F5 unqualified | Central | 37,957 | +83 | -298 |
| Partial, F5 unqualified | Optimistic | 32,557 | +5,483 | +5,102 |

The full split clears both bars in all three estimates.
The no-split cases all miss both bars, including M3/M10.
Partial central clears 38,040 but misses 37,659.
Its conservative case misses both; its optimistic case clears both.
Without M8b, partial central rises to 39,657.
It misses both bars.

No-split needs 3,827 further LUTs centrally for [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest).
D8 requires 4,208 further LUTs.
Conservative gaps are tabled above.
The partial central case needs 298 further LUTs for D8.
Its conservative case needs 5,898 to clear both bars.
Qualifying F5 supplies the priced route to the full-split scenario.
When switching scenarios, remove M3/M10 credit to avoid overlap.
If F5 cannot qualify, the manager must commission additional redesign.
The week-4 ruling names its measured target and revised schedule.
No additional lever has earned credit in these fallback totals.
A D8 margin exception alone cannot cure an [NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest) miss.
It also needs an explicit ruling; no exception is assumed.

## Lane sequence

All parent lanes start from the third adoption, processor `2ad2f845`.
The earlier [#661](https://github.com/kebag-logic/milan-fpga/issues/661) dependency is satisfied on dev `5603c353`.
Weeks count from 2026-10-12; 2026-12-15 is week 10.
This is a schedule estimate, conditional on split qualification.
Each implementation needs its own settled public scope and review.
Independent lanes may proceed concurrently in isolated worktrees.
Measurements queue serially; no Vivado overlaps another heavy build.

| Order / window | Lane | Scope and files | Dependency | Estimated default saving | Required evidence and risk |
|---|---|---|---|---:|---|
| 0, complete | M0 | Adopted processor pin and current three-endpoint record | [#661](https://github.com/kebag-logic/milan-fpga/issues/661), [#682](https://github.com/kebag-logic/milan-fpga/issues/682), [#686](https://github.com/kebag-logic/milan-fpga/issues/686), [#645](https://github.com/kebag-logic/milan-fpga/issues/645)/[#647](https://github.com/kebag-logic/milan-fpga/issues/647) present at assigned dev | Already in 50,267 | Reuse committed record; do not subtract old lane deltas |
| 0s, now through week 3 | M0s | Manager resource bench: split-aware recipe and gate coverage, then two selected-placement routes | First: integrated F0-F4 with fabric AECP; second: F5 merged; both before week 4 and default flip | No assumed saving | Reviewed measurement support; whole-image metrics, memory-ledger reconciliation, timing and D7 comparison; preserve all-fabric references |
| 1, weeks 1-6 | F0-F5 / L2 | [`sw/firmware/ctrl/`](../../sw/firmware/ctrl/), [`sw/firmware/ctrl_nvm/`](../../sw/firmware/ctrl_nvm/), mailbox contract and parent integration; complete F5 and connect the datapath | Approved [#664](https://github.com/kebag-logic/milan-fpga/issues/664) text; F0-F4 foundations present; both M0s measurements, firmware in block RAM within the ledger, and F2-F5 suites/bench before default flip | 14,000 (11,500-16,000) | Highest risk: exact ownership, full service/wire bounds, all streams/counters and soak; no full credit for a partial flip |
| 2, weeks 1-4 | M2 | MAC packet/CDC and CSR AW/W/B/AR/R FIFOs listed in [L3](#l3-ram-friendly-retained-tables); [SoC wiring](../../sw/litex/milan_soc.py) | Adopted pin; confirm post-D4 FIFO survival; settled split interface allocation; measure final split | 200 (100-400) | RAM inference and per-array lockstep; primitive growth still judged by gate |
| 3, weeks 2-6 | M5 | Existing read mux and snapshots in [`hdl/common/csr/milan_csr.sv`](../../hdl/common/csr/milan_csr.sv) | Adopted pin; preserve both placement faces | 600 (400-1,000) | CSR coherence, AXI-Lite timing and firmware readback |
| 4, weeks 2-6 | M6 | AVTP counter contexts, channel-map capture and render set-point under [`hdl/ieee1722/`](../../hdl/ieee1722/) | Adopted pin; fabric media ownership fixed by [#664](https://github.com/kebag-logic/milan-fpga/issues/664) | 600 (400-900) | Update/read/reset hazards, GET_COUNTERS and full datapath |
| 5, weeks 3-6 | M7 | gPTP engine state tables and parent shadow wrapper | Adopted pin; gPTP remains fabric; excludes M2 arrays | 500 (300-700) | gPTP suites, CDC/timestamps and turnaround |
| 6, weeks 2-8 | M8a/M8b | SoC memory/core selection, firmware layout and [#70](https://github.com/kebag-logic/milan-fpga/issues/70)/F1 staging | D4 approved; D5 conditional; reconcile 50-tile firmware allocation and measured linked storage; prove split service before accepting core | 2,700 (1,700-3,700) | Memory capacity, boot, 8x8 capture <= 24.5 ms, SRP churn; revert core if bounds fail |
| 7, decision at week 4; weeks 4-8 | M3 | Retained fabric AECP dispatch, notification, D3 and entity widths in processor | D1/D3 approved; ACMP/ADP portion replaced; schedule residual only for a selected fabric-AECP image | **0**; fabric-only opportunity 2,600 (1,500-3,600) | PDU/port equivalence and complete processor/consumer bank; no F5 overlap |
| 8, weeks 6-9 | M10 | One gPTP/AECP engine across processor integration | D6 planned; requires fabric AECP remaining and M3 preserving a separate removable engine | **0**; fabric-only opportunity 1,200 (900-1,500) | Sharing turnaround proof; removed AECP cannot be saved twice |
| 9, weeks 9-10 | M9 | Final pin adoption, integrated route, timing closure and resource-gate re-record; budget/ledger update | M0s coverage accepted; selected F2-F5 functions qualified; actual M-lane deltas known; required review complete | No assumed saving | <= 38,040 LUT with timing; aim <= 37,659; all suites/campaigns and physical acceptance |

M1 is dropped by D2; M4 is replaced by F4.
M3/M10's listed order is for any retained fabric-AECP work.
They do not block a fully qualified split.
Their zero default contribution follows from F5's ownership change.
The manager assigns those implementation lanes against their chosen placement.

The [Round 1c decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081534590) schedules M0s before the flip.
The manager's resource bench owns its tooling and measurements.
[The split program](https://github.com/kebag-logic/milan-fpga/issues/665) lands behind build switches, defaulting to all-fabric.
M0s selects split placement explicitly; shipping defaults remain unchanged.

M0s runs two steps, both before the week-4 checkpoint:

1. Now: prepare reviewed split-aware measurement support and its controls.
   Route integrated F0-F4 with AECP still in fabric.
   Firmware presence alone does not satisfy the integration prerequisite.
2. After F5 merges: route the complete selected split.
   Finish this measurement before week 4 and any default flip.

The schedule therefore requires F5 integration by week 3.
Qualification may continue through week 6; measurement precedes qualification.
A delayed F5 merge makes M0s's second measurement late.
Report that missed checkpoint explicitly; do not claim full-split evidence.
The planned default flip waits for both measurements and qualification.
Both M0s routes reconcile RAMB36 use against the [memory ledger](#firmware-and-block-ram-ledger).
The flip reports its own routed LUT, FF and RAMB36 use.
Its firmware resides in block RAM, with the 10 percent reserve intact.

At week 4, replace estimates with M0s's routed figures.
Reprice M3/M10 against the measured remaining fabric ownership.
A missed service bound retains the affected function in fabric.
Publish that placement's residual area gap and revised schedule.
Never omit functions or change acceptance to force the target.

D7 uses M0s figures for each selected-placement comparison.
Compare whole-image resources against the last accepted gate record.
Later lanes also publish their delta from matching M0s placement.
This separates integration cost from subsequent lane savings.
Missing or incomparable measurements cannot produce a pass.
Intermediate measurements enter this ledger; only M9 re-records acceptance.

The all-fabric [recipe](../../syn/ooc/pp_baseline.py) still requires its wrapper.
The selected split recipe checks its own engine population.
M0s supplies split-aware recipe and gate coverage for review.
It precedes both split routes, the checkpoint and default flip.
Name each measured placement and retain comparable whole-image metrics.
Preserve tool/flow identities, route completion, primitive counts and timing.
Retain the all-fabric shipping endpoint and standalone 1x1/8x8 references.
Later lanes record selected routes and both standalone references.
M9 consumes M0s coverage for final qualification and re-recording.
M0s changes measurement support only; acceptance schema and policy stay fixed.

## What holds throughout

- **Equivalent function and tests.** Retain all-fabric suites/campaign counts.
  Reuse protocol stimuli through firmware differential tests.
  Preserve boundary, malformed-input, ordering, reset and backpressure checks.
  Use the pinned revision's inventories rather than historical count totals.
  D1 permits reviewed retargeting of cycle checks, never their deletion.
- **ATDECC state authority.** ATDECC remains the control-state authority.
  Each selected placement has one authoritative protocol owner.
  Firmware owns moved protocol state; fabric owns media and gPTP.
  Snapshot publication and saved-state restore create no competing owner.
- **Future interfaces.** Keep interface indices in contexts and mailboxes.
  The one-port release does not enable Milan Section 8 redundancy.
  Neither redesign nor filtering closes the later second-port seam.
- **D7 resource policy.** Intermediate lanes publish measured deltas here.
  Use M0s figures against the last accepted resource record.
  Publish subsequent lane deltas separately; growth stays visible.
  M9 re-records at the LUT target with timing met.
  The BRAM reserve, tolerances and floors are unchanged.
  RAM conversions may exceed zero primitive-growth tolerances before M9.
  Report that regression for explicit disposition.
  It authorizes neither a pass nor raised thresholds.
- **Bounded timing.** D3 requires deterministic internal service bounds.
  Normative deadlines retain margin and ordering remains independent.
  The 10 ms project budget cannot replace a wire deadline.
  Fast connect, restart under one second and capture bounds remain.
- **Interfaces.** This planning stage changes no port, register or parameter.
  Future split integration and D4 own their approved interface migrations.
  Each needs an explicit implementation contract and compatibility evidence.
  M5/M6 do not silently alter the existing register ABI.
- **Release proof.** Validate the exact integrated route at shipping clocks.
  Run the required build gates, suites and campaigns after adoption.
  Qualify placement on the bench before changing defaults.
  P3/[#396](https://github.com/kebag-logic/milan-fpga/issues/396) then runs on the qualified redesigned image.

## Recorded decisions

Round 1b followed the [assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6080904058).
Round 1c followed its [measurement and review ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081534590).
Round 1d follows the [firmware-memory assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081895732).
It incorporates the [owner's 224 KB decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413).
Later decisions below supersede earlier alternatives explicitly.
They authorize future implementation lanes, not RTL changes here.

| Decision | Recorded outcome | Plan consequence |
|---|---|---|
| D1, equivalence | [Manager ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268): PDU and port-transaction equivalence, every suite and campaign at its count | Retarget cycle-pinned checks under review; never delete them |
| D2, diagnostics | [Owner decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991591637): diagnostics stay | Drop L6/M1's 700-LUT credit; retain equivalent diagnostics across placements |
| D3, internal latency | [Manager ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268): deterministic tested bounds per response path | Preserve normative margin, fast connect, restart under one second and saved-state capture |
| D4, main memory | [Owner decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991591637): replace DDR3 with on-chip memory | M8 sizes staging to each shape's container and plans the memory-map migration |
| D5, control core | [Owner decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991591637): smaller cacheless RV32I, conditionally | Prove 8x8 capture <= 24.5 ms and boot timing; revert otherwise |
| D6, engine sharing | Initially deferred by the manager; then [owner made M10 planned](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991591637) | Retain M10 for fabric AECP; the later split removes its default-image credit |
| D7, re-record | [Manager ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268): intermediate measurements enter this ledger | Gate against the last record; M9 re-records at the target |
| D8, margin | [Manager ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268): 38,040 LUT with timing is the bar | Aim at least 1 percent below it: <= 37,659 LUT; 5 percent was planning guidance |
| D9, placement | Initially excluded by the [owner](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991591637); subsequently made the [Mark II default](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991745829) | L2/F0-F5 replaces ACMP/ADP M3 work and M4; all-fabric stays supported |

The placement decisions progressed as follows:

1. [Milestone 13](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991605450) initially held the slow path separately.
2. [Build-selectable placement](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991626132) initially proposed a CSR boundary.
3. [Packet mailboxes](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991695093) superseded that CSR proposal, with ingress filtering and firmware restore.
4. [Portable interface](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991737927) added ADP and GM-change events: memory-mapped block RAM rings, doorbell, interrupt, 32-bit accesses, no DMA, host bus adapters, portable C/HAL and one YAML contract.
5. [Default split](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991745829) retained easy per-function build selection and the all-fabric option.
6. [Before-release integration](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5993114362) brought ADP, ACMP, MAAP, SRP via lwSRP, AECP and saved-state handling into milestone 12. Milestone 13 retains the hard-core port.

The last decision replaces M3's ACMP/ADP portion and M4 with F0-F5.
M2, M5, M6, M7 and M8 remain area lanes.
Functions change shipping placement only after suites and bench qualification.
Unqualified functions retain fabric ownership.
The [#396](https://github.com/kebag-logic/milan-fpga/issues/396) release campaigns then run on the qualified split image.

The [approved #664 text](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6015500032) is now merged.
[Product ownership](../../REQUIREMENTS.md#1-product-ownership) and [NFR-SCOUT-02/03](../reference/FR_NFR.md#34-fabric-scale-out-and-future-ports) govern implementation.
The project service budget is 10 ms, separately from normative deadlines.
Its approval supersedes the register's retained proposal wording.
F2-F5 acceptance still precedes the shipping default flip.
VERSION stays major 2 until that implementation; split images identify major 3.
See the [version landing contract](../ARCHITECTURE_HW_SW_SPLIT.md#7-version-and-default-flip).

## Method and receipts

The receipts below are the original 2026-10-05 measurements.
Rounds 1b and 1c use committed records without new synthesis.
Current recipe provenance is in the current baseline above.

**Tools and recipe.** Vivado 2026.1 build 6511674 for `xc7a100t-fgg484-2`, the [#234 recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md) unchanged: the shipping `endstation_ax7101_1x1_tdm8` export without `--build`, [`pp_baseline.py`](../../syn/ooc/pp_baseline.py) for the integrated script, `AreaOptimized_high` synthesis, `ExploreArea` optimization, `ExtraPostPlacementOpt` placement, `AggressiveExplore` physical optimization and routing, 32 threads, the default seed; the standalone wrapper with `--integrated-clock` (20 ns).
Each historical Vivado run held the shared lock.
Future runs must also exclude competing heavy builds.

**Historical mapping at `e6172750`.** The gate then described dev `54643724`.
The [mapper](../../syn/resmap/resmap_map.py) required a matching recorded endpoint.
The map was therefore tied to a scratch copy of [`syn/ooc/pp_resource_baseline.json`](../../syn/ooc/pp_resource_baseline.json) into which this route was recorded with `pp_resource_gate.py record --write --baseline <copy>`; the tracked baseline is unchanged.
A Mark II lane maps its own route the same way:

```sh
cp syn/ooc/pp_resource_baseline.json "$WORK/scratch_baseline.json"
python3 syn/ooc/pp_resource_gate.py record "$WORK/ax7101/gateware" --endpoint route-1x1 \
  --baseline "$WORK/scratch_baseline.json" --write
mkdir "$WORK/route-map" && (cd "$WORK/route-map" && flock /tmp/milan-vivado.lock vivado -mode batch \
  -source "$REPO/syn/resmap/route_map.tcl" -nojournal -log route_map.log \
  -tclargs "$WORK/ax7101/gateware/alinx_ax7101_route.dcp")
python3 syn/resmap/resmap_map.py map "$WORK/route-map" --baseline "$WORK/scratch_baseline.json" \
  --endpoint route-1x1 --out "$WORK/route-map/out"
```

**The core pricing (L11b).** Three cacheless RV32I cores synthesized out of context with `AreaOptimized_high` for the same part: the shipping VexiiRiscv netlist the export reads, LiteX's VexRiscv `Min` netlist, and PicoRV32 with LiteX's `minimal` parameters. Each is the core alone, with whatever bus bridges its netlist contains; the figures are in [L11](#l11-the-soc-side).

### Reproduce L11b core pricing

This recipe reproduces the three historical area-only syntheses.
It is documentation; Round 1c executes no Vivado run.
Use Vivado 2026.1 build 6511674.
Match the named source bytes.
Set these environment variables to absolute paths:

| Variable | Meaning |
|---|---|
| `WORK` | Fresh scratch output directory, outside the repository |
| `CPU_VEXII_DIR` | VexiiRiscv package's `verilog` directory |
| `CPU_VEXMIN_DIR` | VexRiscv package's `verilog` directory |
| `CPU_PICO_DIR` | PicoRV32 package's `verilog` directory |

The retained sources have these sizes and SHA-256 digests:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `Ram_1w_1rs_Generic.v` | 1,580 | `c319d54c5a0bbe20a72ab9b394a3a1e57ef34866ae2478c5caed50e064a72523` |
| `Ram_1w_1ra_Generic.v` | 1,068 | `c8361e5fd0bc23be5f91cb2b63a091ab41bcdd857cc1c97f6e7e4ef8b6f61626` |
| `VexiiRiscvLitex_f5f08b170311db53220574624f819159.v` | 1,575,730 | `c208df0b7fafcaab190dba3f1734f2a38acd54645b33a834b0e59282e6a7813d` |
| `VexRiscv_Min.v` | 198,950 | `758874a989724fe2b92a5413b43265c9a5129638fee9d7358fcd6724992b598f` |
| `picorv32.v` | 94,657 | `0836050971b3c6cdd28ac3b1e5719a67fb645161912bef1e472e63995ceb0622` |

Check the digests before reproduction; regeneration may change the netlist.
Export the variables above and put Vivado on `PATH`.
Create this Tcl in the scratch directory:

```sh
bash -c 'cat > "$WORK/price_core.tcl"' <<'TCL'
set_param general.maxThreads 8
set name [lindex $argv 0]
set options {}
switch -- $name {
  vexii {
    set root $::env(CPU_VEXII_DIR)
    read_verilog [file join $root Ram_1w_1rs_Generic.v]
    read_verilog [file join $root Ram_1w_1ra_Generic.v]
    set top VexiiRiscvLitex_f5f08b170311db53220574624f819159
    read_verilog [file join $root ${top}.v]
  }
  vexmin {
    set top VexRiscv
    read_verilog [file join $::env(CPU_VEXMIN_DIR) VexRiscv_Min.v]
  }
  pico {
    set top picorv32
    read_verilog [file join $::env(CPU_PICO_DIR) picorv32.v]
    foreach {parameter value} {
      ENABLE_COUNTERS 0 ENABLE_COUNTERS64 0 ENABLE_REGS_16_31 1
      ENABLE_REGS_DUALPORT 1 LATCHED_MEM_RDATA 0 TWO_STAGE_SHIFT 0
      TWO_CYCLE_COMPARE 0 TWO_CYCLE_ALU 0 CATCH_MISALIGN 0
      CATCH_ILLINSN 1 ENABLE_PCPI 0 ENABLE_MUL 0 ENABLE_DIV 0
      ENABLE_FAST_MUL 0 ENABLE_IRQ 1 ENABLE_IRQ_QREGS 1
      ENABLE_IRQ_TIMER 0 ENABLE_TRACE 0
    } {
      lappend options -generic ${parameter}=${value}
    }
  }
  default { error "Unknown core: $name" }
}
synth_design -mode out_of_context -directive AreaOptimized_high \
  -part xc7a100t-fgg484-2 -top $top {*}$options
report_utilization -file ${name}_util.rpt
report_utilization -hierarchical -hierarchical_depth 4 \
  -hierarchical_min_primitive_count 0 -file ${name}_hier.rpt
puts "PRICED $name"
TCL
```

Run sequentially under one lock, without another heavy build:

```sh
flock /tmp/milan-vivado.lock bash -c '
  set -eu
  for core in vexii vexmin pico; do
    mkdir "$WORK/$core"
    cd "$WORK/$core"
    rc=0
    vivado -mode batch -source "$WORK/price_core.tcl" -nojournal \
      -log "$core.log" -tclargs "$core" > "$core.stdout" 2>&1 || rc=$?
    echo "$rc" > "$core.rc"
    test "$rc" -eq 0 || exit "$rc"
  done
'
```

No XDC or clock constraint was supplied in these syntheses.
Synthesis-worker settings were defaults; general threads were eight.
These match the retained Tcl, including every PicoRV32 override.
The reports should show 3,066 / 843 / 1,051 LUTs.
Read FF and BRAM against the [L11 table](#l11-the-soc-side).
A changed source digest makes this a different pricing experiment.
Neither result establishes integrated replacement cost or timing acceptance.

| Run | rc | Minutes | Log | Log SHA-256, first 16 | Log bytes |
|---|---:|---:|---|---|---:|
| Shipping export, [`milan_soc.py`](../../sw/litex/milan_soc.py) without `--build` | 0 | about 2 | `ax7101-elaboration.log` | `437f11cf5ddd1ce4` | 60,087 |
| Integrated route, 1x1 | 0 | 52.5 | `baseline.log` | `16cbfa00cca1f514` | 816,503 |
| Standalone synthesis, 1x1, 20 ns | 0 | 21.0 | `baseline.log` | `96910f8fcb64bf1c` | 248,489 |
| Route map, [`route_map.tcl`](../../syn/resmap/route_map.tcl) | 0 | 0.5 | `route_map.log` | `0881e5e4dcd735f2` | 6,929 |
| Map tie, `resmap_map.py map` (175 blocks, every tie held) | 0 | - | `resmap.log` | `2e789a95f2c5064e` | 107 |
| Gate, `check --endpoint route-1x1` against the record | 0 | - | `gate_route_vs_record.log` | `b82def0b753d4fd6` | 1,051 |
| Gate, `check --endpoint ooc-1x1` against the record | 0 | - | `gate_ooc_vs_record.log` | `b2469c8f91130e4b` | 371 |
| Core pricing, the shipping VexiiRiscv netlist | 0 | about 1 | `vexii.log` | `f933a1b83daf101d` | 103,103 |
| Core pricing, VexRiscv `Min` | 0 | about 1 | `vexmin.log` | `75ee4a4f8a55d345` | 32,238 |
| Core pricing, PicoRV32 `minimal` | 0 | about 1 | `pico.log` | `fdbb010a293c3750` | 36,210 |

The route waited 75 minutes for the lock and ran its synthesis with the lane's memory limit reached; no process was killed.
No log contains a `Synth 8-4445` diagnostic: the one match in the route's and the standalone run's logs is the echoed command that promotes it to an error, and the other logs have none.
The routed checkpoint `alinx_ax7101_route.dcp` hashes to `ac7a716819091b49` (110,137,721 bytes) and the image manifest `baseline_images.json` to `1fab9d504ab04761`.

Reports, checkpoints and full digests stay outside the repository with the measurement directories; the lane's handoff lists them.

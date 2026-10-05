# Mark II area plan

Stage 1 of issue #640: the measured baseline, the inventory, the redesign levers and the lane sequence that would bring the routed shipping image under NFR-RES-01's 60 percent LUT target.
It was measured on 2026-10-05 at dev `e617275074e370cec342af99b929e2588fc8d43f`.
This page changes no RTL, configuration, register map or parameter.
The manager rules on the lane sequence before any RTL work starts.
Milestone 12 is due 2026-12-15, before the release gate of milestone 6, so the #396 soak and audio runs will run on the redesigned image.

## Contents

- **[Summary](#summary)** -- The baseline, the gap, what the levers add up to, and the decisions the plan waits on.
- **[Target](#target)** -- NFR-RES-01's 38,040-LUT limit, the plan's 5 percent margin, the timing gate and the due date.
- **[Baseline at dev e6172750](#baseline-at-dev-e6172750)** -- The routed shipping image and `KL_pp_shadow` at 1x1 measured at this head, per hierarchy down to each protocol engine, and the second pin adoption's measured image.
- **[Inventory](#inventory)** -- Every hierarchy above 500 LUTs: its protocol function and clause, how it is built, and which of its cost a standard sets.
- **[Levers](#levers)** -- Twelve levers, each with its saving and basis, risk, verification cost and protocol-visible effect.
- **[Ledger](#ledger)** -- What the shared sequencer displaces, block by block, and every lever subtracted from the projected start at central, low and high estimates.
- **[Lane sequence](#lane-sequence)** -- The ordered lanes to 2026-12-15, each with its LUT target, repository, verification, risks and dependencies.
- **[What holds throughout](#what-holds-throughout)** -- The suites and counts, ATDECC as the only source of state, the second port, the gate's re-record and timing.
- **[Decisions needed](#decisions-needed)** -- The rulings the lanes need before any RTL work: the equivalence bar, diagnostics, internal timing, the SoC, the margin and the RISC-V direction.
- **[Method and receipts](#method-and-receipts)** -- The recipe, how a head the gate does not describe is mapped, the core pricing, and every run's exit status and log digest.

## Summary

- **The baseline.** At dev `e6172750` the routed shipping image uses 50,702 LUTs, 79.97 percent of the device: 12,662 over NFR-RES-01's 38,040 and 14,562 over this plan's 36,140. The protocol processor holds 24,051 of them, the gPTP plane 4,999, the CSR plane 2,907 and the SoC side 8,564.
- **The start.** The second pin adoption (#661), which carries the #232, #230 and #639 area work, measured its route at 50,318 LUTs (author evidence under review): 384 below this head, 358 above what the three lanes' own deltas added up to.
- **The gap.** From that start, 12,278 LUTs must go to meet the limit and 14,178 to meet the plan target: about 28 percent of the image. Most of the area is in the processor, as #649 found.
- **What the levers give.** Inside today's requirements, the ten hardware levers in the [ledger](#ledger) sum to about 12,750 LUTs at central estimates and reach 37,568: under the limit by 472, short of the plan target by 1,428. One more engine-sharing lever reaches 36,368, still 228 above the plan target. Across the levers' ranges the result lies between about 33,000 and 41,900. **No priced sequence reaches the 5 percent margin at central estimates** (D8).
- **What that rests on.** About 6,000 of the saving is one redesign that no prototype has measured yet: the protocol engines time-multiplexed onto one micro-coded sequencer (L1). Another 3,300 is the SoC side (on-chip main memory and a smaller control core), which needs owner decisions and a change to #70's staging buffers. Without the SoC levers the image stays near 40,900, over the limit.
- **The RISC-V direction** (L2) is the one lever large enough to reach the target on its own, and it needs REQUIREMENTS section 1, NFR-SCOUT-02, NFR-SCOUT-03 and the ownership rule changed. It is priced, not planned.
- **The schedule.** Ten weeks hold only if the [decisions](#decisions-needed) are taken before week 1 and the sequencer's three sub-lanes run in parallel from week 1. The plan should be re-measured when the sequencer's first sub-lane routes, in week 4.
- **No RTL, configuration or parameter changed here.** The resource gate's record is unchanged; it is re-recorded only by the lane that reaches the target (D7).

## Target

| Item | Value |
|---|---|
| NFR-RES-01 ([requirements](../reference/FR_NFR.md)) | at most 60 percent of `xc7a100t`'s 63,400 LUTs: 38,040 |
| Plan target, about 5 percent below the limit (D8) | at most 36,140 LUTs, 57.0 percent |
| Timing | the [build gate](../integration/BUILDING.md#5-gates-before-a-build-is-good) at the shipping 50 MHz datapath clock: WNS at least +0.03 ns and WHS at least 0 at every corner |
| Function | unchanged: every suite, campaign and compliance check at its counts |
| Due | 2026-12-15 (milestone 12) |

The owner kept NFR-RES-01 at 60 percent on 2026-10-03 and assigned the gap to this redesign ([decision](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967924270)).
The [area budget](AREA_BUDGET.md#protocol-processor-budget-and-resource-gate) holds the gate's record until then.

## Baseline at dev `e6172750`

### What changed since the gate's record

The resource gate's record describes dev `54643724` ([area budget](AREA_BUDGET.md#the-resource-gate)).
Since then dev changed one shipping-image input functionally: `KL_crf_rx.sv` now scores a locked CRF input's unbind as one MEDIA_UNLOCKED (#653).
`KL_nvm_backend.sv` gained a named constant with no logic, `milan_datapath.sv` a comment, the builder a generation-time refusal (#652), and `syn/ooc/pp_baseline.py` the `--integrated-clock` option.
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
22 slices are free: placement, not LUTs, is the binding limit until this plan lands.

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

The run equals the gate's `ooc-1x1` record in every gated figure (`check --endpoint ooc-1x1` exits 0 with no movement): no wrapper input changed since dev `54643724`, and its sub-blocks match the #234 page's combination C.
The routed wrapper is 0.988 of it (24,051 LUTs), the ratio the [ledger](#ledger) uses to carry standalone savings to the route.
The two hierarchies attribute differently: the AECP dynamic-state store is 152 LUTs here and 1,265 in the routed hierarchy, which places other AECP logic under its name.

### After the second pin adoption

The second pin adoption (#661) moves the processor to `ead80360`, which carries #232, #230 and #639.
Its lane published its measured image on 2026-10-05 ([REVIEW READY](https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5990292142), head `42f65447`, on dev `506d91db`, which already carries #653).
That is author evidence under review, not a merged record; this plan starts from it because it is the only measurement of the adopted image.

| Endpoint | LUT | FF | Slice | RAMB36 | WNS / WHS ns | Against the gate's record |
|---|---:|---:|---:|---:|---:|---|
| Route, second pin (#661) | 50,318 | 54,214 | 15,789 | 74 | +0.108 / +0.036 | -449 LUT, -5,420 FF, -43 slices, -5 RAMB36 |
| Route, this head | 50,702 | 59,677 | 15,828 | 79 | +0.244 / +0.036 | -65 LUT, +43 FF, -4 slices |
| Standalone 1x1, second pin (#661) | 23,178 | 19,776 | - | - | - | -1,154 LUT, -5,569 FF |
| Standalone 8x8, second pin (#661) | 29,853 | 27,370 | - | - | - | -1,703 LUT, -6,567 FF |

So the adoption moves the route by -384 LUTs against this head and leaves 61 slices free.
The three area lanes' own routes, each measured against one base route with the C8, P2-P1 and C10 parent patches, explain most of it:

| Change | Base route LUT / FF | Head route LUT / FF | LUT change | FF change | Other |
|---|---:|---:|---:|---:|---|
| Processor `main` before the area lanes, with the parent patches, against the gate's record | 50,767 / 59,634 | 51,434 / 59,691 | +667 | +57 | C7, C8, P1, P2, #143, C10 |
| #232, notification registry in distributed RAM (processor PR #153) | 51,434 / 59,691 | 50,671 / 57,660 | -763 | -2,031 | `u_notify` -927 LUT |
| #230, SRP timer FIFOs and walk storage (processor PR #154) | 51,434 / 59,691 | 51,005 / 57,262 | -429 | -2,429 | `u_srp` 4,340 to 3,711 LUT |
| #639, timer-arm rings and listener records (processor PR #155) | 51,434 / 59,691 | 51,152 / 58,598 | -282 | -1,093 | RAMB36 79 to 74 |
| The three added, as a projection | | 49,960 / 54,138 | -807 against the record | | |

The measured adoption is 358 LUTs and 76 FFs above that projection: the lanes' deltas do not add exactly, and processor PRs #152 (tests) and #157 (one GET_DYNAMIC_INFO classifier hunk) were in none of those routes.
The [ledger](#ledger) starts from the measured 50,318.

## Inventory

Every hierarchy of the routed image above 500 LUTs, in the rebuilt hierarchy's names; the image itself is left out, and a parent whose only large child is that child shares its row.
"Set by the standard" is the part of the cost a Milan or IEEE clause fixes: a state machine's existence, a field's width, a count's minimum.
"Implementation choice" is the part this design chose: how state is stored, how many copies of the logic exist, how wide an internal path is.
Clauses are IEEE 1722.1-2021, IEEE 1722-2016, IEEE 802.1Q-2018, IEEE 802.1AS-2011 and Milan v1.2.

**Protocol processor**

| Hierarchy | LUT | FF | Protocol function and clause | How it is built | Set by the standard | Implementation choice |
|---|---:|---:|---|---|---|---|
| `milan_datapath` | 42,138 | 48,474 | the whole fabric endpoint below the SoC: the protocol processor, the gPTP plane, AVTP/AAF/CRF media, the CSR plane | one module with the blocks below and its own per-stream registers | see the blocks | see the blocks |
| `milan_datapath/pp_shadow` | 24,051 | 24,263 | The ATDECC entity: ADP, ACMP, AECP, SRP, the saved-state backend (1722.1 clauses 6 to 9; Milan v1.2 Sections 4.2.7 and 5) | `KL_pp_shadow` around `protocol_processor_top`, the NVM backend and the control-frame FIFO | the protocols and their state | one engine per protocol, contexts per stream |
| `.../pp_shadow/u_pp` | 23,480 | 23,433 | `protocol_processor_top`: every engine below, the packet engine and the timer-arm queues | one engine per protocol around a shared RX parser, TX slot pool and timer service | the protocols | one engine per protocol; its own logic holds the timer-arm queues in flip-flops at this head (#639 moves them to distributed RAM) |
| `.../u_pp/u_aecp` | 7,451 | 3,500 | AECP AEM commands and responses (1722.1 clauses 7.4 and 9; Milan v1.2 Section 5.4) | a dispatch cone, the micro-coded engine, the dynamic-state store, the descriptor store over DRAM, the saved-state writer and the response-buffer DMA | the served command set, the response formats, the dynamic state Milan lets a controller set | the dispatch decode in logic, dynamic state in flip-flops |
| `.../u_aecp/@own` | 1,798 | 1,099 | command dispatch and AECPDU framing | a pop-time opcode decode feeding the microcode address, operand staging and the TX slot writer | the opcode set and PDU layout | the decode as a logic cone rather than a dispatch ROM |
| `.../u_aecp/u_ucpu` | 1,720 | 495 | executes every AEM command's microprogram | four-stage pipeline, 16 x 64 operand file in distributed RAM, 2,048 x 48 microcode in three RAMB36 | none | the engine itself: it is the time-multiplexed form L1 extends |
| `.../u_aecp/u_d3` | 1,405 | 485 | saving and restoring the non-binding dynamic state (Milan v1.2 Sections 5.3.5.1, 5.3.7.1, 5.3.8.1, 5.3.11.1) | a hardwired record writer per group with debounce, framing and restore transaction | which values survive power loss | a second record manager beside the binding manager, hardwired |
| `.../u_aecp/u_dyn` | 1,265 | 467 | the settable dynamic state (Milan v1.2 Sections 5.3.5, 5.3.7, 5.3.8, 5.3.11, 5.3.12) | flip-flop fields behind a read multiplexer addressed by field | the set of values and their widths | flip-flops rather than a RAM table |
| `.../u_aecp/u_store` | 974 | 694 | READ_DESCRIPTOR and the name table (1722.1 Section 7.4.5; Milan v1.2 Section 5.3.13) | index map in distributed RAM, line and names in block RAM, a DRAM read master | the descriptors and names served | the image in DRAM, the index in distributed RAM |
| `.../u_pp/u_notify` | 3,118 | 3,299 | registered controllers, the entity lock and unsolicited notifications (Milan v1.2 Sections 5.3.4.1, 5.3.4.2, 5.4.5; 1722.1 Sections 7.4.2, 7.4.37, 7.4.38) | at this head, a 16 x 128-bit registry in flip-flops with 16 parallel identity compares, pending-class vectors per controller, throttle stamps (#232 moves the registry to distributed RAM) | at least 16 controllers, each with its own sequence ID; 60 s lock | parallel compares and flop storage |
| `.../u_pp/u_listener` | 1,414 | 1,110 | the ACMP listener state machine (Milan v1.2 Section 5.5.3; 1722.1 clause 8) | already one event-at-a-time executor over per-sink records, a ROM transition matrix and hardwired action primitives, records in five RAMB36 at this head (#639 moves them to distributed RAM) | the state machine and the ACMPDU | hardwired actions and a 376-bit record |
| `.../u_pp/u_talker` | 689 | 517 | the stateless ACMP talker responder and the destination-MAC gate (Milan v1.2 Sections 5.5.2.7, 5.5.4) | response logic and one gate per source | the four responses | per-source gate replication |
| `.../u_pp/u_timer` | 884 | 179 | every protocol timer: MRP, ACMP and AECP timeouts, ADP valid time, the lock | prescalers, a millisecond timebase, a 61-slot deadline RAM swept one slot per cycle | the timers and their values | per-slot armed flip-flops and wide modular compares |
| `.../u_pp/u_dispatch` | 775 | 635 | per-protocol command queues between the parser and the engines | four queues of wide transaction records in distributed RAM (depths 4, 4, 4, 2) | none | one queue per protocol |
| `.../u_pp/u_nvm_shadow` | 790 | 1,118 | saving and restoring each sink's binding (Milan v1.2 Sections 5.3.8.1, 5.5.3) | capture of the listener's record writes, a preload face, a record serializer | which binding fields survive power loss | a hardwired manager of its own |
| `.../u_pp/u_originator` | 721 | 885 | entity-initiated commands: ACMP PROBE_TX, AECP CONTROLLER_AVAILABLE, their retries and timeouts | an in-flight table matched on key and sequence ID | sequence IDs, one retry, the timeouts | a separate table and matcher |
| `.../u_pp/u_rx_validator` | 543 | 751 | the shared receive front end: address and EtherType gates, subtype demux, common-header extraction, the MRP bypass | a beat-wise parser | the address, EtherType and header rules | one parser for every protocol, already shared |
| `.../u_pp/u_srp` | 4,219 | 6,264 | the MSRP and MVRP participant (802.1Q-2018 clauses 10, 11, 35; Milan v1.2 Section 4.2.7) | stream FSMs per context, a vector decoder, an encoder with pending tables, admission, VLAN and Domain | one applicant and registrar per declared attribute, the exact three-field match, the MRP timers | every context evaluated in parallel every cycle |
| `.../u_srp/u_encoder` | 1,320 | 1,062 | MRPDU vector encoding, one MRPDU per application per join tick (802.1Q-2018 Sections 10.8, 35.2.2) | two pending tables in distributed RAM, run detection, three- and four-packed coding | the PDU format and the aggregation rule | table storage and parallel run compares |
| `.../u_srp/@own` | 862 | 2,792 | SRP glue: the event merge, the service port and the timer-arm FIFOs | at this head the two FIFOs are one flop array (#230 moves them to distributed RAM) | none | the FIFO storage |
| `.../u_srp/u_talker` | 612 | 672 | the talker-side applicant and registrar per source (802.1Q-2018 Tables 10-3, 10-4; Milan v1.2 Section 4.2.7.2.2) | one FSM pair per context, evaluated in parallel | the state machines | parallel evaluation per context |
| `.../u_srp/u_decoder` | 584 | 630 | MRPDU vector decoding and its malformed-PDU tolerance (802.1Q-2018 Section 10.8.1.2; Milan v1.2 Section 4.2.7.1) | a byte-serial walker emitting one value per cycle | the PDU grammar | none of note |
| `.../pp_shadow/u_nvm` | 504 | 476 | the saved-state backend (#70) | record framing and the KLJ2 container over the NVM port | which state is saved | a fabric backend |

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

Each lever below states its estimated saving in routed LUTs, the basis of the estimate, its risk, its verification cost and its protocol-visible effect.
A saving is an estimate until a matched before-and-after route measures it.
Where a measured prototype exists it is named; most levers here have only a measured analog or a measured upper bound, and each lever's basis says which.
"Routed block" means the block's own row in the routed hierarchy above: removing the block cannot save more than that before re-placement, and replacing it saves that minus the replacement's cost.

The levers are numbered L1 to L12.
L1 to L6 are the six the assignment names; L7 to L11 are the others the inventory found; L12 lists the prunes that would cost function.

### L1 Time-multiplexing the protocol engines onto one sequencer

**What.** The processor already serves AECP from a micro-coded engine, `KL_aecp_ucpu` (four-stage pipeline, 2,048 x 48 microcode ROM in block RAM, 16 x 64 operand file in distributed RAM).
The other control engines are hardwired, one per protocol: the ADP advertise and discovery machines, the ACMP talker responder and listener executor, the originator, the notification scheduler, and the two saved-state record managers.
L1a moves their sequencing onto one time-multiplexed engine of the same family, keeps the byte datapaths (parser, TX slots, timer service) hardwired, and moves every per-entity table (registry, records, pending vectors, dynamic state) into block RAM read through the engine's state port.
L1b extends the same move to the SRP stream FSMs, admission and encoder tables; L7 is the smaller SRP-only form.

**Saving.** About 4,700 LUTs for L1a (range 2,800 to 6,400) and 1,300 more for L1b (range 700 to 1,700), figured block by block in the [ledger](#ledger).

**Basis.** No prototype of the consolidated engine exists; this is the plan's largest uncertainty.
The displaced blocks are measured: `u_adp`, `u_talker`, `u_listener`, `u_originator`, `u_notify`, `u_aecp/@own`, `u_aecp/u_dyn`, `u_aecp/u_d3`, `u_nvm_shadow` and the dispatch queues, read from the standalone synthesis, which attributes in source terms.
The engine's cost is measured twice: the AECP engine skeleton at 1,068 LUTs out of context (the protocol processor's own resource and effort record, `10_RESOURCE_AND_EFFORT` in its documentation, section 6; called "the processor record" below) and 1,720 routed in this image.
The fraction of each block a sequencer displaces follows the processor record's scenario C model (65 to 85 percent of a block's mass).
The processor's substitution for the legacy control plane, whose AECP made the same move, measured 3,459 fewer LUTs after synthesis and 2,919 after placement on the shipping shape (same record, section 1b).
Each block's displaceable share and the engine's added cost are tabled in the [ledger](#ledger).

**Risk: high.**
The engines being replaced implement Milan-normative state machines that were corrected against live controllers and bridges; ACMP is the processor's highest-rework engine.
One engine serves several protocols, so contention must be bounded: the processor record (section 7) gives AECP a 615x to 8,000x margin on its 240 ms response line and ACMP a 200 ms limit, and the sequencer must hold both with the notification fan-out of 16 controllers.
Response latency moves from under a microsecond to tens of microseconds: inside every normative timeout, but not cycle-exact.

**Verification.** Every processor suite at its count (33 suites, about 1,021,600 checks at the second pin), lint, `make check`, the Yosys gate, and the `pp_top`, ACMP, ADP, notification, AECP, dispatch, D3, GSI and name-write campaigns at their recorded counts; the parent consumer set of 17; `pp_shadow`, `nvm_cosim` and the `milan_dp` suites; `check_nvm_capture.py` (8x8 capture at most 24.5 ms); the bench suite; the #396 soak.
Cycle-exact lockstep against the old engines is not possible; equivalence is at the PDU and port-transaction level (see [decisions](#decisions-needed)).

**Protocol-visible effect.** None on the wire: every PDU's bytes, order and timeout behaviour are kept. The internal latency change needs the ruling in [decisions](#decisions-needed).

**Second port.** The sequencer's tables stay indexed by AVB interface (`N_IF_P`), as the ADP engine's are today, so a second interface adds table rows, not engines.

### L2 Moving slow-path control to the RISC-V

**What.** Descriptor serving, MAAP, the SRP declaration bookkeeping and ACMP state served by the bare-metal firmware on the cacheless RV32I control hart, with fabric keeping the parsers, framers, timers and a mailbox.

**Saving.** About 5,500 to 6,500 LUTs if the four named functions move; up to about 15,000 if the whole ATDECC control plane moves; about 300 to 600 if only descriptor serving moves.

**Basis.** The standalone rows below as the upper bound, less an estimated 800 to 1,500 LUTs of fabric mailbox and queue logic. The four named functions are about 7,100 LUTs: descriptor serving (about 600 of the AECP engine), MAAP (519 routed), the SRP declaration bookkeeping (the stream FSMs, admission, the encoder's tables and the glue #230 left, about 2,400) and ACMP state (the listener, the talker responder, the binding store and part of the originator, about 3,700). The whole plane adds the rest of the AECP engine, notification and ADP, about 16,500 in all.
The processor record priced the legacy plane's move to software at 6,206 LUTs and 9 RAMB36 (section 6).
Descriptor serving alone frees only part of `u_aecp/u_store`, because the AECP engine still serves every other command.

**Risk: very high, and blocked by the requirements.**
REQUIREMENTS section 1 gives the fabric MAAP and IEEE 1722.1 processing.
NFR-SCOUT-02 keeps protocol control with its fabric owner, and NFR-SCOUT-03 forbids packet deadlines that depend on firmware service latency.
The [ownership rule](../ARCHITECTURE_HW_SW_SPLIT.md#1-ownership-rule) puts ADP, AECP, ACMP and SRP in fabric.
NFR-SCOUT-01 fixes the CPU at one cacheless RV32I hart, and the firmware runs from the 128 KiB integrated ROM.

**Verification.** The processor suites that test the moved engines would be replaced by firmware tests, so their counts cannot be held; every compliance item touching the moved protocols re-runs on the bench.

**Protocol-visible effect.** Response latency becomes firmware service latency (milliseconds), inside the normative timeouts but not deterministic.

It is priced here and not planned: it needs the owner to change four normative statements, and its firmware stack cannot be written and qualified by 2026-12-15.

### L3 Block RAM in place of LUT and flip-flop tables

**What.** Arrays held in distributed RAM or flip-flops whose readers already register their output move to block RAM, cycle for cycle.
L3 covers the arrays outside the engines L1 replaces, so nothing is moved twice: the SRP timer-arm FIFOs and walk copies (#230's distributed RAM), the processor timer-arm rings (#639), the descriptor index, the gPTP engine's state regions, the render set-point table and the SoC's generated FIFO storage.
The notification registry, the listener records and the dispatch queues move with L1, into the sequencer's block RAM tables.

**Saving.** About 800 LUTs (range 500 to 1,200) for 4 to 8 block RAM tiles, inside the 121.5-tile ceiling.

**Basis.** The routed LUTRAM column per block (measured, in the [routed hierarchy](#the-routed-hierarchy)); #639's measured exchange (5 RAMB36 traded for 63 RAM32M and 38 to 195 LUTs); the processor record's measured precedent of 1,051 slice LUTs freed for 1.5 tiles.
A LUT-RAM LUT moved to block RAM saves itself and part of its read multiplexer; the operand files of the two micro-coded engines stay, because they need two reads in one cycle.

**Risk: medium.** An array whose reader needs a same-cycle read either keeps its distributed RAM or takes a pinned read-latency change. Wide records (376 bits) waste block RAM unless packed over several beats.

**Verification.** A lockstep bench per array, as #232 and #639 did; the owning block's suites and campaigns at their counts; the route and the resource gate.

**Protocol-visible effect.** None when cycle-exact; a moved read cycle is pinned by a suite check first.

### L4 Width narrowing derived from the entity model

**What.** Internal widths sized from the generated shape header instead of the protocol field width: descriptor indices, name and record indices, per-type counts. Wire fields keep their protocol width: entity IDs (64 bits), MAC addresses (48), sequence IDs (16) and Milan counters (32) are set by the standards.

**Saving.** About 200 LUTs (range 100 to 400).

**Basis.** #649's measured sensitivities: a descriptor index entry costs 3.5 Yosys LUTs, a name entry 1.7, the descriptor line nothing measurable, and Vivado reads about 0.45 of a Yosys figure at this shape. The stream-shaped parameters are already derived (#233 audit).

**Risk: low.** **Verification:** the owning suites. **Protocol-visible effect:** none.

### L5 The remaining #233 items

**What.** The VLAN reference counter `REFCNT_W_P` (5 bits against the 3 a 2/2 shape needs), `DESC_LINE_BYTES_P` (576, coupled to the 524-byte GET_DYNAMIC_INFO buffer) and the FIFO depths (dispatch 4/4/4/2, notification command queue 16, SRP timer FIFOs 32).

**Saving.** About 30 to 100 LUTs in total.

**Basis.** Measured: `u_srp/u_vlan` is 138 routed LUTs; #649 measured the descriptor line at -0.08 Yosys LUTs per byte and the index at 3.45 per entry (`DESC_IDX_ENTRIES_P` 32 to 16: -53 Yosys LUTs); since #230 and #639 the FIFOs and queues sit in distributed RAM, where depth costs almost nothing.

**Risk: low.** Each needs a processor parameter, which the #233 audit stopped on.

**Verification:** the SRP, dispatch and notification suites. **Protocol-visible effect:** none.

These are folded into L1's and L4's lanes rather than given a lane: alone they move nothing that matters.

### L6 Diagnostic-only logic off in the shipping build

**What.** The AAF latency taps (`LTAP_P`) and the datapath probe groups (`DPROBES_P`) are already build-selectable Tier 1 blocks ([area budget](AREA_BUDGET.md#tier-1---implemented-optional-fabric-blocks)); the shipping configuration keeps both on. The processor's trace ring is diagnostic too and is not yet selectable.
L6 turns them off in the shipping configuration and keeps a diagnostic configuration that builds them.

**Not diagnostic, and kept:** the talker counters (`talker_diag`, Milan v1.2 Table 5.4), the listener monitor (Table 5.6), the MAC counters (REQ-MAC-04), the loopback lane (its clusters are in the entity model), the RX address filter (REQ-MAC-02 is a MUST), the CSR diagnostic words (already structural zero).

**Saving.** About 700 LUTs (range 650 to 750).

**Basis.** Measured routed blocks: the latency taps, 672 LUTs and 620 FFs; the trace ring, 37 LUTs and one RAMB36; #649's Yosys marginal for the probes (26 LUTs, about 12 after calibration).

**Risk: low technically; it is a product decision.** #649 records that the shipping image keeps the taps on purpose, and their silicon latency figures cannot be repeated on an image without them.

**Verification.** The builder bank (Tier 1 table, `check_sweep_shape.py`, `check_deploy_shape.py`, `check_entity_shape.py`), `milan_dp` at both settings, the latency-tap suites in the diagnostic build, the CSR bench (the LTAP window reads zero), the route and the gate.

**Protocol-visible effect.** None. The LTAP CSR window reads structural zero in the shipping build.

### L7 SRP: one shared evaluator per FSM

**What.** #230's option (a), recorded for this redesign ([ruling](https://github.com/kebag-logic/milan-fpga/issues/230#issuecomment-5977836860)): one evaluator per SRP stream FSM, with the per-stream contexts in distributed RAM evaluated one per cycle.

**Saving.** About 450 LUTs at 1x1 (range 300 to 600); about 3,100 at 8x8.

**Basis.** #638's estimate from the measured per-context marginals, 212 LUTs per talker context and 227 per listener context (the [#234 baseline](../findings/234_PP_SHADOW_AREA_BASELINE.md#processor-sub-blocks)); #230's measured marginals after its storage change (200 and 210).
At 1x1 two contexts share one evaluator, so the saving is one context's marginal per FSM.

**Risk: medium.** `KL_srp_decoder` gains a ready on its event port. The SRP plane is silicon-validated against live bridges.

**Verification.** `srp_top` (128 arms), `srp_admission`, `srp_stream_fsms`, `srp_decoder` and `srp_encoder` suites and campaigns, `pp_top`, the bench suite's SRP items.

**Protocol-visible effect.** Registration indications and LISTENER_REG_CHANGE move by up to M - 1 and N - 1 cycles: one 20 ns cycle at 1x1, far inside MRP's 200 ms join time, but a cycle-level change the pre-adoption track ruled out. L1b subsumes L7 if it is taken.

### L8 The CSR plane's read path

**What.** `milan_csr` already keeps its inert RW groups in a block RAM shadow; its LUTs are the live read multiplexer over the fabric's status faces and the snapshot registers.
L8 restructures that read path (registered per-group pre-selection, the per-stream groups read through their index window), with no register address, width or reset value changed.

**Saving.** About 600 LUTs (range 400 to 1,000).

**Basis.** The routed block, 2,907 LUTs and 2,141 FFs (measured); #649's out-of-context fit, 2,893 LUTs fixed and 211 per stream. No prototype.

**Risk: medium.** The register map is an ABI (NFR-SCOUT-06); REQ-CSR-02's snapshot coherence must hold; an AXI-Lite read may take one or two more cycles.

**Verification.** The CSR bench, `tcam_csr`, the `milan_dp` suites, the firmware host tests, the register-map checks, a boot on the bench.

**Protocol-visible effect.** None.

### L9 Datapath per-stream contexts in RAM

**What.** The Table 5.6 listener monitor, the Table 5.4 talker counters, the channel-map capture and the render set-point hold their per-stream state in flip-flops behind read multiplexers. Each counter moves at most once per frame or observation interval, so a read-modify-write RAM serves it.

**Saving.** About 600 LUTs (range 400 to 900).

**Basis.** The routed blocks (measured); #649's per-stream marginals out of context (channel map 317, monitor 208, set-point 205 LUTs per stream) bound the per-stream part.

**Risk: medium.** GET_COUNTERS coherence and the Table 5.6 interval semantics.

**Verification.** `avtp_rxmon`, `tkdiag`, `chmap_capture`, `render_setpoint`, the `milan_dp` suites, the GET_COUNTERS campaigns.

**Protocol-visible effect.** None.

### L10 The gPTP plane

**What.** (a) Distributed RAM and flip-flop tables inside the plane move to block RAM or narrow, in the gPTP processor submodule. (b) One micro-coded engine serves both gPTP and AECP (#649's rank 3).

**Saving.** (a) About 500 LUTs (range 300 to 700). (b) About 1,200 more (range 900 to 1,500).

**Basis.** (a) The routed rows (measured), the engine's 464 LUT-RAM LUTs among them. (b) The smaller engine's routed 1,720 LUTs is the ceiling, less an estimated 300 for arbitration; the gPTP engine is a measured superset of the AECP skeleton.

**Risk.** (a) Medium. (b) High: gPTP handlers are time-critical (Sync and peer-delay turnaround) and would share an engine with AECP; it crosses two submodules and needs its own timing proof. NFR-SCOUT-02 keeps time discipline in fabric, which (b) does.

**Verification.** The gPTP processor's own suites; `gptp_plane`, `gptp_shadow`, `gptp_txts` and `milan_dp_gptp`; the gPTP bench evidence (#117).

**Protocol-visible effect.** None intended; (b) must prove its turnaround bounds.

### L11 The SoC side

**What.** (a) Replace the DDR3 main memory with on-chip RAM. (b) A smaller cacheless RV32I core. (c) The generated FIFO storage in block RAM (counted in L3).

**Saving.** (a) About 1,600 LUTs (range 1,200 to 2,000). (b) About 1,700 (range 1,300 to 2,200).

**Basis.** (a) #649's census by name: the DDR3 controller and PHY hold 823 and 873 LUT cells and 2,599 flip-flops (measured cells, not LUT sites). (b) Measured here, out of context at `AreaOptimized_high` ([method](#method-and-receipts)): the shipping VexiiRiscv netlist is 3,066 LUTs, 5,017 FFs and 4.5 tiles, about 600 LUTs of it the DMA bridges the processor's DRAM masters use; LiteX's VexRiscv `Min` is 843 LUTs, 791 FFs and one tile; PicoRV32 at LiteX's `minimal` parameters is 1,051 LUTs and 549 FFs. The routed core is 3,522 LUTs. The estimate keeps 300 to 600 LUTs for the interconnect, timer and interrupt logic LiteX adds around a core without them.

**Risk: high for both.**
(a) Main memory holds the descriptor image (7.5 KiB at 1x1), the response buffer (592 bytes) and the saved-state live and stage buffers, one 64 KiB erase block each. 29 tiles (about 116 KiB) are free under the ceiling at this head, so it fits only if #70's staging buffers shrink to the shape's container size, and it changes the SoC memory map.
(b) The firmware's timing obligations bound the core: the saved-state capture (8x8 at most 24.5 ms) and boot. NFR-SCOUT-01 allows any cacheless RV32I hart.

**Verification.** (a) The firmware host tests, `nvm_cosim`, `nvm_capture_cpu`, the builder and deploy shape gates, a boot and saved-state cycle on the bench. (b) The same, plus `check_nvm_capture.py`.

**Protocol-visible effect.** None.

### L12 Prunes that cost function, recorded and excluded

| Block | Routed LUT | Why it stays |
|---|---:|---|
| RX address filter | 513 | REQ-MAC-02 (MUST) requires station unicast and multicast filtering |
| Loopback lane | about 22 | its eight clusters are in the entity model |
| MAAP engine | 519 | dynamic stream addresses; the builder requires it for every talker |
| Media-clock servo, AAF clock meter | 899, 488 | CRF and AAF media-clock following (Milan v1.2 Section 7) |
| CRF sink and output | about 2,900 | the CRF stream ports |
| TDM render lane | 499 | the TDM8 output |
| Fewer than 16 controllers | 635 Yosys LUT each | FR-CTRL-03 and Milan v1.2 Section 5.3.4.2 require at least 16 |

## Ledger

**L1a, what the sequencer displaces.**
Each block's share is the part of it that is sequencing, state storage or a per-protocol PDU builder, which the shared engine and its block RAM tables take over; the rest (parsing, framing beats, counters on the wire path) stays.
The shares follow the processor record's 65 to 85 percent for the AECP emit mass, lowered where a block is already shared or table-driven.
The figures are the standalone synthesis's, which attribute in source terms; the routed wrapper is 0.988 of the standalone one.
The notification, saved-state writer and listener rows take the second pin's measured changes into account.

| Block | Standalone LUT | After the second pin | Share displaced | Displaced LUT |
|---|---:|---:|---:|---:|
| `u_pp/u_notify` | 3,175 | 2,248 (#232: -927) | 0.60 | 1,349 |
| `u_pp/u_aecp/u_d3` | 1,066 | 1,685 (P1's saved-state writer: +619) | 0.70 | 1,180 |
| `u_pp/u_aecp`, its own logic | 1,416 | same | 0.50 | 708 |
| `u_pp/u_aecp/u_dyn` | 152 | same | 0.70 | 106 |
| `u_pp/u_listener` and `u_pp/u_lsn_admit` | 1,441 | about 1,561 (#639: +38 to +195) | 0.50 | 780 |
| `u_pp/u_nvm_shadow` | 815 | same | 0.70 | 570 |
| `u_pp/u_originator` | 782 | same | 0.60 | 469 |
| `u_pp/u_talker` | 894 | same | 0.60 | 536 |
| `u_pp/u_adp` | 628 | same | 0.60 | 377 |
| `u_pp/u_dispatch` | 896 | same | 0.40 | 358 |
| **Displaced** | 11,265 | 11,077 | | **6,434**; 5,326 to 7,542 with every share 0.1 lower or higher |
| The engine: a second AECP-class engine (1,068 LUTs out of context, 1,608 in this standalone run) or the shared one with its arbitration and state regions (the gPTP engine's state regions route at 852) | | | | -1,000 to -2,500, central -1,700 |
| **L1a, standalone** | | | | **4,734**; 2,827 to 6,542 |
| **L1a, routed** at the wrapper's routed-to-standalone ratio of 0.988 | | | | **about 4,700**; 2,800 to 6,400 |

L1b is figured the same way from the standalone SRP rows: the talker and listener FSMs (662 and 420 LUTs, share 0.7), admission (337, 0.5), the encoder's tables (1,461, 0.4) and the glue #230 left (354 LUTs standalone after #230, 0.3): 1,616 displaced, less about 300 (200 to 600) for its tables and state regions on the shared engine, about 1,300 (700 to 1,700).

**The ledger, central estimates and ranges.**
The start is the second pin's measured image (#661, under review); each row subtracts one lever.

| Lane | Lever | Central | Range | Image after, central | Low end | High end |
|---|---|---:|---:|---:|---:|---:|
| M0 | the second pin adoption, measured by #661 | - | - | 50,318 | 50,318 | 50,318 |
| M1 | L6 diagnostics off | -700 | 650 to 750 | 49,618 | 49,668 | 49,568 |
| M2 | L3 block RAM tables outside L1 | -800 | 500 to 1,200 | 48,818 | 49,168 | 48,368 |
| M3 | L1a the shared sequencer | -4,700 | 2,800 to 6,400 | 44,118 | 46,368 | 41,968 |
| M3 | L4 and L5, widths and the #233 items | -250 | 130 to 500 | 43,868 | 46,238 | 41,468 |
| M4 | L1b SRP onto the sequencer | -1,300 | 700 to 1,700 | 42,568 | 45,538 | 39,768 |
| M5 | L8 CSR read path | -600 | 400 to 1,000 | 41,968 | 45,138 | 38,768 |
| M6 | L9 datapath contexts in RAM | -600 | 400 to 900 | 41,368 | 44,738 | 37,868 |
| M7 | L10a gPTP tables | -500 | 300 to 700 | 40,868 | 44,438 | 37,168 |
| M8 | L11a on-chip main memory | -1,600 | 1,200 to 2,000 | 39,268 | 43,238 | 35,168 |
| M8 | L11b smaller control core | -1,700 | 1,300 to 2,200 | 37,568 | 41,938 | 32,968 |
| M10 | L10b one engine for gPTP and AECP | -1,200 | 900 to 1,500 | 36,368 | 41,038 | 31,468 |

The limit is 38,040 and the plan target 36,140.
At central estimates every hardware lever but L10b reaches 37,568, under the limit by 472 (1.2 percent); with L10b, 36,368, still 228 above the plan target.

## Lane sequence

The sequence orders lanes by saving per unit of risk, keeps processor and parent lanes running in parallel, and puts every decision a lane needs in front of it.
Weeks count from Monday 2026-10-12, after the second pin adoption; the milestone's due date, 2026-12-15, falls in week 10.
"Image after" is the projected routed LUT count once that lane and every lane above it have landed, at central estimates, from #661's measured route.

| Lane | Weeks | Levers | Repository | Image after (LUT) | Needs first |
|---|---|---|---|---:|---|
| M0 | before week 1 | the second pin adoption (#661), at review | parent | 50,318 (measured by #661, under review) | in flight |
| M1 | 1-2 | L6 diagnostics off in the shipping build | parent; the trace ring's parameter in the processor | 49,618 | D2 |
| M2 | 1-4 | L3 block RAM for the tables outside L1 | processor, gPTP processor, parent | 48,818 | none |
| M3 | 1-8 | L1a the shared sequencer, in three sub-lanes: notification and originator; ACMP and ADP; the record managers and AECP dispatch. L4 and L5 ride with it | processor | 43,868 | D1, D3 |
| M4 | 3-8 | L1b SRP onto the sequencer, or L7 alone if L1b is refused | processor | 42,568 | D1, D3 |
| M5 | 2-6 | L8 CSR read path | parent | 41,968 | none |
| M6 | 2-6 | L9 datapath contexts in RAM | parent | 41,368 | none |
| M7 | 3-6 | L10a gPTP plane tables | gPTP processor, parent | 40,868 | none |
| M8 | 2-8 | L11a on-chip main memory; L11b once the smaller core is shown to hold the capture bound | parent SoC, firmware | 37,568 | D4, D5, #70 |
| M10 | 6-9, if needed | L10b one engine for gPTP and AECP | gPTP processor, processor | 36,368 | D6 |
| M9 | 9-10 | the pin adoptions, the integrated route, timing closure, the resource gate re-recorded at the target, every suite and campaign, the bench suite | parent | at most 38,040; 36,140 needs D8 | every lane above |

At central estimates M0 to M8 reach 37,568 LUTs: under the 38,040 limit by 472, short of the 36,140 plan target by 1,428.
M10 brings it to 36,368, still 228 above the plan target: no priced lever closes the margin at central estimates, and D8 asks how it is closed.
At the low end of every range the same sequence stops near 41,900 (41,000 with M10), above the limit; at the high end near 33,000 (31,500).
Without the SoC lane M8 it stops near 40,900 at central estimates: the limit is not reached inside today's requirements without the SoC decisions.
The plan is re-measured when M3's first sub-lane routes (week 4); that measurement decides whether M10 and D8's options are needed.

Per lane, its own LUT target, the files it changes, what it must show before its review, its risks and what it waits on:

| Lane | LUT target for its own change | Files | Verification it runs | Main risks | Depends on |
|---|---:|---|---|---|---|
| M1 | -700 | `configs/endstation_ax7101_1x1_tdm8.yaml` (`board.features`), its generated fragments; `protocol-processor/hdl/top/protocol_processor_top.sv` (a trace-ring parameter) | builder bank, shape gates, `milan_dp` both ways, latency-tap suites in the diagnostic build, CSR bench, route | the owner keeps the taps | D2 |
| M2 | -800 | `protocol-processor/hdl/srp/KL_srp_top.sv`, `protocol-processor/hdl/top/protocol_processor_top.sv`, `protocol-processor/hdl/aecp/KL_aecp_desc_store.sv`, `gptp-processor/hdl/top/KL_gptp_engine.sv`, `hdl/ieee1722/aaf/KL_render_setpoint.sv`, `sw/litex/milan_soc.py` | per-array lockstep with planted controls, owning suites and campaigns at their counts, standalone and route | an array needing a same-cycle read | none |
| M3 | -4,950 | `protocol-processor/hdl/adp/`, `protocol-processor/hdl/acmp/`, `protocol-processor/hdl/aecp/` and its microcode generator `protocol-processor/hdl/aecp/ucode/gen_ucode.py`, `protocol-processor/hdl/packet_engine/KL_pp_originator.sv`, `protocol-processor/hdl/top/protocol_processor_top.sv` | every processor suite and campaign at its count, a transaction-level equivalence bench, consumer set of 17, `pp_shadow`, `nvm_cosim`, `milan_dp`, NVM capture, bench suite | contention, latency, ACMP rework | D1, D3 |
| M4 | -1,300 (-450 for L7 alone) | `protocol-processor/hdl/srp/` | SRP suites and campaigns, `pp_top`, the bench suite's SRP items against live bridges | MRP cadence on a shared engine | D1, D3, M3's engine |
| M5 | -600 | `hdl/common/csr/milan_csr.sv` | CSR bench, `tcam_csr`, `milan_dp`, firmware host tests, register-map checks, bench boot | snapshot coherence, read latency | none |
| M6 | -600 | `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv`, `hdl/ieee1722/avtp/KL_talker_diag_ctx.sv`, `hdl/ieee1722/aaf/KL_chan_map_capture.sv`, `hdl/ieee1722/aaf/KL_render_setpoint.sv` | `avtp_rxmon`, `tkdiag`, `chmap_capture`, `render_setpoint`, `milan_dp`, GET_COUNTERS campaigns | counter coherence | none |
| M7 | -500 | `gptp-processor/hdl/top/KL_gptp_engine.sv` and its state regions, `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv` | gPTP processor suites, `gptp_plane`, `gptp_shadow`, `gptp_txts`, `milan_dp_gptp` | timestamp path timing | none |
| M8 | -3,300 | `sw/litex/milan_soc.py`, `sw/firmware/milan_baremetal/milan_baremetal.c`, the saved-state staging layout | firmware host tests, `nvm_cosim`, `nvm_capture_cpu`, `check_nvm_capture.py`, builder and deploy gates, bench boot and saved-state cycle | #70's staging redesign, memory map, core performance | D4, D5, #70 |
| M10 | -1,200 | `gptp-processor/hdl/ucpu/`, `protocol-processor/hdl/aecp/KL_aecp_ucpu.sv`, `hdl/ieee8021as/gptp_plane/KL_gptp_shadow.sv` | gPTP and processor suites, a turnaround proof, gPTP bench evidence | time-critical handlers on a shared engine | D6 |
| M9 | to at most 38,040, and 36,140 if D8 provides the rest | the `protocol-processor` and `gptp-processor` gitlinks, `syn/ooc/pp_resource_baseline.json`, the [area budget](AREA_BUDGET.md#protocol-processor-budget-and-resource-gate) | everything in [what holds throughout](#what-holds-throughout) | timing closure at the new density | all |

Each lane measures itself with the #234 recipe in a scratch parent, as #232, #230 and #639 did: the route and both standalone endpoints, before and after, one Vivado at a time under the host lock.

**The schedule is the plan's second risk.** The processor record's effort model put scenario C, one engine displacing the AECP emit mass, at 131 to 321 lane-days, 4 to 15 calendar weeks at 3 to 5 concurrent lanes. M3 and M4 displace about twice that mass. Ten weeks holds only with M3's three sub-lanes running in parallel from week 1 and the decisions below taken before week 1.

## What holds throughout

- **Every suite, campaign and compliance check at its counts.** The processor suites (33 suites, about 1,021,600 checks at the second pin), lint, `make check`, the Yosys gate, every recorded campaign, the parent consumer set of 17, the builder bank in both compiler modes, the parent Verilator suites, `check_entity_shape.py`, `check_nvm_capture.py`, the docs gates and the bench suite. A lane that cannot keep a count stops and asks; it does not rewrite the test (AGENTS section 8).
- **ATDECC is the only source of state.** Every protocol value has one owner. Moving a table to block RAM or onto the sequencer moves its owner; it never creates a copy. The CSR plane keeps republishing the processor's class-D face and stores no protocol state of its own. Firmware keeps its section 1 role and gains no protocol state.
- **The second-port redundancy path stays open.** No lever hard-wires one AVB interface: the sequencer's tables, the notification registry's port field and the ADP engine keep their interface index (`N_IF_P`). Milan v1.2 Section 8 redundancy stays out of scope for v1.2 (FR-MVU-03, NFR-SCOUT-05, #394); the measured per-port replication, about 7,100 routed LUTs plus a MAC, only fits once this plan lands.
- **The resource gate is re-recorded only in the lane that reaches the target** (M9), as the assignment and #640's acceptance say. Until then each lane passes the gate as an improvement ("re-baseline recommended") and records its measured image in this plan's ledger, not in `pp_resource_baseline.json`. This differs from the budget's rule that a merge which moves the image records its own re-baseline: see D7.
- **No port, register-map or wire change.** Register addresses, widths and reset values stay; every PDU keeps its bytes and its order.
- **Timing at the shipping clock.** Each route meets the build gate (WNS at least +0.03 ns, WHS at least 0, every corner) at the 50 MHz datapath clock.

## Decisions needed

- **D1, the equivalence bar for a redesigned engine.** L1 cannot be cycle-exact. Proposed: PDU-level and port-transaction equivalence against the current engines, every suite at its count, and committed tests that pin a cycle re-targeted under review rather than deleted.
- **D2, diagnostics in the shipping image.** Whether the shipping configuration drops the latency taps and probes (L6), with a diagnostic configuration kept buildable.
- **D3, internal timing is not protocol-visible.** Whether a change of internal latency inside every normative timeout, with no wire change, counts as "no protocol-visible effect" for L1 and L7. #230's ruling excluded it from the cycle-exact pre-adoption track only.
- **D4, on-chip main memory.** Whether the SoC drops DDR3 (L11a). It needs #70's staging buffers sized to the container and a memory-map change.
- **D5, the control core.** Whether the control hart becomes a smaller cacheless RV32I core (L11b, about 1,700 LUTs, priced here), provided it holds the saved-state capture bound and the boot timing.
- **D6, one engine for gPTP and AECP** (L10b): at central estimates M0 to M8 leave the margin short, so it is needed for any margin above 1.2 percent.
- **D7, the re-baseline rule during Mark II.** The budget's rule makes every image-moving merge record its own re-baseline; the assignment re-records only at the target. Proposed: Mark II lanes record their measured image in this plan's ledger and leave the gate's record alone, since an improvement already passes; the rule's purpose, that growth is never hidden, holds because the gate still judges each lane against the last record.
- **D8, the margin.** This plan reads "about 5 %" as 5 percent of the limit: at most 36,140 LUTs, 57.0 percent of the device; read as 5 points of the device it is 34,870. At central estimates the priced levers reach 37,568 (472 under the limit) without L10b and 36,368 with it, so neither reading is met. The ruling needed: accept a smaller margin, or close the last 1,400 to 2,700 LUTs with part of L2 (which needs D9), or decide after M3's first measured route.
- **D9, the RISC-V direction** (L2). Its saving is the largest single figure here, and it needs REQUIREMENTS section 1, NFR-SCOUT-02 and NFR-SCOUT-03 and the ownership rule changed. It is not schedulable by 2026-12-15.

**Not a decision, a follow-up.** The [area budget](AREA_BUDGET.md#allocation-to-the-protocol-processor) still places the redesign "after Instrument verification"; the owner's correction of 2026-10-05 puts milestone 12 before P3 ([comment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5988555968)). The budget page is not edited here.

## Method and receipts

**Tools and recipe.** Vivado 2026.1 build 6511674 for `xc7a100t-fgg484-2`, the [#234 recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md) unchanged: the shipping `endstation_ax7101_1x1_tdm8` export without `--build`, `pp_baseline.py` for the integrated script, `AreaOptimized_high` synthesis, `ExploreArea` optimization, `ExtraPostPlacementOpt` placement, `AggressiveExplore` physical optimization and routing, 32 threads, the default seed; the standalone wrapper with `--integrated-clock` (20 ns).
Each Vivado run held the host's Vivado lock and was this lane's only Vivado; other lanes' Verilator and Yosys jobs shared the host.

**Mapping a head the gate does not describe.** `syn/resmap/resmap_map.py map` ties the route map to a recorded `route-1x1` endpoint, and the gate's record describes dev `54643724`, not this head.
The map was therefore tied to a scratch copy of `syn/ooc/pp_resource_baseline.json` into which this route was recorded with `pp_resource_gate.py record --write --baseline <copy>`; the tracked baseline is unchanged.
A Mark II lane maps its own route the same way:

```sh
cp syn/ooc/pp_resource_baseline.json "$WORK/scratch_baseline.json"
python3 syn/ooc/pp_resource_gate.py record "$WORK/ax7101/gateware" --endpoint route-1x1 \
  --baseline "$WORK/scratch_baseline.json" --write
mkdir "$WORK/route-map" && (cd "$WORK/route-map" && vivado -mode batch \
  -source "$REPO/syn/resmap/route_map.tcl" -nojournal -log route_map.log \
  -tclargs "$WORK/ax7101/gateware/alinx_ax7101_route.dcp")
python3 syn/resmap/resmap_map.py map "$WORK/route-map" --baseline "$WORK/scratch_baseline.json" \
  --endpoint route-1x1 --out "$WORK/route-map/out"
```

**The core pricing (L11b).** Three cacheless RV32I cores synthesized out of context with `AreaOptimized_high` for the same part: the shipping VexiiRiscv netlist the export reads, LiteX's VexRiscv `Min` netlist, and PicoRV32 with LiteX's `minimal` parameters. Each is the core alone, with whatever bus bridges its netlist contains; the figures are in [L11](#l11-the-soc-side).

| Run | rc | Minutes | Log | Log SHA-256, first 16 | Log bytes |
|---|---:|---:|---|---|---:|
| Shipping export, `milan_soc.py` without `--build` | 0 | about 2 | `ax7101-elaboration.log` | `437f11cf5ddd1ce4` | 60,087 |
| Integrated route, 1x1 | 0 | 52.5 | `baseline.log` | `16cbfa00cca1f514` | 816,503 |
| Standalone synthesis, 1x1, 20 ns | 0 | 21.0 | `baseline.log` | `96910f8fcb64bf1c` | 248,489 |
| Route map, `route_map.tcl` | 0 | 0.5 | `route_map.log` | `0881e5e4dcd735f2` | 6,929 |
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

# Protocol processor area baseline for issue #234

Measured 2026-10-03 for issue #234, the first step of the #229 area epic.
The [re-baseline](#re-baseline-of-2026-10-03-after-pr-634) measures the shipping image again after PR #634, at dev `54643724`.
It is the resource gate's current record.
The sections after it keep the first record, at dev `1269cdaf`, as history.
This change modifies no RTL and no processor source.
The [area budget](../design/AREA_BUDGET.md#protocol-processor-budget-and-resource-gate) states the budget and the gate built on these figures.

## Contents

- **[Re-baseline of 2026-10-03, after PR #634](#re-baseline-of-2026-10-03-after-pr-634)** -- The three endpoints measured again at dev `54643724`, their delta from the first record per endpoint and sub-block, and its sources: the AAF clock meter, one more name entry and the firmware ROM.
- **[Combinations](#combinations)** -- The first record's dev head and the next processor adoption, and the only functional HDL change between them.
- **[Method](#method)** -- The recipe, tools and clocks, the standalone clock taken from the build, and the 8x8 parameters from an elaboration.
- **[Shipping route](#shipping-route)** -- Whole-image LUT, FF, slice, block RAM, DSP and timing for both, the critical paths and the routed hierarchy.
- **[Standalone synthesis](#standalone-synthesis)** -- The wrapper alone at 1x1 and 8x8, and how far blocks a change did not touch still move.
- **[Processor sub-blocks](#processor-sub-blocks)** -- LUT, FF, RAMB, DSP and CARRY4 per SRP, ADP, ACMP, AECP, notification, NVM and packet-storage block, and the cost of each stream context.
- **[Storage mapping](#storage-mapping)** -- Which arrays became flip-flops, distributed RAM or block RAM, with source lines, flop counts and read-side logic.
- **[Yosys reconciliation](#yosys-reconciliation)** -- The flattened Yosys mapping of the same geometry, and the three contributions that explain its gap to Vivado.
- **[Reduction ranking](#reduction-ranking)** -- The 1x1 levers by measured cost and estimated saving, with #230, #232, #233 and #639 placed among them.
- **[Run receipts](#run-receipts)** -- Every Vivado and Yosys run's exit status, duration and log digest.

## Re-baseline of 2026-10-03, after PR #634

After the first record, dev merged PR #634 (`bbf704ec`) and PR #644, which changes documentation only.
PR #634 changes the shipping image's inputs, so the first record no longer described dev's image.
Against it, dev's route exits 1 at the gate.
This section measures the three endpoints again and records them as the gate's baseline.
That records PR #634's growth as PR #634's, by the [re-baseline rule](../design/AREA_BUDGET.md#the-resource-gate).

Combination C is this lane's merge of dev `546437243e87eb5a78783a9e3cd5d1badcc3423e`, commit `4d81e10d`.
Its processor pin is still `631eeb34`.
This PR changes no build input, so C's image is dev's.
C used A's recipe, tools, host, directives and seed.

PR #634 reaches the endpoints through three inputs:

| Input | Change | Endpoints |
|---|---|---|
| AAF clock meter, `KL_aaf_clock_meter` | new: one instance, `g_aaf_meter.aaf_clock_meter`, because the 1x1 shape offers one AAF clock source | route |
| AEM name entries | the shape header's `AEM_NAME_ENTRIES_C`, bound as the wrapper's `DESC_NAME_ENTRIES_P` (`milan_datapath.sv:7681`): 38 to 39 at 1x1, 99 to 107 at 8x8 | all three |
| Firmware ROM, `alinx_ax7101_rom.init` | constants only, same size: the AEM image grows from 7,352 to 7,512 bytes with a new CRC, the entity model ID changes, and the NVM name count goes from 38 to 39 | route |

`DESC_NAME_ENTRIES_P` is the only wrapper parameter that moved at either shape.
No wrapper source changed, and the processor's microcode and timer ROMs are byte-identical.
The parameter reaches two blocks.
One is the AECP descriptor store, `u_pp/u_aecp/u_store`, whose name table holds eight 64-bit lanes per entry.
The other is the NVM backend, `u_nvm`, which keeps one NAME record per entry.

**Shipping route**

| Combination | LUT | FF | Slice | RAMB36 | RAMB18 | BRAM tiles | DSP | CARRY4 | WNS ns | WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A, dev `1269cdaf` | 50,128 | 59,006 | 15,815 | 79 | 27 | 92.5 | 14 | 3,405 | +0.063 | +0.036 |
| C, dev `54643724` | 50,767 | 59,634 | 15,832 | 79 | 27 | 92.5 | 14 | 3,506 | +0.193 | +0.024 |
| C minus A | +639 | +628 | +17 | 0 | 0 | 0 | 0 | +101 | +0.130 | -0.012 |
| C, percent of `xc7a100t` | 80.07 | 47.03 | 99.89 | 58.52 | 10.00 | 68.52 | 5.83 | - | - | - |

C routes all 106,622 routable nets fully, with 0 nets with routing errors.
It meets the [build gate](../integration/BUILDING.md#5-gates-before-a-build-is-good), and 18 slices are left.
Its critical path starts at `u_pp/u_notify/rows_r_reg[9][68]` and ends at `u_pp/u_tx_arbiter/slot_r_reg[0]`.
That is 39 logic levels and 19.545 ns, 71 percent of it routing, and it starts in the registry that lever 1 below moves.
Against the first record, C exceeds the LUT tolerance by 139 and the FF tolerance by 28.
So the gate exits 1 on it with "RESULT: MATERIAL REGRESSION".

| Scope in the routed hierarchy | LUT A / C | LUT change | FF A / C | FF change |
|---|---:|---:|---:|---:|
| Whole image | 50,128 / 50,767 | +639 | 59,006 / 59,634 | +628 |
| `milan_datapath` | 41,527 / 42,200 | +673 | 47,804 / 48,433 | +629 |
| `milan_datapath/g_aaf_meter.aaf_clock_meter`, the meter | - / 483 | +483 | - / 630 | +630 |
| `milan_datapath/pp_shadow`, the wrapper | 23,937 / 23,904 | -33 | 24,263 / 24,265 | +2 |
| The rest of `milan_datapath` | 17,590 / 17,813 | +223 | 23,541 / 23,538 | -3 |
| CPU core | 3,526 / 3,524 | -2 | 4,735 / 4,734 | -1 |
| SoC top-level logic | 4,857 / 4,847 | -10 | 6,072 / 6,072 | 0 |

The meter is the largest source.
It places 483 LUTs, 32 of them as memory, and 630 FFs, as PR #634 published.
That is 76 percent of the image's LUT growth and all of its FF growth.
The other top-level instances and the report's cross-child LUT-sharing adjustment make up the remaining -22 LUTs.

The rest of `milan_datapath` grew by 223 LUTs.
PR #634 changed the source of four of its moved instances: `csr` (`milan_csr.sv`) +58, `media_nco` +9, `media_grid_align` +1 and `g_mmcm_servo.mmcm_servo` -2.
The other moved instances' modules are unchanged.
The largest are `aaf_latency_tap_bank` +68, `talker_diag` +61, `ctl_tx_mux` +54 and `chan_map_capture` +33.
Their movement comes from the changed `milan_datapath.sv` around them or from optimization; the reports do not separate the two.

Inside the wrapper the name entry shows where it reaches: `u_nvm` +19 LUTs and `u_pp/u_aecp/u_store` +9.
Blocks it does not reach moved more: `u_pp/u_aecp/u_dyn` -83, `u_pp/u_aecp/u_d3` +25 and `u_pp/u_notify` +14.
The firmware ROM's new constants move no block RAM, and the SoC top-level logic around it moved by -10 LUTs.

**Standalone synthesis**

| Shape and combination | LUT | FF | RAMB36 | RAMB18 | BRAM tiles | DSP | CARRY4 | Internal WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, A | 24,343 | 25,344 | 21 | 3 | 22.5 | 8 | 1,623 | -1.616 |
| 1x1, C | 24,332 | 25,345 | 21 | 3 | 22.5 | 8 | 1,623 | -1.616 |
| 1x1, C minus A | -11 | +1 | 0 | 0 | 0 | 0 | 0 | 0 |
| 8x8, A | 31,562 | 33,929 | 26 | 5 | 28.5 | 8 | 2,001 | -1.947 |
| 8x8, C | 31,556 | 33,937 | 26 | 5 | 28.5 | 8 | 2,001 | -1.947 |
| 8x8, C minus A | -6 | +8 | 0 | 0 | 0 | 0 | 0 | 0 |

The name entries are the standalone endpoints' only changed input.
At 1x1 the two blocks they reach move: `u_nvm` by -11 LUTs and +1 FF, and `u_pp/u_aecp/u_store` by +7 LUTs.
`u_pp/u_aecp/u_d3`, which the parameter does not reach, moves by -7 LUTs, and two other blocks by one LUT each.
At 8x8, eight more entries move `u_nvm` by -5 LUTs and +8 FFs, and `u_pp/u_aecp/u_store` by -3 LUTs.
Two other blocks move by one LUT each.
No block RAM, DSP or carry count moves at either shape.
Both standalone endpoints pass the gate against the first record too.

**Recorded**

`record --write` wrote all three endpoints into [`pp_resource_baseline.json`](../../syn/ooc/pp_resource_baseline.json).
Every tolerance, floor and ceiling stayed unchanged.
Each endpoint's `measured` note names dev `54643724`.
Against the new record, `check` exits 0 on all three runs and `check-baseline` passes.
The ranking, storage mapping and Yosys reconciliation below stay A's: no wrapper source changed.

| Combination | Run | rc | Minutes | Log | Log SHA-256, first 16 | Log bytes |
|---|---|---:|---:|---|---|---:|
| C | Integrated route, 1x1 | 0 | 39.2 | `baseline.log` | `57efe65ef4f02e2d` | 817,907 |
| C | RTL elaboration, 8x8 parameters | 0 | 1.1 | `elaborate.log` | `ab04ec47f060de17` | 213,657 |
| C | Standalone synthesis, 1x1 | 0 | 19.3 | `baseline.log` | `c4a5ebf768070c2e` | 247,793 |
| C | Standalone synthesis, 8x8 | 0 | 23.5 | `baseline.log` | `312bacb6db2c49b6` | 247,911 |

Each run held the host's Vivado lock and was this lane's only Vivado; another lane's Vivado shared the host during the route.
No log contains a `Synth 8-4445` diagnostic, and every recorded image rehashed to its digest after the runs.

## Combinations

The first record measured two trees with the same recipe, tools and host.

| Combination | Parent | Protocol processor | Parent patches |
|---|---|---|---|
| A | dev `1269cdafb4bb964c757baae0f0c5a932d43f540b` | `631eeb342ca1e3fa80e734077a56a943aee76ff1`, the current pin | none |
| B | the same | `ddb3119dbbce59f81bf7a536a1ad90a20546edb2` | the C8 and P2 parent-adoption patches, revision `cdf49d1a` |

B is the next processor adoption, built as a local scratch commit and never published.
Between the two pins only two processor HDL changes are functional.
`KL_pp_nvm_port` gains its device deadline, `MEM_TIMEOUT_CYC_P`.
`protocol_processor_top` binds it to `NVM_MEM_TMO_CYC_P`, equal to `CLK_HZ_P`.
Three other HDL files change only in comments.
The C8 patch changes the builder's descriptor-lint pass-through and the 8x8 configuration's lint waiver.
The P2 patch changes documentation only.
Neither patch changes a `KL_pp_shadow` parameter at either shape.

The gPTP processor is `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` in both.
The AXIS library is `48ff7a7e2ef782cf778d47910cf85835c64b1bce` in both.

## Method

The [baseline recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md) was followed for both trees.
Vivado 2026.1 build `6511674` targeted `xc7a100t-fgg484-2`.
Each tree was exported with `sw/litex/build.sh ax7101` and `ax8x8` previews.
Their `milan_soc.py` command ran without `--build`.

The integrated endpoint routes the shipping `endstation_ax7101_1x1_tdm8` image.
Synthesis uses `AreaOptimized_high` and optimization `ExploreArea`.
Placement uses `ExtraPostPlacementOpt`; physical optimization and routing use `AggressiveExplore`.
Every run used 32 threads and the default seed.
The Milan datapath clock is 50 MHz in both shapes.

The standalone endpoint synthesizes `KL_pp_shadow` out of context.
It binds every wrapper parameter the integrated elaboration reported.
It keeps the integrated source set, include order and synthesis directive.
Its clock is the build's own: `--integrated-clock` derives 20 ns from `CLK_HZ_P`.
The #231 baseline used 10 ns, so its standalone figures are not directly comparable.

The 8x8 shape needed no integrated synthesis.
An RTL elaboration of its integrated script supplied the wrapper's parameter block.
The 1x1 control below shows that block equals the full synthesis's.

| Shape | Processor inputs / outputs | Stream ports in / out | Name entries | `CLK_HZ_P` |
|---|---:|---:|---:|---:|
| 1x1 shipping | 2 / 2 | 1 / 1 | 38 | 50,000,000 |
| 8x8 | 9 / 9 | 8 / 8 | 99 | 50,000,000 |

The extra processor stream contexts belong to CRF.
The remaining wrapper parameters are equal at both shapes and in both trees.

## Shipping route

The routed `endstation_ax7101_1x1_tdm8` image, whole design, default flow:

| Combination | LUT | FF | Slice | RAMB36 | RAMB18 | BRAM tiles | DSP | CARRY4 | WNS ns | WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | 50,128 | 59,006 | 15,815 | 79 | 27 | 92.5 | 14 | 3,405 | +0.063 | +0.036 |
| B | 50,753 | 59,014 | 15,827 | 79 | 27 | 92.5 | 14 | 3,423 | +0.101 | +0.036 |
| B minus A | +625 | +8 | +12 | 0 | 0 | 0 | 0 | +18 | +0.038 | 0 |
| A, percent of `xc7a100t` | 79.07 | 46.53 | 99.78 | 58.52 | 10.00 | 68.52 | 5.83 | - | - | - |

Both routes finish with zero routing errors and no failing endpoint.
The resource gate reads each run's `alinx_ax7101_route_status.rpt`, and A's reads clean.
A routes all 105,566 routable nets fully, with 0 nets with routing errors; B routes all 105,559.
The gate reads that report at every check; the baseline file does not store it.
All four signoff corners agree with the summary.
Setup is worst at the slow corners and hold at the fast corners.
Both meet the [build gate](../integration/BUILDING.md#5-gates-before-a-build-is-good): WNS at least +0.03 ns, WHS at least 0.

Both critical paths end at `u_pp/u_tx_arbiter` inside the protocol processor.
A starts at `u_pp/u_rx_validator/hdr_ctlr_eid_r_reg[28]`: 36 logic levels, 19.684 ns.
B starts at `u_pp/u_notify/rows_r_reg[5][69]`: 37 logic levels, 19.507 ns.
Routing is about 74 percent of each path's delay.

The routed hierarchy splits the image as follows.
Its names are rebuilt after cross-boundary optimization.
They describe placement, not source ownership.

| Scope in the routed hierarchy | LUT A / B | FF A / B | RAMB36 / RAMB18 | DSP |
|---|---:|---:|---:|---:|
| Whole image | 50,128 / 50,753 | 59,006 / 59,014 | 79 / 27 | 14 |
| `milan_datapath`, the non-CPU stack | 41,527 / 42,175 | 47,804 / 47,815 | 30 / 12 | 14 |
| `milan_datapath/pp_shadow` | 23,937 / 24,196 | 24,263 / 24,274 | 21 / 3 | 8 |
| CPU core | 3,526 / 3,509 | 4,735 / 4,736 | 2 / 5 | 0 |
| SoC top-level logic | 4,857 / 4,854 | 6,072 / 6,068 | 47 / 10 | 0 |

B adds 259 LUTs under the wrapper's name and 389 elsewhere in the datapath.
No datapath RTL changed between A and B.
Integrated synthesis already moved the whole image by 402 LUTs, from 52,807 to 53,209.
So most of the routed growth is optimization moving in response to the change.

## Standalone synthesis

`KL_pp_shadow` out of context at the build's 20 ns clock:

| Shape and combination | LUT | FF | RAMB36 | RAMB18 | BRAM tiles | DSP | CARRY4 | Internal WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, A | 24,343 | 25,344 | 21 | 3 | 22.5 | 8 | 1,623 | -1.616 |
| 1x1, B | 24,505 | 25,470 | 21 | 3 | 22.5 | 8 | 1,638 | -0.496 |
| 1x1, B minus A | +162 | +126 | 0 | 0 | 0 | 0 | +15 | - |
| 8x8, A | 31,562 | 33,929 | 26 | 5 | 28.5 | 8 | 2,001 | -1.947 |
| 8x8, B | 31,390 | 33,844 | 26 | 5 | 28.5 | 8 | 2,016 | -1.221 |
| 8x8, B minus A | -172 | -85 | 0 | 0 | 0 | 0 | +15 | - |

Standalone WNS is a synthesis estimate with no I/O constraints.
It is not a closure verdict: the integrated route meets timing at the same clock.

A control run repeats A's 1x1 standalone synthesis at #231's 10 ns clock.
It measures 24,370 LUTs, 25,345 FFs, 21 RAMB36, 3 RAMB18, 8 DSPs and 1,623 CARRY4.
That is within 27 LUTs and one FF of the 20 ns run, with equal block RAM, DSP and carry counts.
So the clock does not explain the step from #231's 1x1 figures.
The wrapper has grown since #231's revision, processor pin `990f9652`: 2,020 LUTs, 812 FFs and 3 DSPs.
The three DSPs are in the parent's NVM backend, `u_nvm`.

In the 1x1 standalone synthesis, B grows `u_nvm_port` by 83 LUTs and 33 FFs.
That block's deadline is the only functional processor change.
The rest of the wrapper moved by a net +79 LUTs and +93 FFs.
That partition is the own logic of every instance the gate record lists outside `u_nvm_port`, 51 terms.
The record lists the wrapper and three levels below it; each term is one listed instance without its listed children.
Its absolute movements sum to 391 LUTs and 121 FFs.
The processor top's own logic, `u_pp` outside its sub-blocks, is one term: -23 LUTs and +107 FFs.
Those 107 FFs are its timer-arm queues `armq_r`, 1,260 flops in B against A's 1,153.
At 8x8 the same change measures 172 LUTs and 85 FFs smaller than A.
The adopted block still grows there, by 66 LUTs and 33 FFs.
These figures set the gate's tolerances in the budget.

## Processor sub-blocks

The standalone hierarchy attributes resources inside the wrapper.
Instance names are relative to `KL_pp_shadow`; RAMB and DSP counts are exact.
CARRY4 counts come from the primitive census under each instance.

**1x1 shipping shape, A / B**

| Sub-block | Instances | LUT A / B | FF A / B | RAMB36 A / B | RAMB18 A / B | DSP A / B | CARRY4 A / B |
|---|---|---:|---:|---:|---:|---:|---:|
| SRP | `u_pp/u_srp` | 4,573 / 4,555 | 6,439 / 6,438 | 0 / 0 | 1 / 1 | 2 / 2 | 247 / 247 |
| ADP | `u_pp/u_adp` | 628 / 629 | 479 / 479 | 0 / 0 | 0 / 0 | 1 / 1 | 44 / 44 |
| ACMP talker | `u_pp/u_talker` | 894 / 881 | 551 / 551 | 0 / 0 | 0 / 0 | 0 / 0 | 18 / 18 |
| ACMP listener | `u_pp/u_listener`, `u_pp/u_lsn_admit` | 1,441 / 1,516 | 1,111 / 1,100 | 5 / 5 | 0 / 0 | 0 / 0 | 31 / 34 |
| AECP engine, total | `u_pp/u_aecp` | 5,598 / 5,604 | 3,500 / 3,500 | 6 / 6 | 0 / 0 | 1 / 1 | 355 / 354 |
| AECP microcontroller | `u_pp/u_aecp/u_ucpu` | 1,608 / 1,609 | 495 / 495 | 3 / 3 | 0 / 0 | 0 / 0 | 68 / 68 |
| AECP saved-state writer (NVM manager) | `u_pp/u_aecp/u_d3` | 1,073 / 1,076 | 485 / 485 | 0 / 0 | 0 / 0 | 0 / 0 | 88 / 88 |
| Notification | `u_pp/u_notify` | 3,175 / 3,193 | 3,299 / 3,299 | 0 / 0 | 0 / 0 | 0 / 0 | 182 / 179 |
| NVM port | `u_pp/u_nvm_port` | 453 / 536 | 127 / 160 | 0 / 0 | 0 / 0 | 0 / 0 | 58 / 73 |
| NVM manager arbiter | `u_pp/u_nvm_arb` | 13 / 7 | 4 / 4 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| ACMP binding store (NVM manager) | `u_pp/u_nvm_shadow` | 815 / 812 | 1,118 / 1,118 | 0 / 0 | 0 / 0 | 0 / 0 | 51 / 51 |
| NVM backend (wrapper) | `u_nvm` | 603 / 610 | 475 / 475 | 0 / 0 | 0 / 0 | 4 / 4 | 47 / 47 |
| Packet storage: RX pools | `u_pp/g_rx_pool[*].u_rx_slots` | 252 / 256 | 206 / 206 | 5 / 5 | 0 / 0 | 0 / 0 | 19 / 19 |
| Packet storage: TX slots | `u_pp/u_tx_slots` | 347 / 349 | 138 / 138 | 1 / 1 | 0 / 0 | 0 / 0 | 5 / 5 |
| Packet storage: trace ring | `u_pp/u_trace` | 37 / 40 | 18 / 18 | 1 / 1 | 0 / 0 | 0 / 0 | 4 / 4 |
| Packet storage: control frame FIFO (wrapper) | `ctl_fifo` | 79 / 79 | 33 / 33 | 1 / 1 | 1 / 1 | 0 / 0 | 3 / 3 |
| Wrapper total | `wrapper` | 24,343 / 24,505 | 25,344 / 25,470 | 21 / 21 | 3 / 3 | 8 / 8 | 1,623 / 1,638 |

**8x8 shape, A / B**

| Sub-block | Instances | LUT A / B | FF A / B | RAMB36 A / B | RAMB18 A / B | DSP A / B | CARRY4 A / B |
|---|---|---:|---:|---:|---:|---:|---:|
| SRP | `u_pp/u_srp` | 8,702 / 8,652 | 11,191 / 11,191 | 0 / 0 | 1 / 1 | 2 / 2 | 463 / 462 |
| ADP | `u_pp/u_adp` | 809 / 769 | 465 / 465 | 1 / 1 | 0 / 0 | 1 / 1 | 86 / 86 |
| ACMP talker | `u_pp/u_talker` | 1,564 / 1,512 | 569 / 569 | 1 / 1 | 1 / 1 | 0 / 0 | 19 / 19 |
| ACMP listener | `u_pp/u_listener`, `u_pp/u_lsn_admit` | 1,616 / 1,534 | 1,125 / 1,133 | 5 / 5 | 0 / 0 | 0 / 0 | 30 / 30 |
| AECP engine, total | `u_pp/u_aecp` | 6,141 / 6,156 | 4,684 / 4,684 | 7 / 7 | 0 / 0 | 1 / 1 | 358 / 358 |
| AECP microcontroller | `u_pp/u_aecp/u_ucpu` | 1,608 / 1,614 | 495 / 495 | 3 / 3 | 0 / 0 | 0 / 0 | 68 / 68 |
| AECP saved-state writer (NVM manager) | `u_pp/u_aecp/u_d3` | 1,282 / 1,397 | 530 / 530 | 0 / 0 | 0 / 0 | 0 / 0 | 88 / 88 |
| Notification | `u_pp/u_notify` | 2,921 / 2,886 | 3,799 / 3,799 | 0 / 0 | 0 / 0 | 0 / 0 | 67 / 67 |
| NVM port | `u_pp/u_nvm_port` | 455 / 521 | 127 / 160 | 0 / 0 | 0 / 0 | 0 / 0 | 57 / 72 |
| NVM manager arbiter | `u_pp/u_nvm_arb` | 20 / 23 | 4 / 4 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| ACMP binding store (NVM manager) | `u_pp/u_nvm_shadow` | 790 / 788 | 1,013 / 1,014 | 2 / 2 | 1 / 1 | 0 / 0 | 51 / 51 |
| NVM backend (wrapper) | `u_nvm` | 1,118 / 1,121 | 1,026 / 1,026 | 0 / 0 | 0 / 0 | 4 / 4 | 57 / 57 |
| Packet storage: RX pools | `u_pp/g_rx_pool[*].u_rx_slots` | 254 / 253 | 206 / 206 | 5 / 5 | 0 / 0 | 0 / 0 | 19 / 19 |
| Packet storage: TX slots | `u_pp/u_tx_slots` | 364 / 221 | 138 / 138 | 1 / 1 | 0 / 0 | 0 / 0 | 5 / 5 |
| Packet storage: trace ring | `u_pp/u_trace` | 28 / 28 | 18 / 18 | 1 / 1 | 0 / 0 | 0 / 0 | 4 / 4 |
| Packet storage: control frame FIFO (wrapper) | `ctl_fifo` | 79 / 79 | 33 / 33 | 1 / 1 | 1 / 1 | 0 / 0 | 3 / 3 |
| Wrapper total | `wrapper` | 31,562 / 31,390 | 33,929 / 33,844 | 26 / 26 | 5 / 5 | 8 / 8 | 2,001 / 2,016 |

`u_pp/u_aecp/u_d3` is the AECP saved-state writer, which manages its NVM records.
`u_pp/u_nvm_shadow` is the ACMP binding store, the other NVM manager.
`u_pp/u_nvm_arb` arbitrates both onto the one NVM port.
The fourth receive pool, `g_rx_pool[3]`, is absent from both hierarchies.

From 1x1 to 8x8 the processor gains seven stream contexts in each direction.
Dividing each block's growth by seven gives its cost per added context:

| Instance | LUT 1x1 | LUT 8x8 | LUT per context | FF 1x1 | FF 8x8 | FF per context |
|---|---:|---:|---:|---:|---:|---:|
| `u_pp/u_srp/u_talker`, the SRP talker FSM | 662 | 2,147 | 212 | 714 | 2,260 | 221 |
| `u_pp/u_srp/u_listener`, the SRP listener FSM | 420 | 2,012 | 227 | 667 | 2,615 | 278 |
| `u_pp/u_srp/u_admission` | 337 | 847 | 73 | 271 | 977 | 101 |
| `u_pp/u_srp`, total | 4,573 | 8,702 | 590 | 6,439 | 11,191 | 679 |
| `wrapper`, total | 24,343 | 31,562 | 1,031 | 25,344 | 33,929 | 1,226 |

The talker FSM grows with the sources and the listener FSM with the sinks.
The wrapper row also carries seven more stream ports and 61 more name entries.
SRP takes 57 percent of the wrapper's LUT growth and 55 percent of its FF growth.
The SRP encoder does not grow with the stream count; the decoder grows by 267 LUTs and no FFs.

## Storage mapping

Vivado's final mapping reports and the primitive census give each array's actual primitive.
Flip-flop counts are census cells under each array's register name, 1x1 shape, A.
Read-cone LUTs are the combinational cells after the array inside its own module.
A cone can include logic shared with other inputs, so it bounds the saving from above.

**Arrays held in flip-flops**

| Array | Source | 1x1 shape | Intended | Actual | FF | Read-side logic |
|---|---|---|---|---|---:|---|
| Notification controller registry, `rows_r` | `KL_aecp_notify.sv:329` | 16 x 128 bits | distributed RAM, by attribute | flip-flops | 2,048 | 2,292 LUTs in the cone |
| SRP timer-arm FIFOs, `tf_ram_r` | `KL_srp_top.sv:947` | 2 x 32 x 47 bits | a FIFO memory | flip-flops | 2,304 | 648 LUTs and 288 MUXF7 |
| Processor timer-arm queues, `armq_r` | `protocol_processor_top.sv:2921` | 8 x 4 x 47 bits | a packed shift queue | flip-flops | 1,153 | 1,178 LUTs on the write side |
| Counter throttle timestamps, `ctr_last_r` | `KL_aecp_notify.sv:392` | 6 x 32 bits; 20 at 8x8 | reset with the block | flip-flops | 192 | 48 CARRY4 compares |

For the registry Vivado reports `Synth 8-7186`: the attribute is ignored.
"`rows_r` is not inferred as ram due to incorrect usage".
It is read at three sites: `:337`, `:551-552` and a 16-way identity compare at `:541-544`.
The SRP FIFOs are one two-dimensional array written for both FIFOs in one process (`:959-968`).
The throttle stamps are reset with the block (`:934`) and compared in parallel (`:1034-1037`).
The timer-arm queues need one LUT per flop to shift.
Constant fields leave fewer flops than the declared bits in both queue structures.

**Arrays in distributed or block RAM**

| Array | Source | 1x1 shape | Actual |
|---|---|---|---|
| Notification command queue, `cmdq_*` | `KL_aecp_notify.sv:371-376` | 16 x 132 bits | 24 RAM32M |
| Descriptor index, `idx_r` | `KL_aecp_desc_store.sv:279` | 32 x 128 bits | 22 RAM32M |
| Descriptor lines and names, `line_r`, `name_r` | `KL_aecp_desc_store.sv:291`, `:303` | 72 x 64 and 304 x 64 bits | block RAM |
| AECP map staging, `amap_stage_r` | `KL_aecp_engine.sv:1188` | 256 x 64 bits | block RAM |
| Microcontroller microcode, `rom_r` | `KL_aecp_ucpu.sv:149` | 2,048 x 48 bits | 3 RAMB36 |
| Microcontroller register file, `rf_r` | `KL_aecp_ucpu.sv:159` | 16 x 64 bits | 33 RAM32M |
| ACMP listener records, `rec_ram_r` | `KL_pp_acmp_listener.sv:385` | 2 x 376 bits | 5 RAMB36 |
| Receive pools, `mem_r` | `KL_pp_rx_slots.sv:193` | 5 x 2,048 bytes | 5 RAMB36 |
| Transmit slots, `mem_r` | `KL_pp_tx_slots.sv:263` | 3,072 bytes | 1 RAMB36 |
| Trace ring, `mem_r` | `KL_pp_trace_ring.sv:86` | 256 x 128 bits | 1 RAMB36 |
| Timer slots, `slot_ram_r` | `KL_pp_timer_service.sv:108` | 61 x 40 bits | 1 RAMB36 |
| Wrapper control-frame FIFO | `axis_fifo`, in `ctl_fifo` | 512 x 73 bits | 1 RAMB36, 1 RAMB18 |

The table lists the arrays the #232 inventory names and the packet stores.
The remaining block RAMs are the MRP strip buffer, the SRP decoder's RAM and the validator's MRP memory.
The listener records use five RAMB36 for 752 bits at 1x1.
The width, 376 bits, sets the count, not the depth.

The AECP response buffer is no longer on chip.
`KL_aecp_resp_buf.sv` writes it to the integrator's main memory at `RESP_BASE_P`.
Its 5,079-flop spill in #229's history therefore cannot recur.
`u_pp/u_aecp/u_resp` now holds 260 FFs.

Issue #234's second acceptance criterion is not met at A.
Two buffers still spill into about 2,000 FFs each: the registry and the SRP FIFOs.
The registry's own attribute shows that spill is unintended.

## Yosys reconciliation

The recipe's Yosys comparison maps the same numeric parameters with `synth_xilinx -family xc7 -flatten`.
Yosys 0.66 and sv2v v0.0.13 ran it; Yosys reports no timing and proves no fit.

| Shape and combination | Logic LUT | LUT RAM equivalents | LUT total | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1, A | 44,582 | 5,996 | 50,578 | 23,831 | 15 | 4 | 10 | 2,067 |
| 1x1, B | 44,685 | 5,996 | 50,681 | 23,876 | 15 | 4 | 10 | 2,083 |
| 8x8, A | 87,066 | 6,160 | 93,226 | 33,453 | 16 | 4 | 10 | 8,134 |
| 8x8, B | 86,903 | 6,160 | 93,063 | 33,498 | 16 | 4 | 10 | 8,150 |

The Yosys LUT total minus Vivado's LUT count splits into three measured parts at A:

| Contribution | 1x1 | 8x8 |
|---|---:|---:|
| Yosys logic LUTs minus Vivado's raw `LUT1` to `LUT6` cells | 17,328 | 51,733 |
| Vivado's LUT-combining adjustment, raw cells minus logic LUTs | 4,153 | 4,809 |
| Yosys LUT RAM equivalents minus Vivado's LUTs as memory | 4,754 | 5,122 |
| Total, equal to the gap | 26,235 | 61,664 |

Vivado's raw cell census is 27,254 at 1x1 and 35,333 at 8x8.
Its combined logic LUTs are 23,101 and 30,524.

The memory part follows the mapping reports.
Yosys maps the controller registry, the listener records and the timer slots to LUT RAM.
Vivado keeps the registry in flops and puts the other two in block RAM.
Both tools keep the SRP timer-arm FIFOs in flops, so that spill is the RTL's shape, not one vendor's.
That is why Yosys reports fewer flops and fewer block RAMs.

The recipe's hierarchy-preserving mapping locates the raw-logic part at A.
It maps the same converted source without `-flatten` and partitions both netlists by source scope:

| Raw logic contribution | Yosys 1x1 | Vivado 1x1 | Difference 1x1 | Yosys 8x8 | Vivado 8x8 | Difference 8x8 |
|---|---:|---:|---:|---:|---:|---:|
| `u_pp/u_srp` | 14,743 | 5,265 | 9,478 | 29,732 | 9,814 | 19,918 |
| `u_pp/u_talker`, the ACMP talker | 1,243 | 1,041 | 202 | 21,457 | 1,837 | 19,620 |
| `u_pp` own logic | 7,280 | 487 | 6,793 | 12,128 | 515 | 11,613 |
| `u_pp/u_notify` | 5,780 | 3,367 | 2,413 | 6,387 | 3,085 | 3,302 |
| Remaining scopes | 21,152 | 17,094 | 4,058 | 24,188 | 20,082 | 4,106 |
| Hierarchical total | 50,198 | 27,254 | 22,944 | 93,892 | 35,333 | 58,559 |
| Flattening residual | -5,616 | 0 | -5,616 | -6,826 | 0 | -6,826 |
| Flattened total | 44,582 | 27,254 | 17,328 | 87,066 | 35,333 | 51,733 |

SRP dominates at both shapes, as in #231.
At 8x8 the ACMP talker joins it: Yosys maps it to nearly twelve times Vivado's raw cells.
That one scope accounts for about half of Yosys's logic growth from 1x1 to 8x8.
Vivado's talker grows only from 1,041 to 1,837 raw cells.
So it is a portability finding, not a Vivado area lever.

Yosys LUT totals move with B in the same direction as Vivado's standalone figures: +103 at 1x1, -163 at 8x8.
Its flop count rises by 45 at both shapes.
Its LUT counts remain a portability alarm, never an implementation estimate.

## Reduction ranking

The ranking is for the 1x1 shipping shape, measured at A.
Costs are measured; savings are estimates until a matched before-and-after run measures them.
Each estimate keeps the array's contents and protocol behaviour, and changes only its storage or evaluation.
Every lever changes processor RTL, so each belongs to its own processor lane.

| Rank | Lever | Issue | Where | Measured cost, 1x1 | Estimated saving, 1x1 | Estimate basis |
|---:|---|---|---|---|---|---|
| 1 | Hold the controller registry in distributed RAM and walk it for the command-hit check | #232 | `KL_aecp_notify.sv:329`, `:541-544`, `:551-552` | 2,048 FF; 2,292 LUTs in the read cone | about 2,000 FF and 1,500 LUT | one 16-deep RAM of 22 RAM32M and one 112-bit comparator replace 16 parallel comparators and two 16-way read multiplexers |
| 2 | Infer the two SRP timer-arm FIFOs as distributed RAM | #230 (joins its scope) | `KL_srp_top.sv:947`, `:959-973` | 2,304 FF; 648 LUT and 288 MUXF7 read multiplexer | about 2,300 FF, 580 LUT and 288 MUXF7 | two 32-deep distributed RAMs of 8 RAM32M each, 64 LUTs, behind the existing 72-flop read registers |
| 3 | Replace the eight processor timer-arm shift queues with RAM-backed FIFOs | #639 | `protocol_processor_top.sv:2921` | 1,153 FF; 1,178 LUT on the write side | about 1,100 FF and 1,000 LUT | eight 4-deep distributed RAM FIFOs, about 260 LUTs, keep the depth and the drain order |
| 4 | Share the SRP per-stream FSM evaluation across stream contexts | #230 | `KL_srp_talker_fsm.sv:351-392`, loops `:401-816`; `KL_srp_listener_fsm.sv:348-388`, loops `:403-850` | talker FSM 662 LUT, 714 FF; listener FSM 420 LUT, 667 FF | about 440 LUT | one evaluator per FSM instead of two saves one context's marginal cost, 212 and 227 LUTs; the per-stream context flops stay, since a 2-deep RAM would cost about as many LUTs; at 8x8 about 3,100 LUTs, and context RAM pays |
| 5 | Serialize the counter throttle check and store its timestamps in RAM | #232 | `KL_aecp_notify.sv:392`, `:934`, `:1034-1037` | 192 FF, 48 CARRY4 | about 190 FF, 50 LUT and 48 CARRY4 | 6 stamps at 1x1; 640 FFs at 8x8 |
| 6 | Hold the two listener records in distributed RAM or flops | #639 | `KL_pp_acmp_listener.sv:385` | 5 RAMB36 for 752 bits | 5 block RAM tiles, for about 250 more LUTs | 63 RAM32M for the 376-bit record |

Levers 1 to 5 together remove an estimated 5,600 FFs and 3,600 LUTs from the 1x1 wrapper.
Lever 6 trades LUTs for block RAM and only matters if block RAM becomes short.
Lever 1 also removes the source of B's and C's critical paths.

Slices, not LUTs, stop placement: 35 were left at A and 23 at B, and 18 are left at C, after PR #634.
Removing that many flops and LUTs should free several hundred slices or more.
Only a route of the changed image can measure it, so no slice saving is claimed.

Even levers 1 to 5 leave C's image near 47,200 LUTs, about 74 percent of the device.
That is still about 9,100 LUTs above NFR-RES-01's 60 percent; at A it was 46,500 and 8,500.
The owner's decision on that gap is in the [budget](../design/AREA_BUDGET.md#allocation-to-the-protocol-processor): a redesign, #640.

#233 is the 1x1 specialization.
Its phase-1 audit found every stream-shaped wrapper and processor parameter already derived for 1x1.
Its remaining candidates are small: a 5-bit VLAN reference count that 3 bits would serve, and FIFO and queue depths.
Levers 2 and 3 move those FIFOs and queues into RAM, where depth costs almost nothing.
The 15-entry descriptor index sits in a 32-deep RAM32M either way.
So #233 is not needed for placement headroom, and it cannot close the NFR-RES-01 gap.

## Run receipts

Every run below returned rc 0 and was started without a pipeline.
Minutes include time shared with another run on the same host.
No measured log contains a `Synth 8-4445` diagnostic.
The single match in each is the echoed command that promotes it to an error.
Every recorded memory image still hashed to its recorded digest after the runs.

| Combination | Run | rc | Minutes | Log | Log SHA-256, first 16 | Log bytes |
|---|---|---:|---:|---|---|---:|
| A | Integrated route, 1x1 | 0 | 55.7 | `baseline.log` | `395cded8cb594609` | 771,306 |
| B | Integrated route, 1x1 | 0 | 50.0 | `baseline.log` | `22827544082d3165` | 773,586 |
| A | Standalone synthesis, 1x1 | 0 | 24.1 | `baseline.log` | `a0e4b8840d222fff` | 247,587 |
| B | Standalone synthesis, 1x1 | 0 | 14.8 | `baseline.log` | `b56d184831a5332e` | 243,973 |
| A | RTL elaboration, 8x8 parameters | 0 | 1.4 | `elaborate.log` | `811fb62b09f3e05e` | 213,350 |
| B | RTL elaboration, 8x8 parameters | 0 | 1.4 | `elaborate.log` | `d34b71c4d92ea891` | 213,416 |
| A | RTL elaboration, 1x1 control | 0 | 1.0 | `elaborate.log` | `c48fd7ef6f0aecf4` | 216,663 |
| A | Standalone synthesis, 8x8 | 0 | 26.6 | `baseline.log` | `fc79d75051306915` | 247,514 |
| B | Standalone synthesis, 8x8 | 0 | 22.3 | `baseline.log` | `fdd2ed5b027fc2dc` | 246,365 |
| A | Storage cone probe, 1x1 | 0 | 0.4 | `probe.log` | `982c90f8b6c93edd` | 6,411 |
| A | Yosys flattened, 1x1 | 0 | 2.6 | `ooc.sh.log` | `f2d242b6c25cebf6` | 299 |
| B | Yosys flattened, 1x1 | 0 | 2.9 | `ooc.sh.log` | `49856a4424805472` | 299 |
| A | Yosys flattened, 8x8 | 0 | 4.6 | `ooc.sh.log` | `da030111144b9bcf` | 299 |
| B | Yosys flattened, 8x8 | 0 | 4.6 | `ooc.sh.log` | `fd4429350b7b5c07` | 299 |
| A | Yosys hierarchical, 1x1 | 0 | 1.7 | `hierarchical.log` | `653c9c0f496408e2` | 10,322,436 |
| A | Yosys hierarchical, 8x8 | 0 | 2.9 | `hierarchical.log` | `613178858673d3c9` | 15,287,495 |
| A | Standalone synthesis, 1x1 at 10 ns (#231 clock control) | 0 | 18.2 | `baseline.log` | `389bfa697ea02e95` | 247,605 |

B's first route launch was stopped during synthesis, before any report, to stay within the host's memory budget.
It was rerun alone; only the rerun is listed.
B's Yosys run first refused, rc 2, because `syn/yosys/rom_digests.tsv` has no rows for `ddb3119d`.
Recording them in B's scratch tree, with `ooc.sh --record-rom-digests`, gave the same digests as `631eeb34`.
The next adoption must add those two rows, or `ooc.sh` refuses at its pin.

Reports, checkpoints and full digests stay outside the repository, with the measurement directories.

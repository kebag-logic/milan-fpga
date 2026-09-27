# Protocol processor area baseline

Original measurements: 2026-09-26, issue #231, optimization epic #229.
Original measured revision: `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
This change modifies no RTL.
Issue #587 repeats integrated 8x8 synthesis at 50 MHz.
Its 2026-09-27 revision is `63fe4fb0164d798d44a6476001dc8b887cdd4609`.

## Contents

- **[Provenance](#provenance)** -- Bind tools, configuration and processor revisions.
- **[Measurements](#measurements)** -- Separate standalone and integrated results.
- **[50 MHz 8x8 rerun](#50-mhz-8x8-rerun)** -- Compare the declared clock against history.
- **[Hierarchical consumers](#hierarchical-consumers)** -- Attribute standalone and integrated resource use.
- **[Integrated implementation](#integrated-implementation)** -- Compare the three placement directives.
- **[Input integrity](#input-integrity)** -- Bind complete ROM images to their source revisions.
- **[Mapping differences](#mapping-differences)** -- Explain measured resource tradeoffs between tools.
- **[Historical comparison](#historical-comparison)** -- Preserve the retired substitution evidence.

## Provenance

Use the [reproduction recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md).
The assignment decision defines the integrated comparison:
[issue #231](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5844867171).
The [round-two decision](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5846064333) separates ownership attribution.
Default-flow totals remain the implementation baseline.
The retired control planes have no current build.
Current integrated measurements therefore replace a new substitution comparison.

These are the original #231 inputs.
Its 8x8 measurements use 100 MHz and processor pin `990f9652`.
The #587 50 MHz rerun uses processor pin `0922e434`.

| Original #231 input | Revision or configuration |
|---|---|
| Protocol processor | `990f96526bb89356c963a260ebbdcf2a77e6623a` |
| gPTP processor | `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` |
| AXIS library | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` |
| Part | `xc7a100tfgg484-2` |
| Vivado | 2026.1 |
| Vivado build | `6511674` |
| Yosys | `0.66`, package revision `86f2ddebc-dirty` |
| sv2v | `v0.0.13` |
| Synthesis directive | `AreaOptimized_high` |

The Yosys revision string is the installed package's reported identity.
Its figures describe that version, not a pinned portability result.

| Original #231 product configuration | Processor inputs / outputs | Name entries | Ports in / out | Timer MHz | OOC MHz |
|---|---:|---:|---:|---:|---:|
| `endstation_ax7101_1x1_tdm8` | 2 / 2 | 38 | 1 / 1 | 50 | 100 |
| `endstation_ax7101_8x8`, historical #231, pin `990f9652` | 9 / 9 | 99 | 8 / 8 | 100 | 100 |

The extra processor contexts belong to CRF.
The configuration names count audio streams.
Both use 64-bit input data and a 4,096-byte FIFO.
Both use one audio unit and one clock domain.
The descriptor window starts at `0x7f700000`.
The response window starts at `0x7f7ff000`.
Descriptor lines contain 576 bytes; the index contains 32 entries.
The descriptor timeout is 4,096 cycles.
The default SRP VID is two.
The generated parameter record binds every remaining value.

## Measurements

Vivado standalone measurements use a 10 ns clock constraint.
The constraint is loaded before synthesis.
Synthesis retains the integrated source set and include order.
Vivado implicitly defines `SYNTHESIS`; Yosys defines it explicitly.
No standalone input/output delays are specified.
Standalone WNS therefore measures internal paths only.

| Measurement | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| Vivado OOC, product 1x1, 100 MHz | 22,350 | 24,533 | 21 | 3 | 5 | 1,415 | -6.180 |
| Vivado OOC, product 8x8, historical 100 MHz, pin `990f9652` | 28,992 | 32,984 | 26 | 5 | 5 | 1,775 | -10.987 |
| Vivado integrated synthesis, whole 1x1 SoC, 50 MHz | 51,125 | 58,006 | 79 | 27 | 11 | 3,214 | -1.201 |
| Vivado integrated route, whole 1x1 SoC, 50 MHz | 48,618 | 57,854 | 79 | 27 | 11 | 3,203 | +0.013 |
| Vivado integrated synthesis, whole 8x8 SoC, historical 100 MHz, pin `990f9652` | 68,136 | 70,835 | 80 | 29 | 11 | 3,916 | -11.331 |

The separate attribution variant preserves the protocol-wrapper boundary.
It adds `KEEP_HIERARCHY TRUE` on `milan_datapath/pp_shadow`.
No RTL, geometry, image or synthesis directive changes.
Both 118-source exports retain identical commands and source order.
Generated Verilog differs only in comments and work-root strings.
These wrapper counts describe that variant only.
They cannot be subtracted from the default whole-design totals.

| Attribution-only wrapper | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | Internal WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1x1 synthesis, 50 MHz | 22,314 | 24,535 | 21 | 3 | 5 | 1,415 | -1.201 |
| 1x1 route, 50 MHz | 20,655 | 23,558 | 21 | 3 | 5 | 1,321 | +0.041 |
| 8x8 synthesis, historical 100 MHz, pin `990f9652` | 29,489 | 32,991 | 26 | 5 | 8 | 1,809 | -10.846 |

Standalone 1x1 consumes 22.5 BRAM tiles at 100 MHz.
Historical 8x8 OOC uses 100 MHz and processor pin `990f9652`.
It consumes 28.5 BRAM tiles.
Both standalone WNS values are estimates, not closure verdicts.
At 1x1, the worst path crosses notification logic into the transmit arbiter.
The endpoints are `u_pp/u_notify/pend_r_reg[4]/C`
and `u_pp/u_tx_arbiter/slot_r_reg[0]/D`.
For historical 100 MHz 8x8, the processor pin is `990f9652`.
Its source is `u_pp/u_notify/pend_r_reg[11]/C`.
The destination remains the same; that path spans 41 logic levels.

These original integrated clocks were 50 MHz and 100 MHz.
The 100 MHz 8x8 measurements are retained as history.
Whole-design WNS also includes the other clock domains.
Wrapper WNS requires both endpoints inside `milan_datapath/pp_shadow`.
It excludes paths entering or leaving that wrapper.

Historical 100 MHz 8x8 synthesis exceeded device capacity.
That #231 run uses processor pin `990f9652`.
Its 68,136 LUTs exceeded 63,400 by 4,736.
Its utilization is 107.47 percent before placement.
It has no placement or routing result.

## 50 MHz 8x8 rerun

The [assignment](https://github.com/kebag-logic/milan-fpga/issues/587#issuecomment-5855348441) repeats the two integrated synthesis variants.
The configuration declares 50 MHz after issue #565.

No recipe, RTL or configuration change was needed.
The original 100 MHz results remain labelled history.

Default synthesis measures 68,047 LUTs at 50 MHz.
That is 89 fewer than the historical 68,136 LUTs.
The historical 100 MHz processor pin is `990f9652`.
The 50 MHz rerun's processor pin is `0922e434`.

The total remains 4,647 above the device's 63,400 LUTs.
Whole-design WNS is -1.708 ns at 50 MHz.

These synthesis estimates establish neither placement nor timing closure.
The 1x1 results remain unchanged.

| Default integrated 8x8 synthesis | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | Whole-design WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| Historical 100 MHz, 2026-09-26 | 68,136 | 70,835 | 80 | 29 | 11 | 3,916 | -11.331 |
| Declared 50 MHz, 2026-09-27 | 68,047 | 70,744 | 80 | 29 | 11 | 3,913 | -1.708 |
| 50 MHz minus historical 100 MHz | -89 | -91 | 0 | 0 | 0 | -3 | +9.623 |

The reported Milan clock has a 20.000 ns period.
The worst default path crosses notification into event-router logic.

Its endpoints are `u_pp/u_notify/ctr_pend_r_reg[3]/C`
and `u_pp/u_event_router/sel_r_reg[3]/D` inside the wrapper.
The path contains 43 logic levels.

The current processor pin is `0922e43408f891fc0b84a84691df86b4fd0f1c0d`.
Its HDL matches historical pin `990f96526bb89356c963a260ebbdcf2a77e6623a` byte-for-byte.

The gPTP and AXIS pins remain unchanged.
Only two wrapper parameters differ from the historical record:

| Wrapper parameter | Historical 100 MHz, pin `990f9652` | Declared 50 MHz, pin `0922e434` |
|---|---:|---:|
| `CLK_HZ_P` | 100000000 | 50000000 |
| `TIM_DIV_US_P` | 100 | 50 |
| `TIM_DIV_MS_P` | 1000 | 1000 |

The gPTP image changes with the declared clock.
Firmware and both processor ROM hashes match the historical record.

The attribution run preserves `milan_datapath/pp_shadow` with `KEEP_HIERARCHY TRUE`.
It uses the same 50 MHz inputs and synthesis directive.

Only the additional boundary constraint changes synthesis behavior.
Generated comments and build-directory strings differ between exports.

Both source lists contain 118 reads, in identical order.
The normalized generated RTL and all image bytes match.
Normalization replaces build roots with `$BUILD` and checkout with `$REPO`.
It then strips block and line comments from generated Verilog.
The [input manifest](PP_SHADOW_BASELINE_50MHZ_INPUTS.json) records the resulting SHA-256 digest.

The following historical 100 MHz row uses processor pin `990f9652`.
The 50 MHz row uses processor pin `0922e434`.

| Attribution-only 8x8 wrapper synthesis | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | Internal WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| Historical 100 MHz, 2026-09-26 | 29,489 | 32,991 | 26 | 5 | 8 | 1,809 | -10.846 |
| Declared 50 MHz, 2026-09-27 | 28,955 | 32,982 | 26 | 5 | 5 | 1,774 | -1.700 |
| 50 MHz minus historical 100 MHz | -534 | -9 | 0 | 0 | -3 | -35 | +9.146 |

The 50 MHz attribution whole-design total is 69,923 LUTs.
It uses 72,421 FFs, 80 RAMB36s and 29 RAMB18s.

It also uses 11 DSPs and 4,013 CARRY4s.
Its whole-design WNS is -1.700 ns at 50 MHz.

These attribution totals never replace the default fit baseline.
At 50 MHz, NVM uses three fewer DSPs.

| Integrated 8x8 endpoint | Whole LUT, default / attribution | Wrapper-name LUT, default / attribution | AECP LUT, default / attribution | Dynamic-state LUT, default / attribution |
|---|---:|---:|---:|---:|
| Historical 100 MHz synthesis, pin `990f9652` | 68,136 / 70,206 | 37,809 / 29,489 | 15,199 / 5,025 | 6,915 / 574 |
| Declared 50 MHz synthesis | 68,047 / 69,923 | 38,351 / 28,955 | 15,660 / 5,022 | 7,544 / 574 |

The [50 MHz ranking](PP_SHADOW_BASELINE_50MHZ_RANKING.tsv) includes both synthesis variants.
Its zero threshold includes every direct child and own logic.

Parent totals retain the report's LUT-sharing reconciliation.
The following 50 MHz attribution table is a timing subset.

It does not replace the complete consumer ranking.

| Attribution scope at 50 MHz | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | Internal WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| `u_pp` | 28,123 | 31,599 | 25 | 4 | 4 | 1,712 | -1.700 |
| `u_pp/u_aecp` | 5,022 | 4,155 | 7 | 0 | 1 | 264 | +0.609 |
| `u_pp/u_srp` | 8,359 | 11,130 | 0 | 1 | 2 | 429 | +10.005 |
| `u_pp/u_notify` | 2,917 | 3,799 | 0 | 0 | 0 | 68 | +11.314 |
| `u_pp/u_listener` | 1,626 | 1,124 | 5 | 0 | 0 | 30 | +7.647 |
| `u_pp/u_talker` | 1,402 | 522 | 1 | 1 | 0 | 19 | +6.673 |
| `u_nvm` | 752 | 1,023 | 0 | 0 | 1 | 37 | +13.058 |

Both 50 MHz checkpoints passed the unchanged public boundary probes.
The table counts raw LUT cells, before utilization combining.

| Scope at 50 MHz | Raw LUT cells, default / attribution | Only external loads, default / attribution | External input and only external loads, default / attribution |
|---|---:|---:|---:|
| `u_pp/u_aecp/u_dyn` | 9,010 / 607 | 5,824 / 0 | 3,098 / 0 |
| `u_pp/u_aecp` | 17,923 / 5,616 | 6,075 / 18 | 3,284 / 0 |
| `u_pp/u_srp` | 9,134 / 9,457 | 57 / 442 | 48 / 432 |
| `u_pp/u_notify` | 3,528 / 3,058 | 3 / 0 | 3 / 0 |
| `wrapper` | 43,110 / 32,303 | 6,276 / 518 | 3,440 / 467 |

At 50 MHz, attribution removes dynamic-state external-only loads entirely.
The corresponding load histogram is empty.
Default dynamic-state loads include `amap_out_owner_r` and `amap_out_cluster_r`.
Its `amap_edit_oclaim` cluster, expectation and word registers also appear.

The attribution wrapper retains 518 external-only raw LUT cells.
Residual stems include `gsi_data_r`, `csr/live_mux_q` and `ctl_tx_mux`.

The manifest records every observed load stem and count.
External loads can include legitimate exported signals.
Internal child hierarchy remains rebuilt; reverse relocation is not measured.

Both runs used Vivado 2026.1, build `6511674`.
The part was `xc7a100tfgg484-2`; synthesis used `AreaOptimized_high`.

Both used 32 threads and the default seed.
Python was 3.14.7; the verified target compiler was GCC 14.3.0.

The pinned SDK release was `riscv32-ilp32d--glibc--stable-2025.08-1`.
The [50 MHz input manifest](PP_SHADOW_BASELINE_50MHZ_INPUTS.json) binds both runs.

It records parameters, source hashes, image geometries and tool versions.
Large reports and checkpoints remain outside the public packet.

Their SHA-256 hashes and byte lengths are recorded instead.

Reproduce only the recipe's `ax8x8` export and synthesis endpoints.
Use separate work directories for default and attribution exports.

The launcher derives `--milan-clk-freq 50e6` from the configuration.
Retain every other emitted design argument and all constraints.

Run both prepared scripts in their respective gateware directories.

Both synthesis commands returned rc 0, without pipelines.
Both logs contain zero `Synth 8-4445` diagnostics.

Every recorded source and image hash matched after synthesis.
Existing `12-4739`, `12-5201` and `20-1307` warnings remain.

Both reports have zero unclocked or unconstrained internal endpoints.
However, 46 inputs and 86 outputs lack I/O delays.

No placement, routing, bitstream or hardware result is claimed.

## Hierarchical consumers

The [original resource ranking](PP_SHADOW_BASELINE_RANKING.tsv) covers eight measured endpoints.
Its historical #231 8x8 rows use processor pin `990f9652`.
Their clock and timer geometry are both 100 MHz.
Its threshold is zero: every reported direct child appears.
Wrapper and processor own-logic rows are included.
LUT and FF ranks are independent, with lexical tie-breaking.
Rankings use reports with the small-instance filter disabled.
Each scope includes a parent total and LUT-sharing reconciliation.
Children plus reconciliation equal the parent in every resource column.
Storage and DSP columns need no reconciliation adjustment.

Default integrated ranks describe reconstructed names, not source ownership.
Use the attribution rows for the integrated wrapper's consumers.

The following tables are timing-scope subsets, not dominance rankings.
Every resource row includes descendants.
Do not add a parent row to its children.
Internal WNS requires both endpoints inside that row's instance.
Sibling crossings appear in the wrapper total, not individual children.

**Vivado OOC, product 1x1, 100 MHz**

| Instance | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | Internal WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| `u_pp` | 21,762 | 23,704 | 20 | 2 | 4 | 1,353 | -6.180 |
| `u_pp/u_aecp` | 4,663 | 3,010 | 6 | 0 | 1 | 257 | -2.040 |
| `u_pp/u_srp` | 4,296 | 6,377 | 0 | 1 | 2 | 242 | +0.138 |
| `u_pp/u_notify` | 3,150 | 3,299 | 0 | 0 | 0 | 184 | +1.605 |
| `u_pp/u_listener` | 1,553 | 1,099 | 5 | 0 | 0 | 30 | -2.224 |
| `u_pp/u_talker` | 860 | 514 | 0 | 0 | 0 | 18 | -1.773 |
| `u_nvm` | 507 | 469 | 0 | 0 | 1 | 37 | +4.668 |

**Vivado OOC, product 8x8, historical 100 MHz, pin `990f9652`**

| Instance | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | Internal WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| `u_pp` | 28,166 | 31,600 | 25 | 4 | 4 | 1,712 | -10.987 |
| `u_pp/u_aecp` | 5,053 | 4,152 | 7 | 0 | 1 | 263 | -2.507 |
| `u_pp/u_srp` | 8,302 | 11,130 | 0 | 1 | 2 | 429 | +0.138 |
| `u_pp/u_notify` | 2,948 | 3,799 | 0 | 0 | 0 | 68 | +1.447 |
| `u_pp/u_listener` | 1,669 | 1,131 | 5 | 0 | 0 | 30 | -0.514 |
| `u_pp/u_talker` | 1,354 | 522 | 1 | 1 | 0 | 18 | -1.514 |
| `u_nvm` | 745 | 1,024 | 0 | 0 | 1 | 38 | +4.219 |

**Vivado attribution-only integrated synthesis, product 8x8, historical 100 MHz, pin `990f9652`**

| Instance | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | Internal WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| `u_pp` | 28,277 | 31,607 | 25 | 4 | 4 | 1,719 | -10.846 |
| `u_pp/u_aecp` | 5,025 | 4,154 | 7 | 0 | 1 | 264 | -10.588 |
| `u_pp/u_srp` | 8,382 | 11,130 | 0 | 1 | 2 | 429 | +0.010 |
| `u_pp/u_notify` | 2,895 | 3,799 | 0 | 0 | 0 | 68 | +1.319 |
| `u_pp/u_listener` | 1,655 | 1,124 | 5 | 0 | 0 | 30 | -1.297 |
| `u_pp/u_talker` | 1,350 | 522 | 1 | 1 | 0 | 19 | -2.315 |
| `u_nvm` | 1,131 | 1,024 | 0 | 0 | 4 | 58 | +3.907 |

**Vivado attribution-only integrated route, shipping product 1x1, 50 MHz**

| Instance | LUT | FF | RAMB36 | RAMB18 | DSP | CARRY4 | Internal WNS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| `u_pp` | 20,110 | 22,737 | 20 | 2 | 4 | 1,254 | +0.041 |
| `u_pp/u_aecp` | 4,504 | 3,010 | 6 | 0 | 1 | 257 | +2.581 |
| `u_pp/u_srp` | 3,998 | 6,246 | 0 | 1 | 2 | 241 | +4.783 |
| `u_pp/u_notify` | 3,111 | 3,299 | 0 | 0 | 0 | 184 | +3.736 |
| `u_pp/u_listener` | 1,404 | 1,103 | 5 | 0 | 0 | 30 | +5.272 |
| `u_pp/u_talker` | 789 | 492 | 0 | 0 | 0 | 17 | +5.660 |
| `u_nvm` | 474 | 469 | 0 | 0 | 1 | 37 | +12.015 |

Integrated instance names are relative to `milan_datapath/pp_shadow`.
Standalone names are relative to the OOC top.
The following standalone growth compares the original #231 configurations.
Both use a 100 MHz OOC clock and pin `990f9652`.
Their timer geometries are 50 MHz and 100 MHz, respectively.
The SRP engine drives most of the standalone growth: 4,006 LUTs.
Its listener FSM grows from 451 to 2,109 LUTs.
Its talker FSM grows from 679 to 1,905 LUTs.

The default flow rebuilds hierarchy after cross-boundary optimization.
Its names can therefore contain logic from neighboring modules.
The boundary-preserving variant prevents that relocation across the wrapper.
Internal child hierarchy remains rebuilt in both flows.
Preserving the boundary also changes optimization and resource sharing.
Historical 100 MHz 8x8 attribution uses processor pin `990f9652`.
It uses eight wrapper DSPs.
The default reconstructed wrapper uses five DSPs.
The three additional DSPs appear in `u_nvm`.

| Endpoint | Whole LUT, default / attribution | Wrapper-name LUT, default / attribution | AECP LUT, default / attribution | Dynamic-state LUT, default / attribution |
|---|---:|---:|---:|---:|
| 1x1 synthesis, 50 MHz | 51,125 / 52,210 | 23,272 / 22,314 | 6,639 / 4,678 | 1,296 / 111 |
| 1x1 route, 50 MHz | 48,618 / 48,825 | 22,441 / 20,655 | 6,428 / 4,504 | 1,299 / 111 |
| 8x8 synthesis, historical 100 MHz, pin `990f9652` | 68,136 / 70,206 | 37,809 / 29,489 | 15,199 / 5,025 | 6,915 / 574 |

The unchanged public boundary probe supplies a separate ownership check.
These are raw LUT cells, not combined utilization LUTs.

| Synthesis scope | Raw LUT cells, default / attribution | Only external loads, default / attribution | External input and only external loads, default / attribution |
|---|---:|---:|---:|
| 1x1, 50 MHz `u_pp/u_aecp/u_dyn` | 1,624 / 144 | 763 / 0 | 476 / 0 |
| 1x1, 50 MHz `u_pp/u_aecp` | 7,649 / 5,269 | 903 / 18 | 574 / 0 |
| 1x1, 50 MHz `u_pp/u_srp` | 4,960 / 4,947 | 87 / 96 | 86 / 96 |
| 1x1, 50 MHz `u_pp/u_notify` | 3,419 / 3,361 | 0 / 0 | 0 / 0 |
| 1x1, 50 MHz `wrapper` | 26,213 / 24,983 | 1,175 / 173 | 792 / 131 |
| 8x8, historical 100 MHz, pin `990f9652`, `u_pp/u_aecp/u_dyn` | 8,817 / 607 | 5,922 / 0 | 3,108 / 0 |
| 8x8, historical 100 MHz, pin `990f9652`, `u_pp/u_aecp` | 17,872 / 5,607 | 6,187 / 18 | 3,357 / 0 |
| 8x8, historical 100 MHz, pin `990f9652`, `u_pp/u_srp` | 9,110 / 9,480 | 74 / 442 | 67 / 432 |
| 8x8, historical 100 MHz, pin `990f9652`, `u_pp/u_notify` | 3,565 / 3,027 | 1 / 0 | 0 / 0 |
| 8x8, historical 100 MHz, pin `990f9652`, `wrapper` | 42,962 / 32,833 | 6,397 / 519 | 3,499 / 467 |

The following historical 8x8 probes use 100 MHz, pin `990f9652`.
Their default dynamic-state loads name datapath audio-map registers.
They include `amap_out_owner_r` and `amap_out_cluster_r`.
The `amap_edit_oclaim` word, expectation and cluster registers also appear.
The attribution dynamic-state probe has no external-only loads.
Its load-histogram files are empty at both synthesis shapes.
The routed attribution checkpoint is probed separately as well.
Remaining wrapper-level external loads include legitimate exported signals.
The probe classifies cell locations; reverse relocation is not measured.
This evidence replaces the earlier AECP ownership interpretation.
Historical #231 standalone growth uses a 100 MHz OOC clock.
The processor pin is `990f9652` at both shapes.
The 8x8 timer geometry is 100 MHz; 1x1 uses 50 MHz.
The standalone timer grows by 758 LUTs, alongside SRP growth.

## Integrated implementation

The shipping configuration is `endstation_ax7101_1x1_tdm8` at 50 MHz.
Synthesis uses `AreaOptimized_high`; optimization uses `ExploreArea`.
Placement uses `ExtraPostPlacementOpt` in the shipping recipe.
The two comparison placements are `AltSpreadLogic_high` and `ExtraTimingOpt`.
All reuse the same synthesis checkpoint.
Post-placement, routing and post-route optimization use `AggressiveExplore`.
Every run sets 32 threads and leaves the seed at its default.

| Placement directive | Whole LUT | Rebuilt wrapper-name LUT | Final WNS ns | Final WHS ns | Setup / hold failing endpoints |
|---|---:|---:|---:|---:|---:|
| `ExtraPostPlacementOpt`, shipping | 48,618 | 22,441 | +0.013 | +0.014 | 0 / 0 |
| `AltSpreadLogic_high` | 48,972 | 22,560 | +0.123 | +0.036 | 0 / 0 |
| `ExtraTimingOpt` | 48,893 | 22,534 | +0.106 | +0.026 | 0 / 0 |

Wrapper-name counts above use the default rebuilt hierarchy.
They are retained for reproduction, not ownership attribution.

The best measured WNS is +0.123 ns with `AltSpreadLogic_high`.
That run uses 354 more whole-design LUTs than the shipping placement.
All three placement runs finish at rc 0 with no setup or hold failures.
Their checkpoints and reports are retained separately.

The shipping run fully routes all 102,740 routable nets.
Its final WNS is +0.013 ns; final hold slack is +0.014 ns.
No setup, hold or pulse-width endpoints fail in that report.
The route command's earlier timing warning precedes post-route optimization.
The final report is taken after that optimization.
The shipping IOB check passes every active constrained port.

These margins describe the repository's existing constraints.
Both integrated synthesis logs retain `12-4739`, `12-5201` and `20-1307` warnings.
They concern unmatched clock objects and unsupported conditional XDC commands.
The final 1x1 report has zero unclocked or unconstrained internal endpoints.
It still lists 46 inputs and 87 outputs without I/O delays.
This measurement does not establish complete board-interface timing signoff.
No bitstream or hardware test was produced.

## Input integrity

The [input manifest](PP_SHADOW_BASELINE_INPUTS.json) records every wrapper parameter.
It describes original #231 inputs at processor pin `990f9652`.
Its historical 8x8 clock and timer geometry are 100 MHz.
It also records image geometries, byte lengths and SHA-256 hashes.
Each image record names its path root: repository or external work directory.

Both protocol-processor ROMs match the pinned processor's digest ledger.
The listener table contains 128 words of 32 bits.
The AECP microcode contains 2,048 words of 48 bits.
Each generated gPTP image contains 1,024 words of 48 bits.
The builder generates it with the station MAC, priority1 and clock frequency.
Its configuration-specific hash differs from the default-image ledger hash.
The compiled firmware contains 12,939 words at 1x1 and 12,979 at 8x8.
Identifier memories contain 49 bytes.
The writable SRAM has an intentionally empty initialization file.
It is not an empty instruction ROM.

All measured Vivado synthesis logs contain zero `Synth 8-4445` diagnostics.
The preparation helper promotes that diagnostic to an error.
It also rejects missing, short, malformed and ambiguous inputs before synthesis.
Its self-test retains nine original refusal cases.
Synthetic exports exercise inventory, geometry, binding and declaration refusals.
They also exercise endpoint, pathname and CLI containment refusals.
Three default scripts promote missing-ROM diagnostics before synthesis.
The attribution constraint is also checked before synthesis.
Every maintained enforcement-removal mutant fails; the unchanged control passes.
The fast CI workflow runs these checks automatically.
All source and image hashes were checked again after measurement.

## Mapping differences

Yosys uses flattened `synth_xilinx -family xc7` mapping.
All mappings below describe historical #231, processor pin `990f9652`.
These historical mappings retain 50/100 MHz timer parameters, respectively.
Every 8x8 figure below uses the 100 MHz timer geometry.
No timing constraint or WNS applies to these mappings.
Its geometry matches the original integrated wrapper parameters.
These counts have no placement or timing verdict.

| Product | Logic LUT | LUTRAM equivalents | LUT total | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 | 41,258 | 5,972 | 47,230 | 23,041 | 15 | 4 | 5 | 1,813 |
| 8x8, historical 100 MHz timers, pin `990f9652` | 65,724 | 6,136 | 71,860 | 32,615 | 16 | 4 | 7 | 2,108 |

The differences are 24,880 LUTs at 1x1 and 42,868 at 8x8.
Both include distributed-memory LUT equivalents.
Vivado's report explicitly adjusts its LUT count for LUT combining.
Its raw `LUT1` through `LUT6` census totals 24,941 and 32,350 cells.
Its combined logic counts are 21,148 and 27,998 LUTs.
These quantities reconcile the complete reported gap:

| Contribution to Yosys minus Vivado LUT total | 1x1 | Historical 8x8, 100 MHz timers, pin `990f9652` |
|---|---:|---:|
| Difference between raw logic-cell mappings | 16,317 | 33,374 |
| Vivado LUT-combining adjustment | 3,793 | 4,352 |
| Difference in distributed-memory LUT equivalents | 4,770 | 5,142 |
| Total | 24,880 | 42,868 |

An equivalent-geometry run now preserves Yosys module hierarchy.
It changes only the mapping command's `-flatten` option.
Its raw logic counts are 48,915 and 70,222 LUTs.
The [complete reconciliation](PP_SHADOW_BASELINE_MAPPING.tsv) partitions both netlists.
Every direct processor child and both own-logic scopes appear.
Library simulation cells never inflate their primitive's count.
Vivado's internal child hierarchy remains rebuilt.
Child deltas include optimization and relocation across those boundaries.
The [recipe](../testing/PP_SHADOW_BASELINE_RECIPE.md#hierarchical-mapping-comparison) reproduces this accounting.

| Raw logic contribution | Hierarchical Yosys 1x1 | Raw Vivado 1x1 | Difference 1x1 | Hierarchical Yosys 8x8, historical 100 MHz timers, pin `990f9652` | Raw Vivado 8x8, historical 100 MHz, pin `990f9652` | Difference 8x8 |
|---|---:|---:|---:|---:|---:|---:|
| `u_pp/u_srp` | 13,924 | 4,971 | 8,953 | 28,045 | 9,423 | 18,622 |
| `u_pp` own logic | 7,075 | 628 | 6,447 | 11,381 | 505 | 10,876 |
| `u_pp/u_notify` | 7,090 | 3,305 | 3,785 | 6,387 | 3,083 | 3,304 |
| Remaining disjoint scopes | 20,826 | 16,037 | 4,789 | 24,409 | 19,339 | 5,070 |
| Hierarchical total | 48,915 | 24,941 | 23,974 | 70,222 | 32,350 | 37,872 |
| Flattening residual | -7,657 | 0 | -7,657 | -4,498 | 0 | -4,498 |
| Original flattened total | 41,258 | 24,941 | 16,317 | 65,724 | 32,350 | 33,374 |

SRP dominates the hierarchy-preserved logic difference at both shapes.
The processor's own logic is the second-largest contribution.
Notification logic supplies the third-largest positive contribution.
Together they locate the dominant difference in named source scopes.

Flattening removes hierarchy barriers to cross-module optimization.
The residual includes those changed optimization and mapping opportunities.
It is measured globally, without assigning it to individual children.
In particular, hierarchical Yosys retains the unused fourth receive pool.
The flattened and Vivado netlists eliminate that pool.
Preserved-hierarchy figures therefore explain mapping, not integrated fit.
Vivado remains the target implementation's resource and timing instrument.
An architectural lever needs a matched before/after implementation measurement.

The flattened netlist also contains dedicated non-LUT primitives:

| Primitive | 1x1 | Historical 8x8, 100 MHz timers, pin `990f9652` |
|---|---:|---:|
| `INV` | 14,204 | 17,624 |
| `IBUF` | 1,283 | 1,741 |
| `OBUF` | 2,174 | 5,733 |
| `MUXF7` | 371 | 772 |
| `MUXF8` | 102 | 243 |

These cells are excluded from both logic-LUT columns.
Reset inversion and top-level I/O mapping affect structural comparisons.
Neither buffer nor inverter counts should be added as LUTs.

Three concrete memory mappings explain part of the storage difference:

| Structure, product 1x1 | Vivado | Yosys |
|---|---|---|
| Notification controller rows | 2,048 FFs | 1,024 `RAM32M`, equivalent to 4,096 LUTs |
| Listener record RAM | Five RAMB36 | 52 `RAM32M`, equivalent to 208 LUTs |
| Timer slot RAM | One RAMB36 | 14 `RAM64M`, equivalent to 56 LUTs |

The notification rows have several simultaneous read consumers.
Yosys honors their distributed-memory attribute through replicated RAM mapping.
Vivado instead implements those rows as registers.
The Yosys log names the forced distributed-memory mapping.
The mapped netlists supply the primitive counts above.

The primitive inventories also account for the complete BRAM tile difference.
Unlisted blocks use the same tile count in both mappings.
One RAMB18 counts as half a tile.

| Instance | Historical Vivado tiles 1x1 / 8x8, 100 MHz OOC, pin `990f9652` | Historical Yosys tiles 1x1 / 8x8, 50/100 MHz timers, pin `990f9652` |
|---|---:|---:|
| `u_pp/u_listener` | 5 / 5 | 0 / 0 |
| `u_pp/u_timer` | 1 / 1 | 0 / 0 |
| `u_pp/u_rx_validator` | 0.5 / 0.5 | 0 / 0 |
| `u_pp/u_trace` | 1 / 1 | 2 / 2 |
| `u_pp/u_adp` | 0 / 1 | 0 / 0 |
| `u_pp/u_nvm_shadow` | 0 / 2.5 | 0 / 0 |
| `u_pp/u_talker` | 0 / 1.5 | 0 / 0 |
| Total tile difference | 5.5 / 10.5 | Reference |

The control FIFO consumes 1.5 tiles in both flows.
Vivado uses one RAMB36 and one RAMB18 there.
Yosys uses three RAMB18 instances.

At 8x8, Yosys also uses three DSPs in `u_nvm`; Vivado uses one.
The extra mapped multipliers calculate rate and clock-source record offsets.
The other four DSP locations agree between the flows.

The table separates logic mapping from combining and memory equivalents.
Yosys primitive LUT counts differ from combined Slice LUTs.
Neither its LUT total nor its BRAM count predicts placement.
The baseline records the difference without changing memory architecture.

## Historical comparison

The [historical August record](../history/v1/findings/PP_SHADOW_AREA_0812.md) remains evidence.
Its August 13 substituted tree was `eff99a9c`.
Post-synthesis LUTs fell from 56,779 to 55,466: minus 1,313.
BRAM usage rose from 109 to 135 tiles.
Placement failed after the response buffer became 5,079 flops.
These results do not describe the current firmware or RTL.

The later datapath pin comparison also has a correction.
Its exact-head result supersedes the earlier 38,611-LUT claim:
[corrected issue evidence](https://github.com/kebag-logic/milan-fpga/issues/231#issuecomment-5411378865).
At `b3507ddd`, the measured count was 38,879 LUTs.
The corresponding base, `04b55dad`, measured 34,215 LUTs.
The corrected increase was 4,664 LUTs.
Both were whole-datapath OOC synthesis, with both processor ROMs.

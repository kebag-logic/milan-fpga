# AX7101 split image route at 3926c271 (1x1/1if, the shipping point)

Recipe: S9's (the tools in `tools/`, paths filled for this scratch): `boot.sh` (split boot, PASS),
`route_image.sh` (`endstation_builder.py --placement split`, stand-in export, flash map,
`ctrl_plat_image.py --interfaces 1`, the split export with the identity gate, `pp_baseline.py
--placement full-split --single-thread-synthesis`), then `chain_all.sh`: the integrated run
(`route_one.sh split`: synthesis AreaOptimized_high, opt ExploreArea, place ExtraPostPlacementOpt,
route, signoff corners), then ExtraTimingOpt and AltSpreadLogic_high from its synthesis checkpoint
(`prep_directives3.py`: only the place_design directive differs). Each Vivado run through
`vivado-slot.sh`, one at a time (slot 0), with no sweep running. Vivado 2026.1, xc7a100t-fgg484-2.

Export at 3926c271 equals the 84d8a214 export file for file outside the netlist's comment banner;
the firmware in it is `bb04b696...` (145,496 B), the base's (`split-image_manifest-3926c271.json`).

## Signoff (each corner's WNS / WHS, ns; 0 failing endpoints, 0 routing errors in every run)

| Directive | Slow 85C | Slow 0C | Fast 85C | Fast 0C | Floor WNS and WHS >= +0.030 |
|---|---|---|---|---|---|
| ExtraPostPlacementOpt (integrated) | +0.202 / +0.052 | +0.202 / +0.052 | +1.687 / +0.016 | +1.687 / +0.016 | not met (hold +0.016) |
| ExtraTimingOpt | +0.063 / +0.102 | +0.063 / +0.102 | +1.636 / +0.036 | +1.636 / +0.036 | met |
| AltSpreadLogic_high | +0.203 / +0.102 | +0.203 / +0.102 | +1.636 / +0.036 | +1.636 / +0.036 | met |

Best of three: **AltSpreadLogic_high, +0.203 / +0.036**. Base (the tree-identical 084cf7a8, same recipe,
#810's route): ExtraPostPlacementOpt +0.148 / +0.028, ExtraTimingOpt +0.189 / +0.008,
AltSpreadLogic_high +0.074 / +0.008: no base directive met the +0.030 hold floor.

Worst setup paths (`1x1/<directive>/worst10.txt`, `paths3.txt`): ExtraTimingOpt's two worst are the
receive verdict, `KL_mbx/u_rx/ch_r_reg[1]` -> `vd_acc_r_reg/D` +0.063 (21 levels, 11 CARRY4) and ->
`vd_rate_r_reg/D` +0.099: the registered verdict now also reads the channel's held flag. The other two
directives' worst are elsewhere (EPPO `KL_mbx/rd_off_r` -> `reg_rdata_r` +0.202; ASL `KL_mbx/u_evt/
pend_r` -> `tick_cnt_r` +0.203). Worst hold: EPPO +0.016, ETO and ASL +0.036 (`paths3.txt`).

## Area (placed, `alinx_ax7101_utilization_place.rpt` and the hierarchical report), base -> head

| Directive | Slice LUT | FF | LUTRAM | BRAM tiles (RAMB36/RAMB18) | DSP | Slices | `KL_mbx` LUT/FF | `KL_mbx_rx` LUT/FF |
|---|---|---|---|---|---|---|---|---|
| ExtraPostPlacementOpt | 31,255 -> 31,329 (+74) | 42,090 -> 42,166 (+76) | 1,119 -> 1,120 | 78.5 (60/37), unchanged | 9, unchanged | 13,585 -> 13,383 | 5,346/8,739 -> 5,546/8,816 | 1,654/1,290 -> 1,778/1,367 |
| ExtraTimingOpt | 31,215 -> 31,391 (+176) | 42,090 -> 42,166 (+76) | 1,119 -> 1,119 | 78.5 (60/37), unchanged | 9, unchanged | 13,975 -> 14,086 | 5,337/8,739 -> 5,572/8,816 | 1,653/1,290 -> 1,783/1,367 |
| AltSpreadLogic_high | 31,210 -> 31,391 (+181) | 42,091 -> 42,166 (+75) | 1,119 -> 1,119 | 78.5 (60/37), unchanged | 9, unchanged | 13,972 -> 14,078 | 5,338/8,739 -> 5,577/8,816 | 1,655/1,290 -> 1,788/1,367 |

The receive leaf adds +124 to +133 LUT and +77 FF (the per-channel write head and held flag, 5 x 17
bits, and their muxes); at synthesis Vivado also counted 115 LUT of the write-address logic in the
ACMP receive ring's instance (`KL_mbx` +262 LUT at synthesis, +200 to +239 placed).

Vivado peak memory: 6.3 GB (integrated, with synthesis), 4.7 and 4.8 GB. Checkpoints and reports stay
in scratch; their sha256 and sizes are in `1x1/<directive>/artifacts.txt`.

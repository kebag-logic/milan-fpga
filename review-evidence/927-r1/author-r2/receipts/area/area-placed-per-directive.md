Placed utilization per route (each directive's own alinx_ax7101_utilization_place.rpt): base netlist 70f4056f (this lane's base8 reproduction; #925's route8 and route-base of the same netlist) against the head's routes
| route | Slice LUTs | LUT as Logic | LUT as Memory | Slice Registers | Slice | Block RAM Tile |
|---|---:|---:|---:|---:|---:|---:|
| <scratch>/rt/base8/split/gateware | 42607 | 41466 | 1141 | 50722 | 15415 | 92.5 |
| <tmp>/925-a790/rt/route8/split-ExtraTimingOpt | 42604 | 41460 | 1144 | 50724 | 15082 | 92.5 |
| <tmp>/925-a790/rt/route8/split-AltSpreadLogic_high | 42596 | 41453 | 1143 | 50723 | 15071 | 92.5 |
| <scratch>/rt/h2-8x8/split/gateware | 41906 | 40764 | 1142 | 50655 | 15630 | 92.5 |
| <scratch>/rt/h2-8x8/split-ExtraTimingOpt | 41886 | 40744 | 1142 | 50655 | 15187 | 92.5 |
| <scratch>/rt/h2-8x8/split-AltSpreadLogic_high | 41896 | 40754 | 1142 | 50655 | 15179 | 92.5 |
| <tmp>/925-a790/rt/route-base/split/gateware | 31352 | 30232 | 1120 | 42127 | 13309 | 81 |
| <tmp>/925-a790/rt/route-base/split-ExtraTimingOpt | 31318 | 30199 | 1119 | 42119 | 14002 | 81 |
| <scratch>/rt/h2-1x1/split/gateware | 31979 | 30730 | 1249 | 42311 | 13575 | 78 |
| <scratch>/rt/h2-1x1/split-ExtraTimingOpt | 32103 | 30855 | 1248 | 42312 | 14222 | 78 |
| <scratch>/rt/h2-1x1/split-AltSpreadLogic_high | 32061 | 30813 | 1248 | 42312 | 14204 | 78 |

Control sets (alinx_ax7101_control_sets.rpt, Total control sets):
<scratch>/rt/base8/split/gateware | Total control sets | 2614 |
<scratch>/rt/h2-8x8/split/gateware | Total control sets | 2613 |
<tmp>/925-a790/rt/route-base/split/gateware | Total control sets | 1522 |
<scratch>/rt/h2-1x1/split/gateware | Total control sets | 1500 |

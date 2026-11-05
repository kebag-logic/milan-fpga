# Area: milan_datapath, base and head, one instrument

Instrument: `syn/ooc/milan_datapath_ooc.tcl` (Vivado 2026.1 `synth_design -mode out_of_context`, part
xc7a100tfgg484-2, 100 MHz on `axis_clk`), on a fresh clean clone at each commit, through `vivado-slot.sh`, run by
`ooc.sh`. The elaboration shape is the script's default, the 1x1 `arty_current` config the Yosys gate also uses; it
is not the routed AX7101 TDM8 shipping image (that build is the daily area flow's, which touches the bench console in
its preflight, outside this lane's permissions). The change is shape-independent: two flops, a two-bit beat counter,
eight AND gates and the stamp's 48-bit select on the control lane.

| Figure | base `604899c0` | head `8d2dfb65` | Delta |
|---|---:|---:|---:|
| Slice LUTs | 45,176 | 45,275 | +99 |
| LUT as logic | 41,886 | 41,985 | +99 |
| LUT as memory | 3,290 | 3,290 | 0 |
| Slice registers | 40,222 | 40,233 | +11 |
| F7 muxes | 805 | 920 | +115 |
| F8 muxes | 104 | 109 | +5 |
| Block RAM tiles | 27.5 | 27.5 | 0 |
| DSPs | 13 | 13 | 0 |
| WNS (ns), OOC, 10 ns | -4.914 | -4.914 | 0 |
| TNS (ns) | -1854.240 | -1854.364 | -0.124 |
| TNS failing endpoints | 2683 | 2683 | 0 |

Both runs exit 0 (`rc-base`, `rc-head`); each clone's tree is clean after the run. The OOC WNS is the base's own
figure (other clocks unconstrained out of context), unchanged by this change; it is not a routed timing claim.
Reports: `util_base.rpt`, `util_head.rpt`, `util_hier_*.rpt`, `timing_*.rpt`. The two Vivado transcripts are over
200 KB and are recorded by size and sha256 in `LARGE-LOGS.txt`, with their tails beside them.

# Routes, round 2

Each directory is one Vivado route through S9's recipe (the image's export, `pp_baseline.py --placement full-split
--single-thread-synthesis`, `baseline_integrated.tcl` for ExtraPostPlacementOpt, `prep_directives3.py` for the two other
directives from its synthesis checkpoint), collected by `../tools/collect.sh.txt`: `signoff.txt` (every corner's
WNS and WHS from the signoff reports), `worst10.txt`, `paths3.txt`, the route status, the placed utilization table, and
`artifacts.txt` (sha256 and size of the routed checkpoint and reports, kept in scratch; route start, end and rc).

- `h2-8x8-*`: 8x8/1if at 5d098172's clone, the three directives.
- `h2-1x1-*`: 1x1/1if at 338ece89's clone, the three directives.
- `rel2-head-1x1-tdm8-release`: the release image (all-fabric `endstation_ax7101_1x1_tdm8`) at 338ece89, the
  integrated route. `signoff.py` reports the split floor (WNS and WHS >= +0.030) as not met because it tests both
  floors; the release's own floor (WNS >= +0.03, WHS >= 0) is met at every corner (`../release/`).
- `f2-8x8-fill-*`, `f2-1x1-fill-*`: each split shape with 2,168 B of ROM added (`../tools/fill_patch.py.txt`, in a
  scratch clone of 338ece89 only), the recipe's directive.

Since 5d098172 nothing under `hdl/` changed but comments in `cdc_pair_fifo.sv` and a generated README.

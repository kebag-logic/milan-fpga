#!/usr/bin/env bash
# collect_directives.sh: the round-2 directive receipts into receipts/directives/, host paths redacted, large reports by digest.
set -u
S=$(cd "$(dirname "$0")" && pwd); W=$VALIDATION_STORAGE/scratch/806-a701b; O=$(dirname "$S")/receipts/directives
G=$VALIDATION_STORAGE/scratch/806-a701/viv-cf3ef596/w1/ax7101/gateware
mkdir -p "$O"
python3 "$S/copy_receipts.py" "$O" "$W/gate/directive-figures.txt" "$W/synth-dcp.sha256.before"
sha256sum "$G/alinx_ax7101_synth.dcp" | sed "s#$G/##" > "$O/synth-dcp.sha256.after"
for d in ExtraPostPlacementOpt AltSpreadLogic_high ExtraTimingOpt; do
  python3 "$S/copy_receipts.py" "$O/gate" "$W/gate/$d.log"; mv "$O/gate/$d.log" "$O/gate/route-1x1-check-$d.log"
done
journalctl --user -u 'milan-806-a701b-viv-*' --no-pager -o short-iso | grep -E "vivado-slot|START|END" | sed 's/^[^ ]* [^ ]* //' > "$O/timeline.txt"
for d in AltSpreadLogic_high ExtraTimingOpt; do
  R=$W/ax7101-$d; T=$O/$d; mkdir -p "$T"
  python3 "$S/copy_receipts.py" "$T" "$R/baseline_implementation.tcl" "$R/vivado.rc" "$R/alinx_ax7101_route_status.rpt" \
    "$R/alinx_ax7101_iob_pack.rpt" "$R/baseline_utilization.rpt" "$R/alinx_ax7101_utilization_place.rpt" \
    "$R/baseline_scope_timing.tsv" "$R/alinx_ax7101_signoff_grade.txt" \
    "$R"/alinx_ax7101_signoff_*_negative.rpt "$R"/alinx_ax7101_signoff_*_operating.rpt
  f=$R/alinx_ax7101_signoff_Slow_0C_timing.rpt
  n=$(grep -n "^Slack (MET) :" "$f" | head -1 | cut -d: -f1)
  wns=$(python3 -c "import re,sys; t=open(sys.argv[1]).read(); print(min(float(x) for x in re.findall(r'^Slack \(\w+\) :\s+(-?[\d.]+)ns.*\n.*\n.*\n.*\n.*\n.*\n  Path Type:\s+Setup', t, re.M)))" "$f")
  n=$(grep -n "^Slack (MET) :\s*${wns}ns" "$f" | head -1 | cut -d: -f1)
  sed -n "${n},$((n+70))p" "$f" > "$T/worst-setup-path-Slow_0C.txt"
  ( cd "$R" && sha256sum vivado.out baseline.log alinx_ax7101_signoff_*_timing.rpt alinx_ax7101_signoff_all_timing.rpt \
      baseline_timing.rpt baseline_hierarchy.rpt baseline_cells.tsv alinx_ax7101_route.dcp alinx_ax7101_place.dcp ) > "$T/large.sha256"
  ( cd "$R" && stat -c '%s %n' vivado.out baseline.log alinx_ax7101_route.dcp ) > "$T/large.sizes"
done
du -sh "$O"

#!/usr/bin/env bash
# collect.sh <part...>: copy receipts into the output directory, host paths replaced (receipt.py), large reports
# reduced to their summary lines with the full file's size and sha256. parts: route ooc ledger m8a2 endpoint tools
set -uo pipefail
S=<scratch>; O=<home>/milan-fpga-management/2026-09-23/665s9-a760/receipts
R="python3 $S/tools/receipt.py"
mkdir -p "$O"
big() {  # big <src> <dest>: size and sha256 of a file too large to copy
  mkdir -p "$(dirname "$2")"
  printf 'not copied (over 200 KB or a binary): %s\nbytes %s\nsha256 %s\n' "$(basename "$1")" "$(stat -c %s "$1")" \
    "$(sha256sum "$1" | cut -d' ' -f1)" > "$2"
}
route_dir() {  # route_dir <src dir> <dest dir> <head> <what>
  local g=$1 d=$2 h=$3 w=$4
  mkdir -p "$d"
  for f in baseline_utilization.rpt alinx_ax7101_route_status.rpt alinx_ax7101_signoff_grade.txt baseline_placement.tsv \
           baseline_scope_timing.tsv route.start route.end route.rc signoff.txt; do
    [ -f "$g/$f" ] && $R "$g/$f" "$d/$f" "$h" "$w" > /dev/null
  done
  python3 $S/tools/signoff.py "$g" > "$S/tmp/signoff.txt" 2>&1; $R "$S/tmp/signoff.txt" "$d/signoff.txt" "$h" "tools/signoff.py <route dir>" > /dev/null
  for c in Slow_85C Fast_85C; do
    t=$g/alinx_ax7101_signoff_${c}_timing.rpt
    { grep -m1 -A3 "    WNS(ns)" "$t"; echo; grep -m1 -A14 "Intra Clock Table" "$t"; } > "$S/tmp/clocks.txt"
    $R "$S/tmp/clocks.txt" "$d/timing-summary-$c.txt" "$h" "the design and per-clock summary of $(basename "$t")" > /dev/null
    big "$t" "$d/$(basename "$t").sha256"
  done
  n=$g/alinx_ax7101_signoff_Slow_85C_negative.rpt
  grep -E "^Slack|^  Source:|^  Destination:|^  Data Path Delay|^  Logic Levels|^  Path Group" "$n" > "$S/tmp/neg.txt"
  $R "$S/tmp/neg.txt" "$d/violations-Slow_85C.txt" "$h" "every violating path's header lines of $(basename "$n")" > /dev/null
  [ -f "$g/baseline_hierarchy.rpt" ] && $R "$g/baseline_hierarchy.rpt" "$d/baseline_hierarchy.rpt" "$h" "$w" > /dev/null
  [ -f "$g/baseline_cells.tsv" ] && {
    awk -F'\t' '$2 ~ /^RAMB(36|18)E1$/ { n=$1; sub(/\/.*/, "", n); sub(/_reg.*/, "", n); c[n" "$2]++ } END { for (k in c) print c[k], k }' \
      "$g/baseline_cells.tsv" | sort -k2 > "$S/tmp/bram.txt"
    $R "$S/tmp/bram.txt" "$d/block-ram-by-owner.txt" "$h" "block RAM primitives by top-level owner, from baseline_cells.tsv" > /dev/null
    big "$g/baseline_cells.tsv" "$d/baseline_cells.tsv.sha256"
  }
  for f in "$g"/*.dcp; do [ -f "$f" ] && big "$f" "$d/$(basename "$f").sha256"; done
}
mkdir -p "$S/tmp"
for part in "$@"; do
  case $part in
    route)
      H=5d6d28356a6c73bdfba43a9b023e60279a0d461b
      route_dir $S/route/split/gateware "$O/route/split-ExtraPostPlacementOpt" $H "integrated split route, the recipe's directive (baseline_integrated.tcl)"
      route_dir $S/route/split-ExtraTimingOpt "$O/route/split-ExtraTimingOpt" $H "the split route's synthesis checkpoint, placed at ExtraTimingOpt (#818)"
      route_dir $S/route/split-AltSpreadLogic_high "$O/route/split-AltSpreadLogic_high" $H "the split route's synthesis checkpoint, placed at AltSpreadLogic_high (#818)"
      route_dir $S/route/fabric/gateware "$O/route/fabric" $H "the all-fabric endpoint route (baseline_integrated.tcl, default selection)"
      for f in route_image.log fabric_route_image.log split-inputs.sha256 slot-split.log slot-best3.log slot-fabric.log \
               gate-check-gateware.log gate-check-split-ExtraTimingOpt.log gate-check-route-set.log gate-check-fabric.log; do
        $R "$S/route/$f" "$O/route/$f" $H "see the file name" > /dev/null
      done
      big $S/route/split/gateware/alinx_ax7101.v "$O/route/split-export-alinx_ax7101.v.sha256"
      big $S/route/fabric/gateware/alinx_ax7101.v "$O/route/fabric-export-alinx_ax7101.v.sha256"
      $R $S/route/split/image_manifest.json "$O/route/split-image_manifest.json" $H "the split image's manifest" > /dev/null
      ;;
    ooc)
      H=e16c1343057ca23e544f22c4c023065809c3b5bf
      for v in if1-head if1-tied if2-head if2-tied; do
        for f in util_hier.rpt route_status.rpt src.sha256 rc ooc.tcl; do
          $R "$S/ooc/$v/$f" "$O/ooc/$v/$f" $H "tools/ooc_term.sh" > /dev/null
        done
        grep -m1 -A3 "    WNS(ns)" "$S/ooc/$v/timing.rpt" > "$S/tmp/t.txt"; $R "$S/tmp/t.txt" "$O/ooc/$v/timing-summary.txt" $H "design summary of timing.rpt" > /dev/null
      done
      $R $S/ooc/slot.log "$O/ooc/slot.log" $H "tools/ooc_term.sh through the slot wrapper" > /dev/null
      $R $S/ooc/if2-gen.log "$O/ooc/if2-gen.log" $H "gen_mailbox.py --variant-interfaces 2" > /dev/null
      ;;
    ledger)
      H=5d6d28356a6c73bdfba43a9b023e60279a0d461b
      for p in 1x1-1if 1x1-2if 8x8-1if 8x8-2if; do
        $R "$S/ledger/$p/size.json" "$O/ledger/$p-size.json" $H "ctrl_plat_image.py (tools/ledger_points.sh)" > /dev/null
        $R "$S/ledger/$p/size.txt" "$O/ledger/$p-size.txt" $H "ctrl_plat_image.py" > /dev/null
        big "$S/ledger/$p/ctrl_app.elf" "$O/ledger/$p-ctrl_app.elf.sha256"
      done
      $R $S/ledger/ledger_points.log "$O/ledger/ledger_points.log" $H "tools/ledger_points.sh" > /dev/null
      $R $S/ledger/ledger_rows.json "$O/ledger/ledger_rows.json" 0f3c475685b6247779398457249beafebb0b275a "tools/ledger_table.py" > /dev/null
      for f in ctrl_memory_plan.json ctrl_memory_ooc.tsv emit.log slot.log rc; do
        $R "$S/memooc/$f" "$O/ledger/memooc-$f" 0f3c475685b6247779398457249beafebb0b275a "ctrl_memory_ooc.py --ledgered s8i2=platform-8x8-two-interfaces; tools/memooc.sh" > /dev/null
      done
      ;;
    m8a2)
      for f in $S/m8a2/*.log $S/m8a2/*.rc; do
        h=$(head -1 "$f" | grep -oE "[0-9a-f]{40}" | head -1); [ -n "$h" ] || h=see-log
        $R "$f" "$O/m8a2/$(basename "$f")" "$h" "tools/m8a2_runs.sh" > /dev/null
      done
      ;;
    endpoint)
      for f in $S/endpoint-flow/compare-*.json; do
        $R "$f" "$O/endpoint/$(basename "$f")" 5d6d28356a6c73bdfba43a9b023e60279a0d461b "tools/endpoint_compare.py, base 1d6bf555" > /dev/null
      done
      for f in base.sha256 head.sha256; do
        $R "$S/builder-cmp/$f" "$O/endpoint/builder-all-fabric-$f" ad2ed0e3ab3daa9697bdf42ae504b4504bfd04aa "endstation_builder.py <cfg> for the five shipped configs" > /dev/null
      done
      ;;
    gates)
      H=ad2ed0e3ab3daa9697bdf42ae504b4504bfd04aa
      for f in $S/gates/*.log; do
        case $(basename "$f") in *-clone.log) continue ;; esac
        $R "$f" "$O/gates/$(basename "$f")" $H "tools/gates.sh, tools/budget-points.sh (see the file name)" > /dev/null
      done
      $R $S/gates-run.log "$O/gates/gates-run.log" $H "every standalone gate's finish line, in order" > /dev/null
      sed -e "s#$S#<scratch>#g; s#<home>#<home>#g" $S/gates/docsyml-not_run.json > "$O/gates/docsyml-not_run.json"
      C=$S/ci/ad2ed0e3ab3d
      python3 $S/tools/replay/ci_replay.py table $H "$S/tmp/ci-table.md" "$S/tmp/not_run.json" > "$S/tmp/ci-table.out" 2>&1
      echo "rc=$?" >> "$S/tmp/ci-table.out"
      $R "$S/tmp/ci-table.md" "$O/ci/ci-table.md" $H "ci_replay.py table: every run: step of every job a pull_request to dev-soft-core triggers" > /dev/null
      $R "$S/tmp/ci-table.out" "$O/ci/ci-table.out" $H "ci_replay.py table" > /dev/null
      sed -e "s#$S#<scratch>#g; s#<home>#<home>#g; s#<data>#<data>#g" "$S/tmp/not_run.json" > "$O/ci/not_run.json"
      for j in $C/jobs/*/ $C/attempts/*/; do
        n=$(basename "$j"); k=$(basename "$(dirname "$j")")
        [ -f "$j/result.json" ] && $R "$j/result.json" "$O/ci/$k/$n/result.json" $H "ci_replay.py job" > /dev/null
        [ -f "$j/KILLED-BY-RESET" ] && cp "$j/KILLED-BY-RESET" "$O/ci/$k/$n.KILLED-BY-RESET" 2>/dev/null
        for l in "$j"/logs/*.log; do
          [ -f "$l" ] && $R "$l" "$O/ci/$k/$n/$(basename "$l")" $H "ci_replay.py job (the step's own log)" > /dev/null
        done
      done
      for k in 0 1 2 3; do
        d=$S/sweep/shard-$k
        [ -d "$d" ] || continue
        $R "$d/spec.json" "$O/sweep/shard-$k/spec.json" $H "sweep-shard.py $k" > /dev/null
        [ -f "$d/spec/results.json" ] && $R "$d/spec/results.json" "$O/sweep/shard-$k/results.json" $H "run-recorded-gates.py" > /dev/null
        for l in "$d"/spec/*.log; do [ -f "$l" ] && $R "$l" "$O/sweep/shard-$k/$(basename "$l")" $H "scripts/run_all_suites.sh --shard $k/4" > /dev/null; done
        [ -d "$d/logs" ] && for l in "$d"/logs/*; do [ -f "$l" ] && $R "$l" "$O/sweep/shard-$k/logs/$(basename "$l")" $H "the suite's own log" > /dev/null; done
      done
      ;;
    tools)
      mkdir -p "$O/tools"
      mkdir -p "$O/tools/docsyml"
      for f in $S/tools/docsyml/*; do sed -e "s#$S#<scratch>#g; s#<lane>#<lane>#g; s#<home>#<home>#g; s#<data>#<data>#g" "$f" > "$O/tools/docsyml/$(basename "$f")"; done
      for f in $S/tools/*.sh $S/tools/*.py $S/tools/replay/ci_replay.py $S/tools/replay/overrides.json $S/tools/replay/pidfd_shim.py; do
        sed -e "s#$S#<scratch>#g; s#<lane>#<lane>#g; s#<tools>#<tools>#g; s#<home>#<home>#g; s#<data>#<data>#g" "$f" > "$O/tools/$(basename "$f")"
      done
      ;;
  esac
done
echo "collected: $*"

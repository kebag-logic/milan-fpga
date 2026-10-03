#!/usr/bin/env bash
# R446-8 probe: plant one change at a time into a disposable copy of the
# head's syn/ooc/pp_resource_baseline.json and run check-baseline on it.
# A policy plant (tolerance, floor, ceiling) must exit non-zero; a note-only
# or record-figure plant is outside what check-baseline polices.
# usage: probe_policy_plants.sh <repo> <head> <scratch-dir>
set -u
repo=$1 head=$2 work=$3
rm -rf "$work"; mkdir -p "$work"
git -C "$repo" archive "$head" syn/ooc docs/design/AREA_BUDGET.md | tar -x -C "$work"
cd "$work" || exit 2
cp syn/ooc/pp_resource_baseline.json base.json
plant() {
  name=$1 expr=$2 want=$3
  python3 - "$expr" <<'EOF'
import json, sys
d = json.load(open("base.json"))
e = d["endpoints"]
exec(sys.argv[1])
open("syn/ooc/pp_resource_baseline.json", "w").write(json.dumps(d, indent=1) + "\n")
EOF
  python3 syn/ooc/pp_resource_gate.py check-baseline > "out-$name.log" 2>&1
  rc=$?
  if [ "$want" = nonzero ]; then [ $rc -ne 0 ] && v=AS-EXPECTED || v=UNEXPECTED
  else [ $rc -eq 0 ] && v=AS-EXPECTED || v=UNEXPECTED; fi
  printf '%-28s rc=%s want=%-7s %s | %s\n' "$name" "$rc" "$want" "$v" "$(tail -n 1 "out-$name.log")"
}
plant control 'pass' zero
plant route-lut-tol-501 'e["route-1x1"]["tolerance"]["LUT"]=501' nonzero
plant route-ff-tol-599 'e["route-1x1"]["tolerance"]["FF"]=599' nonzero
plant route-slice-tol-81 'e["route-1x1"]["tolerance"]["SLICE"]=81' nonzero
plant route-wns-floor-0.029 'e["route-1x1"]["floor"]["WNS_ns"]=0.029' nonzero
plant route-whs-floor-neg 'e["route-1x1"]["floor"]["WHS_ns"]=-0.001' nonzero
plant route-ceiling-122 'e["route-1x1"]["ceiling"]["BRAM_TILE"]=122' nonzero
plant route-ceiling-drop 'del e["route-1x1"]["ceiling"]' nonzero
plant ooc1-lut-tol-251 'e["ooc-1x1"]["tolerance"]["LUT"]=251' nonzero
plant ooc8-ff-tol-340 'e["ooc-8x8"]["tolerance"]["FF"]=340' nonzero
plant ooc8-dsp-tol-1 'e["ooc-8x8"]["tolerance"]["DSP"]=1' nonzero
plant route-timing-fall-0.3 'e["route-1x1"]["tolerance"]["WNS_ns"]=0.3' nonzero
plant measured-note-edit 'e["route-1x1"]["measured"]="dev 5fabb46e, probe"' zero
plant record-lut-minus-1 'e["route-1x1"]["record"]["figures"]["LUT"]-=1' zero

#!/usr/bin/env bash
# rsweep2.sh <clone> <work> <base-clone> <base-work>: rsweep.sh at <clone> (every SoC variant), then
#  1. the focused missing-image control: the same export tree (copied, its builder-out link removed) exported with a
#     copy of the plan whose soc section names the split placement: soc_sweep.py must refuse before any export,
#     naming the platform image, and write no export;
#  2. the accepted exports (ship, axilite) against the base's, file for file, each side's roots normalised.
set -u
C=$1; W=$2; BC=$3; BW=$4
S=<scratch>
bash $S/bin/rsweep.sh "$C" "$W"; r0=$?
source $S/bin/env.sh
X=$W-split-control; rm -rf "$X"; mkdir -p "$X"
cp -a "$W/tree" "$X/tree"; rm -f "$X/tree/sw/builder/out"
python3 - "$C/syn/resmap/sweep_plan.json" "$X/plan-split.json" <<'EOF'
import json, sys
plan = json.load(open(sys.argv[1])); plan["soc"]["placement"] = "split"
json.dump(plan, open(sys.argv[2], "w"), indent=1)
EOF
echo "== control: the plan copy names placement $(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['soc']['placement'])" "$X/plan-split.json")"
echo "   platform images in the control tree before: $(find "$X" -name ctrl_app.elf | wc -l)"
(cd "$C" && python3 -B syn/resmap/soc_sweep.py --work "$X" --plan "$X/plan-split.json" --litex-python "$(command -v python3)" \
  --sdk "$SDK/host" export ship axilite); rc=$?
echo "   control rc=$rc; exports written: $(find "$X" -path '*/soc/*/export' -type d | wc -l); exports.json: $([ -e "$X/soc/exports.json" ] && echo present || echo absent)"
for v in ship axilite; do
  echo "== $v: base export vs this head's"
  python3 $S/bin/cmp_export.py "$BW/soc/$v/export" "$BC,$BW" "$W/soc/$v/export" "$C,$W"
  echo "   argv: $(python3 - "$BW/soc/exports.json" "$W/soc/exports.json" "$v" "$BC" "$BW" "$C" "$W" <<'EOF'
import json, sys
a, b, v, bc, bw, c, w = sys.argv[1:]
na = [x.replace(bw, "<WORK>").replace(bc, "<REPO>") for x in json.load(open(a))[v]["argv"]]
nb = [x.replace(w, "<WORK>").replace(c, "<REPO>") for x in json.load(open(b))[v]["argv"]]
print("equal" if na == nb else f"DIFFER {sorted(set(na) ^ set(nb))}")
EOF
)"
done
echo "END sweep=$r0 control=$rc $(date -Iseconds)"

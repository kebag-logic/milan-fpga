#!/bin/sh
# Re-derive the #649 page tables at the review head from #649's published
# inputs. The head's `summary` records a point whose shape the builder refused
# as {"builder": {"refusal": line}} and keeps every other entry; this applies
# that rule to #649's published summary.json using this review's own `shapes`
# outcomes, then runs the head's models and tables against the head page
# (check mode, nothing written to the clone). The base page is checked the
# same way from the untransformed summary with the base scripts.
# Usage: reproduce_649_tables.sh <clone> <inputs dir> <shapes work> <scratch>
set -u
C=$1; IN=$2; SW=$3; S=$4
M=$S/map649; rm -rf "$M"; cp -r "$IN/map" "$M"; xz -dc "$IN/map_cells.tsv.xz" > "$M/map_cells.tsv"
for side in head base; do
  W=$S/w649-$side; rm -rf "$W" "$S/m649-$side"; mkdir -p "$W"
  cp -r "$IN/work/." "$W/"; xz -dk "$W/summary.json.xz"; rm "$W/summary.json.xz"
done
mkdir -p "$S/w649-head/shapes"; cp "$SW/shapes/outcomes.json" "$S/w649-head/shapes/"
python3 - "$C" "$S/w649-head" <<'PY'
import json, sys
from pathlib import Path
clone, work = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(clone / "syn/resmap"))
import yosys_sweep as ys
plan = ys.load_plan(ys.PLAN)
summary = json.loads((work / "summary.json").read_text())
changed = []
for point in plan["points"]:
    line = ys.builder_refusal(work, plan, point)
    if line:
        summary[point["name"]] = {"builder": {"refusal": line}}
        changed.append(point["name"])
(work / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n")
print(f"head summary: {len(summary)} entries, builder-refused: {changed}")
PY
# head scripts against the head page
(cd "$C" && python3 syn/resmap/resmap_models.py --work "$S/w649-head" --map "$M" --out "$S/m649-head" \
  && python3 syn/resmap/resmap_tables.py --work "$S/w649-head" --models "$S/m649-head" --map "$M" \
     --soc-variants "$IN/soc_prices.json" --out "$S/t649-head.md" \
     --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md); echo "head page check rc=$?"
# base scripts against the base page, from the scratch base export
(cd "$S/base" && python3 syn/resmap/resmap_models.py --work "$S/w649-base" --map "$M" --out "$S/m649-base" \
  && python3 syn/resmap/resmap_tables.py --work "$S/w649-base" --models "$S/m649-base" --map "$M" \
     --soc-variants "$IN/soc_prices.json" --out "$S/t649-base.md" \
     --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md); echo "base page check rc=$?"

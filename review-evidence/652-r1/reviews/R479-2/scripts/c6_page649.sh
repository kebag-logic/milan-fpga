#!/bin/sh
# Campaign 6: the #649 page against a fresh generation at the head, from #649's
# published inputs (649-review-evidence 113a1fb9, review-evidence/649-r2/author/
# inputs). The head's `summary` cannot be re-run without #649's point receipts,
# so the summary it would give is reconstructed: the published summary with each
# point whose shape is a builder-refused variant replaced by its builder record,
# the refusal line taken from this campaign's own real `shapes` run (c4).
# Usage: c6_page649.sh <head tree> <base tree> <receipt dir> <scratch dir> <c4 outcomes.json>
H=$1; B=$2; R=$3; S=$4; OUTC=$5; mkdir -p "$R"; rm -rf "$S"; mkdir -p "$S"
cd "$H" || exit 9
git archive 113a1fb9108321cafa5f90592138b79757680c6b review-evidence/649-r2/author/inputs | tar -x -C "$S"
I=$S/review-evidence/649-r2/author/inputs
xz -dk "$I/work/summary.json.xz" "$I/models/models.json.xz" "$I/map_cells.tsv.xz"
mv "$I/map_cells.tsv" "$I/map/map_cells.tsv"
sha256sum "$I/work/summary.json" "$I/models/models.json" > "$R/c6_published_inputs.sha256"
# base code on the published inputs must reproduce the published models.json (instrument check)
(cd "$B" && python3 syn/resmap/resmap_models.py --work "$I/work" --map "$I/map" --out "$S/base-models") \
  > "$R/c6_base_models.log" 2>&1; echo $? > "$R/c6_base_models.rc"
cmp "$S/base-models/models.json" "$I/models/models.json" > "$R/c6_base_models_vs_published.txt" 2>&1
echo "cmp_rc=$?" >> "$R/c6_base_models_vs_published.txt"
# the head's summary, reconstructed
mkdir -p "$S/work"; cp -a "$I/work/." "$S/work/"; rm -f "$S/work/summary.json.xz"
python3 - "$S/work/summary.json" "$OUTC" > "$R/c6_summary_derivation.txt" <<'EOF'
import json, sys
sys.path.insert(0, "syn/resmap")
import yosys_sweep
summary_path, outcomes_path = sys.argv[1:3]
plan = yosys_sweep.load_plan(yosys_sweep.PLAN)
outcomes = json.load(open(outcomes_path))
summary = json.load(open(summary_path))
refused = {n for n, o in outcomes.items() if o["outcome"] == "refused"}
print("refused variants from the live shapes run:", sorted(refused))
for point in plan["points"]:
    shape = point.get("shape")
    if shape in refused:
        print(f"point {point['name']} (shape {shape}) -> builder record: {outcomes[shape]['refusal']}")
        summary[point["name"]] = {"builder": {"refusal": outcomes[shape]["refusal"]}}
print("entries:", len(summary), "builder records:", sum("builder" in e for e in summary.values()))
open(summary_path, "w").write(json.dumps(summary, indent=1, sort_keys=True) + "\n")
EOF
python3 syn/resmap/resmap_models.py --work "$S/work" --map "$I/map" --out "$S/models" > "$R/c6_head_models.log" 2>&1
echo $? > "$R/c6_head_models.rc"
sha256sum "$S/models/models.json" | sed "s|$S/||" > "$R/c6_head_models.sha256"
python3 -c "import json,sys; g=json.load(open(sys.argv[1]))['guards']; print(json.dumps({'by_builder': g.get('by_builder'), 'refused_builder': {k: v for k, v in g['refused'].items() if k in (g.get('by_builder') or [])}}, indent=1))" \
  "$S/models/models.json" > "$R/c6_head_guards_by_builder.json"
cp docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md "$S/page.md"
python3 syn/resmap/resmap_tables.py --work "$S/work" --models "$S/models" --map "$I/map" \
  --soc-variants "$I/soc_prices.json" --out "$S/tables.md" --page "$S/page.md" > "$R/c6_head_tables_check.log" 2>&1
echo $? > "$R/c6_head_tables_check.rc"
cmp "$S/page.md" docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md > "$R/c6_page_untouched.txt" 2>&1; echo "cmp_rc=$?" >> "$R/c6_page_untouched.txt"
grep -o '<!-- table: [a-z0-9-]* -->' docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md | wc -l > "$R/c6_page_block_count.txt"
git status --porcelain > "$R/c6_status_after.txt"
echo done > "$R/c6.done"

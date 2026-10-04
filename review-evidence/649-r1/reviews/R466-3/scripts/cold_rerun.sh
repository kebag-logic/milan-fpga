#!/usr/bin/env bash
# Cold re-run of the #649 map, models and page check from the published round-2 inputs,
# in a git archive of the exact head under review. Usage: cold_rerun.sh <repo> <head> <evidence author dir> <out dir>
set -u
repo=$1 head=$2 ev=$3 out=$4
rm -rf "$out" && mkdir -p "$out/tree"
git -C "$repo" archive "$head" | tar -x -C "$out/tree"
cd "$out/tree" || exit 2
cp "$ev/inputs/map_cells.tsv" "$ev/inputs/map/map_cells.tsv"
{
echo "# head $head"; echo "# census sha256 $(sha256sum "$ev/inputs/map/map_cells.tsv" | cut -d' ' -f1)"
for t in resmap_map resmap_models resmap_tables yosys_sweep soc_sweep; do
  echo "\$ python3 syn/resmap/$t.py --selftest"; python3 syn/resmap/$t.py --selftest 2>&1 | tail -3; echo "rc=${PIPESTATUS[0]}"
done
echo "\$ python3 syn/resmap/resmap_map.py map inputs/map --out map-out"
python3 syn/resmap/resmap_map.py map "$ev/inputs/map" --out "$out/map-out"; echo "rc=$?"
echo "\$ python3 syn/resmap/resmap_models.py --work inputs/work --map inputs/map --out models"
python3 syn/resmap/resmap_models.py --work "$ev/inputs/work" --map "$ev/inputs/map" --out "$out/models"; echo "rc=$?"
echo "\$ cmp models/models.json inputs/models/models.json"; cmp "$out/models/models.json" "$ev/inputs/models/models.json"; echo "rc=$?"
echo "\$ python3 syn/resmap/resmap_tables.py --work inputs/work --models models --map inputs/map --soc-variants inputs/soc_prices.json --out tables.md --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md"
python3 syn/resmap/resmap_tables.py --work "$ev/inputs/work" --models "$out/models" --map "$ev/inputs/map" --soc-variants "$ev/inputs/soc_prices.json" --out "$out/tables.md" --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md; echo "rc=$?"
for f in blocks_ranked.md partition.md lut_sharing.md map.json; do
  echo "\$ cmp map-out/$f outputs/$f"; cmp "$out/map-out/$f" "$ev/outputs/$f"; echo "rc=$?"; done
echo "\$ cmp tables.md outputs/tables.md"; cmp "$out/tables.md" "$ev/outputs/tables.md"; echo "rc=$?"
} 2>&1

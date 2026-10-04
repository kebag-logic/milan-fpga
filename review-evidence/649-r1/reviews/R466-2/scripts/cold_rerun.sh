#!/bin/sh
# R466-2 probe: cold re-run of the map tie, the models and the page table check from the
# published round-2 inputs, in a git archive of the exact head.
# Usage: cold_rerun.sh <tree: archive of the head with inputs/ placed beside it, the two
#        .xz files decompressed and the census at inputs/map/map_cells.tsv> <out dir>
set -u
cd "$1" || exit 2
OUT=$2
mkdir -p "$OUT"
echo "\$ python3 syn/resmap/resmap_map.py map inputs/map --out $OUT/map"
python3 syn/resmap/resmap_map.py map inputs/map --out "$OUT/map"; echo "rc=$?"
echo "\$ python3 syn/resmap/resmap_models.py --work inputs/work --map inputs/map --out $OUT/models"
python3 syn/resmap/resmap_models.py --work inputs/work --map inputs/map --out "$OUT/models"; echo "rc=$?"
echo "\$ cmp $OUT/models/models.json inputs/models/models.json"
cmp "$OUT/models/models.json" inputs/models/models.json; echo "rc=$?"
echo "\$ python3 syn/resmap/resmap_tables.py --work inputs/work --models inputs/models --map inputs/map --soc-variants inputs/soc_prices.json --out $OUT/tables.md --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md"
python3 syn/resmap/resmap_tables.py --work inputs/work --models inputs/models --map inputs/map \
  --soc-variants inputs/soc_prices.json --out "$OUT/tables.md" \
  --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md; echo "rc=$?"
echo "\$ python3 syn/resmap/resmap_tables.py (regenerated models) --page"
python3 syn/resmap/resmap_tables.py --work inputs/work --models "$OUT/models" --map inputs/map \
  --soc-variants inputs/soc_prices.json --out "$OUT/tables-fresh-models.md" \
  --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md; echo "rc=$?"

#!/usr/bin/env bash
# Generate every AEM-derived output from one committed tree, in a scratch
# extract, and write a sha256 manifest of everything generated.
#
#   gen_outputs.sh <checkout> <rev> <outroot>
#
# <checkout> supplies the three initialised public submodules (copied, never
# symlinked, .git files dropped); <rev> is archived with `git archive`, so the
# lane checkout itself is never written. Outputs land in <outroot>/out and the
# manifest in <outroot>/manifest.sha256.
set -euo pipefail
checkout=$(realpath "$1"); rev=$2; outroot=$(realpath -m "$3")
rm -rf "$outroot"; mkdir -p "$outroot/tree" "$outroot/out"
tree="$outroot/tree"; out="$outroot/out"
git -C "$checkout" archive "$rev" | tar -x -C "$tree"
for sub in protocol-processor gptp-processor third_party/verilog-axis; do
  want=$(git -C "$checkout" rev-parse "$rev:$sub")
  have=$(git -C "$checkout/$sub" rev-parse HEAD)
  [ "$want" = "$have" ] || { echo "submodule $sub at $have, $rev pins $want"; exit 2; }
  rm -rf "${tree:?}/$sub"; mkdir -p "$tree/$sub"
  tar -C "$checkout/$sub" --exclude=.git -cf - . | tar -x -C "$tree/$sub"
done
cd "$tree"
configs=(arty_4x4 arty_8ch arty_current ax7101_1x1_tdm8 ax7101_8x8)
# 1. the shipping descriptor image, exactly as the builder derives it
python3 -B - "$out" "${configs[@]}" <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, "sw/builder")
import endstation_builder as eb
out = Path(sys.argv[1])
for name in sys.argv[2:]:
    cfg = eb.load_config(f"configs/endstation_{name}.yaml")
    ovl = eb.emit_aem_overlay(cfg)
    d = out / "image" / name
    d.mkdir(parents=True)
    (d / "aem_overlay.json").write_text(json.dumps(ovl, indent=1) + "\n")
    for fname, content in eb._entity_model_image(cfg, ovl).items():
        p = d / fname
        p.write_bytes(content) if isinstance(content, bytes) else p.write_text(content)
PY
# 2. the full builder CLI per config
for name in "${configs[@]}"; do
  python3 -B sw/builder/endstation_builder.py "configs/endstation_$name.yaml" \
    -o "$out/builder" > "$out/builder_$name.log"
done
# 3. the store generator CLI: default target, builtin --out-dir, each overlay
python3 -B avdecc/gen_aem_store.py > "$out/gen_default.log"
cp avdecc/aem_rom.json "$out/default_aem_rom.json"
python3 -B avdecc/gen_aem_store.py --out-dir "$out/store/builtin" > "$out/store_builtin.log"
for name in "${configs[@]}"; do
  python3 -B avdecc/gen_aem_store.py --overlay "$out/image/$name/aem_overlay.json" \
    --out-dir "$out/store/$name" > "$out/store_$name.log"
done
# 4. record whether the TRACKED default target equals its regeneration
# (reported, not gated: at ec34fcde it is already 4 bytes stale, see
# preexisting_aem_rom_json_drift.txt)
if git -C "$checkout" show "$rev:avdecc/aem_rom.json" | cmp -s - avdecc/aem_rom.json; then
  echo "tracked avdecc/aem_rom.json: regenerates byte-identical at $rev"
else
  echo "tracked avdecc/aem_rom.json: DIFFERS from its regeneration at $rev"
fi
cd "$out"
find . -type f ! -name '*.log' -print0 | sort -z | xargs -0 sha256sum > "$outroot/manifest.sha256"
echo "$(wc -l < "$outroot/manifest.sha256") generated files hashed for $rev ($(git -C "$checkout" rev-parse "$rev"))"

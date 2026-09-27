#!/usr/bin/env bash
# Build every tracked end-station configuration in two disposable trees (base and
# head) through the builder CLI, then the AEM store and AEM image generators on
# each emitted overlay, and hash every produced file plus any tracked file the
# build touched. Usage: shipping_identity.sh <tree> <outroot> <hashfile>
set -euo pipefail
tree=$1; outroot=$2; hashes=$3
rm -rf "$outroot"; mkdir -p "$outroot"
cd "$tree"
for cfg in $(git ls-files 'configs/endstation_*.yaml'); do
  name=$(basename "$cfg" .yaml)
  python3 -B sw/builder/endstation_builder.py "$cfg" -o "$outroot/builder" > "$outroot/$name.builder.log" 2>&1
  overlay="$outroot/builder/$name/aem_overlay.json"
  test -f "$overlay"
  python3 -B avdecc/gen_aem_store.py --overlay "$overlay" --out-dir "$outroot/store/$name" > "$outroot/$name.store.log" 2>&1
  mkdir -p "$outroot/image/$name"
  python3 -B avdecc/gen_aemi_image.py --overlay "$overlay" -o "$outroot/image/$name/aem_desc.bin" \
    -m "$outroot/image/$name/aem_desc.map" --json "$outroot/image/$name/aem_desc.json" > "$outroot/$name.image.log" 2>&1
  # tracked files the builder may rewrite in the tree (generated svh, fragments)
  mkdir -p "$outroot/tracked/$name"
  git status --porcelain --untracked-files=no | awk '{print $2}' | while read -r f; do
    mkdir -p "$outroot/tracked/$name/$(dirname "$f")"; cp "$f" "$outroot/tracked/$name/$f"; done
  cp hdl/common/gen/adp_shape_defaults.svh "$outroot/tracked/$name/adp_shape_defaults.svh" 2>/dev/null || true
  git checkout -q -- . 2>/dev/null || true
done
(cd "$outroot" && find builder store image tracked -type f -print0 | sort -z | xargs -0 sha256sum) > "$hashes"
wc -l < "$hashes"

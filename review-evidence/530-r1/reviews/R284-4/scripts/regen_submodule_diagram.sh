#!/usr/bin/env bash
# Regenerate the submodule diagram in a review clone, compare against the
# committed artifacts, render each parent's SVG, then restore exact head bytes.
# Usage: regen_submodule_diagram.sh <clone> <merge> <parent1> <parent2>
set -u
C=$1; M=$2; P1=$3; P2=$4
cd "$C" || exit 2
S=$(mktemp -d)
for f in drawio svg png; do cp docs/diagrams/submodule_boundaries.$f "$S/committed.$f"; done
cp docs/diagrams/PNG_MANIFEST.json "$S/committed.manifest.json"
python3 docs/diagrams/submodule_boundaries.gen.py; echo "regen rc=$?"
for f in drawio svg; do cmp -s "$S/committed.$f" docs/diagrams/submodule_boundaries.$f && echo "$f: byte-identical to regeneration" || echo "$f: DIFFERS from regeneration"; done
cmp -s "$S/committed.png" docs/diagrams/submodule_boundaries.png && echo "png: byte-identical" || echo "png: bytes differ (compression may vary)"
cmp -s "$S/committed.manifest.json" docs/diagrams/PNG_MANIFEST.json && echo "manifest: byte-identical to regeneration" || { echo "manifest: DIFFERS"; diff "$S/committed.manifest.json" docs/diagrams/PNG_MANIFEST.json; }
python3 - "$S" <<'PY'
import sys; sys.path.insert(0,'scripts')
from pathlib import Path
from png_artifact import inspect_png
S=Path(sys.argv[1])
a=inspect_png(S/'committed.png'); b=inspect_png(Path('docs/diagrams/submodule_boundaries.png'))
print('committed raster', a.raster_sha256, a.width, a.height, a.text if hasattr(a,'text') else '')
print('regenerated raster', b.raster_sha256, b.width, b.height)
print('raster equal:', a.raster_sha256==b.raster_sha256)
PY
# renderer identity: render each parent's committed SVG, compare to its committed raster
for P in "$P1" "$P2"; do
  git show "$P:docs/diagrams/submodule_boundaries.svg" > "$S/p.svg"
  git show "$P:docs/diagrams/submodule_boundaries.png" > "$S/p.png"
  rsvg-convert -b white -w 2400 "$S/p.svg" -o "$S/r.png"
  python3 - "$S" "$P" <<'PY'
import sys; sys.path.insert(0,'scripts')
from pathlib import Path
from png_artifact import inspect_png
S=Path(sys.argv[1]); a=inspect_png(S/'p.png'); b=inspect_png(S/'r.png')
print('parent', sys.argv[2][:10], 'recorded raster == local render:', a.raster_sha256==b.raster_sha256)
PY
done
git checkout -- docs/diagrams/
git status --porcelain; echo "restore done"
rm -rf "$S"

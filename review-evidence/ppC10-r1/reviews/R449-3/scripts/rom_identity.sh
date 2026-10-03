#!/usr/bin/env bash
# Regenerate every ROM (ucode.hex, ltn_rom.hex, two descriptor images + maps)
# at the base, both merge parents and the head; print sha256 per revision.
# usage: rom_identity.sh <repo> <scratchdir>
set -euo pipefail
repo=$1; sc=$2
for rev in f4167536d358c996f4e1b70b875879c1651f85d3 b6f17f22426fb6362c41a2faf839735c455a8651 \
           c4cb84ff 39298e03aa53d5f82c7485b8d12d2b69a47b0d55; do
  d="$sc/rom/$rev"; rm -rf "$d"; mkdir -p "$d/src" "$d/out"
  git -C "$repo" archive "$rev" hdl | tar -x -C "$d/src"
  ( cd "$d/src/hdl/aecp/ucode" && python3 -B gen_ucode.py -o "$d/out/ucode.hex" >/dev/null )
  ( cd "$d/src/hdl/acmp/rom" && python3 -B gen_ltn_rom.py -o "$d/out/ltn_rom.hex" >/dev/null )
  ( cd "$d/src/hdl/aecp/desc" &&
    python3 -B gen_desc_image.py --no-lint -i example_milan_8.json -o "$d/out/example_milan_8.bin" -m "$d/out/example_milan_8.map" >/dev/null &&
    python3 -B gen_desc_image.py -i milan_min.json -o "$d/out/milan_min.bin" -m "$d/out/milan_min.map" >/dev/null )
  echo "== $(git -C "$repo" rev-parse --short=8 "$rev")"
  ( cd "$d/out" && sha256sum * )
done

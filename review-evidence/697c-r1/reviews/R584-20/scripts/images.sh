#!/usr/bin/env bash
# images.sh <tree> <outdir>
# Link the standalone control image of one tree at every shipped shape with the
# pinned RV32 SDK (MILAN_RV32_CC) and write <outdir>/MANIFEST
# (sha256  size  variant), one line per linked ELF. Run it on two trees and
# compare the manifests. The 60 runtime variants (ctrl_srp_image.py) need
# runtime archives built from external sources and are not linked here.
set -u
tree=$1; out=$2
mkdir -p "$out"
cd "$tree" || exit 2
shapes=$(ls configs/*.yaml | xargs -n1 basename | sed 's/\.yaml$//')
fail=0
for shape in $shapes; do
  python sw/firmware/ctrl/test/ctrl_image.py --shape "$shape" --out "$out/standalone/$shape" \
    > "$out/standalone-$shape.log" 2>&1 || { echo "FAIL standalone $shape"; fail=1; }
done
: > "$out/MANIFEST"
for shape in $shapes; do
  found=$(find "$out/standalone/$shape" -name ctrl_app.elf)
  [ "$(printf '%s\n' "$found" | grep -c .)" = 1 ] || { echo "standalone $shape: expected one ELF, got: $found"; fail=1; continue; }
  printf '%s  %s  %s\n' "$(sha256sum "$found" | cut -d' ' -f1)" "$(stat -c %s "$found")" "standalone/$shape" >> "$out/MANIFEST"
done
cat "$out/MANIFEST"
echo "elfs=$(wc -l < "$out/MANIFEST") manifest_sha256=$(sha256sum "$out/MANIFEST" | cut -d' ' -f1)"
exit $fail

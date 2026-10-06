#!/bin/sh
# R506-2: build klj2_boundary_probe.c against a checkout's nvm_klj2.c, as shipped and with the
# guard `pos + NVM_REC_HDR > loaded` turned into `>=`, both under AddressSanitizer, and run them.
# Usage: klj2_boundary_probe.sh <checkout> <gen dir holding nvm_shape_gen.h> <work dir>
# (the gen dir is any shape's suite/gen from a gate run, e.g. fw_coverage.py --check --keep DIR)
set -u
S=$1/sw/firmware/ctrl_nvm; G=$2; W=$3; HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$W"
cp "$S/nvm_klj2.c" "$W/orig.c"
sed 's/if (pos + NVM_REC_HDR > loaded)/if (pos + NVM_REC_HDR >= loaded)/' "$S/nvm_klj2.c" > "$W/ge.c"
diff "$W/orig.c" "$W/ge.c"
for v in orig ge; do
  gcc -std=c11 -g -O0 -fsanitize=address -I"$S" -I"$G" "$HERE/klj2_boundary_probe.c" "$W/$v.c" -o "$W/$v" || exit 2
done
for v in orig ge; do echo "== $v boundary"; "$W/$v"; done
echo "== orig asan"; "$W/orig" asan; echo "asan rc=$?"

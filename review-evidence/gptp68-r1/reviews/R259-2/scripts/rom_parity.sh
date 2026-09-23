#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Regenerate every tracked ROM image from its own revision's generator and
# compare bytes; print SHA-256, real-word count and leg bases.
set -eu
. "$(dirname "$0")/env.sh"
out="$SCRATCH/rom"
mkdir -p "$out"
for rev in base reviewed head; do
  case $rev in base) sha=$BASE_SHA;; reviewed) sha=$REVIEWED_SHA;; head) sha=$HEAD_SHA;; esac
  gen=$(mktemp -d "$SCRATCH/gen.XXXXXX")
  git -C "$CLONE" show "$sha:hdl/ucode/gen_gptp_ucode.py" > "$gen/gen.py"
  for spec in "tb/verilator/engine/gptp_ucode.hex|--clk-hz 2000000 --cease-ms 3000" \
              "tb/tsngen/gptp_ucode.hex|--clk-hz 2000000" \
              "tb/verilator/ucpu/gptp_ucode.hex|" \
              "syn/ooc/work/gptp_ucode.hex|"; do
    path=${spec%%|*}; args=${spec#*|}
    tag=$(echo "$path" | tr '/' '_')
    # shellcheck disable=SC2086
    python3 "$gen/gen.py" $args -o "$out/$rev.$tag" > "$out/$rev.$tag.log"
    git -C "$CLONE" show "$sha:$path" > "$out/$rev.$tag.tracked"
    if cmp -s "$out/$rev.$tag" "$out/$rev.$tag.tracked"; then v=EQUAL; else v=DIFFERENT; fi
    echo "$rev $path [$args] generated=$(sha256sum < "$out/$rev.$tag" | cut -c1-64) $v"
    sed -n '1p' "$out/$rev.$tag.log" | sed 's/^/    /'
    test "$v" = EQUAL
  done
  sed -n '2p' "$out/$rev.tb_verilator_engine_gptp_ucode.hex.log" | tr ' ' '\n' | grep -E '^(SERVO|PDPAIR|SRTO|BECOME)@' | tr '\n' ' ' | sed "s/^/  $rev legs: /"; echo
  rm -rf "$gen"
done
for tag in tb_verilator_engine_gptp_ucode.hex tb_tsngen_gptp_ucode.hex tb_verilator_ucpu_gptp_ucode.hex; do
  n=$(python3 - "$out/base.$tag" "$out/head.$tag" <<'PY'
import sys
a=open(sys.argv[1]).read().split(); b=open(sys.argv[2]).read().split()
print(sum(1 for x,y in zip(a,b) if x!=y))
PY
)
  echo "words differing base->head in $tag: $n"
done

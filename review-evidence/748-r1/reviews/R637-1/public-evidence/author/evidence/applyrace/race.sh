#!/bin/bash
# Two concurrent apply.sh runs on ONE interpreter's site-packages, N trials.
# $1 = a patched venv to copy, $2 = trials, $3 = shared|private
set -u
SRC=$1; N=$2; MODE=$3; W=$(pwd)/$MODE; rm -rf "$W"; mkdir -p "$W"
APPLY=$LANES/748-elab-race/sw/litex/patches/apply.sh
fail=0
for i in $(seq 1 "$N"); do
  rm -rf "$W/a" "$W/b"; cp -a "$SRC" "$W/a"
  if [ "$MODE" = shared ]; then B="$W/a"; else cp -a "$SRC" "$W/b"; B="$W/b"; fi
  PYTHON="$W/a/bin/python3" "$APPLY" > "$W/l0.$i" 2>&1 & p0=$!
  PYTHON="$B/bin/python3" "$APPLY" > "$W/l1.$i" 2>&1 & p1=$!
  wait $p0; r0=$?; wait $p1; r1=$?
  [ $r0 -ne 0 ] || [ $r1 -ne 0 ] && fail=$((fail+1))
  echo "trial $i: rc $r0 $r1"
done
echo "$MODE: $fail of $N trials had a failing leg"

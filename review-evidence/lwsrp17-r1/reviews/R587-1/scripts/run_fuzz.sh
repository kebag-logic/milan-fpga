#!/usr/bin/env bash
# Differential fuzz campaign: base vs head library, both Registrar profiles.
# Usage: run_fuzz.sh <lwSRP checkout> <base lib dir prefix> <scratch> <receipt file> [seeds] [steps]
# <base lib dir prefix>/eq-{OFF,ON}/build-{base,candidate}/libshlan.so must exist
# (they are produced by tests/check_equivalence.py).
set -u
SRC=$(readlink -f "$1"); EQ=$(readlink -f "$2"); SCR=$(readlink -m "$3"); OUT=$(readlink -m "$4")
SEEDS=${5:-60}; STEPS=${6:-400}
HERE=$(dirname "$(readlink -f "$0")")
mkdir -p "$SCR"
: > "$OUT"
for p in OFF ON; do
  for side in base candidate; do
    lib="$EQ/eq-$p/build-$side"
    gcc -std=c11 -O1 -I"$SRC/src/include" -I"$SRC/src" "$HERE/r587_fuzz.c" -o "$SCR/fuzz-$p-$side" \
        -L"$lib" -lshlan -Wl,-rpath,"$lib" || exit 1
  done
done
ETH=(22ea 88f5 88f6)
job() { # profile app mode seed
  local p=$1 app=$2 mode=$3 seed=$4 m=0
  [ "$mode" = tight ] && m=1
  local tag="$p-$app-$mode-$seed"
  "$SCR/fuzz-$p-candidate" "$seed" "$app" "$m" "$STEPS" > "$SCR/$tag.head" 2>&1
  local base=-
  if [ "$mode" = roomy ]; then
    "$SCR/fuzz-$p-base" "$seed" "$app" "$m" "$STEPS" > "$SCR/$tag.base" 2>&1
    base="$SCR/$tag.base"
  fi
  python3 -I "$HERE/r587_fuzz_compare.py" "${ETH[$app]}" "$mode" "$base" "$SCR/$tag.head" > "$SCR/$tag.res" 2>&1
  echo "$tag rc=$? $(head -1 "$SCR/$tag.res")"
}
export -f job
export SCR HERE STEPS
export ETH_LIST="${ETH[*]}"
for p in OFF ON; do for app in 0 1 2; do for mode in roomy tight; do for s in $(seq 1 "$SEEDS"); do
  echo "$p $app $mode $s"; done; done; done; done |
  xargs -P 16 -L 1 bash -c 'ETH=($ETH_LIST); job "$@"' _ | sort > "$OUT"
echo "jobs=$(wc -l < "$OUT") failing=$(grep -vc ' rc=0 ' "$OUT")"

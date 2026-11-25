#!/bin/sh
# usage: follow_ring_make_probe.sh REPO OUTDIR [BASE [HEAD ...]]
# Extracts tb/verilator/follow_ring (with hdl and the shape headers) at the base and at each
# head into OUTDIR, then for each tree (1) records `make -n run`, (2) runs
# `make -j4 --jobserver-style=pipe small-pullin` with VERILATOR=true (no model is built; the
# small_pulls step then fails on the missing model, which is expected) and counts make's
# jobserver warning, and (3) records `make -n exec-pullin-small` (LEG_BUILD empty: must not
# rebuild). Each head's `make -n run` is compared byte for byte with the base's.
set -u
repo=$1; out=$2; shift 2
[ $# -gt 0 ] || set -- 13e6d869d8 9c62539365 b0f2bc1a78
base=$1; mkdir -p "$out"; out=$(cd "$out" && pwd)
for c in "$@"; do
  d="$out/fr-$c"; rm -rf "$d"; mkdir -p "$d"
  git -C "$repo" archive "$c" hdl configs/generated/endstation_ax7101_1x1_tdm8 tb/verilator/follow_ring | tar -x -C "$d"
  (cd "$d/tb/verilator/follow_ring" && make -n run 2>&1 | sed "s#$d#ROOT#g") > "$out/make-n-run.$c.txt"
  (cd "$d/tb/verilator/follow_ring" && rm -rf obj_dir_fine && make -j4 --jobserver-style=pipe small-pullin VERILATOR=true SWEEP_JOBS=1 2>&1 | sed "s#$d#ROOT#g") > "$out/small-pullin-pipe.$c.txt"
  if (cd "$d/tb/verilator/follow_ring" && make -n exec-pullin-small >/dev/null 2>&1); then
    (cd "$d/tb/verilator/follow_ring" && make -n exec-pullin-small 2>&1 | sed "s#$d#ROOT#g") > "$out/make-n-exec-pullin-small.$c.txt"
    printf '%s: exec-pullin-small rebuild lines (verilator/dp_glue): %s\n' "$c" "$(grep -c -e "verilator --cc" -e "dp_glue.py" "$out/make-n-exec-pullin-small.$c.txt"; true)"
  else
    printf '%s: exec-pullin-small: no such target\n' "$c"
  fi
  printf '%s: jobserver warnings: %s\n' "$c" "$(grep -c 'jobserver unavailable' "$out/small-pullin-pipe.$c.txt")"
done
for c in "$@"; do
  [ "$c" = "$base" ] && continue
  if cmp -s "$out/make-n-run.$base.txt" "$out/make-n-run.$c.txt"; then echo "make -n run $base vs $c: IDENTICAL"
  else echo "make -n run $base vs $c: DIFFERS"; diff "$out/make-n-run.$base.txt" "$out/make-n-run.$c.txt" | cut -c1-160 | head -12; fi
done

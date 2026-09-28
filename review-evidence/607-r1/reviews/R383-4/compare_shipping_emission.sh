#!/usr/bin/env bash
# Emit the shipping AX7101 build Tcl/XDC through #607's real-Builder probe in two exported trees
# (source head and composed candidate) and compare them after path normalisation.
# Usage: compare_shipping_emission.sh <packet> <litex-python> <treeA> <treeB>
set -u
PKT=$1; PY=$2; A=$3; B=$4
OUT=$PKT/receipts/30_emission; mkdir -p "$OUT"
export PATH="$PKT/scratch/bin:$PATH" PYTHONHASHSEED=0
for tree in "$A" "$B"; do
  tag=$(basename "$tree")
  for cfg in ax7101_1x1_tdm8 ax7101_8x8; do
    for port in e1 e2; do
      od="$PKT/scratch/emit-$tag-$cfg-$port"
      ( cd "$tree/sw/litex" && "$PY" -B "$tree/sw/builder/test_shipping_clock_constraints.py" --config $cfg --port $port --output-dir "$od" ) \
        > "$OUT/$tag-$cfg-$port.log" 2>&1
      echo "$tag $cfg $port rc=$? $(grep '^\[constraints\] shipping' "$OUT/$tag-$cfg-$port.log" | sed 's/.*: milan_eth/milan_eth/' | cut -c1-60)"
      for f in alinx_ax7101.tcl alinx_ax7101.xdc; do
        sed -e "s#$tree#<TREE>#g" -e "s#$od#<OUT>#g" "$od/gateware/$f" > "$OUT/$tag-$cfg-$port-$f.norm" 2>/dev/null
      done
    done
  done
done
ta=$(basename "$A"); tb=$(basename "$B")
for cfg in ax7101_1x1_tdm8 ax7101_8x8; do for port in e1 e2; do for f in alinx_ax7101.tcl alinx_ax7101.xdc; do
  if cmp -s "$OUT/$ta-$cfg-$port-$f.norm" "$OUT/$tb-$cfg-$port-$f.norm"; then r=IDENTICAL; else
    if diff <(sort "$OUT/$ta-$cfg-$port-$f.norm") <(sort "$OUT/$tb-$cfg-$port-$f.norm") >/dev/null; then r=SAME-LINES-REORDERED; else r=DIFFERENT; fi; fi
  echo "$cfg $port $f: $r ($(sha256sum < "$OUT/$tb-$cfg-$port-$f.norm" | cut -c1-16))"
done; done; done

#!/usr/bin/env bash
# xvlog -sv analysis, packages first, one module file per invocation, over
# every .sv under <tree>/hdl. Usage: xvlog_all.sh <tree> <work-dir>
# Prints one line per file: XVLOG OK|FAIL <file> [first VRFC error].
set -u
tree=$(readlink -f "$1"); w=$2; rm -rf "$w"; mkdir -p "$w"; cd "$w"
XVLOG=${XVLOG:-xvlog}  # Vivado 2026.1 xvlog
pkgs=$(cd "$tree" && find hdl -name '*_pkg.sv' | sort)
for f in $(cd "$tree" && find hdl -name '*.sv' ! -name '*_pkg.sv' | sort); do
  d="$w/$(echo "$f" | tr / _)"; mkdir -p "$d"
  ( cd "$d" && "$XVLOG" -sv $(for p in $pkgs; do printf '%s ' "$tree/$p"; done) "$tree/$f" > log 2>&1; echo $? > rc )
  if [ "$(cat "$d/rc")" = 0 ]; then echo "XVLOG OK   $f"
  else echo "XVLOG FAIL $f $(grep -m1 "^ERROR" "$d/log" | sed "s|$tree/||g")"; fi
done

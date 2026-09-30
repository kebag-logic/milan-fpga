#!/usr/bin/env bash
# For every tb/<suite>, list whether its directory or any HDL file it names differs from each parent.
# A suite whose inputs equal a parent head byte for byte inherits that parent's gate result.
# Usage: 60-suite-inputs.sh <repo>
set -euo pipefail
cd "${1:?}"
H=47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346; L=921fff59d6e1243284e477f7a368173018420d35; M=0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff
for d in tb/*/; do
  s=$(basename "$d"); [ -f "$d/Makefile" ] || continue
  hdl=$(grep -oE '[A-Za-z0-9_/.]*\.(sv|svh)' "$d/Makefile" | sed -E 's#^(\.\./)+##; s#^\$\(HDL\)/#hdl/#' | grep '^hdl/' | sort -u || true)
  paths="$d scripts $hdl"
  eqL=yes; eqM=yes
  git diff --quiet $L $H -- $paths || eqL=no
  git diff --quiet $M $H -- $paths || eqM=no
  echo "$s inputs==lane:$eqL inputs==main:$eqM"
done

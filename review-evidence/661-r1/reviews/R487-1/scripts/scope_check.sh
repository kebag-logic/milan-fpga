#!/usr/bin/env bash
# List what the PR range changes in parent RTL, firmware, SoC and constraint paths, and the processor top's
# port/parameter declaration lines between the two pins.
# Usage: scope_check.sh <repo> <base> <head>
set -eu
repo=$1; base=$2; head=$3; cd "$repo"
echo "## parent files changed in RTL/firmware/SoC/constraint/tb-RTL paths"
git diff --name-status "$base" "$head" -- 'hdl/' 'sw/firmware/' 'sw/litex/' '*.sv' '*.v' '*.svh' '*.xdc' '*.c' '*.h' | sed 's/^/  /'
echo "## sw/litex/milan_soc.py change (function scope)"
git diff -U0 "$base" "$head" -- sw/litex/milan_soc.py | grep '^@@' | sed 's/^/  /'
old=$(git ls-tree "$base" protocol-processor | awk '{print $3}'); new=$(git ls-tree "$head" protocol-processor | awk '{print $3}')
echo "## processor gitlink $old -> $new"
echo "## protocol_processor_top.sv added/removed port or parameter lines"
git -C protocol-processor diff "$old" "$new" -- hdl/top/protocol_processor_top.sv \
  | grep -E '^[-+][[:space:]]*(input|output|inout|parameter)\b' | sed 's/^/  /' || true
echo "## KL_pp_shadow instantiation of protocol_processor_top unchanged:"
git diff --quiet "$base" "$head" -- hdl/milan/KL_pp_shadow.sv && echo "  KL_pp_shadow.sv identical"

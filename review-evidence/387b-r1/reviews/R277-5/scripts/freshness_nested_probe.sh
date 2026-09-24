#!/bin/sh
# R277-5 reviewer probe: gmstep_mutants.is_fresh() for BOTH positive legs
# (gmstep -> obj_gmstep, option-off -> obj_dir), evaluated inside a parent
# `make -C` recipe (no -s, and an explicit -w parent), under a given GNU make.
# Cases per leg:
#   fresh     - the built binary as the recipe left it: expect True
#   src-newer - one RTL file of print-srcs (not the harness, not the Makefile)
#               made newer than the binary: expect False (proves the SRCS list
#               is actually parsed, not just the two always-added inputs)
# Only mtimes are touched, and each is restored; no byte changes.
#   usage: freshness_nested_probe.sh <repo-root with obj_gmstep and obj_dir built> <make-binary>
set -eu
ROOT=$(cd "$1" && pwd); MAKEBIN=$2
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
mkdir -p "$W/bin"; ln -s "$MAKEBIN" "$W/bin/make"
D=$ROOT/tb/verilator/milan_dp
RTL=$ROOT/hdl/ieee1722/avtp/KL_media_clock_restart.sv
# the probed RTL file must be in print-srcs, or the src-newer case proves nothing
(cd "$D" && PATH="$W/bin:$PATH" make --no-print-directory -s print-srcs) | tr ' ' '\n' \
  | grep -q 'hdl/ieee1722/avtp/KL_media_clock_restart.sv$' \
  || { echo "probe setup: RTL file not in print-srcs"; exit 2; }
cat > "$W/wrap.mk" <<MK
t:
	cd $D && for leg in gmstep option-off; do python3 -c 'import sys, gmstep_mutants as g; l = g.LEGS[sys.argv[1]]; print(sys.argv[1], sys.argv[2], "is_fresh:", g.is_fresh(l, l.clean_mdir / l.exe_name))' \$\$leg "\$(CASE)"; done
MK
"$W/bin/make" --version | head -1
for parent in "" "-w"; do
  echo "== parent: make $parent -C (recipe runs the runner's freshness check)"
  PATH="$W/bin:$PATH" make $parent -C "$W" -f "$W/wrap.mk" t CASE=fresh
  cp -p "$RTL" "$W/mtime_ref"                     # keep the original mtime
  touch -d '+1 hour' "$RTL"
  PATH="$W/bin:$PATH" make $parent -C "$W" -f "$W/wrap.mk" t CASE=src-newer || true
  touch -r "$W/mtime_ref" "$RTL"                  # restore it
  PATH="$W/bin:$PATH" make $parent -C "$W" -f "$W/wrap.mk" t CASE=fresh-again
done

#!/bin/sh
# R277-4 reviewer probe: evaluate gmstep_mutants.is_fresh() for the clean
# gmstep leg when the runner is started from a recipe of a parent `make -C`,
# as the sweep starts it, under a given GNU make.
#   usage: repro_gmstep_freshness.sh <repo-root with a built obj_gmstep> <make-binary>
# Prints the first print-srcs tokens and the freshness verdict.
set -eu
ROOT=$(cd "$1" && pwd); MAKEBIN=$2
W=$(mktemp -d); trap 'rm -rf "$W"' EXIT
mkdir -p "$W/bin"; ln -s "$MAKEBIN" "$W/bin/make"
D=$ROOT/tb/verilator/milan_dp
cat > "$W/wrap.mk" <<MK
t:
	cd $D && python3 -c 'import subprocess, gmstep_mutants as g; l = g.LEGS["gmstep"]; o = subprocess.run(["make", "-s", "-C", str(g.HERE), "print-srcs"], capture_output=True, text=True); print("print-srcs first tokens:", o.stdout.split()[:3]); print("is_fresh:", g.is_fresh(l, l.clean_mdir / l.exe_name))'
MK
"$W/bin/make" --version | head -1
echo "direct run (no parent make):"
(cd "$D" && PATH="$W/bin:$PATH" python3 -c 'import gmstep_mutants as g; l = g.LEGS["gmstep"]; print("is_fresh:", g.is_fresh(l, l.clean_mdir / l.exe_name))')
echo "inside a parent make -C recipe (parent without -s, as the hosted log shows):"
PATH="$W/bin:$PATH" make -C "$W" -f "$W/wrap.mk" t  # no -s: the sweep parent prints its directory

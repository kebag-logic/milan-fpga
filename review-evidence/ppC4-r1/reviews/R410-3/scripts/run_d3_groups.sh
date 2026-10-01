#!/usr/bin/env bash
# R410-3: run tb/pp_top/d3_mutants.py in full at the head, in bounded groups
# (each group repeats its suites' goldens).  run_d3_groups.sh TREE VBIN OUT GROUP
#   GROUP: small (every acmp_nvm and rx_validator mutant) or ppN (the N-th
#   slice of 16 tb/pp_top mutants, N = 0..4)
set -uo pipefail
tree=$1; vbin=$2; out=$3; group=$4
export PATH="$vbin:$PATH" TMPDIR="${R410_TMP:?set R410_TMP}"; mkdir -p "$TMPDIR" "$out"
cd "$tree" || exit 2
names=$(python3 - "$group" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("d3", "tb/pp_top/d3_mutants.py")
m = importlib.util.module_from_spec(spec); sys.modules["d3"] = m; spec.loader.exec_module(m)
g = sys.argv[1]
if g == "small":
    sel = [x.name for x in m.MUTANTS if x.suite.directory != "tb/pp_top"]
else:
    pp = [x.name for x in m.MUTANTS if x.suite.directory == "tb/pp_top"]
    n = int(g[2:]); sel = pp[16 * n:16 * (n + 1)]
print(" ".join(sel))
PY
)
t0=$(date +%s)
# shellcheck disable=SC2086
taskset -c 0-7 python3 tb/pp_top/d3_mutants.py --output "$out/d3_$group" --verilator "$vbin/verilator" --jobs 8 --only $names > "$out/d3_$group.log" 2>&1
rc=$?
echo "d3_$group rc=$rc wall=$(( $(date +%s) - t0 ))s n=$(echo $names | wc -w)" | tee -a "$out/rc-summary.txt"
tail -1 "$out/d3_$group.log" | tee -a "$out/rc-summary.txt"

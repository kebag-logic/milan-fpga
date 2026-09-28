#!/usr/bin/env bash
# Run reviewer probe cases (probe_cases.hpp) inside a disposable export of
# SRC_CLONE HEAD, at head RTL and under selected single mutations.
# Usage: run_probe_cases.sh SRC_CLONE SCRATCH VERILATOR OUT
set -uo pipefail
src=$1; scratch=$2; vl=$3; out=$4
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$scratch" "$out"
mk() {  # name, python-replacement-or-empty
  t="$scratch/$1"; rm -rf "$t"; mkdir -p "$t"
  git -C "$src" archive HEAD | tar -x -C "$t"
  cp "$here/probe_cases.hpp" "$t/tb/acmp_talker/probe_cases.hpp"
  python3 - "$t" "$2" <<'PY'
import sys, pathlib
t = pathlib.Path(sys.argv[1]); mut = sys.argv[2]
cpp = t / "tb/acmp_talker/sim_main.cpp"; s = cpp.read_text()
s = s.replace('#include "retry_cases.hpp"\n', '#include "retry_cases.hpp"\n#include "probe_cases.hpp"\n', 1)
s = s.replace('  check_retry_cases();\n  return report();', '  check_retry_cases();\n  run_reviewer_probes(checks, fails);\n  return report();', 1)
cpp.write_text(s)
if mut:
    old, new = mut.split("=>")
    old = old.encode().decode("unicode_escape"); new = new.encode().decode("unicode_escape")
    rtl = t / "hdl/acmp/KL_acmp_talker.sv"; r = rtl.read_text()
    assert r.count(old) == 1, ("anchor", r.count(old))
    rtl.write_text(r.replace(old, new))
PY
  ( cd "$t/tb/acmp_talker" && make VERILATOR="$vl" ) > "$out/probe-$1.log" 2>&1
  echo "$1 rc=$? $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/probe-$1.log" | tail -1)"
  grep '^FAIL: P' "$out/probe-$1.log" | head -8 | sed 's/^/    /'
  rm -rf "$t"
}
{
echo "head $(git -C "$src" rev-parse HEAD)"
mk head ""
mk init_elig_no_avail "|| (maap_avail_w && |init_ready_w));=>|| |init_ready_w);"
mk no_conflict_wait_clear "|| !en_q_r[i] || set_conflict_w[i])=>|| !en_q_r[i])"
mk no_probe_initset "    if ((state_r == S_TXN_ACT) && txn_initset_w) set_init_w[tsrc_w]   = 1'b1;\n=>"
mk no_lsn_initset "          ev_initset_w = 1'b1;    // a listener appeared: retry allocation=>"
mk no_backoff_exit_initset "            ev_initset_w     = 1'b1;   // re-allocate, then re-declare=>"
} | tee "$out/summary-probes.txt"

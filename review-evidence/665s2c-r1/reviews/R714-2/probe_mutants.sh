#!/bin/sh
# Disposable source mutants against the exact-head harness self-test and the SoC option test.
# Usage: probe_mutants.sh <scratch dir holding base/ (git archive of the head)> <python with LiteX> <receipt dir>
set -u
S=$1; PY=$2; R=$3; C=${4:?clone with submodules}
# The archive has no submodule trees; the SoC option test reads them, so link the clone's read-only.
for sm in protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
  [ -e "$S/base/$sm/.git" ] || { rmdir "$S/base/$sm" 2>/dev/null; ln -sfn "$C/$sm" "$S/base/$sm"; }
done
mut() { # name file old new
  d=$S/m-$1; rm -rf "$d"; cp -a "$S/base" "$d"
  python3 -I - "$d/$2" "$3" "$4" <<'PYEOF'
import sys; p, old, new = sys.argv[1:]; s = open(p).read(); assert s.count(old) == 1, (p, old, s.count(old)); open(p, 'w').write(s.replace(old, new))
PYEOF
}
mut bas_xip tb/verilator/ctrl_service_budget/run.py "spec.get('xip', False))" "False)"
mut bas_default tb/verilator/ctrl_service_budget/run.py "spec.get('fetch_l1', 'none')" "spec.get('fetch_l1', 'split')"
mut bld_fetch tb/verilator/ctrl_service_budget/build.py "rom_elf, n_if, core.cpu_regions, core.fetch_l1)" "rom_elf, n_if, core.cpu_regions, 'split')"
mut sel_xip tb/verilator/ctrl_service_budget/run.py "args.variant, args.fetch_l1, args.xip" "args.variant, args.fetch_l1, False"
mut soc_call sw/litex/milan_soc.py "ctrl_cpu_args(CTRL_FETCH_L1))))" "ctrl_cpu_args((128, 1)))))"
for m in base m-bas_xip m-bas_default m-bld_fetch m-sel_xip; do
  ( cd "$S/$m" && python3 -B tb/verilator/ctrl_service_budget/run.py --self-test > "$R/probe-selftest-$m.log" 2>&1; echo $? > "$R/probe-selftest-$m.rc" ) &
done
for m in base m-soc_call; do
  ( cd "$S/$m" && "$PY" -B sw/builder/test_soc_options.py > "$R/probe-socopt-$m.log" 2>&1; echo $? > "$R/probe-socopt-$m.rc" ) &
done
wait

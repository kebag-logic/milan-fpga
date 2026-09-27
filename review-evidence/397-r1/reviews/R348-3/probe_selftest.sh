#!/bin/sh
# Disposable self-test probes on a copy of the candidate tree. Usage: probe_selftest.sh <clone> <scratch>
# Each probe copies the candidate, plants one fault, runs the unchanged self-test and records rc.
set -u
R=$1; S=$2; B=$S/probe-base
rm -rf "$B"; mkdir -p "$B"
git -C "$R" archive HEAD | tar -x -C "$B"
run() { name=$1; out=$S/probe-$name.log
  ( cd "$B" && timeout 900 python3 -B tb/verilator/fw_service_budget/run.py --self-test ) > "$out" 2>&1
  printf '%s rc=%s last=%s\n' "$name" "$?" "$(tail -n 1 "$out")"; }
F=sw/firmware/milan_baremetal/milan_baremetal.c
run control
cp "$B/$F" "$S/fw.orig"
printf '\ndefine_command(milan_extra, milan_status_handler, "probe", 0);\n' >> "$B/$F"
run extra-command
cp "$S/fw.orig" "$B/$F"
cp "$B/tb/verilator/fw_service_budget/run.py" "$S/run.orig"
sed -i 's/row\[.period_bound_margin_ms.\] = 500 - /row["period_bound_margin_ms"] = 900 - /' "$B/tb/verilator/fw_service_budget/run.py"
grep -c '900 - ' "$B/tb/verilator/fw_service_budget/run.py"
run period-budget-900
cp "$S/run.orig" "$B/tb/verilator/fw_service_budget/run.py"
run control-restored

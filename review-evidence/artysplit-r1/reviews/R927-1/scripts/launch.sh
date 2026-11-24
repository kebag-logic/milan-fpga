#!/usr/bin/env bash
# Start the review campaigns concurrently, each with its own log and rc file.
# usage: launch.sh <packet-dir>
set -u
P=$1
S=$P/scratch
H=$S/work-head
B=$S/work-base
R=$P/receipts/raw
V=${VERILATOR:-verilator}   # the pinned Verilator 5.050
mkdir -p "$R"
LITEX=$(ls -d "$HOME"/litex-milan/{litex,migen,litex-boards,liteeth,litespi,litedram,litei2c,litescope,pythondata-cpu-vexiiriscv,pythondata-software-picolibc,pythondata-software-compiler_rt} 2>/dev/null | paste -sd:)

job() {  # name, dir, command...
    local name=$1 dir=$2; shift 2
    ( cd "$dir" && "$@" ) > "$R/$name.log" 2>&1
    echo $? > "$R/$name.rc"
}

job probe-mii-clean "$H" python3 -I "$P/scripts/mii_guard_probe.py" "$H" "$S/probe-clean" clean &
job probe-mii-noguard "$H" python3 -I "$P/scripts/mii_guard_probe.py" "$H" "$S/probe-noguard" noguard &
job probe-mii-forcedten "$H" python3 -I "$P/scripts/mii_guard_probe.py" "$H" "$S/probe-forcedten" forcedten &
job probe-mii-forcedten-noguard "$H" python3 -I "$P/scripts/mii_guard_probe.py" "$H" "$S/probe-fng" forcedten-noguard &
job arty-grade "$H" python3 -I tb/verilator/ctrl_service_budget/arty_grade.py &
job arty-grade-selftest "$H" python3 -I tb/verilator/ctrl_service_budget/arty_grade.py --selftest &
job service-selftest "$H" python3 tb/verilator/ctrl_service_budget/selftest.py &
job ax-identity "$P" bash "$P/scripts/ax_identity.sh" "$B" "$H" "$S/identity" &
job gptp-txts-latw "$H/tb/verilator/gptp_txts" make VERILATOR="$V" run-latw &
job gptp-shadow "$H/tb/verilator/gptp_shadow" make VERILATOR="$V" &
job timing-grade "$H" env PYTHONPATH="$LITEX" python3 sw/builder/test_timing_grade.py &
wait
echo ALL-DONE > "$R/launch.done"

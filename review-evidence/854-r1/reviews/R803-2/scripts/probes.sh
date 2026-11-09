#!/usr/bin/env bash
# probes.sh <clean-copy-a> <clean-copy-b> <receipts> <verilator>
#  probe_rxfilt0_control: the base leg built with RXFILT=0 (rx_mac_filter pruned), [DR] alone, unmodified sources.
#  probe_counts_runts_filtered: the counts-runts plant (last_kept_r also set at FW_HEAD0) in copy b, built in the
#  default filtered leg (RXFILT=1); [DR] passing there shows the arm is equivalent in the suite's builds.
set -u
a=$1; b=$2; out=$3; V=$4
python3 - "$b/hdl/milan/KL_pp_shadow.sv" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1]); t = p.read_text()
old = "      last_kept_r <= (fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w);\n"
new = "      last_kept_r <= (fw_S == FW_BODY) || ((fw_S == FW_HEAD1) && accept_w) || (fw_S == FW_HEAD0);\n"
assert t.count(old) == 1; p.write_text(t.replace(old, new))
PY
( cd "$a/tb/verilator/pp_shadow" && make --no-print-directory build-base exec-base VERILATOR="$V" VERILATOR_JOBS=4 RXFILT=0 BUILD_DIR=obj_rxfilt0 SIM_ARGS=--drops-only > "$out/probe_rxfilt0_control.log" 2>&1; echo $? > "$out/probe_rxfilt0_control.rc" ) &
( cd "$b/tb/verilator/pp_shadow" && make --no-print-directory build-base exec-base VERILATOR="$V" VERILATOR_JOBS=4 RXFILT=1 BUILD_DIR=obj_p2 SIM_ARGS=--drops-only > "$out/probe_counts_runts_filtered.log" 2>&1; echo $? > "$out/probe_counts_runts_filtered.rc" ) &
wait

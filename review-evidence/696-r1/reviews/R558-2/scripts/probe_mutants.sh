#!/usr/bin/env bash
# Reviewer probes on the new M5 link-loss check. Each probe is one exact source
# replacement written to a scratch copy of KL_maap.sv (the checkout is not
# edited), built with the MAAP harness, and must fail the named M5 check.
# Usage: probe_mutants.sh <tree>   (VERILATOR must name the pinned binary)
set -u
T=$1
RTL=$T/hdl/ieee1722/maap/KL_maap.sv
W=$T/probe_work
mkdir -p "$W"
CHECK='M5 B.3.5.9 link loss is no event; return reprobes'
fails=0
probe() {  # name anchor replacement
    local name=$1
    python3 -I - "$RTL" "$W/$name.sv" "$2" "$3" <<'EOF' || { echo "[ANCHOR] $name"; fails=$((fails+1)); return; }
import sys
src = open(sys.argv[1]).read()
anchor, repl = sys.argv[3], sys.argv[4]
if src.count(anchor) != 1:
    sys.exit(f"anchor count {src.count(anchor)}")
open(sys.argv[2], "w").write(src.replace(anchor, repl))
EOF
    make -s -C "$T/tb/verilator/maap" build MAAP_RTL="$W/$name.sv" MDIR="$W/obj_$name" \
        VERILATOR="$VERILATOR" VERILATOR_JOBS=4 > "$W/$name.build.log" 2>&1 \
        || { echo "[BUILD-FAIL] $name"; fails=$((fails+1)); return; }
    "$W/obj_$name/VKL_maap_sim" > "$W/$name.run.log" 2>&1
    local rc=$?
    local named=no
    grep -q "\[FAIL\] $CHECK" "$W/$name.run.log" && named=yes
    echo "$name rc=$rc named_check_failed=$named"
    grep '\[FAIL\]' "$W/$name.run.log" | sed 's/^/    /'
    [ "$rc" = 1 ] && [ "$named" = yes ] || fails=$((fails+1))
}
# a restart on both edges (loss and return)
probe both_edges "port_operational_i && !port_operational_r" "port_operational_i != port_operational_r"
# the probe and announce timers freeze while the link is down
probe timers_freeze_on_loss "if (tick_ms_w && timer_ms_r != '0)" "if (tick_ms_w && timer_ms_r != '0 && port_operational_i)"
# link loss releases the claim to IDLE
probe loss_releases "if (!enable_i) state_r <= IDLE_S;" "if (!enable_i || !port_operational_i) state_r <= IDLE_S;"
# transmission is suppressed while the link is down
probe tx_gated_on_loss "else if (timer_ms_r == '0 && !tx_busy_r) begin" "else if (timer_ms_r == '0 && !tx_busy_r && port_operational_i) begin"
echo "probes escaped or broken: $fails"
exit $(( fails ? 1 : 0 ))

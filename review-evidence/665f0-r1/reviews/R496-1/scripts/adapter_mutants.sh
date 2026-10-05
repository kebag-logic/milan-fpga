#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# adapter_mutants.sh - reviewer probe for PR #668 (#665 F0).
# Plants AXI4-Lite adapter handshake defects into disposable copies of the
# tree and runs, for each, (a) the mailbox suite's own AXI4-Lite build
# (make run-axil, the 120 checks) and (b) the reviewer stress probe.
# A defect the suite passes is a blind spot of the suite.
# usage: adapter_mutants.sh <clean-tree> <workdir>
set -u
SRC=$(cd "$1" && pwd); W=$2; mkdir -p "$W"
V=${VERILATOR:?set VERILATOR to the pinned Verilator 5.050}
HERE=$(cd "$(dirname "$0")" && pwd)
F=hdl/milan/mailbox/KL_mbx_axil.sv
declare -A OLD NEW
OLD[b-dropped-without-bready]='        BRESP_S: if (s_bready_i) st_r <= IDLE_S;'
NEW[b-dropped-without-bready]='        BRESP_S: st_r <= IDLE_S;'
OLD[r-dropped-without-rready]='        RRESP_S: if (s_rready_i) st_r <= IDLE_S;'
NEW[r-dropped-without-rready]='        RRESP_S: st_r <= IDLE_S;'
OLD[read-taken-beside-write]='  assign take_r_w = (st_r == IDLE_S) \&\& !take_w_w \&\& s_arvalid_i;'
NEW[read-taken-beside-write]='  assign take_r_w = (st_r == IDLE_S) \&\& s_arvalid_i;'
OLD[write-without-w]='  assign take_w_w = (st_r == IDLE_S) \&\& s_awvalid_i \&\& s_wvalid_i;'
NEW[write-without-w]='  assign take_w_w = (st_r == IDLE_S) \&\& s_awvalid_i;'
run_one() {
    local m=$1 t=$W/$1
    rm -rf "$t"; cp -a "$SRC" "$t"
    sed -i "s|${OLD[$m]}|${NEW[$m]}|" "$t/$F"
    if git -C "$t" diff --quiet -- "$F"; then echo "$m: PROBE-BROKEN (substitution did not apply)"; return; fi
    sed -i 's/--build -j 0/--build -j 4/' "$t/tb/verilator/mbx/Makefile"
    (cd "$t/tb/verilator/mbx" && timeout 900 make run-axil VERILATOR=$V > "$W/$m.suite.log" 2>&1)
    local s; s=$(grep -o 'checks: [0-9]*   failures: [0-9]*' "$W/$m.suite.log" | tail -1)
    bash "$HERE/axil_stress/run.sh" "$t" "$W/$m.stress" > "$W/$m.stress.log" 2>&1
    local p; p=$(grep -o 'AXI4-Lite): checks: [0-9]*   failures: [0-9]*' "$W/$m.stress.log")
    echo "$m: suite [${s:-no tally}]  stress [${p:-no tally}]"
}
export -f run_one; export SRC W V HERE F
for m in b-dropped-without-bready r-dropped-without-rready read-taken-beside-write write-without-w; do
    run_one "$m" &
done
wait

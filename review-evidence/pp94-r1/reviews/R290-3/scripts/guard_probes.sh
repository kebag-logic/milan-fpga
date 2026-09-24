#!/usr/bin/env bash
# Portable probe script: guard suite, baseline, hold mutant, inverted-priority mutant.
# Usage: guard_probes.sh <clone> <packet-dir> <verilator>
set -u
CLONE=$1; PKT=$2; VER=$3
HEAD=2e1675d2d20bbc0bb549b36b9d485b2f9b747d5f
R=$PKT/receipts; S=$PKT/scratch/src
rm -rf "$S"; mkdir -p "$S" "$R"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$S"
T=$S/tb/desc_mem_guard
{ echo "verilator: $($VER --version)"; echo "head: $HEAD"; } > "$R/guard-env.txt"
make -C "$T" run VERILATOR="$VER" > "$R/guard-head.log" 2>&1; echo "guard head make rc=$?" | tee "$R/guard-head.rc"
make -C "$T" baseline VERILATOR="$VER" > "$R/guard-baseline.log" 2>&1; echo "baseline make rc=$?" | tee "$R/guard-baseline.rc"
# Hold mutant via the committed controller (it calls make; put pinned verilator first in PATH)
PATH=$(dirname "$VER"):$PATH python3 "$T/mutate.py" --output "$PKT/scratch/hold-mutant" > "$R/guard-hold-mutant.txt" 2>&1; echo "mutate.py rc=$?" >> "$R/guard-hold-mutant.txt"
cp "$PKT/scratch/hold-mutant/mutant-no-hold.log" "$R/guard-hold-mutant.log"
# Inverted priority: terminal beat clears before acceptance sets.
M=$PKT/scratch/prio-mutant; mkdir -p "$M"
python3 - "$S/hdl/aecp/KL_aecp_desc_mem_guard.sv" "$M/KL_aecp_desc_mem_guard.prio.sv" <<'PY'
import sys
src=open(sys.argv[1]).read()
a="""    end else if (m_req_valid_o && m_req_ready_i) begin
      owed_r <= 1'b1;
    end else if (m_rsp_valid_i && m_rsp_ready_o
                 && (m_rsp_last_i || m_rsp_err_i)) begin
      owed_r <= 1'b0;
    end"""
b="""    end else if (m_rsp_valid_i && m_rsp_ready_o
                 && (m_rsp_last_i || m_rsp_err_i)) begin
      owed_r <= 1'b0;
    end else if (m_req_valid_o && m_req_ready_i) begin
      owed_r <= 1'b1;
    end"""
assert src.count(a)==1, "REFUSED: priority block not found exactly once"
open(sys.argv[2],"w").write(src.replace(a,b))
PY
diff -u "$S/hdl/aecp/KL_aecp_desc_mem_guard.sv" "$M/KL_aecp_desc_mem_guard.prio.sv" > "$R/guard-prio-mutant.diff"
make -C "$T" run VERILATOR="$VER" GUARD_SRC="$M/KL_aecp_desc_mem_guard.prio.sv" OBJ_DIR=obj_prio > "$R/guard-prio-mutant.log" 2>&1; echo "prio mutant make rc=$?" | tee "$R/guard-prio-mutant.rc"
# Clear-only mutant (acceptance ignored when coincident terminal): confirm the new CHECK is the only discriminator
grep -E '^FAIL|checks:' "$R"/guard-*.log

#!/usr/bin/env bash
# M8: give the terminal-beat clear priority over request acceptance (priority swap only).
source "$(dirname "$0")/00_env.sh"
MUT=$PKT/scratch/mut; mkdir -p "$MUT"
G=$TREE/hdl/aecp/KL_aecp_desc_mem_guard.sv
python3 - "$G" "$MUT/M8_clear_priority.sv" <<'PY'
import sys
src = open(sys.argv[1]).read()
old = """    end else if (m_req_valid_o && m_req_ready_i) begin
      owed_r <= 1'b1;
    end else if (m_rsp_valid_i && m_rsp_ready_o
                 && (m_rsp_last_i || m_rsp_err_i)) begin
      owed_r <= 1'b0;
    end"""
new = """    end else if (m_rsp_valid_i && m_rsp_ready_o
                 && (m_rsp_last_i || m_rsp_err_i)) begin
      owed_r <= 1'b0;
    end else if (m_req_valid_o && m_req_ready_i) begin
      owed_r <= 1'b1;
    end"""
assert src.count(old) == 1, "REFUSED: anchor not found exactly once"
open(sys.argv[2], "w").write(src.replace(old, new))
PY
diff -u "$G" "$MUT/M8_clear_priority.sv" > "$RCPT/mut-M8_clear_priority.diff" || true
set +e
make -C "$TREE/tb/desc_mem_guard" run GUARD_SRC="$MUT/M8_clear_priority.sv" OBJ_DIR=obj_M8p > "$RCPT/mut-M8_clear_priority.log" 2>&1
echo "M8_clear_priority rc=$? $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$RCPT/mut-M8_clear_priority.log" | tail -1)" >> "$RCPT/mut-rc.txt"
tail -1 "$RCPT/mut-rc.txt"

#!/usr/bin/env bash
# Reviewer-owned mutation probes over the exact-head export (never the clone).
# Each guard mutant runs the FULL guard suite; M10 runs the product-top suite.
source "$(dirname "$0")/00_env.sh"
MUT=$PKT/scratch/mut; rm -rf "$MUT"; mkdir -p "$MUT"
G=$TREE/hdl/aecp/KL_aecp_desc_mem_guard.sv
mk() { # name  sed-expression   (asserts the edit changed the file)
  local n=$1 e=$2; sed -e "$e" "$G" > "$MUT/$n.sv"
  if cmp -s "$G" "$MUT/$n.sv"; then echo "REFUSED $n: edit did not apply"; exit 3; fi
  diff -u "$G" "$MUT/$n.sv" > "$RCPT/mut-$n.diff" || true; }
mk M1_no_valid_hold  's/assign m_req_valid_o = s_req_valid_i \&\& !owed_r;/assign m_req_valid_o = s_req_valid_i;/'
mk M2_no_ready_hold  's/assign s_req_ready_o = m_req_ready_i \&\& !owed_r;/assign s_req_ready_o = m_req_ready_i;/'
mk M3_last_only      's/(m_rsp_last_i || m_rsp_err_i)/m_rsp_last_i/'
mk M4_ignore_ready   's/m_rsp_valid_i \&\& m_rsp_ready_o/m_rsp_valid_i/'
mk M5_any_beat       's/\&\& (m_rsp_last_i || m_rsp_err_i))/)/'
mk M6_debt_tied0     's/assign debt_o = owed_r;/assign debt_o = 1'"'"'b0;/'
mk M9_never_set      's/owed_r <= 1'"'"'b1;/owed_r <= 1'"'"'b0;/'
: > "$RCPT/mut-rc.txt"
runguard() { local n=$1; set +e
  make -C "$TREE/tb/desc_mem_guard" run GUARD_SRC="$MUT/$n.sv" OBJ_DIR="obj_$n" > "$RCPT/mut-$n.log" 2>&1
  echo "$n rc=$? $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$RCPT/mut-$n.log" | tail -1)" >> "$RCPT/mut-rc.txt"; }
export -f runguard; export MUT TREE RCPT PATH
printf '%s\n' M1_no_valid_hold M2_no_ready_hold M3_last_only M4_ignore_ready M5_any_beat M6_debt_tied0 M9_never_set \
  | xargs -P 4 -I{} bash -c 'runguard {}'
# M7: wrapper wires the store-only reset into the guard (reset-seam mutant).
W=$MUT/M7tree; mkdir -p "$W/tb"; cp -r "$TREE/hdl" "$W/"; cp -r "$TREE/tb/common" "$W/tb/"
mkdir -p "$W/tb/desc_mem_guard"; cp "$TREE"/tb/desc_mem_guard/{Makefile,sim_main.cpp,wrap.sv} "$W/tb/desc_mem_guard/"
sed -i '/u_guard (/,/);/s/\.clk_i(clk_i), \.rst_n(rst_n),/.clk_i(clk_i), .rst_n(rst_n \&\& store_rst_n),/' "$W/tb/desc_mem_guard/wrap.sv"
diff -u "$TREE/tb/desc_mem_guard/wrap.sv" "$W/tb/desc_mem_guard/wrap.sv" > "$RCPT/mut-M7_store_reset_reaches_guard.diff" && { echo "REFUSED M7"; exit 3; }
set +e; make -C "$W/tb/desc_mem_guard" run > "$RCPT/mut-M7_store_reset_reaches_guard.log" 2>&1
echo "M7_store_reset_reaches_guard rc=$? $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$RCPT/mut-M7_store_reset_reaches_guard.log" | tail -1)" >> "$RCPT/mut-rc.txt"
# M10: product top with both request holds deleted (the shipped control's edit), full pp_top suite.
T=$MUT/M10tree; mkdir -p "$T/tb"; cp -r "$TREE/hdl" "$T/"; cp -r "$TREE/tb/common" "$T/tb/"
mkdir -p "$T/tb/pp_top"; (cd "$TREE/tb/pp_top" && tar -c --exclude=obj_dir . ) | tar -x -C "$T/tb/pp_top"
sed -i 's/ && !owed_r//' "$T/hdl/aecp/KL_aecp_desc_mem_guard.sv"
diff -u "$G" "$T/hdl/aecp/KL_aecp_desc_mem_guard.sv" > "$RCPT/mut-M10_pp_top_no_hold.diff" && { echo "REFUSED M10"; exit 3; }
make -C "$T/tb/pp_top" > "$RCPT/mut-M10_pp_top_no_hold.log" 2>&1
echo "M10_pp_top_no_hold rc=$? $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$RCPT/mut-M10_pp_top_no_hold.log" | tail -1)" >> "$RCPT/mut-rc.txt"
sort "$RCPT/mut-rc.txt"

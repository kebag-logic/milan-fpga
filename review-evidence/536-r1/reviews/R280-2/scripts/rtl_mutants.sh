#!/bin/sh
# Two RTL mutants of a disposable pp_top probe copy; each is rebuilt and the
# recorded frames replayed. Expect: nib (only @26's high nibble compared)
# diverges from the model on the C2 row only; len (Figure 5.3 length made
# exact) diverges on the cdl 24 and cdl 112 rows only.
# Usage: rtl_mutants.sh <packet-dir> <verilator>
set -u
P=$1; vl=$2
for arm in nib len; do
  d=$P/scratch/mut_$arm; rm -rf "$d"; cp -a "$P/scratch/pp" "$d"; rm -rf "$d/tb/pp_top/obj_dir"
  f=$d/hdl/aecp/KL_aecp_engine.sv
  case $arm in
    nib) old='pid_lo_r[1] <= (rxs_rd_data_i == MVU_PID_L1_C);'
         new='pid_lo_r[1] <= (rxs_rd_data_i[7:4] == MVU_PID_L1_C[7:4]);';;
    len) old='&& (pld_cmd_r  >= MVU_CMD_PLD_C)'
         new='\&\& (pld_cmd_r  == MVU_CMD_PLD_C)';;
  esac
  n=$(grep -cF "$old" "$f"); [ "$n" = 1 ] || { echo "$arm: anchor count $n"; continue; }
  python3 - "$f" "$old" "$new" <<'PY'
import sys
p, o, n = sys.argv[1], sys.argv[2], sys.argv[3].replace("\\&", "&")
s = open(p).read(); open(p, "w").write(s.replace(o, n, 1))
PY
  grep -n "MVU_PID_L1_C\[7:4\]\|pld_cmd_r  == MVU_CMD_PLD_C" "$f"
  (cd "$d/tb/pp_top" && make VERILATOR="$vl" probe_build > build.log 2>&1) || { echo "$arm build failed"; continue; }
  python3 -B "$P/scripts/rtl_vs_model.py" "$P/receipts/contract_frames_head.jsonl" \
     "$d/tb/pp_top/obj_dir/Vpp_top_sim" "$P/scratch/mut_$arm.cmp" 89 300
  echo "arm $arm exit $?"
  grep MISMATCH "$P/scratch/mut_$arm.cmp.txt" | cut -c1-110
done

#!/bin/sh
# arb_busy_plants.sh TREE SCRATCH VERILATOR : plant tb/tx_arbiter README M6 and M7 in copies
# of TREE and run the arbiter bench on each
set -u
A='  assign busy_o      = (arb_st_r != A_IDLE);'
for m in M6 M7; do
  W="$2/arb-$m"; rm -rf "$W"; cp -a "$1" "$W"; rm -rf "$W/tb/tx_arbiter/obj_dir"
  f="$W/hdl/packet_engine/KL_pp_tx_arbiter.sv"
  [ "$(grep -cF "$A" "$f")" = 1 ] || { echo "$m anchor missing"; continue; }
  case $m in
    M6) sed -i 's/  assign busy_o      = (arb_st_r != A_IDLE);/  assign busy_o      = (arb_st_r == A_STREAM);/' "$f" ;;
    M7) sed -i 's/  assign busy_o      = (arb_st_r != A_IDLE);/  assign busy_o      = (arb_st_r != A_IDLE) \&\& !(ser_valid_i \&\& ser_last_i);/' "$f" ;;
  esac
  grep -n "assign busy_o" "$f"
  make -C "$W/tb/tx_arbiter" VERILATOR="$3" > "$W.log" 2>&1; echo "$m rc=$?"
  grep -E "^FAIL|checks:" "$W.log" | head -12
  rm -rf "$W"
done

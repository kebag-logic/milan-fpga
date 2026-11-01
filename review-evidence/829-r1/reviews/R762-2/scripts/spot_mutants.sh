#!/usr/bin/env bash
# spot_mutants.sh <clean head tree> <work root> <receipts>: independent planted defects on the closed-loop suite.
set -u
H=$1 W=$2 R=$3; mkdir -p "$W" "$R/spot"
TXRET=hdl/ieee8021as/gptp_plane/KL_gptp_txret.sv; OBS=hdl/ieee8021as/gptp_plane/KL_gptp_gmii_launch.sv; SIM=tb/verilator/gptp_txts/sim_main.cpp
NEED='RECON_NEED_CYC_C = TXTS_CORR_NS_P / DP_TICK_NS_P + 15;'
run() { # name target file python-replace-old python-replace-new [file2 old2 new2]
  n=$1 t=$2; shift 2; T=$W/$n; rsync -a --delete --exclude='obj_*' "$H/" "$T/"
  while [ $# -gt 0 ]; do python3 - "$T/$1" "$2" "$3" <<'PY' || { echo "$n ANCHOR MISSING" ; return; }
import sys
p,o,n=sys.argv[1:4]; o=o.encode().decode('unicode_escape'); n=n.encode().decode('unicode_escape')
s=open(p).read(); assert s.count(o)>=1,o; open(p,'w').write(s.replace(o,n))
PY
    shift 3; done
  ( cd "$T/tb/verilator/gptp_txts" && make -s $t > "$R/spot/$n.log" 2>&1; echo $? > "$R/spot/$n.rc" )
}
DEL_OLD='                        oidx_r, gen_r, type_r, seq_r, delta_r,\n                        (delta_r != TXTS_DELTA_W_P\x27(TXTS_DELTA_EXP_P))};'
DEL_NEW='                        oidx_r, gen_r, type_r, seq_r,\n                        TXTS_DELTA_W_P\x27(TXTS_DELTA_EXP_P),\n                        1\x27b0};'
run shipped_mii run-mii &
run guard188_mii run-mii $TXRET "$NEED" 'RECON_NEED_CYC_C = 188;' &
run guard189_mii run-mii $TXRET "$NEED" 'RECON_NEED_CYC_C = 189;' &
run gmii_floor63 run $TXRET 'parameter int unsigned RECON_GUARD_CYC_P = 64,' 'parameter int unsigned RECON_GUARD_CYC_P = 63,' &
run forced_delta_new_check_mii run-mii $OBS "$DEL_OLD" "$DEL_NEW" &
run forced_delta_old_check_mii run-mii $OBS "$DEL_OLD" "$DEL_NEW" $SIM 'records_[target].delta != 45 * kEthCycPerOctet' 'records_[target].delta != 45' &
wait
for f in "$R"/spot/*.rc; do n=$(basename "$f" .rc); echo "== $n rc=$(cat "$f")"; grep -E '^\[FAIL\]|^RESULT|anchor' "$R/spot/$n.log" | sort | uniq -c | cut -c1-150 | head -12; done

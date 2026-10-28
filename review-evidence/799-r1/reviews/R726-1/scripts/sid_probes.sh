#!/usr/bin/env bash
# Reviewer fault probes for the processor #202 Stream ID wiring.
# Each probe writes a MUTATED COPY of hdl/milan/milan_datapath.sv into
# <work>/<name>/ (the tracked file is never edited), builds the sidmove leg
# through the Makefile's own recipe with DP_SRC and SIDMOVE_MDIR overridden,
# runs it, and requires RESULT: FAIL with the named check among the failures.
# usage: sid_probes.sh <milan_dp dir of a clean clone> <work dir> <receipt dir> <probe...>
set -u
MDP=$1; WORK=$2; OUT=$3; shift 3
DP="$MDP/../../../hdl/milan/milan_datapath.sv"
mkdir -p "$WORK" "$OUT"
plant() {   # name old new
  python3 -I - "$DP" "$WORK/$1/milan_datapath.sv" "$2" "$3" <<'EOF'
import sys
src, dst, old, new = sys.argv[1:5]
t = open(src).read()
n = t.count(old)
if n != 1:
    sys.exit(f"anchor found {n} times: {old!r}")
open(dst, "w").write(t.replace(old, new))
EOF
}
run_probe() {   # name expected-failure-substring
  local name=$1 want=$2 log="$OUT/probe_$1.log"
  ( cd "$MDP" && make sidmove-build DP_SRC="$WORK/$name/milan_datapath.sv" \
      SIDMOVE_MDIR="$WORK/$name/obj" > "$log.build" 2>&1 ) || { echo "$name: BUILD FAILED (not a catch)"; return 1; }
  ( cd "$MDP" && "$WORK/$name/obj/Vmilan_dp_sidmove" > "$log" 2>&1 ); local rc=$?
  if grep -q "RESULT: FAIL" "$log" && grep -F "[FAIL]" "$log" | grep -qF "$want"; then
    echo "$name: CAUGHT rc=$rc by \"$want\" ($(grep -c '^\[FAIL\]' "$log") failing checks)"
  else
    echo "$name: SURVIVED rc=$rc"; return 1
  fi
}
fail=0
for p in "$@"; do
  mkdir -p "$WORK/$p"
  case $p in
    gsi_osid)   # GET_STREAM_INFO selector 2 back on the configured ID
      plant $p "wire [63:0] gsi_osid_w  = pp_cd_src_stream_id_w[64*gsi_oix_w +: 64];" \
               "wire [63:0] gsi_osid_w  = pp_src_sid_w[64*gsi_oix_w +: 64];" || { fail=1; continue; }
      run_probe $p "[AFTER]: GET_STREAM_INFO selector 2 is src_stream_id_o" || fail=1 ;;
    crft_csr)   # the CRF output stamps the CSR ID again
      plant $p "assign crft_tx_sid_w = tx_sid_w[64*CRF_TUID_C +: 64];" \
               "assign crft_tx_sid_w = eff_crft_sid_w;" || { fail=1; continue; }
      run_probe $p "[AFTER]: every one carries src_stream_id_o" || fail=1 ;;
    aaf_derive) # the AAF framer derives {MAC, uid} again
      plant $p ".SID_PP_P      (1'b1)) aaf_packetizer (" \
               ".SID_PP_P      (1'b0)) aaf_packetizer (" || { fail=1; continue; }
      run_probe $p "[AFTER]: every one carries src_stream_id_o" || fail=1 ;;
    *) echo "unknown probe $p"; fail=1 ;;
  esac
done
exit $fail

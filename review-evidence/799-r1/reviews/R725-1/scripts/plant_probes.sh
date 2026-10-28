#!/bin/sh
# Plant the reviewer's three disposable wiring probes, one per copy of the
# candidate tree, and refuse if a pattern does not match exactly once.
# Usage: plant_probes.sh <scratch-dir holding mutA mutB mutC>
set -eu
S=$1
plant() { # <tree> <file> <old> <new>
  n=$(grep -cF -- "$3" "$1/$2" || true)
  [ "$n" = 1 ] || { echo "PATTERN COUNT $n in $1/$2: $3" >&2; exit 2; }
  python3 -I - "$1/$2" "$3" "$4" <<'EOF'
import sys
p, old, new = sys.argv[1:4]
t = open(p).read()
open(p, "w").write(t.replace(old, new, 1))
EOF
  echo "planted in $1/$2"
}
DP=hdl/milan/milan_datapath.sv
# A: an output's GET_STREAM_INFO stream_id read from the reset-time ID again
plant "$S/mutA" $DP "wire [63:0] gsi_osid_w  = pp_cd_src_stream_id_w[64*gsi_oix_w +: 64];" \
                    "wire [63:0] gsi_osid_w  = pp_src_sid_w[64*gsi_oix_w +: 64];"
# B: the AAF framers back on the {station MAC, uid} derivation
plant "$S/mutB" $DP ".SID_PP_P      (1'b1)) aaf_packetizer (" \
                    ".SID_PP_P      (1'b0)) aaf_packetizer ("
# C: the CRF Media Clock Output stamping its CSR / reset-time value again
plant "$S/mutC" $DP "assign crft_tx_sid_w = tx_sid_w[64*CRF_TUID_C +: 64];" \
                    "assign crft_tx_sid_w = eff_crft_sid_w;"
for t in mutA mutB mutC; do git -C "$S/$t" diff --stat; done

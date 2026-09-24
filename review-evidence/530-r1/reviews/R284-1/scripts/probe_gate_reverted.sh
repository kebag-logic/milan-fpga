#!/bin/sh
# Item 2 failing arm, independently: in a scratch COPY of the clone, revert
# only the lwsrp_stream_gate line to the raw admission verdict, build the
# unchanged obj_crflic leg and run it; then restore the line. Usage:
#   COPY=/scratch/copy-of-clone VERILATOR=/path/to/verilator-5.050 OUT=/receipts sh probe_gate_reverted.sh
set -eu
: "${COPY:?}" "${VERILATOR:?}" "${OUT:?}"
export VERILATOR VERILATOR_JOBS=8
f="$COPY/hdl/milan/milan_datapath.sv"
old='  assign lwsrp_stream_gate = pp_cd_srp_active_w[SRP_TALKERS_C-1:0];'
new='  assign lwsrp_stream_gate = pp_cd_srp_sr_admitted_w[SRP_TALKERS_C-1:0];'
test "$(grep -cxF "$old" "$f")" = 1
python3 - "$f" "$old" "$new" <<'EOF'
import sys
p, a, b = sys.argv[1:]
s = open(p).read()
open(p, "w").write(s.replace(a, b))
EOF
git -C "$COPY" diff --stat > "$OUT/gate_reverted_identity.txt"
set +e
make -C "$COPY/tb/verilator/milan_dp" crflic CRFLIC_MDIR=obj_probe_gate_reverted > "$OUT/crflic_gate_reverted.log" 2>&1
echo "rc=$?" >> "$OUT/crflic_gate_reverted.log"
set -e
git -C "$COPY" checkout -q -- hdl/milan/milan_datapath.sv
git -C "$COPY" diff --stat >> "$OUT/gate_reverted_identity.txt"

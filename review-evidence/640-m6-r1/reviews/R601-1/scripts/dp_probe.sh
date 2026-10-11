#!/bin/sh
# R601-1 datapath GET_COUNTERS quadlet-map probe.
# Usage: dp_probe.sh <tree> <outdir> <id>
# Plants one defect into a COPY of hdl/milan/milan_datapath.sv, then builds and
# runs ONLY the N=4 sim_nxn leg of tb/verilator/milan_dp through the suite's own
# variables (DP_SRC overridden, a private --Mdir), via a make include that adds
# one target and changes nothing else. Requires the suite's generated inputs
# (ltn_rom.hex, ucode.hex, gen/) to exist from a prior `make` in that tree.
set -u
TREE=$1; OUT=$2; ID=$3
PATH=$VALIDATION_TOOLS/pinned-verilator-5.050:$PATH; export PATH
mkdir -p "$OUT/$ID"
DP="$TREE/hdl/milan/milan_datapath.sv"
M="$OUT/$ID/milan_datapath.sv"
case "$ID" in
  DP-0-clean) cp "$DP" "$M" ;;
  DP-A-tvswap)
    python3 -I - "$DP" "$M" <<'EOF'
import sys
s = open(sys.argv[1]).read()
a = "      6'd6    : mon_diag_col_w = 4'(MON_TV_C);  // @24  TIMESTAMP_VALID\n      6'd7    : mon_diag_col_w = 4'(MON_TNV_C); // @28  TIMESTAMP_NOT_VALID\n"
b = "      6'd6    : mon_diag_col_w = 4'(MON_TNV_C); // @24  TIMESTAMP_VALID\n      6'd7    : mon_diag_col_w = 4'(MON_TV_C);  // @28  TIMESTAMP_NOT_VALID\n"
assert s.count(a) == 1, s.count(a)
open(sys.argv[2], "w").write(s.replace(a, b))
EOF
    ;;
  DP-B-reservedleak)
    python3 -I - "$DP" "$M" <<'EOF'
import sys
s = open(sys.argv[1]).read()
a = "        ctr_col_v_w    = 1'b0;\n"
assert s.count(a) == 1, s.count(a)
open(sys.argv[2], "w").write(s.replace(a, "        ctr_col_v_w    = 1'b1;\n"))
EOF
    ;;
  *) echo "unknown id"; exit 2 ;;
esac
cat > "$OUT/$ID/probe.mk" <<EOF
probe-nxn:
	\$(VERILATOR) \$(SHAPE_4x4) \$(DP_VFLAGS) --Mdir $OUT/$ID/obj -GN_STREAMS=4 \$(SRCS) sim_nxn.cpp -o Vmilan_dp_nxn
	$OUT/$ID/obj/Vmilan_dp_nxn
EOF
diff "$DP" "$M" > "$OUT/$ID/plant.diff"
make -C "$TREE/tb/verilator/milan_dp" -f Makefile -f "$OUT/$ID/probe.mk" probe-nxn \
  VERILATOR=verilator DP_SRC="$M" > "$OUT/$ID/run.log" 2>&1
rc=$?
echo "$rc" > "$OUT/$ID/rc"
echo "$ID rc=$rc fails=$(grep -c '\[FAIL\]\|FAIL:' "$OUT/$ID/run.log")"

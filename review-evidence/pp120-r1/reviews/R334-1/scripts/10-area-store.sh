#!/usr/bin/env bash
# Focused area probe: sv2v + Yosys synth_xilinx (xc7) of KL_aecp_desc_store alone
# at base and head, default parameters; prints the cell statistics and a diff.
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd)
for t in base head; do
  d=$PK/scratch/area-$t; rm -rf $d; mkdir -p $d
  sv2v $PK/scratch/$t/hdl/common/pp_pkg.sv $PK/scratch/$t/hdl/aecp/KL_aecp_desc_store.sv > $d/store.v 2> $d/sv2v.err
  (cd $d && yosys -q -p "read_verilog $d/store.v; synth_xilinx -family xc7 -top KL_aecp_desc_store; tee -o $d/stat.txt stat" > $d/yosys.log 2>&1)
  echo "$t yosys rc=$?"
  awk '/=== KL_aecp_desc_store ===/{f=1} f' $d/stat.txt | sed 's/^ *//' > $PK/receipts/10-area-store-$t.txt
done
diff $PK/receipts/10-area-store-base.txt $PK/receipts/10-area-store-head.txt || true
python3 - $PK/receipts/10-area-store-base.txt $PK/receipts/10-area-store-head.txt <<'P'
import re, sys
def tot(p):
    c = {m.group(2): int(m.group(1)) for m in re.finditer(r"^(\d+)\s+([A-Z][A-Z0-9_]+)$", open(p).read(), re.M)}
    g = lambda pre: sum(v for k, v in c.items() if k.startswith(pre))
    return dict(LUT=g("LUT"), FF=g("FD"), RAMB=g("RAMB"), LUTRAM=g("RAM32M") + g("RAM64M"),
                DSP=g("DSP"), CARRY4=g("CARRY4"), MUXF=g("MUXF"), OBUF=g("OBUF"), IBUF=g("IBUF"))
b, h = tot(sys.argv[1]), tot(sys.argv[2])
for k in b: print(f"{k:7s} base {b[k]:6d} head {h[k]:6d} delta {h[k]-b[k]:+d}")
P

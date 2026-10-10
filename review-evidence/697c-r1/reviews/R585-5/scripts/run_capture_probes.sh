#!/bin/bash
# R585-5 end-to-end probes of the capture-based boundary judgement, in a DISPOSABLE checkout.
# Plants, in sw/firmware/ctrl/adp/adp_mbx.c, an include of the stack's examples/adp_port.h under
# two modes no builder sets, then runs r585_probe_builder.py under ctrl_capture.py so that one
# recorded compile carries the mode (env: on argv; rsp: inside a @response file), and judges the
# base capture plus that capture with the hosted command (no --selftest). Restores the file after.
# Usage: run_capture_probes.sh TREE BASE_CAPTURE OUTDIR SCRIPTS_DIR
set -u
tree=$1; base=$2; out=$3; scripts=$4
mkdir -p "$out"
cd "$tree" || exit 2
f=sw/firmware/ctrl/adp/adp_mbx.c
python3 - "$f" <<'EOF'
import sys
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
anchor = '#include "adp_mbx.h"\n'
assert t.count(anchor) == 1
plant = ('#ifdef CTRL_R585_ENV\n#include "adp_port.h"\n#endif\n'
         '#ifdef CTRL_R585_RSP\n#include "adp_port.h"\n#endif\n')
open(p, "w", encoding="utf-8").write(t.replace(anchor, anchor + plant))
EOF
cp "$scripts/r585_probe_builder.py" sw/firmware/ctrl/test/r585_probe_builder.py
for how in ${PROBES:-env rsp}; do
    cap=$out/capture-$how
    rm -rf "$cap"
    python3 sw/firmware/ctrl/test/ctrl_capture.py --out "$cap" -- python3 ${PYFLAGS:-} sw/firmware/ctrl/test/r585_probe_builder.py "$how" \
        > "$out/builder-$how.log" 2>&1
    echo "builder $how rc=$?" | tee -a "$out/summary.txt"
    grep -c '' "$cap/records.jsonl" | sed "s/^/  records in capture-$how: /" | tee -a "$out/summary.txt"
    python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --capture "$base" --capture "$cap" --without verilator \
        > "$out/gate-$how.log" 2>&1
    rc=$?
    echo "gate $how rc=$rc" | tee -a "$out/summary.txt"
    grep -E "\[FAIL\]|REFUSED|^ctrl_boundary: (PASS|FAIL)|finding\(s\)" "$out/gate-$how.log" | cut -c1-400 | sed 's/^/  /' | tee -a "$out/summary.txt"
done
git checkout -- "$f"
rm -f sw/firmware/ctrl/test/r585_probe_builder.py
git status --porcelain | sed 's/^/  left: /' | tee -a "$out/summary.txt"

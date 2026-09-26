#!/bin/sh
# Disposable Makefile fault probes against test_sim_pool.py's inventory arm,
# on the composed candidate. Each probe edits tb/verilator/milan_dp/Makefile in
# place, runs the suite's unit test, then restores the exact tracked bytes.
# usage: probe_inventory.sh <clone>
C="$1"
D="$C/tb/verilator/milan_dp"
M="$D/Makefile"
want=$(git -C "$C" rev-parse HEAD:tb/verilator/milan_dp/Makefile)
probe() {
    name="$1"; script="$2"
    python3 - "$M" "$script" <<'EOF'
import sys
path, op = sys.argv[1], sys.argv[2]
text = open(path).read()
crf = "\t  ./$(CRFLIC_MDIR)/Vmilan_dp_crflic \\\n"
if op == "drop-crflic":
    assert crf in text
    text = text.replace(crf, "", 1)
elif op == "swap-nxn-nxndv":
    a = "\t  ./obj_nxn/Vmilan_dp_nxn \\\n"
    b = ("\t  --banner \"---- the DIVERGENT shape: input row 1 declares the 96 kHz base ----\" \\\n"
         "\t  ./obj_nxndv/Vmilan_dp_nxndv \\\n")
    assert a + b in text
    text = text.replace(a + b, b + a, 1)
elif op == "crflic-also-sequential":
    anchor = "\t@echo \"---- #386 render law"
    assert anchor in text
    text = text.replace(anchor, "\t./$(CRFLIC_MDIR)/Vmilan_dp_crflic\n" + anchor, 1)
elif op == "new-leg-outside-pool":
    anchor = "\t@echo \"---- #386 render law"
    text = text.replace(anchor, "\t./obj_new/Vmilan_dp_new\n" + anchor, 1)
elif op == "jobs-default-3":
    text = text.replace("SIM_JOBS ?= 2", "SIM_JOBS ?= 3", 1)
else:
    raise SystemExit(f"unknown probe {op}")
open(path, "w").write(text)
EOF
    out=$(cd "$D" && python3 test_sim_pool.py 2>&1); rc=$?
    arm=$(printf '%s\n' "$out" | grep 'arm_the_makefile_hands' | head -1)
    printf 'PROBE %-24s test_rc=%s  %s\n' "$name" "$rc" "$arm"
    git -C "$C" checkout -q -- tb/verilator/milan_dp/Makefile
    got=$(git -C "$C" hash-object "$M")
    [ "$got" = "$want" ] || { echo "RESTORE FAILED"; exit 3; }
}
probe drop-crflic drop-crflic
probe swap-nxn-nxndv swap-nxn-nxndv
probe crflic-also-sequential crflic-also-sequential
probe new-leg-outside-pool new-leg-outside-pool
probe jobs-default-3 jobs-default-3
echo "Makefile restored to $want"

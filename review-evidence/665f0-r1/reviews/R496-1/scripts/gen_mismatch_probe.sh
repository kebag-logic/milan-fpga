#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# gen_mismatch_probe.sh - reviewer probe for PR #668: mismatches planted
# OUTSIDE gen_mailbox.py's own self-test fixtures must still fail its gates.
# Runs in a disposable copy <tree>; restores each file after its arm.
# usage: gen_mismatch_probe.sh <tree>
set -u
cd "$1" || exit 2
fails=0
arm() {  # arm <name> <file> <sed-expr> <gate-args...>
    local name=$1 file=$2 expr=$3; shift 3
    cp "$file" "$file.orig"
    sed -i "$expr" "$file"
    if cmp -s "$file" "$file.orig"; then echo "[PROBE-BROKEN] $name: substitution did not apply"; fails=$((fails+1));
    elif python3 sw/mailbox/gen_mailbox.py "$@" > /tmp/genprobe.$$ 2>&1; then
        echo "[MISSED] $name: gen_mailbox.py $* exited 0"; fails=$((fails+1))
    else
        echo "[caught] $name: $(grep -m1 FAIL /tmp/genprobe.$$)"
    fi
    mv "$file.orig" "$file"
}
# 1 a reference-page LAYOUT row (not the constant table): byte drift
arm "doc layout row offset" docs/reference/MAILBOX_CONTRACT.md 's/^| `0x03C` | `TMR_CMD` |/| `0x038` | `TMR_CMD` |/' --check
# 2 a derived SV width the constant table carries
arm "SV derived MBX_ADDR_W_C" hdl/milan/mailbox/KL_mbx_pkg.sv 's/MBX_ADDR_W_C = 32'"'"'d13/MBX_ADDR_W_C = 32'"'"'d12/' --crosscheck
# 3 a C field LSB of an event word, crosscheck only
arm "C EV_TICK COUNT width" sw/firmware/ctrl/mbx/mbx_contract.h 's/^#define MBX_EV_TICK_W1_COUNT_WIDTH 16u/#define MBX_EV_TICK_W1_COUNT_WIDTH 8u/' --crosscheck
# 4 the skeleton's decode of one register moved by hand (KL_mbx.sv is generated)
arm "skeleton decode hand edit" hdl/milan/mailbox/KL_mbx.sv '0,/MBX_REG_TICK_CTL_C)) tick_ctl_r/s//MBX_REG_LINK_C)) tick_ctl_r/' --check
# 5 the YAML moved a field and only the C header was regenerated (SV and doc stale)
cp sw/mailbox/mailbox.yaml sw/mailbox/mailbox.yaml.orig
cp sw/firmware/ctrl/mbx/mbx_contract.h sw/firmware/ctrl/mbx/mbx_contract.h.orig
sed -i 's/{name: SLOT, lsb: 16, width: 8, doc: timer slot}/{name: SLOT, lsb: 20, width: 8, doc: timer slot}/' sw/mailbox/mailbox.yaml
python3 - <<'EOF'
import sys; sys.path.insert(0, "sw/mailbox")
from mailbox_model import load
from mailbox_emit import emit_c_header
open("sw/firmware/ctrl/mbx/mbx_contract.h", "w").write(emit_c_header(load()))
EOF
mv sw/mailbox/mailbox.yaml.orig sw/mailbox/mailbox.yaml
if python3 sw/mailbox/gen_mailbox.py --crosscheck > /tmp/genprobe.$$ 2>&1; then echo "[MISSED] stale SV/doc vs regenerated C"; fails=$((fails+1));
else echo "[caught] C regenerated from a moved field, SV and doc not: $(grep -m1 FAIL /tmp/genprobe.$$)"; fi
mv sw/firmware/ctrl/mbx/mbx_contract.h.orig sw/firmware/ctrl/mbx/mbx_contract.h
rm -f /tmp/genprobe.$$
python3 sw/mailbox/gen_mailbox.py --check --crosscheck >/dev/null && echo "restored: gates clean" || { echo "restore FAILED"; fails=$((fails+1)); }
echo "gen_mismatch_probe: $fails missed or broken"
exit $((fails > 0))

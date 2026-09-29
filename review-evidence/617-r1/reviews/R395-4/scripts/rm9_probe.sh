#!/usr/bin/env bash
# RM9 and neighbours: run the committed mga_keepoff.py against the head's
# milan_datapath.sv and against disposable variants of its aligner binding.
# Usage: rm9_probe.sh <repo> <workdir>
set -u
R=$1; W=$2; mkdir -p "$W"
K="$R/tb/verilator/capture_coherence/mga_keepoff.py"
DP="$R/hdl/milan/milan_datapath.sv"
B='    .LOCK_KEEPOFF_CYC_P (MGA_KEEPOFF_CYC_C)'
variant() { # name, python replacement expression on text t
  python3 - "$DP" "$W/$1.sv" "$2" <<'PY'
import sys
src, out, expr = sys.argv[1], sys.argv[2], sys.argv[3]
t = open(src).read(); B = '    .LOCK_KEEPOFF_CYC_P (MGA_KEEPOFF_CYC_C)'
assert t.count(B) == 1, t.count(B)
open(out, 'w').write(eval(expr))
PY
}
run() { printf '%-34s ' "$1"; python3 "$K" "$2" "$W/out-$1.svh" > "$W/$1.err" 2>&1; rc=$?; printf 'rc=%s  %s\n' "$rc" "$(head -c 230 "$W/$1.err" | tr '\n' ' ')"; }
echo "binding lines at head:"; grep -n 'LOCK_KEEPOFF_CYC_P' "$DP"
run head "$DP"
variant rm9_literal128 "t.replace(B, '    .LOCK_KEEPOFF_CYC_P (128)')"; run rm9_literal128 "$W/rm9_literal128.sv"
variant literal256 "t.replace(B, '    .LOCK_KEEPOFF_CYC_P (256)')"; run literal256 "$W/literal256.sv"
variant expr_plus0 "t.replace(B, '    .LOCK_KEEPOFF_CYC_P (MGA_KEEPOFF_CYC_C + 0)')"; run expr_plus0 "$W/expr_plus0.sv"
variant nested_parens "t.replace(B, '    .LOCK_KEEPOFF_CYC_P ((128))')"; run nested_parens "$W/nested_parens.sv"
variant binding_removed "t.replace(B + ',\n', '').replace(',\n' + B, '').replace(B, '')"; run binding_removed "$W/binding_removed.sv"
variant commented_dup "t.replace(B, '    // .LOCK_KEEPOFF_CYC_P (MGA_KEEPOFF_CYC_C)\n' + B)"; run commented_dup "$W/commented_dup.sv"
variant defparam_override "t + '\ndefparam milan_datapath.u_bypass.LOCK_KEEPOFF_CYC_P = 128;\n'"; run defparam_override "$W/defparam_override.sv"

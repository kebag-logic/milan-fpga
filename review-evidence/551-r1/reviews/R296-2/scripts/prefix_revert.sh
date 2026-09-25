#!/bin/sh
# R296-2 control: inside a DISPOSABLE parent clone whose protocol-processor
# checkout is at 990f9652, revert only processor #112's admission RTL
# (a8f8ce81): KL_srp_admission.sv back to its 7a47f578 content and the
# invalidate_i connection removed from KL_srp_top.sv. Everything else in the
# processor pin and the parent is unchanged.
# Usage: prefix_revert.sh <disposable-parent-clone>
set -eu
root=$1
pp=$root/protocol-processor
test "$(git -C "$pp" rev-parse HEAD)" = 990f96526bb89356c963a260ebbdcf2a77e6623a
git -C "$pp" show 7a47f5788ff504f099a47ad4407c340771bb6bdb:hdl/srp/KL_srp_admission.sv \
    > "$pp/hdl/srp/KL_srp_admission.sv"
python3 - "$pp/hdl/srp/KL_srp_top.sv" <<'EOF'
import sys
p = sys.argv[1]
s = open(p).read()
line = "      .invalidate_i        (adm_invalidate_w),\n"
assert s.count(line) == 1, "invalidate_i connection not found exactly once"
open(p, "w").write(s.replace(line, ""))
EOF
git -C "$pp" diff --stat

#!/bin/sh
# Sensitivity control for comment_only_probe.sh step 2: the preprocessed
# comparison must flag a one-token code change and must not flag a
# comment-only change, on the same head copy.
# Usage: pp_sensitivity_control.sh <clone> <head-rev> <verilator> <outdir>
set -eu
clone=$1; head=$2; vl=$3; out=$4
mkdir -p "$out/a/csr" "$out/b/csr" "$out/c/csr"
rel=hdl/common/csr/milan_csr.sv
git -C "$clone" show "$head:$rel" > "$out/a/csr/milan_csr.sv"
# b: one token of the stage-2 OR becomes XOR (exactly one occurrence)
python3 -I - "$out/a/csr/milan_csr.sv" "$out/b/csr/milan_csr.sv" "$out/c/csr/milan_csr.sv" <<'EOF'
import sys
s = open(sys.argv[1]).read()
pat = "r_data <= live_mux_q | shadow_qq;"
assert s.count(pat) == 1
open(sys.argv[2], "w").write(s.replace(pat, "r_data <= live_mux_q ^ shadow_qq;"))
com = "//! rvalid, and no read has a side effect keyed to the old timing."
assert s.count(com) == 1
open(sys.argv[3], "w").write(s.replace(com, "//! rvalid; CONTROL TEXT, a comment-only edit."))
EOF
pp() { "$vl" -E -P +incdir+"$clone/hdl/common/csr" \
        +incdir+"$clone/configs/generated/endstation_ax7101_1x1_tdm8" "$1"; }
pp "$out/a/csr/milan_csr.sv" > "$out/a.pp"
pp "$out/b/csr/milan_csr.sv" > "$out/b.pp"
pp "$out/c/csr/milan_csr.sv" > "$out/c.pp"
rc=0
if cmp -s "$out/a.pp" "$out/b.pp"; then echo "code-token mutant: NOT DETECTED"; rc=1
else echo "code-token mutant: detected ($(diff "$out/a.pp" "$out/b.pp" | grep -c '^[<>]') differing lines)"; fi
if cmp -s "$out/a.pp" "$out/c.pp"; then echo "comment-only edit: identical, as expected"
else echo "comment-only edit: DIFFERENT"; rc=1; fi
exit $rc

#!/usr/bin/env bash
# KL_aecp_resp_buf.gen_g_size: is the bench's passing case (24) the nearest one,
# and does a guard that refuses legal values survive the bench?
# Usage: gsize_probes.sh <head-tree> <scratch-dir> <bin12> <bin13>
#   (writes nothing into <head-tree>; <scratch-dir> must not exist)
set -u; H=$(cd "$1" && pwd); W=$2; B12=$3; B13=$4
SRC() { echo $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort); }
FL="--lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM"
echo "### 1. Verilator lint at the head (scripts/lint_hdl.sh flags)"
(cd "$H" && for n in 16 17 20 23 24; do out=$(PATH=$B12:$PATH verilator $FL --top-module KL_aecp_resp_buf -GRESP_BYTES_P=$n $(SRC) 2>&1); echo "RESP_BYTES_P=$n rc=$? :: $(grep -m1 '^%' <<<"$out")"; done)
echo "### 2. sv2v + Yosys at the head"
for v in 12 13; do b=$B12; [ $v = 13 ] && b=$B13; t=$(mktemp -d); (cd "$H" && PATH=$b:$PATH sv2v $(SRC) > $t/all.v)
  for n in 16 17 24; do out=$(cd $t && yosys -q -p "read_verilog -defer all.v; chparam -set RESP_BYTES_P $n KL_aecp_resp_buf; hierarchy -check -top KL_aecp_resp_buf; proc; opt_clean" 2>&1); echo "sv2v 0.0.$v RESP_BYTES_P=$n rc=$? :: $(grep -m1 ERROR <<<"$out")"; done; rm -rf $t; done
echo "### 3. mutant: the guard's condition RESP_BYTES_P <= 16 becomes <= 23 (refuses legal 17..23)"
mkdir -p "$W" && cp -a "$H/hdl" "$H/tb" "$H/scripts" "$W/"
sed -i 's/if (RESP_BYTES_P <= 16) begin : gen_g_size/if (RESP_BYTES_P <= 23) begin : gen_g_size/' "$W/hdl/aecp/KL_aecp_resp_buf.sv"
grep -n 'begin : gen_g_size' "$W/hdl/aecp/KL_aecp_resp_buf.sv"
(cd "$W" && PATH=$B12:$PATH python3 -B tb/elab_guards/guards.py --root "$W" --only KL_aecp_resp_buf.gen_g_size --jobs 2 | grep -E '^(FAIL|GUARD|ELAB)|elab guards:'; echo "bench rc=${PIPESTATUS[0]} (0 = the mutant SURVIVED)")
(cd "$W" && out=$(PATH=$B12:$PATH verilator $FL --top-module KL_aecp_resp_buf -GRESP_BYTES_P=17 $(SRC) 2>&1); echo "mutant tree, RESP_BYTES_P=17 lint rc=$? :: $(grep -m1 '^%' <<<"$out")")

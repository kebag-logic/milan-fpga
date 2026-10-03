#!/usr/bin/env bash
# Formal equivalence of protocol_processor_top, base f4167536 vs head 54f9411,
# with every submodule instance cut out: submodule outputs become free inputs,
# submodule inputs become compared outputs (seven expression-valued
# connections are first given shared public names), then equiv_make /
# equiv_simple / equiv_induct. Two negative controls must FAIL.
# usage: reorder_equiv.sh <processor-clone> <work-dir> <receipts-dir-with-.ys>
set -uo pipefail
clone=$1 work=$2 ys=$3
mkdir -p "$work"; cd "$work" || exit 2
for r in base:f4167536d358c996f4e1b70b875879c1651f85d3 head:54f9411ab9a4b4aea58393f7fa1303ddcc96ee3c; do
  n=${r%%:*}; c=${r#*:}; rm -rf "t_$n"; mkdir "t_$n"
  git -C "$clone" archive "$c" | tar -x -C "t_$n"
  ( cd "t_$n" && sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) ) > "$n.v"
done
( cd t_head/hdl/aecp/ucode && python3 gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd t_head/hdl/acmp/rom && python3 gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null 2>&1 || true )
sed "21904s/hdr_msg_type_r == 4'd0/hdr_msg_type_r == 4'd1/" head.v > head_neg.v
sed "21552s/16'h0003/16'h0004/" head.v > head_neg2.v
cmp -s head.v head_neg.v && { echo "negative control 1 did not change head.v"; exit 2; }
cmp -s head.v head_neg2.v && { echo "negative control 2 did not change head.v"; exit 2; }
cp "$ys"/pos5.ys "$ys"/neg5.ys "$ys"/neg25.ys .
for c in pos5 neg5 neg25; do
  ( yosys -q -l "$c.log" -s "$c.ys" > "$c.out" 2>&1; echo $? > "$c.rc" ) &
done
wait
rc=0
[ "$(cat pos5.rc)" = 0 ] && echo "pos5: base == head PROVEN" || { echo "pos5: NOT proven"; rc=1; }
for c in neg5 neg25; do
  [ "$(cat $c.rc)" != 0 ] && echo "$c: planted change CAUGHT" || { echo "$c: planted change MISSED"; rc=1; }
done
exit $rc

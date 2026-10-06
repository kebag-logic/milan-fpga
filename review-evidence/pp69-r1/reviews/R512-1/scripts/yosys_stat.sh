#!/bin/bash
# yosys_stat.sh <tree> <tag> : the syn/yosys/run.sh elaboration recipe (sv2v of
# every hdl source, then per top `hierarchy -check; proc; opt_clean`) for the
# tops this PR touches, writing `stat -json` per top; plus the top at
# N_AVB_IF_P=2 when the tree has that parameter. Output under
# receipts/yosys/<tag>/; rc in receipts/yosys/<tag>.rc.
set -u
P=$REVIEWS/pp69-r512-1-packet
tree=$1; tag=$2
out=$P/receipts/yosys/$tag; mkdir -p "$out"
work=$P/scratch/yosys-$tag; rm -rf "$work"; mkdir -p "$work"
start=$(date +%s)
cd "$tree" || exit 2
sv2v $(find hdl -name '*_pkg.sv' | sort) $(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort) > "$work/all.v" || { echo "rc=3 sv2v" > "$P/receipts/yosys/$tag.rc"; exit 3; }
( cd hdl/aecp/ucode && python3 gen_ucode.py -o "$work/ucode.hex" >/dev/null )
( cd hdl/acmp/rom && python3 gen_ltn_rom.py -o "$work/ltn_rom.hex" >/dev/null 2>&1 )
cd "$work"
{
  printf 'read_verilog -defer all.v\ndesign -save parsed\n'
  for t in KL_aecp_notify KL_adp_engine protocol_processor_top; do
    printf 'design -load parsed\nhierarchy -check -top %s\nproc\nopt_clean\ntee -q -o %s/%s.json stat -json\n' "$t" "$out" "$t"
  done
  if grep -q 'N_AVB_IF_P' all.v; then
    printf 'design -load parsed\nhierarchy -check -top protocol_processor_top -chparam N_AVB_IF_P 2\nproc\nopt_clean\ntee -q -o %s/protocol_processor_top-if2.json stat -json\n' "$out"
    printf 'design -load parsed\nhierarchy -check -top KL_aecp_notify -chparam N_IF_P 2\nproc\nopt_clean\ntee -q -o %s/KL_aecp_notify-if2.json stat -json\n' "$out"
  fi
} > gate.ys
yosys -q -s gate.ys > "$out/yosys.log" 2>&1
echo "rc=$? seconds=$(( $(date +%s) - start ))" > "$P/receipts/yosys/$tag.rc"

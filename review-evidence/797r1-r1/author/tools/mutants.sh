#!/bin/bash
# In-tree planted stale-page mutants on the committed head; each is restored with git checkout and re-checked.
# Usage: mutants.sh <receipt dir>   (run from the lane, after the gate run, nothing else reading the tree)
set -u
out="$1"; mkdir -p "$out"
py=/tmp/797-a711-wd/bin/python3
gate() { "$py" scripts/gen_register_reference.py --check "$@"; }
run() {  # name, plant command, file to restore
  local name="$1" plant="$2" file="$3"
  {
    echo "# mutant: $name"
    echo "\$ $plant"
    bash -c "$plant"
    gate > /tmp/797-a711-mut.txt 2>&1; rc=$?
    echo "--- planted: rc=$rc"; tail -4 /tmp/797-a711-mut.txt
    git checkout -- "$file"
    gate > /tmp/797-a711-mut.txt 2>&1; rc=$?
    echo "--- restored: rc=$rc"; tail -1 /tmp/797-a711-mut.txt
    git status --short | wc -l | sed 's/^/dirty files after restore: /'
  } > "$out/$name.txt" 2>&1
}
run rtl-field-rename "sed -i 's/\\bo_tcam_wr_action\\b/o_tcam_wr_action_renamed/g' hdl/common/csr/milan_csr.sv" hdl/common/csr/milan_csr.sv
run reset-value-change "sed -i \"s/\\(A_MAC_IFG\\[10:0\\]:[ ]*csr_default = \\)32'h0C;/\\132'h0D;/\" hdl/common/csr/milan_csr.sv" hdl/common/csr/milan_csr.sv
run page-hand-edit "sed -i '0,/\\[reset = 0x00000001\\]/s//[reset = 0x00000000]/' docs/reference/REGISTER_MAP.md" docs/reference/REGISTER_MAP.md
run unknown-field-description "python3 -c \"import json;p='scripts/register_descriptions.json';d=json.load(open(p));d['registers']['ETH_GUARD']['fields']['NOT_IN_RTL']='x';open(p,'w').write(json.dumps(d,indent=2,ensure_ascii=False)+'\\n')\"" scripts/register_descriptions.json
{
  echo "# SoC extract against the shipping export (fresh), then against an export copy with one bank moved"
  gate --soc-from /tmp/797-a711-export > /tmp/797-a711-mut.txt 2>&1; echo "--- real export: rc=$?"; tail -1 /tmp/797-a711-mut.txt
  rm -rf /tmp/797-a711-export-moved; cp -r /tmp/797-a711-export /tmp/797-a711-export-moved
  sed -i 's/^csr_base,uart,0xf0003800,,/csr_base,uart,0xf0004000,,/' /tmp/797-a711-export-moved/csr.csv
  gate --soc-from /tmp/797-a711-export-moved > /tmp/797-a711-mut.txt 2>&1; echo "--- moved bank: rc=$?"; tail -2 /tmp/797-a711-mut.txt
} > "$out/soc-from-check.txt" 2>&1
sed -i 's#/tmp/797-a711-export-moved#<export copy>#g; s#/tmp/797-a711-export#<export>#g' "$out"/*.txt

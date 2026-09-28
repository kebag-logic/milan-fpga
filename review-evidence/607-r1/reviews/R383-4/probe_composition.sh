#!/usr/bin/env bash
# Disposable composition fault probes on a scratch clone of the candidate. Every mutated byte is restored.
# Usage: probe_composition.sh <scratch-clone> <packet> <litex-python>
set -u
T=$1; PKT=$2; PY=$3
export PATH="$PKT/scratch/bin:$PATH" PYTHONHASHSEED=0
cd "$T"
OUT=$PKT/receipts/50_probes.txt; : > "$OUT"
restore() { git checkout -q -- "$@"; }
# P0 control: the shipping arm is green on unmodified candidate bytes.
"$PY" -B sw/builder/test_shipping_clock_constraints.py > "$PKT/receipts/50_p0.log" 2>&1; echo "P0 control shipping arm rc=$? (expect 0)" >> "$OUT"
# P1 (#595 x #607): an unquoted shipping mac_address, which #595's loader now refuses, must turn
# #607's shipping arm red (not skip), proving the arm sits on #595's config path.
sed -i 's#^  mac_address: "02:00:00:00:00:01"#  mac_address: 0x020000000001#' configs/endstation_ax7101_1x1_tdm8.yaml
git diff --stat >> "$OUT"
"$PY" -B sw/builder/test_shipping_clock_constraints.py > "$PKT/receipts/50_p1.log" 2>&1; rc=$?
echo "P1 unquoted shipping mac_address -> shipping arm rc=$rc (expect nonzero); refusal: $(grep -o -m1 'quote the hexadecimal value as a YAML string' "$PKT/receipts/50_p1.log")" >> "$OUT"
restore configs/endstation_ax7101_1x1_tdm8.yaml
# P2 (#602 x #607): revert #602's RTL bytes; the emitted shipping Tcl/XDC must not change,
# proving the constraint emission is independent of that RTL delta.
git show 7390b43627032c71c470e2aa8d0845eb5b740663:hdl/milan/milan_datapath.sv > hdl/milan/milan_datapath.sv
git show 7390b43627032c71c470e2aa8d0845eb5b740663:hdl/ieee1722/avtp/KL_media_clock_restart.sv > hdl/ieee1722/avtp/KL_media_clock_restart.sv
git diff --stat >> "$OUT"
for od in "$PKT/scratch/p2-mut" "$PKT/scratch/p2-ctl"; do :; done
"$PY" -B sw/builder/test_shipping_clock_constraints.py --config ax7101_1x1_tdm8 --port e1 --output-dir "$PKT/scratch/p2-mut" > "$PKT/receipts/50_p2_mut.log" 2>&1; rm_rc=$?
restore hdl/milan/milan_datapath.sv hdl/ieee1722/avtp/KL_media_clock_restart.sv
"$PY" -B sw/builder/test_shipping_clock_constraints.py --config ax7101_1x1_tdm8 --port e1 --output-dir "$PKT/scratch/p2-ctl" > "$PKT/receipts/50_p2_ctl.log" 2>&1; ctl_rc=$?
for f in alinx_ax7101.tcl alinx_ax7101.xdc; do
  a=$(sed "s#$PKT/scratch/p2-mut#<OUT>#g" "$PKT/scratch/p2-mut/gateware/$f" | sha256sum | cut -c1-16)
  b=$(sed "s#$PKT/scratch/p2-ctl#<OUT>#g" "$PKT/scratch/p2-ctl/gateware/$f" | sha256sum | cut -c1-16)
  echo "P2 #602 RTL reverted rc=$rm_rc control rc=$ctl_rc $f: reverted=$a candidate=$b $([ "$a" = "$b" ] && echo SAME || echo DIFFERENT)" >> "$OUT"
done
# P3: the run-list audit can fail: drop #595's arm, duplicate #607's arm, in a scratch copy only.
cp sw/builder/test_builder.py "$PKT/scratch/tb_mut.py"
python3 - "$PKT/scratch/tb_mut.py" >> "$OUT" <<'PY'
import ast, collections, sys
p = sys.argv[1]; s = open(p).read()
s = s.replace("test_declaration_contracts, test_clock_crossing_constraints,",
              "test_clock_crossing_constraints, test_clock_crossing_constraints,", 1)
tree = ast.parse(s)
main = [n for n in tree.body if isinstance(n, ast.If) and "__main__" in ast.unparse(n.test)][0]
rl = [ast.unparse(e) for n in ast.walk(main) if isinstance(n, ast.For) and isinstance(n.iter, ast.Tuple) for e in n.iter.elts]
c = collections.Counter(rl)
print(f"P3 mutated run list: duplicates={[k for k, v in c.items() if v > 1]} missing_595_arm={'test_declaration_contracts' not in rl} (expect both flagged)")
PY
echo "restored: $(git status --porcelain | wc -l) modified paths" >> "$OUT"
cat "$OUT"

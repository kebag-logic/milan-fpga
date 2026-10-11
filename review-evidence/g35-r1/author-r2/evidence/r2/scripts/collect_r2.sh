#!/usr/bin/env bash
# Copy round 2's small evidence files into the output directory (each well
# under 200 KB); scratch build trees stay in scratch.
set -u
S=$VALIDATION_STORAGE/g35-a599; R=$S/r2
O=$MANAGEMENT/2026-09-23/g35-a599/evidence/r2
mkdir -p "$O/steps" "$O/mutation" "$O/position" "$O/parent/base" "$O/parent/head" "$O/gates-head" "$O/scripts"
cp "$R/stepA/mutants.log" "$O/steps/stepA-mutants.log"
cp "$R/stepB/mutants.log" "$O/steps/stepB-mutants.log"
for f in docs lint mutants; do cp "$R/stepC/$f.log" "$O/steps/stepC-$f.log"; echo "$f rc=$(cat "$R/stepC/$f.rc")"; done > "$O/steps/stepC-rc.txt"
cp "$R/stepB-head/run.log" "$O/steps/parser-suite-head.log"
cp "$R/per-position-base.tsv" "$R/per-position-head.tsv" "$R/per-position-tables.md" "$O/position/"
for m in planted stale-mutant eofterm; do
  [ -f "$R/$m/mutant.diff" ] && cp "$R/$m/mutant.diff" "$O/mutation/$m.diff"
  cp "$R/$m/named.txt" "$O/mutation/$m-named.txt"
  cp "$R/$m/run/run.log" "$O/mutation/$m-suite.log"
done
for side in base head; do
  src=$S/parent-r2-$side; dst=$O/parent/$side; rc=$R/romcheck-r2-$side
  sed "s|$S/parent|<scratch-parent>|g" "$src/identity.txt" > "$dst/identity.txt"
  cp "$src/gate.log" "$src/rom_sha256.txt" "$src/rom_bundle_digest.txt" "$src/netlist_sha256.txt" "$dst/"
  cp "$src/results/top-KL_gptp_shadow.result" "$src/work/hier.stat.txt" "$src/work/flat.stat.txt" "$dst/"
  for g in gate sv2v enforce rom_bundle hier flat; do echo "$g rc=$(cat "$src/$g.rc")"; done > "$dst/rc.txt"
  cp "$rc/pin.txt" "$rc/record.diff" "$rc/check-before-record.log" "$rc/check-after-record.log" "$rc/record.log" "$dst/"
  for f in check-before-record record check-after-record; do echo "$f rc=$(cat "$rc/$f.rc")"; done > "$dst/romcheck-rc.txt"
done
cp "$R/module-compare-base-r2head.txt" "$R/module-compare-r1head-r2head.txt" "$O/parent/"
G=$S/gates-r2-head
if [ -f "$G/tb.rc" ]; then
  for f in identity.txt contract.log lint.log docs.log tb.log; do cp "$G/$f" "$O/gates-head/"; done
  for g in tb contract lint docs; do echo "$g rc=$(cat "$G/$g.rc")"; done > "$O/gates-head/rc.txt"
fi
cp "$R/bin/"*.sh "$R/bin/"*.py "$S/bin/gates.sh" "$S/bin/parent_evidence.sh" "$O/scripts/"
find "$O" -type f -size +200k -print
du -sh "$O"
for v in reverted renamed; do cp "$R/meta/$v.log" "$O/mutation/meta-$v.log"; echo "rc=$(cat "$R/meta/$v.rc")" > "$O/mutation/meta-$v.rc"; done

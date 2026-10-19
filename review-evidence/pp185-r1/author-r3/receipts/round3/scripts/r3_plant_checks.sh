#!/usr/bin/env bash
# round 3: planted mutants of the reconcile and input-hash checks; each must fail (rc 1)
S=$VALIDATION_STORAGE/pp185-a647; O=$MANAGEMENT/2026-09-23/pp185-a647/receipts
R3="$O/round3"; P="$S/scripts"; M="$S/r3/mut-checks"; T="$R3/selftest"
rm -rf "$M"; mkdir -p "$M/compare"
# reconcile: the notify comparison carrying the old figure (baselines counted: 135 unchanged)
cp "$R3/compare/round2"/*.json "$M/compare/"
python3 -I - "$M/compare/notify-base-vs-head.json" <<'EOF'
import json, sys
p = sys.argv[1]; d = json.load(open(p)); d["mutants"]["unchanged"] = 135
open(p, "w").write(json.dumps(d, indent=1) + "\n")
EOF
python3 -I "$P/r3_reconcile.py" "$R3/reconcile/evidence-audit-replayed.json" \
  "$R3/reconcile/evidence-audit-published.json" "$M/compare" > "$T/mutant-reconcile-old-figure.log" 2>&1
echo $? > "$T/mutant-reconcile-old-figure.rc"
# reconcile: a replayed audit that differs from the published one
python3 -I - "$R3/reconcile/evidence-audit-replayed.json" "$M/audit.json" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1])); d["d3"]["goldens"] = 7
open(sys.argv[2], "w").write(json.dumps(d, indent=2) + "\n")
EOF
python3 -I "$P/r3_reconcile.py" "$M/audit.json" "$R3/reconcile/evidence-audit-published.json" \
  "$R3/compare/round2" > "$T/mutant-reconcile-audit-differs.log" 2>&1
echo $? > "$T/mutant-reconcile-audit-differs.rc"
# input hashes: one listed digest altered; the check (r3_compare.sh's inline program) must refuse it
sed '1s/^./0/; 1s/^0\(.\)/f\1/' "$R3/inputs.sha256" > "$M/inputs.sha256"
sed -n '/^python3 -I - "\$R3\/inputs.sha256"/,/^EOF$/p' "$P/r3_compare.sh" | sed '1d;$d' > "$M/inputs_check.py"
python3 -I "$M/inputs_check.py" "$M/inputs.sha256" "$O" > "$T/mutant-inputs-digest-altered.log" 2>&1
echo $? > "$T/mutant-inputs-digest-altered.rc"
python3 -I "$M/inputs_check.py" "$R3/inputs.sha256" "$O" > "$T/inputs-check-extracted.log" 2>&1
echo $? > "$T/inputs-check-extracted.rc"
# old rows: a kept comparison whose DIFFER row lost one failure ID
mkdir -p "$M/root/round2" "$M/root/r1c" "$M/root/round3"
cp -r "$O/round2/compare" "$M/root/round2/"; cp -r "$O/r1c/compare" "$M/root/r1c/"
cp -r "$R3/compare" "$M/root/round3/"
sed -i 's/^\(DIFFER rd-tail-uncut: base 16: RDC0\), RDC1,/\1,/' "$M/root/round2/compare/failsets-aecp_dispatch-base-vs-head.txt"
python3 -I "$P/r3_oldrows.py" "$M/root" > "$T/mutant-oldrows-id-dropped.log" 2>&1
echo $? > "$T/mutant-oldrows-id-dropped.rc"
cp "$P/r3_plant_checks.sh" "$R3/scripts/"
echo done

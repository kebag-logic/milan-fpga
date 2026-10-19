#!/usr/bin/env bash
# round 3: replay the reviewer's audit_evidence.py (R668-2's archived packet) on the
# published round-2 receipts, then reconcile it with the corrected comparison
S=$VALIDATION_STORAGE/pp185-a647; O=$MANAGEMENT/2026-09-23/pp185-a647/receipts
R3="$O/round3"; P="$S/scripts"; X="$S/r3/replay"; F="$S/r3/fetched"
rm -rf "$X"; mkdir -p "$X/receipts/public" "$R3/reconcile"
cp "$F/audit_evidence.py" "$X/"
cd "$O/round2" || exit 1
for f in {base,head}/campaigns/out/{notify,d3,aecp_dispatch}/results.json \
         head-final2/campaigns/out/notify/results.json head-final2/gates/*.rc \
         parent-base/*.rc parent-head/*.rc parent-base/g11_lint_rtl.log parent-head/g11_lint_rtl.log; do
  mkdir -p "$X/receipts/public/$(dirname "$f")"; cp "$f" "$X/receipts/public/$f"
done
cd "$X" || exit 1
python3 -I "$X/audit_evidence.py" > "$R3/reconcile/audit-replay.log" 2>&1
echo $? > "$R3/reconcile/audit-replay.rc"
cp "$X/evidence-audit.json" "$R3/reconcile/evidence-audit-replayed.json"
cp "$F/evidence-audit.json" "$R3/reconcile/evidence-audit-published.json"
sha256sum "$F/audit_evidence.py" "$F/evidence-audit.json" | sed "s#$F/##" > "$R3/reconcile/reviewer-files.sha256"
python3 -I "$P/r3_reconcile.py" "$R3/reconcile/evidence-audit-replayed.json" \
  "$R3/reconcile/evidence-audit-published.json" "$R3/compare/round2" > "$R3/reconcile/reconcile.txt" 2>&1
echo $? > "$R3/reconcile/reconcile.rc"
cp "$P/r3_replay.sh" "$R3/scripts/"
echo done

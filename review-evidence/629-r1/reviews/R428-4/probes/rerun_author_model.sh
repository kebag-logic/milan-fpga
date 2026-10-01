#!/bin/sh
# Re-run the round-4 author desk model from the public evidence branch and compare
# its output byte for byte with the published receipt, then re-run the published
# no-loss comparison against the round-3 published output.
# Usage: rerun_author_model.sh <dir holding author-r4/ and author-r3/ downloads> <outdir>
D="$1"; O="$2"; mkdir -p "$O/run"
cp "$D/author-r4/meter_rules_model_r4.py" "$O/run/"
( cd "$O/run" && python3 -B meter_rules_model_r4.py > rerun.out 2>&1; echo $? > rerun.rc )
cmp "$O/run/rerun.out" "$D/author-r4/meter_rules_model_r4.out"; echo "cmp_rc $?"
sha256sum "$D/author-r4/meter_rules_model_r4.py" "$D/author-r4/meter_rules_model_r4.out" "$O/run/rerun.out" "$D/author-r3/meter_rules_model_r3.out"
python3 -B "$D/author-r4/compare_r3_r4_noloss.py" "$D/author-r3/meter_rules_model_r3.out" "$O/run/rerun.out" | tail -1; echo "compare_rc $?"

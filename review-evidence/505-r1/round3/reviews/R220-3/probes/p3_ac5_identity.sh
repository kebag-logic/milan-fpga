#!/usr/bin/env bash
# p3 (R220-3): the head checker's diagnostic for the AC5 edit (p2's
# c1-carrier-or-true run) against the archived act receipts of A10's AC5
# measurement at 6af65a15 / scratch 66ba2106, plus the published verifier.
# Usage: p3_ac5_identity.sh <evidence-clone> <p2-scratch-dir> <review-clone>
set -uo pipefail
EV=$1 P=$2 C=$3
E=$EV/review-evidence/505-r1
export PYTHONDONTWRITEBYTECODE=1
echo "# p3: AC5 diagnostic at head vs recorded act receipts (A10, measured at 6af65a15 / scratch 66ba2106)"
echo "evidence checkout: $(git -C "$EV" rev-parse HEAD)"
for f in ac5-act/01.log ac5-act/02.log ac5/mutation.diff ac5/input.json; do
  echo "blob $(git -C "$EV" hash-object "$E/$f") $f"
done
head_finding=$(grep '^  FAIL ' "$P/c1-carrier-or-true.out" | sed 's/^  FAIL //')
a1=$(sed -n '1902p' "$E/ac5-act/01.log" | sed 's/^.*|   FAIL //')
a2=$(sed -n '37p' "$E/ac5-act/02.log" | sed 's/^.*|   FAIL //')
echo "head finding : $head_finding"
[ "$head_finding" = "$a1" ] && echo "01.log:1902 finding BYTE-IDENTICAL to head" || echo "01.log:1902 DIFFERS"
[ "$head_finding" = "$a2" ] && echo "02.log:37 finding BYTE-IDENTICAL to head" || echo "02.log:37 DIFFERS"
echo "--- act verdict lines around the finding"
sed -n '1837p;1903,1904p;1909p' "$E/ac5-act/01.log" | cut -c1-200
sed -n '38,39p;44p;88p;99p;105p;149p;161p;167p' "$E/ac5-act/02.log" | cut -c1-200
echo "--- head verdict line"; grep '^ci_events:' "$P/c1-carrier-or-true.out"
echo "--- recorded mutation.diff"; cat "$E/ac5/mutation.diff"
echo "--- head docs.yml line of the AC5 call"; grep -n 'check_py_idiom.py$' "$C/.github/workflows/docs.yml"
echo "--- published verifier on the archive"
(cd "$E" && python3 -B ac5/verify_receipts.py "$E"; echo "exit=$?")
echo "--- recorded exit codes"
python3 -B -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['head'], [r['exit_code'] for r in d['results']])" "$E/ac5-act/results.json"
cat "$E/ac5-act/complete.json"; echo
echo "--- act-ci verdict lines"
grep -n '^act-ci: .*: \(PASS\|FAILED\)' "$E/ac5-act/01.log" "$E/ac5-act/02.log" "$E/act-draft-fast/01.log" | sed "s#$E/##"
echo "--- scratch PR #506 state"
gh pr view 506 --repo kebag-logic/milan-fpga --json number,state,mergedAt,closedAt,headRefOid,isDraft

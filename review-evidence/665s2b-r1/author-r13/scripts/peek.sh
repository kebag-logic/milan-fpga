#!/bin/bash
# Regrade a running leg's finished save windows from copies (the leg untouched): each window's share and its rows.
# usage: peek.sh LEG POINT [extra run.py args]
set -u
. $MANAGEMENT/2026-09-23/665s2b-a683p/scripts/env.sh
T=$VALIDATION_STORAGE/665s2b-a683p; LEG=$1 POINT=$2; shift 2
R=$T/peek-$LEG; rm -rf $R; mkdir -p $R; G=""
for f in $(grep -l '^RESULT' $T/builds/$LEG/results/*@*.log 2>/dev/null); do n=$(basename $f .log); cp $f $T/builds/$LEG/results/$n.txt $R/; G="$G,$n"; done
G=${G#,}; [ -z "$G" ] && { echo "no finished window"; exit 0; }
C=$T/C1; case $LEG in D-*) C=$T/CD;; esac
cd $C && (ulimit -v 6000000; timeout 500 python3 -B tb/verilator/ctrl_service_budget/run.py --point $POINT --build-dir $T/builds/$LEG --reuse-build --regrade --out $R --groups "$G" --record-budget-findings --record-share-findings "$@" > $R/regrade.log 2>&1)
grep "groups graded\|REFUSED\|BUDGET" $R/regrade.log | cut -c1-220
python3 - "$R/results.json" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
for g in d['results']:
    rows = {}
    for r in g['probes']:
        if r['status'] == 'measured':
            key = r['probe'].split('.service.')[-1] if '.service.' in r['probe'] else r['probe'].split('.', 1)[1]
            rows[key] = r['ms']
    srp = max((v for k, v in rows.items() if k.startswith('srp.last')), default=0)
    aecp = max((v for k, v in rows.items() if k.startswith('aecp.last')), default=0)
    s = g['passes']['share']
    print(f"{g['group']}: over {s['over']}, longest {g['passes']['worst']['ms']:.3f} ms, SRP last {srp:.2f}, AECP last {aecp:.2f}")
PY

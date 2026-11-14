#!/bin/bash
# The CPU budget harness at a head (round 2's hs2.sh): a fresh build of one point and arm on a clean clone, the named
# groups run on it, graded by run.py against the stated tables. usage: hs3.sh CLONE NAME POINT GROUPS [run.py args]
set -u
C=$1 NAME=$2 POINT=$3 SEL=$4; shift 4
W=/data-2/milan/tmp/897-a776
. $W/scripts/env.sh
B=$W/r3/builds/$NAME
export TMPDIR=$W/r3/tmp/hs-$NAME MAKEFLAGS="-j8 --no-print-directory" PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) $NAME $POINT $SEL $* start $(date +%T)"
rm -rf "$B"; mkdir -p "$B"
start=$(date +%s)
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --groups "$SEL" \
    --out "$B/results" --record-budget-findings --record-share-findings --jobs 4 "$@"
rc=$?
echo "rc=$rc elapsed=$(( $(date +%s) - start ))s end $(date +%T)"
python3 -c "import json,ast; d=json.load(open('$B/build.json')); p=d['ctrl_plan']; p=ast.literal_eval(p) if isinstance(p,str) else p; print('PLAN', d['variant'], d['shape'], d['interfaces'], 'rom', p['rom']['bytes'], 'in', sum(p['rom']['banks']), 'sram', p['sram']['bytes'], 'in', sum(p['sram']['banks']), 'tiles', p['tiles'])"
git -C "$C" status --porcelain --untracked-files=all
exit $rc

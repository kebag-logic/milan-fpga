#!/bin/bash
# A leg's baseline regrade (#882): the new build against round 26's (images by objcopy, every recorded input
# digest), the sample groups' logs byte for byte against round 26's, then round 26's recorded logs, the new groups'
# logs over them, regraded against the new build.
# usage: regrade.sh CLONE NAME POINT OLD_BUILD OLD_RESULTS SAMPLES NEWGROUPS [run.py args]
set -u
C=$1 NAME=$2 POINT=$3 OLD=$4 RES=$5 SAMPLES=$6 NEW=$7; shift 7
T=<scratch>
. $T/scripts/env.sh
B=$T/builds/$NAME OC=<home>/br-milan-rv32/host/bin/riscv32-linux-objcopy
X=$T/logs/$NAME-compare.txt
{
    echo "# $NAME: builds/$NAME (clone at $(git -C "$C" rev-parse HEAD)) against round 26's $(basename "$OLD")"
    for f in image/ctrl_app.elf split-soc/mapped/image/ctrl_app.elf split-soc/stand-ins/image/ctrl_app.elf; do
        $OC -O binary "$OLD/$f" "$T/tmp/$NAME-old.bin"; $OC -O binary "$B/$f" "$T/tmp/$NAME-new.bin"
        if cmp -s "$T/tmp/$NAME-old.bin" "$T/tmp/$NAME-new.bin"; then r=identical; else r=DIFFERENT; fi
        echo "$f objcopy -O binary $r: old $(sha256sum < "$T/tmp/$NAME-old.bin" | cut -c1-64) new $(sha256sum < "$T/tmp/$NAME-new.bin" | cut -c1-64), $(stat -c %s "$T/tmp/$NAME-new.bin") B"
        if cmp -s "$OLD/$f" "$B/$f"; then echo "$f elf identical"; else echo "$f elf differs"; fi
    done
    python3 - "$OLD/build.json" "$B/build.json" <<'PY'
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
ia, ib = a.get('inputs', {}), b.get('inputs', {})
same = [k for k in sorted(set(ia) | set(ib)) if ia.get(k) == ib.get(k)]
for k in sorted(set(ia) | set(ib)):
    if ia.get(k) != ib.get(k):
        print(f'input differs: {k}')
print(f'inputs compared: {len(set(ia) | set(ib))}, identical: {len(same)}')
print('executable_sha256', 'identical' if a.get('executable_sha256') == b.get('executable_sha256') else 'differs')
PY
    for g in ${SAMPLES//,/ }; do
        if cmp -s "$RES/$g.log" "$B/results-new/$g.log"; then r=identical; else r=DIFFERENT; fi
        echo "group $g log $r: recorded $(sha256sum < "$RES/$g.log" | cut -c1-64) new $(sha256sum < "$B/results-new/$g.log" | cut -c1-64), $(stat -c %s "$B/results-new/$g.log") bytes"
        if cmp -s "$RES/$g.txt" "$B/results-new/$g.txt"; then echo "group $g script identical"; else echo "group $g script DIFFERENT"; fi
    done
} > "$X" 2>&1
M=$B/results-regrade; rm -rf "$M"; mkdir -p "$M"
cp "$RES"/*.txt "$RES"/*.log "$M/"
for g in ${NEW//,/ }; do cp "$B/results-new/$g.txt" "$B/results-new/$g.log" "$M/"; done
R=$T/logs/$NAME-regrade.log
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l) regrade of round 26's groups and the new $NEW" > "$R"
export TMPDIR=$T/tmp/$NAME-regrade PYTHONUNBUFFERED=1; mkdir -p "$TMPDIR"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$M" --record-budget-findings --record-share-findings "$@" >> "$R" 2>&1
echo "rc=$?" >> "$R"

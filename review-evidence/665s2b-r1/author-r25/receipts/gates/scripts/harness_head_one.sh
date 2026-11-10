#!/bin/bash
# One leg of the harness at the final head (harness_head.sh's steps, one leg a process): a fresh build of the head on
# the fresh clean clone hleg-wt-head, the build compared with the one that ran the groups, a sample of groups
# re-simulated and their logs compared byte for byte with the recorded ones, then every recorded group regraded
# against the head's build. With WAITPID set, the sample is already running as that process: wait for it instead.
# usage: [WAITPID=pid] harness_head_one.sh HEAD NAME POINT RESULTS SAMPLE [run.py args]
set -u
H=$1 NAME=$2 POINT=$3 RES=$4 SAMPLE=$5; shift 5
T=<scratch>
. $T/scripts/env.sh
C=$T/hleg-wt-head L=$T/logs/harness-head.txt OLD=$T/builds/$NAME B=$T/builds-head/$NAME G=$T/logs/head-$NAME.log
test "$(git -C "$C" rev-parse HEAD)" = "$H" || { echo "$(date +%T) $NAME: clone not at head" >> $L; exit 4; }
mkdir -p "$B"; export TMPDIR=$T/tmp-head-$NAME MAKEFLAGS="-j8 --no-print-directory"; mkdir -p "$TMPDIR"
if [ -n "${WAITPID:-}" ]; then
    while kill -0 "$WAITPID" 2>/dev/null; do sleep 30; done
    echo "sample ended (its run.py, $WAITPID, was started by harness_head.sh; its rc is not recorded, its output is above)" >> "$G"
else
    echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) build and sample $SAMPLE" > "$G"
    echo "$(date +%T) $NAME build and sample $SAMPLE start" >> $L
    python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --groups "$SAMPLE" \
        --out "$B/results-sample" --record-budget-findings --record-share-findings --jobs 8 "$@" >> "$G" 2>&1
    echo "sample rc=$?" >> "$G"
fi
{
    echo "# $NAME: the head's build (builds-head/$NAME) against the build that ran the groups (builds/$NAME)"
    for f in image/ctrl_app.elf split-soc/mapped/image/ctrl_app.elf split-soc/stand-ins/image/ctrl_app.elf native/Vsim; do
        if cmp -s "$OLD/$f" "$B/$f"; then r=identical; else r=DIFFERENT; fi
        echo "$f $r: old $(sha256sum < "$OLD/$f" | cut -c1-64) head $(sha256sum < "$B/$f" | cut -c1-64)"; done
    python3 - "$OLD/build.json" "$B/build.json" <<'PY'
import json, sys
a, b = (json.load(open(p)) for p in sys.argv[1:3])
ia, ib = a.get('inputs', {}), b.get('inputs', {})
for k in sorted(set(ia) | set(ib)):
    if ia.get(k) != ib.get(k):
        print(f'input differs: {k}')
print(f'inputs compared: {len(set(ia) | set(ib))}')
PY
    for g in ${SAMPLE//,/ }; do
        if cmp -s "$OLD/$RES/$g.log" "$B/results-sample/$g.log"; then r=identical; else r=DIFFERENT; fi
        echo "group $g log $r: recorded $(sha256sum < "$OLD/$RES/$g.log" | cut -c1-64) head $(sha256sum < "$B/results-sample/$g.log" | cut -c1-64), $(stat -c %s "$B/results-sample/$g.log") bytes"
        if cmp -s "$OLD/$RES/$g.txt" "$B/results-sample/$g.txt"; then echo "group $g script identical"; else echo "group $g script DIFFERENT"; fi
    done
} > $T/logs/head-$NAME-compare.txt 2>&1
M=$B/results-regrade; rm -rf "$M"; mkdir -p "$M"
cp "$OLD/$RES"/*.txt "$OLD/$RES"/*.log "$M/"
R=$T/logs/head-$NAME-regrade.log
echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l) regrade of the recorded groups against the head's build" > "$R"
python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
    --out "$M" --record-budget-findings --record-share-findings "$@" >> "$R" 2>&1
echo "rc=$?" >> "$R"
git -C "$C" status --short --untracked-files=all > $T/logs/head-$NAME-tree-after.txt
echo "$(date +%T) $NAME $(tail -1 "$G") regrade $(tail -1 "$R"); $(grep -c -E 'DIFFERENT|differs' $T/logs/head-$NAME-compare.txt) differences" >> $L

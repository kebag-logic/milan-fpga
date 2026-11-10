#!/bin/bash
# The harness at the final head where the groups' recorded logs come from an earlier commit with a byte-identical
# image: on a fresh clean clone of the head, a fresh build per leg (the head's tree digests), the build's image and
# models compared with the build that ran the groups, a sample of groups re-simulated at the head and their logs
# compared byte for byte with the recorded ones, then every recorded group regraded against the head's build.
# usage: harness_head.sh HEAD
set -u
H=$1
T=<scratch>
. $T/scripts/env.sh
C=$T/hleg-wt-head
L=$T/logs/harness-head.txt
[ -d "$C" ] || bash $T/scripts/clone.sh "$C" "$H" > $T/logs/clone-hleg-head.log 2>&1
test "$(git -C "$C" rev-parse HEAD)" = "$H" || { echo "$(date +%T) clone not at head" >> $L; exit 4; }
for spec in "GN8 8x8 results notice-burst-6 --variant answering-every-port" "GN1 1x1 results notice-burst-6 --variant answering-every-port" \
            "GA8 8x8 results-all acmp-cmd,control" "GA1 1x1 results-all fixture,acmp-cmd"; do
    read -r NAME POINT RES SAMPLE ARGS <<< "$spec"
    OLD=$T/builds/$NAME B=$T/builds-head/$NAME
    mkdir -p "$B"; export TMPDIR=$T/tmp-head-$NAME MAKEFLAGS="-j8 --no-print-directory"; mkdir -p "$TMPDIR"
    G=$T/logs/head-$NAME.log
    echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=all | wc -l) build and sample $SAMPLE" > "$G"
    echo "$(date +%T) $NAME build and sample $SAMPLE start" >> $L
    # shellcheck disable=SC2086
    python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --groups "$SAMPLE" \
        --out "$B/results-sample" --record-budget-findings --record-share-findings --jobs 8 $ARGS >> "$G" 2>&1
    echo "sample rc=$?" >> "$G"
    {
        echo "# $NAME: the head's build ($B) against the build that ran the groups ($OLD)"
        for f in image/ctrl_app.elf split-soc/mapped/image/ctrl_app.elf split-soc/stand-ins/image/ctrl_app.elf; do
            echo "$f old $(sha256sum < "$OLD/$f" | cut -c1-64) head $(sha256sum < "$B/$f" | cut -c1-64)"; done
        for v in $(cd "$OLD" && find . -name 'V*' -type f -perm -u+x -size +100k | sort); do
            echo "$v old $(sha256sum < "$OLD/$v" | cut -c1-64) head $(sha256sum < "$B/$v" 2>/dev/null | cut -c1-64)"; done
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
            echo "group $g log $r: recorded $(sha256sum < "$OLD/$RES/$g.log" | cut -c1-64) head $(sha256sum < "$B/results-sample/$g.log" | cut -c1-64) $(stat -c %s "$B/results-sample/$g.log") bytes"
            if cmp -s "$OLD/$RES/$g.txt" "$B/results-sample/$g.txt"; then echo "group $g script identical"; else echo "group $g script DIFFERENT"; fi
        done
    } > $T/logs/head-$NAME-compare.txt 2>&1
    M=$B/results-regrade; mkdir -p "$M"
    cp "$OLD/$RES"/*.txt "$OLD/$RES"/*.log "$M/"
    R=$T/logs/head-$NAME-regrade.log
    echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l) regrade of the recorded groups against the head's build" > "$R"
    # shellcheck disable=SC2086
    python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
        --out "$M" --record-budget-findings --record-share-findings $ARGS >> "$R" 2>&1
    echo "rc=$?" >> "$R"
    git -C "$C" status --short --untracked-files=all > $T/logs/head-$NAME-tree-after.txt
    echo "$(date +%T) $NAME $(tail -1 "$G") regrade $(tail -1 "$R"); $(grep -c -E 'DIFFERENT|differs' $T/logs/head-$NAME-compare.txt) differences" >> $L
done
echo "$(date +%T) done" >> $L

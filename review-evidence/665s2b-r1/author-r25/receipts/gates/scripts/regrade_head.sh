#!/bin/bash
# Bring each harness gate leg's clone to the final head (only tests, harness grading and docs differ from the commit
# its groups ran at; the image is byte-identical, img-out/) and regrade its groups there, one after another.
# usage: regrade_head.sh HEAD
set -u
H=$1
T=<scratch>
for spec in "GN8 8x8 0 --variant answering-every-port" "GN1 1x1 0 --variant answering-every-port" "GA8 8x8 4" "GA1 1x1 3"; do
    read -r NAME POINT N ARGS <<< "$spec"
    C=$T/hleg-wt-$NAME
    git -C "$C" fetch -q <lane> "$H" && git -C "$C" -c advice.detachedHead=false checkout -q "$H"
    echo "$(date +%T) $NAME at $(git -C "$C" rev-parse HEAD), $(git -C "$C" status --porcelain --untracked-files=no | wc -l) changed" >> $T/logs/finish.txt
    if [ "$N" = 0 ]; then
        ( . $T/scripts/env.sh; B=$T/builds/$NAME; L=$T/logs/$NAME-regrade.log
          echo "HEAD $(git -C "$C" rev-parse HEAD) DIRTY $(git -C "$C" status --porcelain --untracked-files=no | wc -l) regrade" > "$L"
          # shellcheck disable=SC2086
          python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point "$POINT" --build-dir "$B" --reuse-build --regrade \
              --out "$B/results" --record-budget-findings --record-share-findings $ARGS >> "$L" 2>&1
          echo "rc=$?" >> "$L"
          git -C "$C" status --short --untracked-files=all > $T/logs/$NAME-tree-after.txt )
    else
        bash $T/scripts/regrade.sh "$NAME" "$POINT" "$N"
    fi
    echo "$(date +%T) $NAME regrade $(tail -1 $T/logs/$NAME-regrade.log)" >> $T/logs/finish.txt
done

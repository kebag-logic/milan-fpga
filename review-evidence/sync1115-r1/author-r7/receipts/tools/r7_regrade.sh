#!/bin/bash
# r7_regrade.sh LEG...: each of round 7's re-simulated legs graded again (--reuse-build --regrade) by the round-7
# harness, into r7/legs/<leg>/: its group logs hard-linked from their run's results (a regrade only reads them), its
# scripts copied. A seed leg (s<tag>) runs its seed clone's harness (10b2fe21, the seed's MAC, the head's harness
# directory); the product and valid-destinations legs (p81, v1, v81) the checkout that built them, r7/c-head, moved to the head (a build attests its inputs under its own checkout). Each build must attest
# against the checkout. Log and rc: r7/legs/<leg>.log, <leg>.log.rc.
set -u
S=<scratch>; . $S/bin/env.sh
for leg in "$@"; do
  case $leg in
    s*) t=${leg#s}; C=$S/seeds/c-sync-$t; B=$S/seeds/b7-sync-$t; R=$B/results; P=8x8-1if; A=(--groups save-held,save-starved) ;;
    p81) C=$S/r7/c-head; B=$S/r7/b81; R=$B/results; P=8x8-1if; A=(--groups save-held,save-starved) ;;
    v1) C=$S/r7/c-head; B=$S/r7/b1x1-V; R=$B/results; P=1x1; A=(--variant valid-destinations) ;;
    v81) C=$S/r7/c-head; B=$S/r7/b81-V; R=$B/results; P=8x8-1if; A=(--variant valid-destinations) ;;
    *) echo "unknown leg $leg"; continue ;;
  esac
  O=$S/r7/legs/$leg; log=$S/r7/legs/$leg.log; mkdir -p "$O"; rm -f "$log.rc"
  for f in "$R"/*.log; do g=$(basename "$f" .log); ln -f "$f" "$O/$g.log"; cp "$R/$g.txt" "$O/$g.txt"; done
  {
    echo "HEAD $(git -C "$C" rev-parse HEAD) PORCELAIN $(git -C "$C" status --porcelain --untracked-files=no | wc -l) harness $(diff -rq -x __pycache__ "$C/tb/verilator/ctrl_service_budget" "$S/r7/c-final/tb/verilator/ctrl_service_budget" >/dev/null && echo '= 544fd72c' || echo 'differs from 544fd72c') leg $leg point $P args ${A[*]} start $(date +%FT%T)"
    python3 -B "$C/tb/verilator/ctrl_service_budget/run.py" --point $P --build-dir "$B" --reuse-build --regrade --out "$O" \
      --record-budget-findings --record-share-findings "${A[@]}"
    rc=$?; echo "END rc=$rc $(date +%FT%T)"; echo $rc > "$log.rc"
  } > "$log" 2>&1
  echo "$leg rc=$(cat "$log.rc") $(grep -m1 'groups graded' "$log" | cut -c1-120)"
done
echo DONE

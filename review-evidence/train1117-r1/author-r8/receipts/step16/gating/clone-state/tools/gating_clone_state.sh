#!/bin/bash
# gating_clone_state.sh HEAD: each gating chain's clone (gate15/clones/g1x1, g8x8) at HEAD and clean (R865-4-F2).
# For each point:
#   - now: `git rev-parse HEAD` and `git status --porcelain` (untracked files included), each line printed;
#   - then: the head and porcelain lines the chain itself printed into its log as it ran, at the clone (clone.sh),
#     the boot simulation (boot.sh), the prep (gprep.sh, before and after) and the Vivado build (gbuild.sh).
# Exit 0 when every head named is HEAD and every porcelain is empty; 1 otherwise.
# Run it as: bash gating_clone_state.sh HEAD > LOG 2>&1; echo $? > LOG.rc
set -u
S=${SCRATCH:-<scratch>}
want=$1 rc=0
echo "gating_clone_state.sh $want $(date -Iseconds)"
for p in 1x1 8x8; do
  C=$S/gate15/clones/g$p L=$S/gate15/gate-$p.log
  head=$(git -C "$C" rev-parse HEAD) porcelain=$(git -C "$C" status --porcelain)
  echo "== $p/1if: clone gate15/clones/g$p"
  echo "now: HEAD $head"
  echo "now: git status --porcelain: $(printf '%s' "$porcelain" | grep -c .) line(s)${porcelain:+; }$porcelain"
  [ "$head" = "$want" ] && [ -z "$porcelain" ] || rc=1
  echo "then (the chain's log, gate-$p.log):"
  grep -E '^(head [0-9a-f]{40}( porcelain [0-9]+|;? status:? ?.*)|# head [0-9a-f]{40} status: ?.*|status after prep: ?.*)$' "$L" |
    sed 's/^/  /'
  # every head the log names is HEAD, and every status it prints is empty (the clone's porcelain line count 0)
  grep -oE '[0-9a-f]{40}' <(grep -E '^(# )?head ' "$L") | grep -vx "$want" && rc=1
  awk '/^(# )?head [0-9a-f]{40} porcelain / { if ($NF != "0") { print "NOT CLEAN: " $0; bad = 1 } }
       /^(# )?head [0-9a-f]{40};? status/ || /^status after prep/ { s = $0; sub(/^.*status( after prep)?:? */, "", s)
         if (s != "") { print "NOT CLEAN: " $0; bad = 1 } }
       END { exit bad }' "$L" || rc=1
done
echo "END rc=$rc $(date -Iseconds)"
exit $rc

#!/bin/sh
# The repository's complete gate (`make` at the root: contract, tb, lint,
# docs), run as its own recipes in make's order, one segment per call.
# This lane's session caps one foreground command at 10 minutes and the whole
# `make` takes longer on this host, so each segment is its own foreground
# call. Every segment is the recipe the root Makefile (or the sub-Makefile it
# enters) runs, unchanged, except `engine-mutants`: the engine suite's
# `python3 mutants.py` is run as four disjoint round-robin slices of the same
# MUTATIONS list through the arm's own main(), in parallel, with the arm's
# verilator build at -j 2 per slice (8 compile jobs at most). See
# engine_mutants_slice.py. full_gate.sh is the one-shot `make` equivalent.
#
# Usage: gate.sh <label> <segment>
#   segments, in order: begin contract ucpu parser engine-run engine-mutants
#                       gaskets tsngen bench lint docs end
# Appends to receipts/<label>.log; each segment's exit goes to
# receipts/<label>.segments; `end` writes receipts/<label>.exit (0 only when
# every segment ran and exited 0).
set -u
. $REVIEWS/gptp68-a188-packet/scripts/env.sh
label=$1; seg=$2
R=$A188_PACKET/receipts
S=$A188_PACKET/scripts
log=$R/$label.log
cd "$A188_LANE" || exit 2
ORDER="contract ucpu parser engine-run engine-mutants gaskets tsngen bench lint docs"

case $seg in
begin)
  : > "$R/$label.segments"
  {
    echo "# label: $label"
    echo "# start: $(date -Is)"
    echo "# host nproc: $(nproc); load: $(cut -d' ' -f1-3 /proc/loadavg)"
    echo "# verilator: $(command -v verilator) -> $(verilator --version)"
    echo "# python3: $(python3 --version 2>&1); make: $(make --version | head -1)"
    echo "# base: c1b617435824929a790739ea8585c3fe1a328cc0"
    echo "# head: $(git rev-parse HEAD) tree: $(git rev-parse 'HEAD^{tree}')"
    echo "# segments: $ORDER"
    echo "# tree-status-before:"
    git status --porcelain
  } > "$log"
  exit 0 ;;
end)
  rc=0
  for s in $ORDER; do
    got=$(awk -v s="$s" '$1 == s { e = $2 } END { print e }' "$R/$label.segments")
    echo "# segment $s: exit ${got:-MISSING}" >> "$log"
    [ "$got" = 0 ] || rc=1
  done
  {
    echo "# end: $(date -Is)"
    echo "# exit: $rc"
    echo "# head: $(git rev-parse HEAD) tree: $(git rev-parse 'HEAD^{tree}')"
    echo "# tree-status-after:"
    git status --porcelain
  } >> "$log"
  echo "$rc" > "$R/$label.exit"
  echo "$label exit=$rc"
  exit $rc ;;
contract)       set -- make contract ;;
ucpu)           set -- make -C tb/verilator/ucpu ;;
parser)         set -- make -C tb/verilator/parser ;;
engine-run)     set -- make -C tb/verilator/engine run ;;
engine-mutants) set -- sh -c "cd tb/verilator/engine && pids= && \
  for k in 0 1 2 3; do python3 $S/engine_mutants_slice.py \$k 4 > $R/$label.mut\$k.tmp 2>&1 & pids=\"\$pids \$!\"; done; \
  rc=0; for p in \$pids; do wait \$p || rc=1; done; \
  for k in 0 1 2 3; do echo \"-- slice \$k of 4 --\"; cat $R/$label.mut\$k.tmp; rm -f $R/$label.mut\$k.tmp; done; \
  exit \$rc" ;;
gaskets)        set -- make -C tb/verilator/gaskets ;;
tsngen)         set -- make -C tb/tsngen ;;
bench)          set -- make -C bench/arty test ;;
lint)           set -- make lint ;;
docs)           set -- make docs ;;
*) echo "unknown segment $seg"; exit 2 ;;
esac

{ echo "# segment: $seg"; echo "# command: $*"; echo "# start: $(date -Is)"; } >> "$log"
"$@" >> "$log" 2>&1
rc=$?
{ echo "# end: $(date -Is)"; echo "# segment-exit: $seg $rc"; } >> "$log"
echo "$seg $rc" >> "$R/$label.segments"
echo "$seg exit=$rc"
exit $rc

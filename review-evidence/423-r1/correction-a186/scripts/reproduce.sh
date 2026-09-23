#!/bin/sh
# Regenerate every final receipt for one exact lane head.
# Usage: scripts/reproduce.sh <full-head-sha>
# Needs: git >= 2.39, python3, localedef with the en_US/zh_TW sources and the
# ISO-8859-1/BIG5 charmaps (installed locales are never changed), the lane
# checkout clean at <full-head-sha>, and its gptp-processor submodule objects.
# Temporary trees live under ../scratch; delete it afterwards.
set -eu
head=$1
here=$(cd "$(dirname "$0")" && pwd)
packet=$(dirname "$here")
lane=$LANES/423-retained-redundant-replay
short=$(printf '%s' "$head" | cut -c1-8)
cd "$packet"
mkdir -p scratch/locales receipts
for spec in "zh_TW BIG5" "en_US ISO-8859-1"; do
  set -- $spec
  [ -d "scratch/locales/$1.$2" ] || localedef --no-archive -i "$1" -f "$2" "scratch/locales/$1.$2"
done
tree=$(git -C "$lane" rev-parse "$head^{tree}")
# 1. Focused gates in the lane itself (clean-at-head is checked first).
python3 -B scripts/run_gates.py "head-$short" "$head" > "receipts/gates-head-$short.txt" 2>&1
# 2. The exact committed sources, for probes that copy or mutate them.
rm -rf "scratch/head-$short"
mkdir -p "scratch/head-$short"
git -C "$lane" archive "$head" scripts | tar -x -C "scratch/head-$short"
# 3. Mutation, restoration and parent-locale probes (8 workers).
python3 -B scripts/mutate_head.py "scratch/head-$short" "head-$short" \
  > "receipts/mutations-head-$short.txt" 2>&1
# 4. The R244-1 finding probes (Big5 merge/linear, multi-target stdout).
python3 -B scripts/run_probes.py "scratch/head-$short" "head-$short" \
  > "receipts/probes-head-$short.txt" 2>&1
# 5. The reviewer's guard histories, mutants copying the new transport module.
GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null TMPDIR="$packet/scratch" \
  python3 -B scripts/probe_guards_adapted.py "$packet/scratch/head-$short" \
  "$packet/scratch/guards-$short" > "receipts/probe-guards-head-$short.txt" 2>&1
# 6. Actual gPTP processor PR61/PR62 verdicts and the decision's patch hashes.
sh scripts/actual_history.sh "head-$short" \
  "$packet/scratch/head-$short/scripts/check_merge_containment.py" \
  > "receipts/actual-pr61-pr62-head-$short.txt" 2>&1
# 7. The published F1 examples, archive taken at this head.
env -u LOCPATH HEAD_SHA_OVERRIDE="$head" bash scripts/locale_transport_probe_adapted.sh \
  "$lane" "$packet/scratch/f1-$short" "$packet/receipts/f1-published-examples-head-$short" \
  > "receipts/f1-published-examples-head-$short.log" 2>&1
# 8. Checkout and submodule integrity by direct hashing.
python3 -B scripts/r244-probes/integrity.py "$lane" "$head" "$tree" \
  > "receipts/integrity-head-$short.json"
echo "reproduced receipts for $head (tree $tree)"

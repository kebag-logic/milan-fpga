#!/usr/bin/env bash
# Classify every path in the merged head: which side's blob it carries.
# usage: merge_composition.sh <repo> [base] [ours] [theirs] [merged]
set -euo pipefail
R=${1:?repo}; B=${2:-b2db3a970cedbbff2f8ba813acb96122c442bc58}
O=${3:-921fff59d6e1243284e477f7a368173018420d35}
T=${4:-0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff}
M=${5:-47afa74d5cb7cf67ec1f606a0b8ea05fda3e3346}
cd "$R"
blob() { git ls-tree "$1" -- "$2" | awk '{print $1" "$3}'; }
paths=$( { git ls-tree -r --name-only "$B"; git ls-tree -r --name-only "$O"; git ls-tree -r --name-only "$T"; git ls-tree -r --name-only "$M"; } | sort -u)
bad=0; declare -A n
while IFS= read -r p; do
  b=$(blob "$B" "$p"); o=$(blob "$O" "$p"); t=$(blob "$T" "$p"); m=$(blob "$M" "$p")
  if [ "$o" = "$b" ] && [ "$t" = "$b" ]; then c=untouched; [ "$m" = "$b" ] || c=EXTRA_CHANGE
  elif [ "$t" = "$b" ]; then c=branch-only; [ "$m" = "$o" ] || c=BRANCH_ONLY_MISMATCH
  elif [ "$o" = "$b" ]; then c=main-only; [ "$m" = "$t" ] || c=MAIN_ONLY_MISMATCH
  else c=both-sides; fi
  n[$c]=$(( ${n[$c]:-0} + 1 ))
  case $c in untouched) ;; both-sides) echo "$c $p";; [A-Z]*) echo "$c $p"; bad=1;; *) echo "$c $p";; esac
done <<< "$paths"
for k in "${!n[@]}"; do echo "COUNT $k ${n[$k]}"; done | sort
echo "RESULT $([ $bad = 0 ] && echo PASS || echo FAIL)"
exit $bad

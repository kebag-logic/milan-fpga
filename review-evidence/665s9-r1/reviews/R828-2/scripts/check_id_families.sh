#!/usr/bin/env bash
# check_id_families.sh <repo> <rev>...: for each rev, list every check-ID prefix used in
# tb/verilator/mbx/suite.hpp and suite_face.hpp, and the files each one appears in.
set -euo pipefail
R=$1; shift
for rev in "$@"; do
  echo "=== $rev"
  for f in suite.hpp suite_face.hpp; do
    git -C "$R" show "$rev:tb/verilator/mbx/$f" | grep -oE '"[A-Z][0-9]{1,2} ' | tr -d '" ' | sort -u | sed "s/\$/ $f/"
  done | awk '{a[$1]=a[$1]" "$2} END {for (k in a) print k":"a[k]}' | sort -V | awk -F: '{n=split($2,x," "); print (n>1?"SHARED ":"       ") $0}'
  echo "--- labels starting U0 / H0 at $rev"
  git -C "$R" grep -n -E '"(U0|H0) ' "$rev" -- tb/verilator/mbx/ | sed "s|^$rev:||"
done

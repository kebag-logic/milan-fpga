#!/usr/bin/env bash
# The self-test at each revision under each interpreter, from `git archive`
# scratch extracts (the checkout is not written).
#   interpreter_matrix.sh <checkout> <python>... -- <rev>...
set -uo pipefail
checkout=$1; shift
pys=(); while [ "$1" != "--" ]; do pys+=("$1"); shift; done; shift
for rev in "$@"; do
  d=$(mktemp -d $AEM_SCRATCH-mx-XXXX)
  git -C "$checkout" archive "$rev" avdecc hdl/common/csr | tar -x -C "$d"
  for py in "${pys[@]}"; do
    (cd "$d" && "$py" -B avdecc/gen_aem_store.py --self-test > out.txt 2>&1
     rc=$?
     echo "rev=$(git -C "$checkout" rev-parse --short "$rev") $("$py" --version) exit=$rc last: $(grep -E 'Error|self-test: ' out.txt | tail -1)")
  done
  rm -rf "$d"
done

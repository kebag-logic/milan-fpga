#!/usr/bin/env bash
# Run the parent consumer's quick static gates on a disposable parent clone
# whose processor gitlink is the head under review. No builds, no simulators.
# Usage: parent-static-gates.sh <parent-clone>
set -u
cd "$1"
echo "parent $(git rev-parse HEAD) processor-gitlink $(git ls-tree HEAD protocol-processor | awk '{print $3}') checked-out $(git -C protocol-processor rev-parse HEAD)"
git status --porcelain --ignore-submodules=none | sed 's/^/dirty: /'
for cmd in "python3 scripts/check_py_idiom.py" "python3 scripts/check_cpp_idiom.py" \
           "python3 scripts/check_rtl_source_lists.py" "python3 scripts/pp_srcs.py --check --selftest" \
           "python3 scripts/check_port_contracts.py" "python3 scripts/measure_naming.py --check" \
           "python3 scripts/measure_test_evidence.py --check" "python3 scripts/docs_check.py" \
           "python3 scripts/gen_toc.py --verify-anchors"; do
  out=$($cmd 2>&1); rc=$?
  echo "=== $cmd -> rc=$rc"; printf '%s\n' "$out" | tail -n 4
done

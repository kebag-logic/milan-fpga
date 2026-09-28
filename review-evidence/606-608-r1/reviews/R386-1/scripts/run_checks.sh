#!/bin/sh
# Run the pin-record and evidence checks in a disposable tree, one receipt each.
# usage: run_checks.sh <tree>   Environment: RECEIPTS (output directory).
set -u
tree=$1
cd "$tree" || exit 2
run() {
    name=$1; shift
    log="$RECEIPTS/30-$name.log"
    echo "parent=$(git rev-parse HEAD) processor=$(git -C protocol-processor rev-parse HEAD)" > "$log"
    echo "command: $*" >> "$log"
    "$@" >> "$log" 2>&1
    rc=$?
    echo "rc=$rc" >> "$log"
    echo "$name rc=$rc"
}
run measure_test_evidence python3 scripts/measure_test_evidence.py --check
run check_nvm_capture python3 scripts/check_nvm_capture.py
run check_submodule_docs python3 scripts/check_submodule_docs.py
run submodule_boundaries_gen python3 docs/diagrams/submodule_boundaries.gen.py --check
run pp_srcs python3 scripts/pp_srcs.py --check --selftest
run check_rtl_source_lists python3 scripts/check_rtl_source_lists.py
run check_port_contracts python3 scripts/check_port_contracts.py
run check_cpp_idiom python3 scripts/check_cpp_idiom.py
run docs_check python3 scripts/docs_check.py
git status --porcelain=v1 --ignore-submodules=none > "$RECEIPTS/30-tree-status-after-checks.txt"

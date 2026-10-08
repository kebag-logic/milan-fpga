#!/usr/bin/env bash
# Lane B: focused suites, lint and documentation gates on an exported tree.
# Args: TREE RECEIPT_PREFIX. Each step writes <prefix>-<step>.log and .rc.
set -uo pipefail
TREE=$1; R=$2
step() { local name=$1; shift; ( cd "$TREE" && "$@" ) >"$R-$name.log" 2>&1; echo $? >"$R-$name.rc"; }
step suite-aecp_notify   make -C tb/aecp_notify
step suite-originator    make -C tb/originator
step suite-ca_originator make -C tb/ca_originator
step lint_hdl            ./scripts/lint_hdl.sh
step make_check          make -j16 check
step gen_matrix          python3 scripts/gen_matrix.py --check
step suite-pp_top        make -C tb/pp_top

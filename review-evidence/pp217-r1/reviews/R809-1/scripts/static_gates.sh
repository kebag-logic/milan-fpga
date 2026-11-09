#!/usr/bin/env bash
# The processor's static gates at the reviewed head, each with its own rc line.
# Run from a git checkout of the head (make stale reads commit times).
cd "$1" || exit 2
BASE=044cb25f
step() { name=$1; shift; echo "=== $name: $*"; "$@"; rc=$?; echo "=== $name rc=$rc"; }
step make_check make check
step lint_hdl bash scripts/lint_hdl.sh
step gen_matrix python3 scripts/gen_matrix.py --check
step diff_check git diff --check $BASE HEAD
step req_tags_static python3 scripts/check-req-tags.py
step aecpcmd python3 -B scripts/check_aecp_commands.py
step desc_untouched git diff --quiet $BASE HEAD -- hdl/aecp/desc hdl/srp
step top_ports bash -c "diff <(git show $BASE:hdl/top/protocol_processor_top.sv | awk '/^module protocol_processor_top/,/^\);/') <(git show HEAD:hdl/top/protocol_processor_top.sv | awk '/^module protocol_processor_top/,/^\);/')"
exit 0

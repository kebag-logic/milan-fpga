#!/bin/bash
# Round-2 extra checks on an export of the committed head, each logged with
# its command and rc: the docs gate under an isolated interpreter (from the
# tree root and from another directory), git diff --check against the base,
# and both reviewers' planted-mutant scripts against the head harness.
# usage: extra_checks.sh <head>
set -u
S=<scratch>
LANE=<lane>
HEAD=$1
export PATH=$S/bin:<user-bin>:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin
export VERILATOR_ROOT=<verilator-5.050-root>
export TMPDIR=$S/tmp
X=$S/extra2; T=$S/revprobes/tree2
rm -rf "$X" "$T" "$S/revprobes/work771b" "$S/revprobes/out771b" "$S/revprobes/work772b"
mkdir -p "$X" "$T"
git -C "$LANE" archive "$HEAD" | tar -x -C "$T"
run() { # log cwd cmd...
  local log=$1 cwd=$2; shift 2
  { echo "\$ (cd $cwd && $*)"; (cd "$cwd" && "$@"); echo "rc=$?"; } > "$X/$log" 2>&1
  tail -1 "$X/$log" | sed "s/^/$log: /"
}
run check_docs-isolated.log "$T" python3 -I scripts/check_docs.py
run check_docs-selftest-isolated.log "$T" python3 -I scripts/check_docs.py --selftest
run check_docs-selftest-isolated-other-cwd.log /tmp python3 -I "$T/scripts/check_docs.py" --selftest
run check_docs-selftest.log "$T" python3 scripts/check_docs.py --selftest
run diff-check.log "$LANE" git diff --check 3e3a4e7695ce66eed609089f280c2fba45b24d36 "$HEAD"
run r771-reviewer-mutants.log "$S/revprobes" python3 -I r771-scripts/reviewer_mutants.py "$T" "$S/revprobes/work771b" "$S/revprobes/out771b"
run r772-extra-mutants.log "$S/revprobes" python3 -I r772-probes/extra_mutants.py "$T" "$S/revprobes/work772b"

#!/usr/bin/env bash
# R307-3 delta review of PR #560 at 9d66cfe0: reproduce every receipt.
# Usage: reproduce.sh <clone> <packet> <python-with-pinned-renderer> [<verilator>]
#   <clone>   detached clone at 9d66cfe0dc87ffe4a5f45691d5c86b041b050b38, submodules initialised
#   <packet>  output directory (receipts/ and scratch/ are created in it)
#   <python>  an interpreter with tools/markdown/requirements.txt installed (--require-hashes)
#   <verilator> optional; when given, runs the focused notify + gsi-mutants leg (Verilator 5.050)
# Every step runs in the foreground. The clone must be restored afterwards
# (the leg leaves obj_notify/, two ROM images and __pycache__ directories).
set -u
CLONE=$1; PKT=$2; PY=$3; VL=${4:-}
HEAD=9d66cfe0dc87ffe4a5f45691d5c86b041b050b38
PRIOR=224ec0e9a9fa129924bf8f0433cf70b4140f7bd2
R=$PKT/receipts; S=$PKT/scratch; mkdir -p "$R" "$S"
cd "$CLONE" || exit 2
[ "$(git rev-parse HEAD)" = "$HEAD" ] || { echo "clone is not at $HEAD"; exit 2; }

# F1: docs_check in git archives with no submodule content (head, and prior head as control)
for rev in $HEAD $PRIOR; do
  rm -rf "$S/archive_$rev"; mkdir -p "$S/archive_$rev"
  git archive "$rev" | tar -x -C "$S/archive_$rev"
  ( cd "$S/archive_$rev" && python3 scripts/docs_check.py; echo "rc=$?" ) > "$R/docs_check_archive_$rev.txt" 2>&1
done
( python3 scripts/docs_check.py; echo "rc=$?" ) > "$R/docs_check_clone.txt" 2>&1

# F1: pinned link targets exist upstream at the gitlink, with the same blob as the local pin
for p in docs/architecture/06_aecp_engine.md docs/architecture/05_acmp_engine.md; do
  gh api "repos/Mister-M-alt/protocol-processor-control-plane-avb-milan/contents/$p?ref=990f96526bb89356c963a260ebbdcf2a77e6623a" --jq '.path+" "+.sha'
  echo "local $p $(git -C protocol-processor rev-parse 990f96526bb89356c963a260ebbdcf2a77e6623a:$p)"
done > "$R/link_targets_remote.txt" 2>&1

# Assigned gates
for a in --verify-anchors --check --selftest; do
  ( "$PY" scripts/gen_toc.py $a; echo "rc=$?" ) > "$R/gen_toc_${a#--}.txt" 2>&1
done
( python3 scripts/measure_test_evidence.py --check; echo "rc=$?" ) > "$R/measure_test_evidence_check.txt" 2>&1
( python3 scripts/measure_test_evidence.py --selftest; echo "rc=$?" ) > "$R/measure_test_evidence_selftest.txt" 2>&1
{
  for b in $PRIOR 573f0052a0e4412e81f0845438fcec2086ce5d55; do "$PY" scripts/check_em_dash.py --base $b; echo "rc=$?"; done
  "$PY" scripts/check_doc_style.py; echo "rc=$?"
} > "$R/em_dash_doc_style.txt" 2>&1

# F2: campaign size derived from the drivers
( python3 "$PKT/scripts/campaign_counts.py" "$CLONE"; echo "rc=$?" ) > "$R/campaign_counts.txt" 2>&1

if [ -n "$VL" ]; then
  ( VERILATOR=$VL VERILATOR_JOBS=8 make -C tb/verilator/milan_dp notify gsi-mutants; echo "rc=$?" ) > "$R/notify_gsi_mutants.log" 2>&1
fi

# Delta scope and the remaining assigned static gates
{
  for c in scripts/check_doc_paths.py scripts/check_py_idiom.py "scripts/check_em_dash.py --base c266432dcb0cdd464205823a3d82cad260eedde2"; do
    echo "\$ python3 $c"; "$PY" $c 2>&1 | tail -3; echo "rc=${PIPESTATUS[0]}"
  done
  git diff --check $PRIOR $HEAD; echo "diff-check rc=$?"
  git diff --numstat $PRIOR $HEAD
  git ls-tree -r $HEAD | awk '$2=="commit"'
  git ls-tree -r $PRIOR | awk '$2=="commit"'
} > "$R/delta_scope_and_extra_gates.txt" 2>&1

# Hosted check runs at the exact head (read only)
gh api "repos/kebag-logic/milan-fpga/commits/$HEAD/check-runs?per_page=100" \
  --jq '.check_runs[] | [.name,.status,(.conclusion//"-"),.html_url] | @tsv' | sort > "$R/hosted_check_runs.tsv"

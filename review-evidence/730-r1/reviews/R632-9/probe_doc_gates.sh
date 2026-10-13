#!/usr/bin/env bash
# Mutation probes: each plants one defect into the composed
# docs/testing/CI_WORKFLOWS.md and requires the named gate to fail, then
# restores the exact committed bytes.
# Usage: probe_doc_gates.sh <candidate-checkout> <receipt-dir> <renderer-python>
set -u
repo=$(cd "$1" && pwd)
out=$(mkdir -p "$2" && cd "$2" && pwd)
py=$3
doc=docs/testing/CI_WORKFLOWS.md
cd "$repo" || exit 2
restore() { git checkout -q -- "$doc"; }
probe() { # name, sed-expression, gate...
  local name=$1 expr=$2; shift 2
  sed -i "$expr" "$doc"
  if git diff --quiet -- "$doc"; then echo "$name: PLANT DID NOT APPLY"; restore; return; fi
  "$@" >"$out/$name.log" 2>&1; local rc=$?
  restore
  if [ "$rc" -ne 0 ]; then echo "$name: KILLED rc=$rc"; else echo "$name: SURVIVED rc=0"; fi
}
# P1: an em dash in a line this PR added, COMMITTED in a disposable shared
# clone (the gate diffs committed history, so a working-tree plant is unseen).
p1=$(mktemp -d "${out}/../../scratch/p1.XXXX")
git clone -q --shared --no-checkout "$repo" "$p1/c" && git -C "$p1/c" checkout -q --detach "$(git rev-parse HEAD)"
sed -i 's/therefore only a staging range\./therefore only a staging range \xe2\x80\x94 nothing more./' "$p1/c/$doc"
git -C "$p1/c" -c user.name=probe -c user.email=probe@invalid commit -q -am plant
( cd "$p1/c" && "$py" -I scripts/check_em_dash.py --base ada26e56ac42ee5de311aef84cb86c8435b97cee ) >"$out/P1_em_dash_in_pr_line.log" 2>&1
rc=$?; [ "$rc" -ne 0 ] && echo "P1_em_dash_in_pr_line: KILLED rc=$rc" || echo "P1_em_dash_in_pr_line: SURVIVED rc=0"
rm -rf "$p1"
# P2: rename the heading that TESTING.md, RUNNING_TESTS.md and the milan_dp README link to.
probe P2_anchor_heading \
  's/^## Exhaustive validation$/## Exhaustive validation runs/' \
  "$py" -I scripts/gen_toc.py --verify-anchors
# P3 (informational): restore the pre-#730 slot CPU wording. Expected to
# SURVIVE: no gate reads that prose, so its composition was judged by reading.
probe P3_ci_events_contract \
  's/^- Slot N owns the CPUs `20N` to `20N+19`/- Slot N owns the CPUs `4N` to `4N+3`/' \
  python3 -I scripts/ci_events.py --check
git diff --quiet -- "$doc" && echo "restored: $(git rev-parse HEAD:$doc) == $(git hash-object $doc)"

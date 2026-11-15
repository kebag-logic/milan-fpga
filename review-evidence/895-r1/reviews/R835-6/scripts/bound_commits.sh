#!/bin/sh
# bound_commits.sh REPO: for each commit the round-11 text binds a figure to, and for HEAD, print its first-parent
# subject, whether it is an ancestor of HEAD, and the constants the bound sentences rest on. Read-only.
set -eu
R=$1
for c in 07ed787e 7e3db6b9 4c9757ee 0c93071e bf0844f1 62298ab5 HEAD; do
  echo "== $c $(git -C "$R" log -1 --format='%h %p | %s' "$c" | cut -c1-140)"
  git -C "$R" merge-base --is-ancestor "$c" HEAD && echo "   ancestor of HEAD"
  git -C "$R" show "$c:sw/firmware/ctrl/aecp/aecp_mbx.h" | grep -E 'define (AECP_PACE_MS|AECP_QUEUED_MS) ' | sed 's/^/   /'
  git -C "$R" show "$c:sw/firmware/ctrl/loop/ctrl_loop.h" | grep -E 'define (CTRL_LOOP_SLICE_US|CTRL_LOOP_TX_MS) ' | sed 's/^/   /'
  git -C "$R" show "$c:tb/verilator/ctrl_service_budget/poll_grade.py" | grep -oE '^STATED_US = \{1: dict\(base=[0-9]+' | sed 's/^/   /'
done
echo "== 7e3db6b9 in round 7B's first-parent run 4c9757ee..0c93071e:"
git -C "$R" log --format='   %h %s' --first-parent 4c9757ee..0c93071e | cut -c1-110

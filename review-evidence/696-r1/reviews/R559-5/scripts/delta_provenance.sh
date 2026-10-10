#!/bin/sh
# Delta provenance for PR #706 round 5. Usage: delta_provenance.sh <repo>
set -eu
cd "$1"
H=6de3904ec2d6b2f04325c94c7686519ecd92a202; M=941ba7463ebfc4fb961db78842ce5012e4f96928
S=30073ee9cc30d1d8fc12163ab3e3f8dc27cc126f; D=e8454e2751d05b02ee8e5a571857589ab358ab86
echo "parents of merge: $(git rev-parse $M^1) $(git rev-parse $M^2)"
echo "parent of head:   $(git rev-parse $H^1)"
echo "auto merge-tree of $S + $D: $(git merge-tree --write-tree $S $D)"
echo "recorded merge tree:          $(git rev-parse $M^{tree})"
echo "--- PR file set (dev..head):"; git diff --name-only $D $H | tee /tmp/pr_files.$$
echo "--- merge diff restricted to PR files ($S..$M):"; git diff --stat $S $M -- $(cat /tmp/pr_files.$$)
echo "--- same files changed on dev side since prior merged dev 8b61b709:"; git diff --stat 8b61b70902f3ebf118e56967277e2686731081bd $D -- $(cat /tmp/pr_files.$$)
echo "--- head commit diff ($M..$H):"; git diff --stat $M $H
echo "--- RTL/test/record/firmware bytes changed since source $S (expect empty):"
git diff --stat $S $H -- hdl tb/verilator/maap sw/firmware/ctrl/test/test_maap_differential.cpp sw/firmware/ctrl/test/maap_differential.py syn/ooc/pp_resource_baseline.json sw/litex
echo "--- head vs dev: only PR files differ, dev-side files identical:"; git diff --stat $D $H | tail -n 1
echo "--- dev changes vs head outside PR files (expect empty):"; git diff --stat $D $H -- . $(sed 's/^/:!/' /tmp/pr_files.$$)
echo "--- blob of baseline JSON at $S / $H:"; git rev-parse $S:syn/ooc/pp_resource_baseline.json $H:syn/ooc/pp_resource_baseline.json
rm -f /tmp/pr_files.$$

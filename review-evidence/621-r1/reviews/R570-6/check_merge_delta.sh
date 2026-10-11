#!/usr/bin/env bash
# Recomputes the plain merge of the reviewed PR head and dev, and compares it
# with the published merge head. Usage: check_merge_delta.sh <checkout>
set -u
cd "$1" || exit 2
ours=2cf985f3206dd519d80142fd2479afe24c3051f6
theirs=cfadd767a7ad47aaee68de655e1066cc000fb8a0
head=8c3e892c2b7130d88d16fb6a26136856975e1ea9
echo "head parents: $(git rev-parse "$head^1" "$head^2" | tr '\n' ' ')"
echo "merge base: $(git merge-base $ours $theirs)"
plain=$(git merge-tree --write-tree --name-only $ours $theirs | head -1)
echo "plain merge tree (with conflict markers where conflicted): $plain"
echo "conflicted paths:"; git merge-tree --write-tree --name-only $ours $theirs | sed -n '2,/^$/p'
echo "head tree: $(git rev-parse "$head^{tree}")"
echo "paths where head differs from the plain merge:"; git diff --raw $plain "$head^{tree}"
echo "generated files, blob per side:"
for p in docs/diagrams/PNG_MANIFEST.json docs/diagrams/submodule_boundaries.drawio docs/diagrams/submodule_boundaries.png docs/diagrams/submodule_boundaries.svg docs/diagrams/timesync_chain.drawio docs/diagrams/timesync_chain.png docs/diagrams/timesync_chain.svg; do
  echo "  $p ours=$(git rev-parse $ours:$p) dev=$(git rev-parse $theirs:$p) head=$(git rev-parse $head:$p)"
done
echo "gitlinks at head:"; git ls-tree $head gptp-processor protocol-processor third_party/lwSRP third_party/verilog-axis external
echo "PR-owned surfaces changed by the merge (expect none):"
git diff --stat $ours $head -- tb/verilator/milan_dp tb/verilator/milan_dp_gm_steps tb/verilator/gptp_plane hdl/ieee8021as gptp-processor scripts/suite_shards.py scripts/check_nvm_capture.py tb/verilator/nvm_capture_cpu
echo "hdl/ differences dev -> head (expect none): $(git diff $theirs $head -- hdl/ | wc -l) lines"

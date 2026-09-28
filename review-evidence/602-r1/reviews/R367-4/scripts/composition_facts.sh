#!/usr/bin/env bash
# Usage: composition_facts.sh <repo>. Records how the candidate composes.
set -u
R=$1
H=a3f95a4cea1faa3470b65b4ffc8a9bb3dc1b0c9c   # candidate
P=1a3c716f6e9fbc1c3227bce0a287ac943944fcbb   # train parent (after #595)
S=d09c72ea2b0be1a2df3e18e77774f14f6df3242c   # reviewed PR source head
D=7a7582f03ce5ba7863a90ac342c21be18d90db0b   # live dev
g() { git -C "$R" "$@" 2>/dev/null; }
echo "candidate $H tree $(g rev-parse $H^{tree}) parents $(g log -1 --format=%P $H)"
echo "recomputed merge-tree($P,$S): $(g merge-tree --write-tree $P $S | head -1) rc=${PIPESTATUS[0]}"
MB=$(g merge-base $P $S); echo "merge-base(train,source) $MB"
echo "live dev $D tree $(g rev-parse $D^{tree}); #70 train step c08becbbf tree $(g rev-parse c08becbbf^{tree})"
echo "train first-parent steps after live dev:"; g log --format='  %h %s' --first-parent c08becbbf..$P
echo "files changed by both train ($MB..$P) and source ($MB..$S):"
comm -12 <(g diff --name-only $MB $P | sort) <(g diff --name-only $MB $S | sort) | sed 's/^/  /'
echo "per-train-step touches of the shared files:"
for c in $(g rev-list --first-parent $MB..$P); do
  f=$(g diff --name-only $c^1 $c -- docs/integration/BAREMETAL_FIRMWARE.md sw/builder/test_builder.py | tr '\n' ' ')
  [ -n "$f" ] && echo "  $(g log -1 --format='%h %s' $c): $f"
done
echo "hunk ranges, train vs source, in shared files (old-side line numbers at merge-base):"
for f in docs/integration/BAREMETAL_FIRMWARE.md sw/builder/test_builder.py; do
  echo "  $f train:  $(g diff -U0 $MB $P -- $f | grep -o '^@@ -[0-9,]*' | tr '\n' ' ')"
  echo "  $f source: $(g diff -U0 $MB $S -- $f | grep -o '^@@ -[0-9,]*' | tr '\n' ' ')"
done
echo "patch equivalence: diff(MB..S) vs diff(P..H), ignoring index lines:"
diff <(g diff $MB $S | grep -v '^index ') <(g diff $P $H | grep -v '^index ') > /dev/null && echo "  IDENTICAL" || echo "  DIFFERENT"
echo "gitlinks: candidate / train parent / source"
for s in protocol-processor gptp-processor third_party/verilog-axis external; do
  echo "  $s $(g rev-parse $H:$s) / $(g rev-parse $P:$s) / $(g rev-parse $S:$s)"
done
echo "hdl/ changed by train: $(g diff --name-only $MB $P -- hdl | wc -l) file(s)"

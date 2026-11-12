#!/bin/sh
# composition.sh <repo with 1d6bf555, 8b1bdfaf, a69fc0f5, 2155eb96>: rebuild both compositions with
# git merge-tree, and prove every line each side added or removed in the shared files is in the result.
set -u
cd "$1"
B=1d6bf5556ae28764361d85012b86394eb467d294; D=8b1bdfaf1dcb9411ce5064f2b4207536e0bb7f32
A=a69fc0f597355a0a200ec5be6bb134b897e97ff5; H=2155eb9666693c0404aadb34ac4dad10a2466e24
echo "dev-soft-core $D tree $(git rev-parse $D^{tree}) (e282ecd2 tree recorded by the manager: 466d464aee94d3086419197f23e0fa862e65db16)"
echo "merge base $(git merge-base $D $H)"
T7=$(git merge-tree --write-tree $D $A); echo "merge-tree $D + $A -> $T7 rc=$? (7a4871d5 tree: 63b2a1605248b1804de5d22e4cdf134fa41981e7)"
TH=$(git merge-tree --write-tree $D $H); echo "merge-tree $D + $H -> $TH rc=$?"
echo "candidate-to-head-composition delta:"; git diff --stat $T7 $TH
strip() { grep -E '^[+-]' | grep -vE '^(\+\+\+|---) '; }
for f in $(comm -12 <(git diff --name-only $B $H | sort) <(git diff --name-only $B $D | sort)); do
  s=$(diff <(git diff -U0 $D $TH -- "$f" | strip) <(git diff -U0 $B $H -- "$f" | strip) >/dev/null && echo kept || echo CHANGED)
  o=$(diff <(git diff -U0 $H $TH -- "$f" | strip) <(git diff -U0 $B $D -- "$f" | strip) >/dev/null && echo kept || echo CHANGED)
  echo "$f: S9 lines $s; dev-soft-core lines $o"
done
for m in external gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis; do
  echo "gitlink $m: base $(git ls-tree $B $m | awk '{print $3}') dsc $(git ls-tree $D $m | awk '{print $3}') head $(git ls-tree $H $m | awk '{print $3}') comp $(git ls-tree $TH $m | awk '{print $3}')"; done

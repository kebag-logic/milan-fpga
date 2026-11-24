#!/bin/bash
# repro.sh <no-submodule worktree> <submodule worktree> <outdir>
# Reproduce the hosted docs-check/elaborate failure at the hosted merge 7bfae19 and show its cause:
#   A. 7bfae19, no submodules (the aggregate jobs' checkout): builder --list, then both verify steps.
#   B. 7bfae19 with protocol-processor present: the same hosted receipts verify.
#   C. the final merge, no submodules: builder --list exits 0 with the byte-identical inventory.
# Both worktrees are returned to the final merge afterwards.
set -u
R=$(dirname "$(readlink -f "$0")")/..
S=$R/scratch
bare=$1 full=$2 out=$3
old=7bfae19dee8a1eb105e8481691a407e66b92c142
final=$(git -C "$bare" rev-parse HEAD)
py=$S/py312/bin/python
mkdir -p "$out"
listing() {  # listing <tree> <label>
  (cd "$1" && "$py" sw/builder/test_builder.py --list > "$out/list-$2.json" 2> "$out/list-$2.stderr")
  echo "$2: builder --list exit $? ; stdout sha256 $(sha256sum < "$out/list-$2.json" | cut -c1-64)"
  sed 's/^/  stderr: /' "$out/list-$2.stderr"
}
submodules() { echo "  protocol-processor files: $(ls "$1/protocol-processor" | wc -l); $(git -C "$1" submodule status protocol-processor | cut -c1-42)"; }
{
  echo "python: $("$py" -V)"
  echo "final merge: $final ($(git -C "$bare" rev-parse HEAD^{tree}))"
  echo "== A. hosted merge $old, no submodules"
  git -C "$bare" checkout -q --detach "$old"; submodules "$bare"
  listing "$bare" 7bfae19-nosub
  for wf in docs elaborate; do
    run=$([ $wf = docs ] && echo 45434456591 || echo 45434456617)
    "$S/verify.sh" "$bare" $wf "$S/hosted-receipts/run-$run" "$out/union-$wf-7bfae19-nosub.json" 2>&1 | grep -v '^    \|^ *\^' | tail -4
  done
  echo "== B. hosted merge $old, protocol-processor present"
  git -C "$full" checkout -q --detach "$old"; git -C "$full" submodule update protocol-processor gptp-processor third_party/verilog-axis third_party/tsn-c-stack >/dev/null 2>&1
  submodules "$full"
  listing "$full" 7bfae19-sub
  for wf in docs elaborate; do
    run=$([ $wf = docs ] && echo 45434456591 || echo 45434456617)
    "$S/verify.sh" "$full" $wf "$S/hosted-receipts/run-$run" "$out/union-$wf-7bfae19-sub.json" 2>&1 | tail -3
  done
  echo "== C. final merge $final, no submodules"
  git -C "$bare" checkout -q --detach "$final"; submodules "$bare"
  listing "$bare" final-nosub
  cmp -s "$out/list-7bfae19-sub.json" "$out/list-final-nosub.json" && echo "inventory: final/no-submodule == 7bfae19/with-submodule, byte-identical"
  git -C "$full" checkout -q --detach "$final"; git -C "$full" submodule update protocol-processor gptp-processor third_party/verilog-axis third_party/tsn-c-stack >/dev/null 2>&1
  echo "worktrees returned: $(git -C "$bare" rev-parse --short HEAD) $(git -C "$full" rev-parse --short HEAD); full tree status: '$(git -C "$full" status --porcelain | head -1)'"
} 2>&1 | tee "$out/repro.log"

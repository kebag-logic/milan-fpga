#!/usr/bin/env bash
# Run the evidence measurement and the Python idiom gate at the commits around
# the DUT_READER_DISPOSITIONS move, from a clone of the repository, and record
# each command's output and rc. Usage: move_equivalence.sh <repo> <outdir>
# The repo's working tree is checked out at each commit in turn and returned
# to its starting HEAD at the end; the caller verifies the restore.
set -u
repo=$1; out=$2; mkdir -p "$out"
cd "$repo" || exit 2
start=$(git rev-parse HEAD)
# Scratch merge of dev 423ac5d9 into c79c178e (the tree before the move with
# #669 merged); a dangling commit object, no ref is written.
t=$(git merge-tree --write-tree c79c178e7edc427df347787aff6a2cf03adb13ae 423ac5d910d09ab189b3acc39ae3ae1d10d50b19 | head -1)
scr=$(git commit-tree "$t" -p c79c178e7edc427df347787aff6a2cf03adb13ae -p 423ac5d910d09ab189b3acc39ae3ae1d10d50b19 -m scratch)
echo "scratch_merge_tree=$t scratch_commit=$scr" > "$out/scratch_merge.txt"
for pair in c79c178e:c79c178e7edc427df347787aff6a2cf03adb13ae e8f7d247:e8f7d2470159d28a235a44ffd070e38fb57db182 \
            pre669:$scr head:0f3d37dbffc4ca3f0e0f69499de80fc256a7db57; do
  tag=${pair%%:*}; c=${pair#*:}
  git -c advice.detachedHead=false checkout -q --detach "$c" || exit 3
  echo "$tag $(git rev-parse HEAD) tree $(git rev-parse HEAD^{tree})" >> "$out/commits.txt"
  i=0
  for cmd in "scripts/measure_test_evidence.py" "scripts/measure_test_evidence.py --check" \
             "scripts/measure_test_evidence.py --selftest" "scripts/check_py_idiom.py" \
             "scripts/check_py_idiom.py --selftest"; do
    i=$((i+1))
    python3 $cmd > "$out/$tag.$i.out" 2>&1; echo "$tag $i rc=$? :: python3 $cmd" >> "$out/rc.txt"
  done
done
git -c advice.detachedHead=false checkout -q --detach "$start"

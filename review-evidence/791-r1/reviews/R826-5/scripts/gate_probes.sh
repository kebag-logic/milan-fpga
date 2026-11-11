#!/usr/bin/env bash
# Disposable falsification probes for the round-4 F1 fix at PR #888 head 6a5acf06.
# Usage: gate_probes.sh <path-to-a-checkout-at-the-head> <scratch-dir>
# Clones the checkout into <scratch-dir>/clone (submodules protocol-processor and
# gptp-processor from the checkout's own module store), then:
#   P0 runs scripts/check_py_idiom.py unmodified        (expect rc 0)
#   P1 re-keys the exec inventory to test_ctrl_memory.py (expect rc 1, exec refused in ctrl_memory_mutant.py)
#   P2 restores test_ctrl_memory.py to its 77e1efa0 bytes (expect rc 1, long module 11 > 10)
# and restores each edit. The source checkout is never written.
set -u
SRC=$(cd "$1" && pwd); S=$2; HEAD=6a5acf06c80c8a04cef0c5d2b3aeb47252393b8c
G=$(git -C "$SRC" rev-parse --absolute-git-dir)
rm -rf "$S/clone"; mkdir -p "$S"
git clone -q --no-hardlinks "$SRC" "$S/clone" && cd "$S/clone" && git checkout -q --detach "$HEAD" || exit 2
for s in protocol-processor gptp-processor; do git config "submodule.$s.url" "$G/modules/$s"; done
git -c protocol.file.allow=always submodule update -q --init protocol-processor gptp-processor || exit 2
export PYTHONDONTWRITEBYTECODE=1
echo "== P0: unmodified head"; python3 -I scripts/check_py_idiom.py > ../p0.log 2>&1; echo "rc=$?"
grep -E "long module|dynamic" ../p0.log
echo "== P1: exec inventory key reverted to sw/litex/test_ctrl_memory.py"
sed -i 's|"sw/litex/ctrl_memory_mutant.py":|"sw/litex/test_ctrl_memory.py":|' scripts/check_py_idiom.py
python3 -I scripts/check_py_idiom.py > ../p1.log 2>&1; echo "rc=$?"; grep -iE "exec|inventor|dynamic" ../p1.log | head -6
git checkout -q -- scripts/check_py_idiom.py
echo "== P2: test_ctrl_memory.py restored to its 77e1efa0 bytes (1003 lines), helper kept"
git show 77e1efa0:sw/litex/test_ctrl_memory.py > sw/litex/test_ctrl_memory.py
python3 -I scripts/check_py_idiom.py > ../p2.log 2>&1; echo "rc=$?"; grep -iE "long module|test_ctrl_memory" ../p2.log | head -6
git checkout -q -- sw/litex/test_ctrl_memory.py
echo "status after restore:"; git status --porcelain

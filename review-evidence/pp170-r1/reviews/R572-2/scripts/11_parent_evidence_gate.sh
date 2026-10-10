#!/bin/sh
# The parent's evidence-classification gate in a disposable, never-committed
# parent: tarball tree of parent 5603c353 (from 06_regen_images.sh) in a fresh
# git index, the processor gitlink staged at the reviewed head (local clone of
# the review clone), gptp-processor at its own parent gitlink. Run without and
# with the adoption input parent-name-evidence.patch.
# Usage: 11_parent_evidence_gate.sh /abs/path/to/parent-name-evidence.patch
set -u; . "$(dirname "$0")/env.sh"
patchfile=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
G=5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d
d="$SCRATCH/parent-evgate"; rm -rf "$d"; mkdir -p "$d"
tar -xzf "$SCRATCH/parent-dl/parent.tgz" -C "$d" --strip-components=1
rm -rf "$d/protocol-processor" "$d/gptp-processor"
git clone -q --no-hardlinks "$SRC" "$d/protocol-processor" && git -C "$d/protocol-processor" checkout -q --detach "$HEAD_SHA"
git clone -q https://github.com/Mister-M-alt/FPGA-gPTP.git "$d/gptp-processor" && git -C "$d/gptp-processor" checkout -q --detach "$G"
( cd "$d" && git init -q && git add -A . 2>/dev/null && git submodule init -- protocol-processor gptp-processor && git submodule status -- protocol-processor gptp-processor ) > "$RCPT/parent-evidence-gate-setup.log" 2>&1
( cd "$d" && python3 scripts/measure_test_evidence.py --check ) > "$RCPT/parent-evidence-gate-without-patch.log" 2>&1
echo $? > "$RCPT/parent-evidence-gate-without-patch.rc"
( cd "$d" && patch -p1 < "$patchfile" ) > "$RCPT/parent-evidence-gate-patch-apply.log" 2>&1 || { echo 3 > "$RCPT/parent-evidence-gate-with-patch.rc"; exit 3; }
( cd "$d" && python3 scripts/measure_test_evidence.py --check ) > "$RCPT/parent-evidence-gate-with-patch.log" 2>&1
echo $? > "$RCPT/parent-evidence-gate-with-patch.rc"

#!/usr/bin/env bash
# [R267] Grade the reviewed head's scripts/act_slot_proof.sh against a stand-in
# runner that refuses every PR run identically and ignores --slot in the live
# interrupt self-test. No Docker, no sudo, no network, no candidate act_ci.py:
# only the proof script's own grading logic is exercised. Everything lands in
# the packet's scratch directory except the copied SUMMARY receipt.
# Usage: run-proof-probe.sh <reviewed-clone> <packet-dir> [--collide-default]
set -euo pipefail
clone=$(cd "$1" && pwd)
packet=$(cd "$2" && pwd)
shift 2
work=$packet/scratch/proof-probe
rm -rf "$work"
mkdir -p "$work/wt-a" "$work/wt-b"
install -m 0555 "$packet/proof-probe/fake_refusing_runner.py" "$work/runner.py"
sha=$(sha256sum "$work/runner.py" | cut -d' ' -f1)
set +e
bash "$clone/scripts/act_slot_proof.sh" --runner "$work/runner.py" --sha256 "$sha" \
  --act-bin /nonexistent/act --logs "$work/logs" \
  --pr-a 101 --worktree-a "$work/wt-a" --pr-b 102 --worktree-b "$work/wt-b" \
  --slot-a 1 --slot-root-a /nonexistent/root --slot-b 2 --slot-root-b /nonexistent/root "$@"
rc=$?
set -e
echo "proof-script rc=$rc (proof script sha256 $(sha256sum "$clone/scripts/act_slot_proof.sh" | cut -c1-64))"
for f in "$work"/logs/*.verdict; do echo "== $(basename "$f")"; cat "$f"; done
echo "== interrupt log"; cat "$work/logs/interrupt-1.log"

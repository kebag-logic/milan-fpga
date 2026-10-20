#!/usr/bin/env bash
# usage: parent_head.sh <processor-sha> <record-dir>   commit the processor head as the scratch
# parent's protocol-processor gitlink on top of the three patches (local branch, never pushed),
# then run every parent consumer gate on it
S=<scratch>; P="$S/parent"; sha="$1"; rec="$2"; br="pp192-a660-head-${sha:0:8}"
set -e
git -C "$P" checkout -q -B "$br" 13bf00e1118bf1ad4a81e95b76bf8ea0dfe301da
git -C "$P" clean -fdXq -- tb/verilator
git -C "$P/protocol-processor" fetch -q origin 192-started-notify
git -C "$P/protocol-processor" checkout -q --detach "$sha"
git -C "$P/protocol-processor" clean -fdXq
git -C "$P" add protocol-processor
git -C "$P" commit -q -m "Scratch: protocol-processor at ${sha:0:8} (head pass)"
set +e
"$S/scripts/parent_gates.sh" "$rec"

#!/usr/bin/env bash
# Reviewer batch (R584-15): earlier reviewers' published probes, unchanged, at the head on one Git.
# usage: r584_15_prior_probes.sh <clone-root> <scratch-dir> <receipt-dir> <tag> <python>
# The Git is the first `git` on PATH. Each probe runs as its own process with its own log and exit status.
set -u
root=$1; scratch=$2; out=$3; tag=$4; py=$5
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$scratch" "$out"
run() { name=$1; shift; rm -rf "$scratch/$name"; mkdir -p "$scratch/$name"; { "$@"; echo "rc=$?"; } > "$out/$name.$tag.txt" 2>&1; }
run stack_spelling "$py" -I "$here/prior-R584-14/stack_spelling_probe.py" "$root" "$scratch/stack_spelling" &
run forged_entrypoints "$py" -I "$here/prior-R584-14/forged_entrypoints.py" "$root" "$scratch/forged_entrypoints" &
run forge_probe "$py" -I "$here/prior-R585-12/forge_probe.py" "$root" "$scratch/forge_probe" &
run store_probe "$py" -I "$here/prior-R584-12/store_probe.py" "$root/sw/firmware/ctrl/test" "$root/third_party/tsn-c-stack" "$scratch/store_probe" &
run sparse_gitlink bash "$here/prior-R585-14/r585_14_superproject_sparse_gitlink.sh" "$root" "$scratch/sparse_gitlink" &
run sparse_gitlink_serve bash "$here/prior-R585-14/r585_14_superproject_sparse_gitlink_serve.sh" "$root" "$scratch/sparse_gitlink_serve" &
wait

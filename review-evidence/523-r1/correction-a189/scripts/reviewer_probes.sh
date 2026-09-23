#!/usr/bin/env bash
# Re-run both reviewers' published fixture probes, unmodified, at this checkout.
# None of them writes into the checkout: each builds disposable fixtures.
# Usage: reviewer_probes.sh CHECKOUT PACKET
set -u
repo="$1"; packet="$2"
reviews="$packet/scratch/review-probes/review-evidence/523-r1/reviews"
r256="$reviews/R256-2/scripts"; r257="$reviews/R257-1/scripts"
out="$packet/receipts/probes"; mkdir -p "$out"
base="$packet/scratch/base-run_all_suites.sh"   # 483a133e blob 2a02c7f3
tmp="$packet/scratch/probe-tmp"; mkdir -p "$tmp"
rc() { python3 "$packet/scripts/rcpt.py" "$@"; }

rc 40-R256-sweep-hardstop --cwd "$repo" --env "TMPDIR=$tmp" -- \
  python3 "$r256/probe_sweep_hardstop.py" "$repo" "$base" "$out/R256-probe-sweep-hardstop.json"
for sig in KILL HUP; do
  rc "41-R257-hardstop-head-$sig" --cwd "$repo" --env "TMPDIR=$tmp" -- \
    python3 "$r257/probe_sweep_hardstop.py" "$repo" "$sig" "$repo/scripts/run_all_suites.sh" "$out/R257-hardstop-head-$sig"
  rc "41-R257-hardstop-base-$sig" --cwd "$repo" --env "TMPDIR=$tmp" -- \
    python3 "$r257/probe_sweep_hardstop.py" "$repo" "$sig" "$base" "$out/R257-hardstop-base-$sig"
done
rc 42-R257-git-env-head --cwd "$repo" --env "TMPDIR=$tmp" -- \
  python3 "$r257/probe_git_env.py" "$repo" "$repo/tb/verilator/gptp_shadow/mutants.py" "$out/R257-git-env-head" \
  none GIT_EDITOR=vi GIT_SEQUENCE_EDITOR=vi GIT_ASKPASS=/bin/false GIT_AUTHOR_NAME=Dev \
  GIT_COMMITTER_EMAIL=dev@example.invalid GIT_SSH_COMMAND=ssh GIT_TRACE=0 GIT_MERGE_AUTOEDIT=no GIT_PAGER=cat \
  GIT_INDEX_FILE=@ROOT@/.git/index GIT_DIR=@ROOT@/.git GIT_WORK_TREE=@ROOT@ GIT_OBJECT_DIRECTORY=@ROOT@/.git/objects
for mode in no-prctl no-pidfd prctl-fails; do
  rc "43-R257-unsupported-$mode" --cwd "$repo" --env "TMPDIR=$tmp" -- \
    python3 "$r257/probe_unsupported.py" "$repo" "$mode"
done
rc 44-R256-unsupported-platform --cwd "$repo" -- python3 "$r256/probe_unsupported_platform.py" "$repo"

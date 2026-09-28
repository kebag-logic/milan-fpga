#!/usr/bin/env bash
# Reproduce the rtl-fast "Prove protocol-processor source lists are derived"
# step (python3 scripts/pp_srcs.py --check --selftest) at base and head, in
# disposable shared clones; the reviewed clone is only read.
# Usage: pp_srcs_base_vs_head.sh <clone> <scratch> <rev>...
set -uo pipefail
clone=$1 scratch=$2; shift 2
for rev in "$@"; do
  d="$scratch/ppsrc-${rev:0:8}"
  rm -rf "$d"
  git clone -q --shared --no-checkout "$clone" "$d"
  git -C "$d" checkout -q --detach "$rev"
  rm -rf "$d/protocol-processor"; mkdir -p "$d/.git/modules"
  cp -a "$clone/protocol-processor" "$d/protocol-processor"
  cp -a "$clone/.git/modules/protocol-processor" "$d/.git/modules/protocol-processor"
  git -C "$d/protocol-processor" config core.worktree "$d/protocol-processor"
  echo "== $rev pp=$(git -C "$d/protocol-processor" rev-parse HEAD) dirty=$(git -C "$d/protocol-processor" status --porcelain | wc -l)"
  ( cd "$d" && python3 -B scripts/pp_srcs.py --check --selftest 2>&1 | tail -6; echo "rc=${PIPESTATUS[0]}" )
done

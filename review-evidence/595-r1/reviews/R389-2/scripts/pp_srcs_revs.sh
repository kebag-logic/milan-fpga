#!/usr/bin/env bash
# `pp_srcs.py --check --selftest` (the rtl-fast verilator-lint step 7 command)
# at each named revision, each in a fresh disposable clone made by mkclone.sh.
# Usage: pp_srcs_revs.sh <clone> <scratch> <rev>...
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd); clone=$1 scratch=$2; shift 2
for rev in "$@"; do
  d="$scratch/pp-${rev:0:8}"
  "$here/mkclone.sh" "$clone" "$rev" "$d" 2>&1 | grep -v commit-graph | head -2
  ( cd "$d" && python3 -B scripts/pp_srcs.py --check --selftest 2>&1 | grep -v "^  prose" | tail -4; echo "rc=${PIPESTATUS[0]} at $rev" )
  rm -rf "$d"
done

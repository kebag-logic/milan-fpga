#!/usr/bin/env bash
# Usage: run_patch_full.sh <head-tree> <scratch-dir> <arm>  -- applies the
# committed tb/srp_top/mutations/<arm>.patch to a copy and runs the FULL default
# srp_top suite (all groups) with the pinned simulator.
set -u
here=$(cd "$(dirname "$0")" && pwd)
src=$1; dst=$2/$3; arm=$3
rm -rf "$dst"; mkdir -p "$dst"; cp -r "$src/hdl" "$src/tb" "$dst/"
(cd "$dst" && git apply "tb/srp_top/mutations/$arm.patch") || { echo "APPLY_FAIL"; exit 3; }
"$here/run_suite.sh" "$dst" srp_top ""

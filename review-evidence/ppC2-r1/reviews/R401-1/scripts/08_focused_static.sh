#!/bin/bash
# Focused static checks at head: lint of the one changed RTL module (lint_hdl.sh's
# exact flags, pinned simulator), matrix drift, whitespace, and the gitlink set.
set -u
. "$(dirname "$0")/00_env.sh"
T="$PKT/scratch/head"
R="$PKT/receipts/static"
mkdir -p "$R"
cd "$T" || exit 1
pkgs=$(find hdl -name '*_pkg.sv' | sort)
all=$(find hdl -name '*.sv' ! -name '*_pkg.sv' | sort)
# shellcheck disable=SC2086
"$VLT" --lint-only -Wall -Wno-DECLFILENAME -Wno-UNUSEDSIGNAL -Wno-UNUSEDPARAM \
  --top-module KL_pp_maap $pkgs $all > "$R/lint-KL_pp_maap.log" 2>&1
echo "lint KL_pp_maap rc=$? warnings=$(grep -cE '%(Warning|Error)' "$R/lint-KL_pp_maap.log")" | tee "$R/summary.txt"
python3 scripts/gen_matrix.py --check > "$R/gen_matrix-check.log" 2>&1
echo "gen_matrix --check rc=$?" | tee -a "$R/summary.txt"
git -C "$CLONE" diff --check c951a9ff0cb5851fb159d33e966e5a2a9a188fe3 "$HEAD_SHA" > "$R/diff-check.log" 2>&1
echo "git diff --check rc=$?" | tee -a "$R/summary.txt"
echo "gitlinks at head: $(git -C "$CLONE" ls-tree -r "$HEAD_SHA" | grep -c '^160000')" | tee -a "$R/summary.txt"

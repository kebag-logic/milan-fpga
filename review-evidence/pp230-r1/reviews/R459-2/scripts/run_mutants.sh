#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# run_mutants.sh JOBS: the committed tb/srp_top/mutants.py campaign of the
# exact head, in a fresh `git archive`, with every arm's receipt kept.
set -u
P=${P:-$(cd "$(dirname "$0")/.." && pwd)}
. "$P/scripts/env.sh"
export TMPDIR=$S/tmp
mkdir -p "$TMPDIR"
if [ ! -d "$S/mhead" ]; then
  mkdir -p "$S/mhead"; git -C "${CLONE:?set CLONE}" archive "$HEAD" | tar -x -C "$S/mhead"
fi
cd "$S/mhead/tb/srp_top" && python3 mutants.py --jobs "${1:-7}" --output "$S/mutants_out"

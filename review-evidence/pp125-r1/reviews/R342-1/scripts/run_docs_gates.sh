#!/usr/bin/env bash
# Run the processor repository's documentation gates against one checkout and
# record each gate's exit status.  Usage:
#   run_docs_gates.sh <checkout> <out-dir> [python-with-wavedrom]
# The optional interpreter must already import `wavedrom`, so render-wavedrom.py
# never bootstraps its own virtualenv inside the checkout.
set -u
repo=$(cd "$1" && pwd)
out=$(mkdir -p "$2" && cd "$2" && pwd)
wdpy=${3:-python3}
summary="$out/gates-summary.tsv"
printf 'gate\trc\n' > "$summary"

run() { # name, command...
  local name=$1; shift
  (cd "$repo" && "$@") > "$out/gate-$name.log" 2>&1
  local rc=$?
  printf '%s\t%s\n' "$name" "$rc" >> "$summary"
}

run head                git rev-parse HEAD
run check-links         python3 scripts/check-links.py
run check-matrix        python3 scripts/check-matrix.py
run check-integrator-params python3 scripts/check-integrator-params.py
run render-wavedrom-check "$wdpy" scripts/render-wavedrom.py --check
run make-stale          make stale
run lint-diagrams       ./scripts/lint-diagrams.sh
run gen-matrix-check    python3 scripts/gen_matrix.py --check
run diff-check          git diff --check 493e5e4bf58a6146bf9310194d71c72e18610704 1d249e6e18a91c16a2620904483634548b0414a6
run packer-body-key-tests python3 -B tb/desc_store/test_gen_desc_image.py -v
cat "$summary"

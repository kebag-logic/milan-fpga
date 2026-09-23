#!/usr/bin/env bash
# Export the reviewed head, the first commit and the base into disposable trees.
# Usage: 00_export_trees.sh <clone> <scratch>
set -euo pipefail
clone=$1; scratch=$2
declare -A revs=([head]=fc155c3ca28b04c2220bf41ebea9214379210452
                 [mid]=9370f8ab80231bbf1a6a833312e6b4ffbd0a4f9b
                 [base]=fbc1f7156d711e5b7f511da8a16d9494256b017b)
for k in head mid base; do
  rm -rf "$scratch/$k"; mkdir -p "$scratch/$k"
  git -C "$clone" archive "${revs[$k]}" | tar -x -C "$scratch/$k"
  echo "$k ${revs[$k]} tree=$(git -C "$clone" rev-parse "${revs[$k]}^{tree}")"
done

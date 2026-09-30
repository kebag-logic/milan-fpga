#!/usr/bin/env bash
# Extract the exact head and the base into scratch/ from a processor clone.
# Usage: extract_trees.sh CLONE   (CLONE has both commits)
set -euo pipefail
PKT="$(cd "$(dirname "$0")/.." && pwd)"; CLONE="$1"
HEAD_SHA=5e806296b73d04ccf095ad00e081cb790fbbaf8d; BASE_SHA=0451d83d9d3f2ed5f4513c59ac5ac219ad9dd7ff
mkdir -p "$PKT/scratch/head" "$PKT/scratch/base"
git -C "$CLONE" archive --format=tar "$HEAD_SHA" | tar -x -C "$PKT/scratch/head"
git -C "$CLONE" archive --format=tar "$BASE_SHA" | tar -x -C "$PKT/scratch/base"
# scratch/bin/verilator and scratch/bin2/verilator are thin wrappers that call a
# pinned Verilator 5.050 and rewrite "-j 0" to "-j 8" / "-j 2" (job cap).

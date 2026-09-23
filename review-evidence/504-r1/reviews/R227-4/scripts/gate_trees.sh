#!/usr/bin/env bash
# R227-4: build disposable full-tree copies of the exact head for whole-gate
# 1b runs, one per mutant, each with the three required submodules copied in.
# Usage: gate_trees.sh <review clone> <scratch dir>
set -euo pipefail
clone=$1
scratch=$2
head=4876423d4cf8e89b820c56f8339f230abefb4827
low='key[-1] <= start + width - 1 and key[-1] + 3 >= start]'

make_tree() {
    local name=$1 old=$2 new=$3 tree="$scratch/gate/$1"
    rm -rf "$tree"
    mkdir -p "$tree"
    git -C "$clone" archive --format=tar "$head" | tar -x -C "$tree"
    for sub in third_party/verilog-axis protocol-processor gptp-processor; do
        rm -rf "${tree:?}/$sub"
        cp -r "$clone/$sub" "$tree/$sub"
        rm -f "$tree/$sub/.git"
    done
    # scripts/pp_srcs.py derives the processor list with `git ls-files`, so
    # the copied processor checkout gets a disposable index of its own bytes.
    git -C "$tree/protocol-processor" init -q
    git -C "$tree/protocol-processor" add -A
    if [ -n "$old" ]; then
        OLD=$old NEW=$new FILE="$tree/sw/builder/test_builder.py" python3 - <<'EOF'
import os
path, old, new = os.environ["FILE"], os.environ["OLD"], os.environ["NEW"]
text = open(path, encoding="utf-8").read()
assert text.count(old) == 1, (path, text.count(old))
open(path, "w", encoding="utf-8").write(text.replace(old, new))
EOF
    fi
    sha256sum "$tree/sw/builder/test_builder.py"
}

make_tree head "" ""
make_tree M1-gt "$low" 'key[-1] <= start + width - 1 and key[-1] + 3 > start]'
make_tree M2-plus4 "$low" 'key[-1] <= start + width - 1 and key[-1] + 4 >= start]'
make_tree U1-high-lt "$low" 'key[-1] < start + width - 1 and key[-1] + 3 >= start]'
make_tree U3-high-term-dropped "$low" 'key[-1] + 3 >= start]'

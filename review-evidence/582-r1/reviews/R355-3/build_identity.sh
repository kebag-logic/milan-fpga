#!/usr/bin/env bash
# Build the five tracked configurations from pristine exports of named commits
# and record per-file SHA-256 identities of every generated artifact.
# Usage: build_identity.sh <clone> <scratch-dir> <receipt-dir> <commit>...
# Each commit is exported with `git archive`; its submodule gitlinks are
# exported from the clone's submodule repositories at the recorded pins.
# Nothing is written inside the clone.
set -euo pipefail
clone=$1
scratch=$2
out=$3
shift 3
export PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0
mkdir -p "$scratch" "$out"
one() {
    local commit=$1 tree="$scratch/tree-$1" log="$out/build-$1.log" sub pin cfg
    rm -rf "$tree"
    mkdir -p "$tree"
    git -C "$clone" archive "$commit" | tar -x -C "$tree"
    git -C "$clone" ls-tree -r "$commit" | awk '$2 == "commit" {print $4, $3}' |
    while read -r sub pin; do
        if [ -e "$clone/$sub/.git" ]; then
            mkdir -p "$tree/$sub"
            git -C "$clone/$sub" archive "$pin" | tar -x -C "$tree/$sub"
            echo "submodule $sub $pin exported"
        else
            echo "submodule $sub $pin not checked out in clone; skipped"
        fi
    done > "$log" 2>&1
    for cfg in "$tree"/configs/endstation_*.yaml; do
        (cd "$tree" && python3 sw/builder/endstation_builder.py "configs/$(basename "$cfg")") >> "$log" 2>&1
        echo "build $(basename "$cfg") rc=$?" >> "$log"
    done
    (cd "$tree" && find sw/builder/out configs/generated hdl/common/gen -type f -print0 |
        sort -z | xargs -0 sha256sum) > "$out/identity-$commit.sha256"
}
export -f one
export clone scratch out
printf '%s\n' "$@" | xargs -P 4 -I{} bash -c 'one {}'

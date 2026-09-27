#!/usr/bin/env bash
# R354-3 five-configuration generated-artifact identity, base versus head.
# Usage: identity.sh <repo-root> <scratch-dir> <python> <base> <head> <receipt-dir>
# Builds every tracked configs/endstation_*.yaml in ONE disposable copy (same
# absolute path for both sides), checked out first at <base> and then at
# <head> (builder CLI, --write-fragment), hashes every generated file (output
# root plus configs/generated/), and diffs the two lists.
set -eu
repo=$1 scratch=$2 py=$3 base=$4 head=$5 out=$6
export PYTHONDONTWRITEBYTECODE=1
mkdir -p "$scratch" "$out"
t="$scratch/id-tree"
rm -rf "$t"
rsync -a --exclude=__pycache__ "$repo/" "$t/"
for side in base head; do
    rev=$base; [ "$side" = head ] && rev=$head
    rm -rf "$t/out-r354"
    git -C "$t" checkout -q -f "$rev"
    git -C "$t" clean -q -fdx -e out-r354
    [ "$(git -C "$t" rev-parse HEAD)" = "$(git -C "$repo" rev-parse "$rev")" ]
    git -C "$t" submodule status > "$out/identity_${side}_submodules.txt"
    list="$out/identity_${side}.sha256"
    for cfg in "$t"/configs/endstation_*.yaml; do
        stem=$(basename "$cfg" .yaml)
        (cd "$t" && "$py" sw/builder/endstation_builder.py "configs/$stem.yaml" \
            -o out-r354 --write-fragment > "$out/identity_${side}_${stem}.log" 2>&1)
    done
    (cd "$t" && find out-r354 configs/generated -type f ! -name '.gitignore' -print0 \
        | sort -z | xargs -0 sha256sum) > "$list"
    echo "$side $(git -C "$t" rev-parse HEAD): $(wc -l < "$list") generated files"
done
if diff "$out/identity_base.sha256" "$out/identity_head.sha256" > "$out/identity_diff.txt"; then
    echo "IDENTITY PASS: every generated file is byte-identical base vs head"
else
    echo "IDENTITY FAIL: see identity_diff.txt"; exit 1
fi

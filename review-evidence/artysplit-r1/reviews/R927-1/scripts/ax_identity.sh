#!/usr/bin/env bash
# Builder export of every shipped config, all-fabric and split, at the base
# tree and at the head tree; then compare every output file byte for byte.
# usage: ax_identity.sh <base-tree> <head-tree> <out-dir>
set -u
base=$1 head=$2 out=$3
rm -rf "$out"; mkdir -p "$out"
for side in base head; do
    tree=${!side}
    for cfg in endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8 endstation_arty_current endstation_arty_4x4 endstation_arty_8ch endstation_arty_split; do
        [ -f "$tree/configs/$cfg.yaml" ] || { echo "$side $cfg ABSENT"; continue; }
        for pl in all-fabric split; do
            d="$out/$side/$cfg-$pl"
            mkdir -p "$d"
            (cd "$tree" && python3 sw/builder/endstation_builder.py -o "$d" --placement "$pl" "configs/$cfg.yaml") \
                > "$d.log" 2>&1
            echo "$side $cfg $pl rc=$?"
        done
    done
done
echo "== compare (AX7101 rows must be identical)"
for d in "$out"/base/*/; do
    n=$(basename "$d")
    if [ -d "$out/head/$n" ]; then
        if diff -r "$d" "$out/head/$n" > "$out/diff-$n.txt" 2>&1; then
            echo "IDENTICAL $n $(find "$d" -type f | wc -l) files"
        else
            echo "DIFFERS $n $(grep -c '' "$out/diff-$n.txt") diff lines"
        fi
    fi
done

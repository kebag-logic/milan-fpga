#!/usr/bin/env bash
# Hash each tracked configuration's sweep fragment (--write-fragment), built
# from disposable base/ and head/ trees. Usage: fragment_compare.sh <scratch-root>
set -u
S=${1:?}
for side in base head; do
  : > "$S/frag-$side.sha256"
  for cfg in endstation_arty_4x4 endstation_arty_8ch endstation_arty_current \
             endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8; do
    rm -rf "$S/fragout-$side"
    ( cd "$S/$side" && python3 sw/builder/endstation_builder.py "configs/$cfg.yaml" \
        -o "$S/fragout-$side" --write-fragment ) > /dev/null 2>&1; rc=$?
    f=$(ls "$S/$side"/configs/generated/sweep_opts_*.sh -t | head -1)
    echo "$side $cfg rc=$rc $(basename "$f")"
    echo "$(sha256sum < "$f" | cut -d' ' -f1)  $cfg/$(basename "$f")" >> "$S/frag-$side.sha256"
  done
done
diff "$S/frag-base.sha256" "$S/frag-head.sha256" && echo "FRAGMENTS IDENTICAL"
cat "$S/frag-head.sha256"

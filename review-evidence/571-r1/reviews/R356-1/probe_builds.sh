#!/usr/bin/env bash
# R356-1 probe: build the five tracked configurations in disposable base and
# head tree copies (git archive + submodule checkouts copied in), then compare
# every generated artifact base vs head, and each regenerated tracked header
# copy against the committed head blob.
# Usage: probe_builds.sh <scratch dir holding base/ and head/ trees> <repo clone>
set -u
S=${1:?scratch}; REPO=${2:?repo}
HEAD_SHA=f8a52f919bd309960046330a5af127b56731cb27
CFGS="endstation_arty_4x4 endstation_arty_8ch endstation_arty_current endstation_ax7101_1x1_tdm8 endstation_ax7101_8x8"
for side in base head; do
  for c in $CFGS; do
    ( cd "$S/$side" && python3 sw/builder/endstation_builder.py "configs/$c.yaml" \
        -o "$S/out-$side" --write-rtl > "$S/build-$side-$c.log" 2>&1; echo "rc=$?" >> "$S/build-$side-$c.log" )
    mkdir -p "$S/rtlcopy-$side/$c"
    cp "$S/$side/hdl/common/gen/adp_shape_defaults.svh" "$S/rtlcopy-$side/$c/hdl_common_adp_shape_defaults.svh"
    cp "$S/$side/configs/generated/$c/gen/adp_shape_defaults.svh" "$S/rtlcopy-$side/$c/configs_adp_shape_defaults.svh"
    tail -1 "$S/build-$side-$c.log" | sed "s/^/$side $c /"
  done
done
echo "== per-artifact comparison base vs head (out dirs) =="
for c in $CFGS; do
  for f in $(cd "$S/out-head/$c" && find . -type f | sort); do
    if cmp -s "$S/out-base/$c/$f" "$S/out-head/$c/$f"; then r=IDENTICAL; else r=DIFFERS; fi
    printf '%s %s %s %s\n' "$c" "$f" "$r" "$(sha256sum < "$S/out-head/$c/$f" | cut -c1-16)"
  done
  nb=$(cd "$S/out-base/$c" && find . -type f | wc -l); nh=$(cd "$S/out-head/$c" && find . -type f | wc -l)
  echo "$c file-count base=$nb head=$nh"
done
echo "== header diffs base -> head (out dirs) =="
for c in $CFGS; do
  echo "--- $c"; diff "$S/out-base/$c/adp_shape_defaults.svh" "$S/out-head/$c/adp_shape_defaults.svh"
done
echo "== regenerated tracked copies vs committed head blobs =="
for c in $CFGS; do
  git -C "$REPO" cat-file blob "$HEAD_SHA:configs/generated/$c/gen/adp_shape_defaults.svh" > "$S/committed-$c.svh"
  cmp -s "$S/committed-$c.svh" "$S/rtlcopy-head/$c/configs_adp_shape_defaults.svh" && echo "$c configs copy == regenerated head: YES" || echo "$c configs copy == regenerated head: NO"
done
git -C "$REPO" cat-file blob "$HEAD_SHA:hdl/common/gen/adp_shape_defaults.svh" > "$S/committed-hdl-common.svh"
for c in $CFGS; do
  cmp -s "$S/committed-hdl-common.svh" "$S/rtlcopy-head/$c/hdl_common_adp_shape_defaults.svh" && echo "hdl/common copy == regenerated head for $c: YES" || echo "hdl/common copy == regenerated head for $c: no"
done

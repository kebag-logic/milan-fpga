#!/usr/bin/env bash
# Build every configs/endstation_*.yaml builder output and AEM image with the
# processor checkout at OLD and then NEW, and compare every file's sha256.
# Usage: five_config_compare.sh <parent clone> <out dir> <old pin> <new pin>
# The processor checkout is returned to NEW (the gitlink) before exit.
set -u
R=$1 OUT=$2 OLD=$3 NEW=$4
restore() { git -C "$R/protocol-processor" checkout -q --detach "$NEW"; }
trap restore EXIT
rc_all=0; mkdir -p "$OUT/logs"
for pin in "$OLD" "$NEW"; do
  git -C "$R/protocol-processor" checkout -q --detach "$pin" || exit 2
  echo "processor checkout: $(git -C "$R/protocol-processor" rev-parse HEAD)"
  for cfg in "$R"/configs/endstation_*.yaml; do
    name=$(basename "$cfg" .yaml); run="$OUT/${pin:0:8}/$name"; rm -rf "$run"; mkdir -p "$run"
    (cd "$R" && python3 sw/builder/endstation_builder.py "$cfg" -o "$run/builder") > "$OUT/logs/${pin:0:8}.$name.builder.log" 2>&1; b=$?
    (cd "$R" && python3 avdecc/gen_aemi_image.py --overlay "$run/builder/$name/aem_overlay.json" \
        --line-bytes 576 -o "$run/aem.bin" -m "$run/aem.map" --json "$run/aem.json") > "$OUT/logs/${pin:0:8}.$name.aem.log" 2>&1; a=$?
    echo "${pin:0:8} $name builder_rc=$b aem_rc=$a"
    [ $b -eq 0 ] && [ $a -eq 0 ] || rc_all=1
  done
done
for side in "${OLD:0:8}" "${NEW:0:8}"; do
  (cd "$OUT/$side" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$OUT/$side.sha256"
done
echo "files old=$(wc -l < "$OUT/${OLD:0:8}.sha256") new=$(wc -l < "$OUT/${NEW:0:8}.sha256")"
if cmp -s "$OUT/${OLD:0:8}.sha256" "$OUT/${NEW:0:8}.sha256"; then echo "IDENTICAL: every file name and sha256 equal between pins"
else echo "DIFFERENT:"; diff "$OUT/${OLD:0:8}.sha256" "$OUT/${NEW:0:8}.sha256"; rc_all=1; fi
exit $rc_all

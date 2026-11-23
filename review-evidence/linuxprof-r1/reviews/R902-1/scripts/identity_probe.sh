#!/usr/bin/env bash
# FPGA artifact identity: build every configs/endstation_*.yaml at its own placement, split and all-fabric,
# and run the three firmware descriptor generators, in a base tree and a head tree; then compare byte for byte.
# Usage: identity_probe.sh <base-tree> <head-tree> <outdir>
set -u
base=$1; head=$2; out=$3
rm -rf "$out"; mkdir -p "$out"
one() {  # tree tag config placement
  local tree=$1 tag=$2 cfg=$3 pl=$4 stem; stem=$(basename "$cfg" .yaml)
  local d="$out/$tag/$stem-$pl"; mkdir -p "$d/b"
  local extra=(); [ "$pl" != own ] && extra=(--placement "$pl")
  (cd "$tree" && python3 -B sw/builder/endstation_builder.py "$cfg" -o "$d/b" "${extra[@]}" > "$d/builder.log" 2>&1; echo $? > "$d/builder.rc")
  if [ "$pl" = own ]; then
    for g in adp/adp_entity aecp/aecp_entity srp/srp_entity; do
      (cd "$tree" && python3 -B "sw/firmware/ctrl/$g.py" "$cfg" -o "$d/$(basename $g).h" > "$d/$(basename $g).log" 2>&1; echo $? > "$d/$(basename $g).rc")
    done
  fi
}
for tag in base head; do
  tree=$base; [ $tag = head ] && tree=$head
  for cfg in $(cd "$tree" && ls configs/endstation_*.yaml); do
    for pl in own split all-fabric; do one "$tree" $tag "$cfg" $pl & done
  done
done
wait
# logs carry no paths that differ by tree except the tree root; normalise it
for tag in base head; do tree=$base; [ $tag = head ] && tree=$head
  find "$out/$tag" -name '*.log' -exec sed -i "s#$tree#<TREE>#g; s#$out/$tag#<OUT>#g" {} +; done
echo "files base: $(find "$out/base" -type f | wc -l)  head: $(find "$out/head" -type f | wc -l)"
echo "nonzero rcs base: $(grep -L '^0$' $(find "$out/base" -name '*.rc') | wc -l)  head: $(grep -L '^0$' $(find "$out/head" -name '*.rc') | wc -l)"
(cd "$out/base" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$out/base.sha256"
(cd "$out/head" && find . -type f -print0 | sort -z | xargs -0 sha256sum) > "$out/head.sha256"
if cmp -s "$out/base.sha256" "$out/head.sha256"; then echo "IDENTITY: all $(wc -l < "$out/base.sha256") files byte-identical"; exit 0
else echo "IDENTITY: DIFFER"; diff "$out/base.sha256" "$out/head.sha256" | head -40; exit 1; fi

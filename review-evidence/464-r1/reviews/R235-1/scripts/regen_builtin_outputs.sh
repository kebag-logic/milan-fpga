#!/usr/bin/env bash
# R235: regenerate the store CLI's builtin-model outputs in the base and head
# scratch extracts (default target and --out-dir) and byte-compare them.
# This does NOT rerun the end-station builder (out of this review's bounds);
# the five configs' aem_desc.bin/.json/.map need builder overlays.
# Usage: regen_builtin_outputs.sh <scratch-root>
set -euo pipefail
root=${1:?scratch root}
py=/usr/bin/python3.14
for t in base head; do
  out="$root/regen-$t"; rm -rf "$out"; mkdir -p "$out"
  cp "$root/$t/avdecc/aem_rom.json" "$out/tracked_aem_rom.json"
  (cd "$root/$t" && $py -B -E -s avdecc/gen_aem_store.py --out-dir "$out/outdir" > "$out/cli-outdir.txt")
  (cd "$root/$t" && $py -B -E -s avdecc/gen_aem_store.py > "$out/cli-default.txt")
  cp "$root/$t/avdecc/aem_rom.json" "$out/default_aem_rom.json"
  cp "$out/tracked_aem_rom.json" "$root/$t/avdecc/aem_rom.json"   # restore the extract
done
for f in outdir/aecp_aem_rom.svh outdir/aem_rom.json default_aem_rom.json cli-outdir.txt cli-default.txt; do
  a="$root/regen-base/$f"; b="$root/regen-head/$f"
  if [ "$f" = cli-outdir.txt ]; then
    # the CLI echoes the --out-dir path, which differs by construction
    if cmp -s <(sed "s#$root/regen-base#R#" "$a") <(sed "s#$root/regen-head#R#" "$b"); then r=IDENTICAL; else r=DIFFER; fi
  elif cmp -s "$a" "$b"; then r=IDENTICAL; else r=DIFFER; fi
  printf '%-28s base=%s head=%s %s\n' "$f" "$(sha256sum < "$a" | cut -c1-16)" "$(sha256sum < "$b" | cut -c1-16)" "$r"
done
echo "tracked avdecc/aem_rom.json base==head: $(cmp -s "$root/regen-base/tracked_aem_rom.json" "$root/regen-head/tracked_aem_rom.json" && echo yes || echo no)"
echo "tracked vs regenerated default (head): $(cmp -s "$root/regen-head/tracked_aem_rom.json" "$root/regen-head/default_aem_rom.json" && echo identical || echo "DIFFER (pre-existing, routed to #495)")"

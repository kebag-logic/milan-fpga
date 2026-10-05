#!/bin/bash
# Build every shipping config's generated artifacts, plus each config's packed
# descriptor image through both emitters' shared path, at two parent revisions
# (each in a disposable worktree with its pinned submodules), and compare.
# Usage: compare_builder_outputs.sh <clone> <scratch> <out> <base-rev> <head-rev>
set -u
clone=$1; scratch=$2; out=$3; base=$4; head=$5
mkdir -p "$out"
mk() { # <rev> <dir>
  git -C "$clone" worktree add -q --detach "$2" "$1" || return 1
  for sm in protocol-processor gptp-processor third_party/verilog-axis; do
    pin=$(git -C "$2" rev-parse "HEAD:$sm") || return 1
    git -C "$clone/$sm" worktree add -q --detach "$2/$sm" "$pin" || return 1
  done
}
rm_wt() { for sm in protocol-processor gptp-processor third_party/verilog-axis; do git -C "$clone/$sm" worktree remove --force "$1/$sm"; done; git -C "$clone" worktree remove --force "$1"; }
for side in base head; do
  rev=$base; [ $side = head ] && rev=$head
  wt="$scratch/builder-$side"
  mk "$rev" "$wt" || { echo "worktree setup failed for $side"; exit 2; }
  (cd "$wt" && for cfg in configs/endstation_*.yaml; do
      name=$(basename "$cfg" .yaml)
      python3 sw/builder/endstation_builder.py "$cfg" -o "$scratch/gen-$side" > "$out/builder-$side-$name.log" 2>&1
      echo "$name rc $?" >> "$out/builder-$side.rc"
    done
    python3 - "$scratch/gen-$side" > "$out/images-$side.txt" 2>&1 <<'PY'
import hashlib, sys, glob, os
sys.path.insert(0, "sw/builder"); sys.path.insert(0, ".")
from sw.builder import endstation_builder as eb
for path in sorted(glob.glob("configs/endstation_*.yaml")):
    cfg = eb.load_config(path)
    blob = eb._entity_model_image(cfg, eb.emit_aem_overlay(cfg))["aem_desc.bin"]
    print(os.path.basename(path), len(blob), hashlib.sha256(blob).hexdigest())
PY
    echo "images rc $?" >> "$out/builder-$side.rc")
  rm_wt "$wt"
done
(cd "$scratch/gen-base" && find . -type f | sort | xargs sha256sum) > "$out/gen-base.sha256"
(cd "$scratch/gen-head" && find . -type f | sort | xargs sha256sum) > "$out/gen-head.sha256"
diff "$out/gen-base.sha256" "$out/gen-head.sha256" > "$out/gen.diff"; echo "generated-tree diff rc $?"
diff "$out/images-base.txt" "$out/images-head.txt" > "$out/images.diff"; echo "image diff rc $?"
cat "$out/builder-base.rc" "$out/builder-head.rc"

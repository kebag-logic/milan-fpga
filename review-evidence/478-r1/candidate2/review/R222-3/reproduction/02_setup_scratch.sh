#!/usr/bin/env bash
# R222-3: isolated scratch copies built from the review clone's object stores.
# /tmp is a separate tmpfs, so no hardlink into the review clone is possible;
# --no-hardlinks is passed anyway. Submodules are registered with local URLs
# pointing at the review clone's own checkouts (no network).
# Usage: 02_setup_scratch.sh <review-clone> <scratch-root> <out-file>
set -euo pipefail
review=$1; S=$2; out=$3
export GIT_NO_REPLACE_OBJECTS=1
mkdir -p "$S"
subs=(protocol-processor gptp-processor third_party/verilog-axis)
{
  echo "date_utc: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  for pair in cand:72e16c6172db723734317b105cff6c6e9168571a \
              src:1496558d82cf35fc98dda0e781b2a1be643c301a \
              dev:52711029f374650dc93830d5ea28e81cb5c8f410; do
    name=${pair%%:*}; sha=${pair#*:}
    d="$S/$name"
    rm -rf "$d"
    git clone -q --no-hardlinks --no-checkout "$review" "$d"
    git -C "$d" checkout -q --detach "$sha"
    for s in "${subs[@]}"; do
      git -C "$d" config "submodule.$s.url" "$review/$s"
    done
    git -C "$d" -c protocol.file.allow=always submodule -q update --init -- "${subs[@]}"
    echo "== $name"
    echo "HEAD: $(git -C "$d" rev-parse HEAD) tree: $(git -C "$d" rev-parse 'HEAD^{tree}')"
    echo "status-lines: $(git -C "$d" status --porcelain | wc -l)"
    for s in "${subs[@]}"; do
      pin=$(git -C "$d" ls-tree HEAD "$s" | awk '{print $3}')
      head=$(git -C "$d/$s" rev-parse HEAD)
      echo "  $s pin=$pin checkout=$head match=$([ "$pin" = "$head" ] && echo yes || echo NO)"
    done
    echo "  hardlink-count>1 files under .git/objects: $(find "$d/.git/objects" -type f -links +1 | wc -l)"
  done
} > "$out" 2>&1
cat "$out"

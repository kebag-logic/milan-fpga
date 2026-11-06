#!/usr/bin/env bash
# Fetch selected blobs of the published evidence tree (kebag-logic/milan-fpga
# commit 3b2b1ef2607c8250dcaa1c55b6dbe496c90588c3, review-evidence/843-r1)
# by blob id into <outdir>. usage: fetch_evidence.sh <tree-listing> <outdir> <regex>
set -euo pipefail
listing=$1 out=$2 re=$3
while read -r type size sha path; do
  [ "$type" = blob ] || continue
  rel=${path#review-evidence/843-r1/}
  [[ $rel =~ $re ]] || continue
  mkdir -p "$out/$(dirname "$rel")"
  gh api "repos/kebag-logic/milan-fpga/git/blobs/$sha" -H 'Accept: application/vnd.github.raw' > "$out/$rel"
  got=$(git hash-object "$out/$rel")
  [ "$got" = "$sha" ] || { echo "blob mismatch $rel" >&2; exit 1; }
done < "$listing"

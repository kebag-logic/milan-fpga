#!/bin/sh
# Fetch the author's public evidence archive at a pinned commit, read-only.
# usage: fetch_evidence.sh <dest-dir>
set -eu
dest=$1
repo=kebag-logic/milan-fpga
ref=274bc30e50664f128b4396b899aa2ac17d90a705
prefix=review-evidence/gptp104-r1
gh api "repos/$repo/git/trees/$ref?recursive=1" \
  --jq ".tree[] | select(.type==\"blob\" and (.path|startswith(\"$prefix/\"))) | \"\(.sha) \(.path)\"" |
while read -r sha path; do
  out="$dest/${path#$prefix/}"
  mkdir -p "$(dirname "$out")"
  gh api "repos/$repo/git/blobs/$sha" -H 'Accept: application/vnd.github.raw' > "$out"
  echo "$sha $path"
done

#!/bin/sh
# Fetch the published 763-r1 evidence tree at a fixed commit into $1 (an empty directory), verifying each blob's git id.
set -eu
out=$1; commit=${2:-c262f8de6c498f412312ad3abd96437c9d25e594}
gh api "repos/kebag-logic/milan-fpga/git/trees/$commit?recursive=1" --jq '.tree[] | select(.type=="blob") | select(.path|startswith("review-evidence/763-r1/")) | "\(.sha) \(.path)"' |
while read -r sha path; do
  dest="$out/${path#review-evidence/763-r1/}"; mkdir -p "$(dirname "$dest")"
  gh api "repos/kebag-logic/milan-fpga/git/blobs/$sha" --jq .content | base64 -d > "$dest"
  got=$(git hash-object --no-filters "$dest"); [ "$got" = "$sha" ] || { echo "MISMATCH $path"; exit 1; }
  echo "ok $sha $path"
done

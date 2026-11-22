#!/bin/sh
# fetch_evidence.sh <commit> <prefix-regex> <outdir>: download the evidence tree's blobs (read-only API)
set -eu
c=$1; pre=$2; out=$3
gh api "repos/kebag-logic/milan-fpga/git/trees/$c?recursive=1" --jq '.tree[] | select(.type=="blob") | "\(.sha) \(.path)"' |
grep -E " $pre" | while read -r sha p; do
  mkdir -p "$out/$(dirname "$p")"
  gh api "repos/kebag-logic/milan-fpga/git/blobs/$sha" -H 'Accept: application/vnd.github.raw' > "$out/$p"
  echo "$sha $p"
done

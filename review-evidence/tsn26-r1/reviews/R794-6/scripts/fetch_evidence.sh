#!/bin/bash
# usage: fetch_evidence.sh TREE_TSV OUTDIR
# Fetches every blob listed in TREE_TSV (type path size sha, from the git trees API of
# kebag-logic/milan-fpga) by its blob sha and checks the git blob hash of every byte fetched.
set -eu
tsv=$1; out=$2
while IFS=$'\t' read -r type path size sha; do
  [ "$type" = blob ] || continue
  mkdir -p "$out/$(dirname "$path")"
  gh api "repos/kebag-logic/milan-fpga/git/blobs/$sha" -H 'Accept: application/vnd.github.raw' > "$out/$path"
  got=$(git hash-object "$out/$path")
  [ "$got" = "$sha" ] || { echo "BLOB MISMATCH $path"; exit 1; }
  echo "ok $sha $path"
done < "$tsv"

#!/usr/bin/env bash
# R347-3 clone integrity snapshot. Usage: clone_integrity.sh <clone>
# Prints head/tree, porcelain line count, index-listing digest, gitlinks,
# and blob id + sha256 + mode for every file changed ac18b509..HEAD.
set -u
cd "$1" || exit 2
base=ac18b50968b12efe4d15c0a06301264b35656b31
echo "head $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
echo "porcelain: [$(git status --porcelain --ignore-submodules=none | wc -l) lines]"
echo "index listing sha256 $(git ls-files -s | sha256sum | cut -d' ' -f1)"
git ls-files -s | awk '$1=="160000"'
echo "HEAD gitlinks:"; git ls-tree -r HEAD | awk '$1=="160000"'
for f in $(git diff --name-only $base HEAD); do
  idx=$(git ls-files -s -- "$f" | awk '{print $1, $2}')
  head=$(git rev-parse "HEAD:$f")
  work=$(git hash-object -- "$f")
  echo "$idx head=$head work=$work $(sha256sum -- "$f" | cut -d' ' -f1) $f"
done

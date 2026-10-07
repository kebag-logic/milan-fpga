#!/bin/sh
# Usage: EXTRA_TERMS='a|b' history_scan.sh <repo>
# Scans every blob reachable from all refs, and every commit message.
# EXTRA_TERMS adds private search terms (account names, tool and model names) that are not published.
set -eu
repo=${1:-.}
cd "$repo"
P='/home/|/data/|/Users/|/tmp/|/mnt/|/opt/|[A-Z]:\\|password|passwd|secret|token|api[_-]?key|BEGIN [A-Z ]*PRIVATE|ghp_|github_pat|192\.168\.|license|licence|copyright|\(c\) [0-9]|GPL|Mozilla|BSD|MIT License|ported from|derived from|taken from'
[ -n "${EXTRA_TERMS:-}" ] && P="$P|$EXTRA_TERMS"
echo "# commits: $(git rev-list --all | wc -l)"
echo "# blobs:"; git rev-list --all --objects | git cat-file --batch-check='%(objecttype) %(objectname) %(rest)' | awk '$1=="blob"' | sort -u -k2,2 > "${TMPDIR:-/tmp}/.blobs.$$"
wc -l < "${TMPDIR:-/tmp}/.blobs.$$"
echo "# paths ever tracked:"; git log --all --format= --name-only | sort -u
while read -r t sha path; do
  git cat-file -p "$sha" | grep -a -n -i -E "$P" | sed "s|^|$sha $path:|" || true
done < "${TMPDIR:-/tmp}/.blobs.$$"
rm -f "${TMPDIR:-/tmp}/.blobs.$$"
echo "# commit messages:"
git log --all --format='%H %B' | grep -n -i -E "$P" || true

#!/usr/bin/env bash
# Confirms a clone's index, working bytes, modes and gitlinks equal the reviewed commit.
# Usage: verify_restore.sh <clone> <commit> <tree> <base>
set -u
cd "$1" || exit 9; commit=$2; tree=$3; base=$4
echo "HEAD $(git rev-parse HEAD) expected $commit"
echo "tree $(git rev-parse 'HEAD^{tree}') expected $tree"
echo "index tree $(git write-tree)"
diff <(git ls-tree -r --full-tree HEAD | awk '{print $1,$3}' FS='[ \t]+' | sort) <(git ls-files -s | awk '{print $1,$2}' | sort) >/dev/null && echo "index modes and blobs equal HEAD" || echo "INDEX DIFFERS"
git ls-tree -r HEAD | awk '$1 ~ /^100/ {sub(/^[^\t]*\t/,""); print}' > /tmp/.paths.$$
git hash-object --no-filters --stdin-paths < /tmp/.paths.$$ > /tmp/.hash.$$
git ls-tree -r HEAD | awk '$1 ~ /^100/ {print $3}' | diff - /tmp/.hash.$$ >/dev/null && echo "working bytes equal HEAD blobs: $(wc -l < /tmp/.hash.$$) files" || echo "WORKING BYTES DIFFER"
rm -f /tmp/.paths.$$ /tmp/.hash.$$
echo "untracked or ignored entries: $(git status --porcelain --ignored | wc -l)"
echo "gitlinks at head:"; git ls-tree -r HEAD | awk '$1=="160000"{print $3,$4}'
echo "gitlink changes against base: $(git diff --raw "$base" HEAD | grep -c '160000')"
echo "non-Markdown paths in the delta: $(git diff --name-only d63b378d27..HEAD | grep -vc '\.md$')"
git log --format='subject lines %B' -1 HEAD | sed '/^$/d' | wc -l | sed 's/^/commit message lines: /'

#!/bin/bash
# clone_integrity.sh CLONE HEAD: HEAD and tree, a clean worktree, index entries (mode, blob, path) equal to the
# head's tree, and the gitlinks (submodule entries) of the head
C=$1; H=$2
echo "HEAD $(git -C "$C" rev-parse HEAD) tree $(git -C "$C" rev-parse 'HEAD^{tree}')"
[ "$(git -C "$C" rev-parse HEAD)" = "$H" ] && echo "head matches" || echo "HEAD MISMATCH"
s=$(git -C "$C" status --porcelain --ignored); echo "status --porcelain --ignored lines: $(printf '%s' "$s" | grep -c .)"
a=$(git -C "$C" ls-files -s | awk '{print $1, $2, $4}' | sha256sum); b=$(git -C "$C" ls-tree -r "$H" | awk '{print $1, $3, $4}' | sha256sum)
[ "$a" = "$b" ] && echo "index equals ls-tree -r HEAD (mode, blob, path)" || echo "INDEX DIFFERS"
echo "gitlinks at head: $(git -C "$C" ls-tree -r "$H" | awk '$1=="160000"' | wc -l)"
echo "files: $(git -C "$C" ls-files | wc -l)"

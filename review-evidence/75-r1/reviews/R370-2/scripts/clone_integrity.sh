#!/usr/bin/env bash
# Verify a review clone still matches the exact head: HEAD, tree, index entries
# (mode + blob) against HEAD's tree, worktree bytes, untracked/ignored files and gitlinks.
# Usage: clone_integrity.sh CLONE HEAD_SHA TREE_SHA
set -u
C="$1"; H="$2"; T="$3"
cd "$C" || exit 2
g() { git "$@" 2>&1 | grep -v 'commit-graph'; }
echo "HEAD=$(g rev-parse HEAD) expected=$H"
echo "TREE=$(g rev-parse HEAD^{tree}) expected=$T"
a="$(git ls-tree -r --full-tree HEAD 2>/dev/null | awk '{print $1" "$3" "$4}' | sha256sum)"
b="$(git ls-files -s 2>/dev/null | awk '{print $1" "$2" "$4}' | sha256sum)"
echo "index-vs-HEAD mode/blob/path digest equal: $([ "$a" = "$b" ] && echo yes || echo NO)"
echo "index stages other than 0: $(git ls-files -s 2>/dev/null | awk '$3!=0' | wc -l)"
echo "worktree status (tracked, incl. submodule dirt):"; g status --porcelain=v1 --ignore-submodules=none
echo "untracked+ignored files outside submodules:"; g status --porcelain=v1 --ignored --untracked-files=all --ignore-submodules=all | grep -E '^(\?\?|!!)' || echo "(none)"
echo "worktree bytes re-hashed vs index (non-gitlink): $(git ls-files -s 2>/dev/null | awk '$1!="160000"{print $4}' | git hash-object --stdin-paths 2>/dev/null | paste -d' ' - <(git ls-files -s | awk '$1!="160000"{print $2}') | awk '$1!=$2' | wc -l) mismatches"
echo "gitlinks at HEAD:"; git ls-tree HEAD external gptp-processor protocol-processor third_party/verilog-axis 2>/dev/null
echo "submodule checkouts:"; g submodule status

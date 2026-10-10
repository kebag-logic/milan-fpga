#!/usr/bin/env bash
# Verify a checkout is the exact published head: HEAD, tree, index == HEAD, every tracked file's bytes and mode
# equal to its blob, no untracked or ignored file, and the submodule gitlinks checked out and clean.
# Usage: verify_restore.sh <checkout> <head> <tree>
set -u; cd "$1"
echo "HEAD $(git rev-parse HEAD) want $2"; echo "tree $(git rev-parse HEAD^{tree}) want $3"
git diff --cached --quiet && echo "index == HEAD: yes" || echo "index == HEAD: NO"
bad=$(git ls-files -s | awk '$1!="160000"' | while read -r mode oid stage path; do
  [ -L "$path" ] && got=$(printf %s "$(readlink "$path")" | git hash-object --stdin) || got=$(git hash-object --no-filters -- "$path")
  m=$([ -L "$path" ] && echo 120000 || { [ -x "$path" ] && echo 100755 || echo 100644; })
  [ "$got" = "$oid" ] && [ "$m" = "$mode" ] || echo "$path"; done | wc -l)
echo "tracked files: $(git ls-files | wc -l); blob or mode mismatches: $bad"
echo "untracked or ignored entries: $(git status --porcelain --ignored --untracked-files=all | wc -l)"
git ls-files -s | awk '$1=="160000"{print $4, $2}' | while read -r p want; do
  got=$(git -C "$p" rev-parse HEAD 2>/dev/null || echo uninitialised); d=$(git -C "$p" status --porcelain 2>/dev/null | wc -l)
  echo "gitlink $p want $want got $got dirty=$d"; done

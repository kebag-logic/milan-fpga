#!/bin/sh
# verify_restore.sh CLONE HEAD TREE : prove the review clone is at exact head bytes.
set -u
C=$1; H=$2; T=$3; fail=0
cd "$C" || exit 2
say(){ printf '%s\n' "$*"; }
[ "$(git rev-parse HEAD)" = "$H" ] && say "OK HEAD $H" || { say "FAIL HEAD $(git rev-parse HEAD)"; fail=1; }
[ "$(git rev-parse HEAD^{tree})" = "$T" ] && say "OK tree $T" || { say "FAIL tree"; fail=1; }
[ "$(git write-tree)" = "$T" ] && say "OK index tree equals HEAD tree" || { say "FAIL index tree"; fail=1; }
git diff --quiet && say "OK worktree equals index (bytes and modes)" || { say "FAIL worktree differs"; git diff --stat; fail=1; }
git diff --cached --quiet && say "OK index equals HEAD" || { say "FAIL index differs"; fail=1; }
st=$(git status --porcelain --ignored --untracked-files=all)
[ -z "$st" ] && say "OK no untracked or ignored entry" || { say "FAIL status:"; say "$st"; fail=1; }
git ls-files -s | sha256sum | sed 's/^/index stage listing sha256 /'
git submodule status | while read -r line; do say "submodule $line"; done
for sm in protocol-processor gptp-processor third_party/verilog-axis; do
  gl=$(git rev-parse "HEAD:$sm"); hd=$(git -C "$sm" rev-parse HEAD)
  if [ "$gl" = "$hd" ] && [ -z "$(git -C "$sm" status --porcelain --ignored)" ]; then say "OK $sm at gitlink $gl, clean"; else say "FAIL $sm gitlink $gl head $hd"; fail=1; fi
done
for sm in external third_party/lwSRP; do
  say "gitlink $sm $(git rev-parse HEAD:$sm) (not initialized in this clone: $(ls -A $sm 2>/dev/null | wc -l) entries)"
done
[ $fail = 0 ] && say "RESTORATION: PASS" || say "RESTORATION: FAIL"
exit $fail

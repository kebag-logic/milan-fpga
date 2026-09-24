#!/bin/sh
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R281-1: prove the review clone is back at exact-head bytes after all probes.
# Usage: verify_clone.sh <clone> <expected-head> <expected-tree>
# Exit 0 only if every check holds; each check prints one line.
set -u
clone=$1 head=$2 tree=$3
cd "$clone" || exit 2
fail=0
chk() { if [ "$1" = "$2" ]; then echo "OK   $3"; else echo "FAIL $3: got '$1' want '$2'"; fail=1; fi; }

chk "$(git rev-parse HEAD)" "$head" "HEAD"
chk "$(git rev-parse 'HEAD^{tree}')" "$tree" "HEAD tree"
chk "$(git status --porcelain --ignored | wc -l | tr -d ' ')" "0" "no modified, untracked or ignored paths in the superproject"
git diff --quiet; chk "$?" "0" "worktree equals index"
git diff --cached --quiet; chk "$?" "0" "index equals HEAD"
chk "$(git ls-files -s | awk '{print $1, $2, $4}' | sort | sha256sum)" \
    "$(git ls-tree -r HEAD | awk '{print $1, $3, $4}' | sort | sha256sum)" \
    "index mode/blob/path records equal HEAD tree"
chk "$(git ls-files -v | grep -v '^H ' | wc -l | tr -d ' ')" "0" "no skip-worktree or assume-unchanged flag"

# every tracked regular file and symlink re-hashes to its HEAD blob with its HEAD mode
bad=0 n=0
git ls-tree -r HEAD | while read -r mode type obj path; do
  [ "$type" = blob ] || continue
  if [ "$mode" = 120000 ]; then
    got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)
    [ -L "$path" ] || got=not-a-symlink
  else
    got=$(git hash-object --no-filters -- "$path")
    if [ -x "$path" ]; then m=100755; else m=100644; fi
    [ "$m" = "$mode" ] || got="mode-$m"
  fi
  [ "$got" = "$obj" ] || echo "MISMATCH $path $got $obj"
done > /tmp/r281_blob_check.$$
chk "$(wc -l < /tmp/r281_blob_check.$$ | tr -d ' ')" "0" "every tracked blob re-hashes to HEAD with HEAD mode ($(git ls-tree -r HEAD | awk '$2=="blob"' | wc -l | tr -d ' ') blobs)"
cat /tmp/r281_blob_check.$$; rm -f /tmp/r281_blob_check.$$

# gitlinks at HEAD and the initialised submodules at those pins, clean
for sm in protocol-processor gptp-processor third_party/verilog-axis external; do
  want=$(git ls-tree HEAD "$sm" | awk '$1=="160000"{print $3}')
  chk "$(git ls-files -s "$sm" | awk '{print $1, $2, $3}')" "160000 $want 0" "index gitlink $sm"
done
for sm in protocol-processor gptp-processor; do
  want=$(git ls-tree HEAD "$sm" | awk '{print $3}')
  chk "$(git -C "$sm" rev-parse HEAD)" "$want" "$sm checkout at its pin"
  chk "$(git -C "$sm" status --porcelain --ignored | wc -l | tr -d ' ')" "0" "$sm has no modified, untracked or ignored path"
  chk "$(git -C "$sm" ls-files -v | grep -v '^H ' | wc -l | tr -d ' ')" "0" "$sm has no skip-worktree or assume-unchanged flag"
  sbad=$(git -C "$sm" ls-tree -r HEAD | awk '$2=="blob" && $1!="120000"{print $3" "$4}' | while read -r obj path; do
           [ "$(git -C "$sm" hash-object --no-filters -- "$path")" = "$obj" ] || echo x; done | wc -l | tr -d ' ')
  chk "$sbad" "0" "$sm every regular blob re-hashes to its pin ($(git -C "$sm" ls-tree -r HEAD | awk '$2=="blob"' | wc -l | tr -d ' ') blobs)"
done
git submodule status | sed 's/^/     submodule status: /'
exit $fail

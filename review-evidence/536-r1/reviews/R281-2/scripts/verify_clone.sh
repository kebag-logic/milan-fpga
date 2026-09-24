#!/bin/sh
# Verify the review clone is byte-exact at the reviewed head after all probes.
# Usage: verify_clone.sh <clone> <expected head sha> <expected tree sha>
set -u
C=$1; H=$2; T=$3
cd "$C" || exit 2
fail=0
say() { printf '%s\n' "$*"; }
[ "$(git rev-parse HEAD)" = "$H" ] && say "HEAD ok $H" || { say "HEAD MISMATCH"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$T" ] && say "tree ok $T" || { say "tree MISMATCH"; fail=1; }
st=$(git status --porcelain --ignored --untracked-files=all)
[ -z "$st" ] && say "worktree clean (incl. ignored and untracked)" || { say "worktree NOT clean:"; say "$st"; fail=1; }
git diff --quiet HEAD && git diff --cached --quiet HEAD && say "index == HEAD, worktree == index" || { say "diff vs HEAD"; fail=1; }
flags=$(git ls-files -v | grep -v '^H ' | head -5)
[ -z "$flags" ] && say "no skip-worktree / assume-unchanged flags" || { say "flags: $flags"; fail=1; }
# every tracked blob re-hashed from disk against HEAD, with its HEAD mode
bad=0; n=0
git ls-tree -r HEAD | while read -r mode type oid path; do
  [ "$type" = blob ] || continue
  if [ "$mode" = 120000 ]; then got=$(readlink "$path" | tr -d '\n' | git hash-object --stdin); dm=120000
  else got=$(git hash-object --no-filters -- "$path"); [ -x "$path" ] && dm=100755 || dm=100644; fi
  [ "$got" = "$oid" ] && [ "$dm" = "$mode" ] || echo "BLOB MISMATCH $mode $oid $path"
done > /tmp/.vc_$$ 2>&1
n=$(git ls-tree -r HEAD | awk '$2=="blob"' | wc -l)
if [ -s /tmp/.vc_$$ ]; then cat /tmp/.vc_$$; fail=1; else say "superproject: $n tracked blobs re-hash to HEAD with HEAD modes"; fi
rm -f /tmp/.vc_$$
for sm in protocol-processor gptp-processor; do
  want=$(git ls-tree HEAD "$sm" | awk '{print $3}')
  if [ -d "$sm/.git" ] || [ -f "$sm/.git" ]; then
    got=$(git -C "$sm" rev-parse HEAD)
    [ "$got" = "$want" ] && say "gitlink $sm ok $want" || { say "gitlink $sm MISMATCH $got != $want"; fail=1; }
    s2=$(git -C "$sm" status --porcelain --ignored --untracked-files=all)
    [ -z "$s2" ] && say "$sm worktree clean (incl. ignored)" || { say "$sm NOT clean: $s2"; fail=1; }
    m=$(git -C "$sm" ls-tree -r HEAD | awk '$2=="blob"' | while read -r mode type oid path; do
          got=$(git -C "$sm" hash-object --no-filters -- "$path"); [ "$got" = "$oid" ] || echo "$path"; done | wc -l)
    k=$(git -C "$sm" ls-tree -r HEAD | awk '$2=="blob"' | wc -l)
    [ "$m" = 0 ] && say "$sm: $k tracked blobs re-hash to its pin" || { say "$sm: $m blob mismatches"; fail=1; }
  else say "$sm not initialized (gitlink $want)"; fi
done
say "gitlinks at HEAD:"; git ls-tree HEAD protocol-processor gptp-processor external third_party/verilog-axis
[ $fail = 0 ] && say "VERIFY PASS" || say "VERIFY FAIL"
exit $fail

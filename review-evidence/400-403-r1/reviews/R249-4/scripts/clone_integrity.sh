#!/usr/bin/env bash
# Verify the candidate clone is byte-exact at the reviewed head after all probes.
set -u
H=09419d88053bd7777de966ce825e4ad7fe71c713; T=d1c94326094b9c9c2ef2f6ecce0f065f003fd7bb
fail=0
[ "$(git rev-parse HEAD)" = "$H" ] && echo "HEAD ok $H" || { echo "HEAD MISMATCH"; fail=1; }
[ "$(git rev-parse 'HEAD^{tree}')" = "$T" ] && echo "tree ok $T" || { echo "tree MISMATCH"; fail=1; }
[ "$(git write-tree)" = "$T" ] && echo "index tree == HEAD tree" || { echo "INDEX differs from HEAD"; fail=1; }
s=$(git status --porcelain --untracked-files=all); [ -z "$s" ] && echo "status clean (tracked + untracked, ignored build outputs excluded)" || { echo "STATUS DIRTY:"; echo "$s"; fail=1; }
v=$(git ls-files -v | grep -v '^H ' | grep -v '^S ' ; git ls-files -v | grep -E '^[a-z]|^S ' ); [ -z "$v" ] && echo "no assume-unchanged/skip-worktree flags" || { echo "INDEX FLAGS:"; echo "$v"; fail=1; }
n=0; bad=0
while IFS=$'\t' read -r meta path; do
  set -- $meta; mode=$1; oid=$3
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin); [ -L "$path" ] || { echo "not symlink: $path"; bad=$((bad+1)); continue; }
  else got=$(git hash-object --no-filters "$path"); fm=$([ -x "$path" ] && echo 100755 || echo 100644); [ "$fm" = "$mode" ] || { echo "MODE $path $fm != $mode"; bad=$((bad+1)); }; fi
  [ "$got" = "$oid" ] || { echo "BLOB $path $got != $oid"; bad=$((bad+1)); }
done < <(git ls-tree -r HEAD)
echo "tracked non-gitlink entries checked: $n, mismatches: $bad"; [ $bad -eq 0 ] || fail=1
git ls-tree -r HEAD | awk '$1=="160000"{print $3" "$4}' | while read -r oid path; do
  if [ -e "$path/.git" ]; then
    got=$(git -C "$path" rev-parse HEAD); d=$(git -C "$path" status --porcelain --untracked-files=no | wc -l)
    echo "gitlink $path recorded $oid checked-out $got dirty-tracked=$d $([ "$got" = "$oid" ] && [ "$d" = 0 ] && echo OK || echo MISMATCH)"
  else echo "gitlink $path recorded $oid not checked out"; fi
done
exit $fail

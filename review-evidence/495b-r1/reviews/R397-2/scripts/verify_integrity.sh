#!/bin/bash
# Verify a checkout equals its HEAD: every tracked regular file / symlink hashes to
# its index blob with its index mode, the index equals HEAD's tree, no tracked file
# is flagged assume-unchanged/skip-worktree, no untracked non-ignored file exists,
# and each initialized submodule sits at its recorded gitlink.
set -u
cd "$1" || exit 2
G=/usr/bin/git
export GIT_NO_REPLACE_OBJECTS=1
echo "HEAD $($G rev-parse HEAD) tree $($G rev-parse 'HEAD^{tree}')"
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  [ "$mode" = 160000 ] && continue
  n=$((n+1))
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] && [ "$(printf %s "$(readlink "$path")" | $G hash-object --stdin)" = "$blob" ] || { echo "BAD symlink $path"; bad=$((bad+1)); }
    continue
  fi
  [ -f "$path" ] && [ ! -L "$path" ] || { echo "BAD not a regular file: $path"; bad=$((bad+1)); continue; }
  [ "$($G hash-object --no-filters -- "$path")" = "$blob" ] || { echo "BAD bytes $path"; bad=$((bad+1)); }
  if [ -x "$path" ]; then fm=100755; else fm=100644; fi
  [ "$fm" = "$mode" ] || { echo "BAD mode $path $fm != $mode"; bad=$((bad+1)); }
done < <($G ls-files -s)
echo "tracked files checked: $n, mismatches: $bad"
[ -z "$($G diff-index --cached HEAD 2>/dev/null)" ] && echo "index == HEAD tree" || { echo "BAD index differs from HEAD"; bad=$((bad+1)); }
flags=$($G ls-files -v | grep -v '^H ' | grep -v '^S ' ; $G ls-files -v | grep -E '^(h|S|s) ' )
[ -z "$flags" ] && echo "no assume-unchanged/skip-worktree flags" || { echo "BAD flags:"; echo "$flags" | head; bad=$((bad+1)); }
ut=$($G ls-files --others --exclude-standard)
[ -z "$ut" ] && echo "no untracked non-ignored files" || { echo "BAD untracked:"; echo "$ut" | head; bad=$((bad+1)); }
$G submodule status 2>/dev/null
for sm in gptp-processor protocol-processor third_party/verilog-axis; do
  want=$($G ls-tree HEAD "$sm" | awk '{print $3}'); have=$($G -C "$sm" rev-parse HEAD)
  dirty=$($G -C "$sm" status --porcelain --untracked-files=no)
  [ "$want" = "$have" ] && [ -z "$dirty" ] && echo "gitlink ok $sm $want" || { echo "BAD gitlink $sm want $want have $have dirty=[$dirty]"; bad=$((bad+1)); }
done
echo "INTEGRITY $([ $bad -eq 0 ] && echo OK || echo FAIL) ($bad)"

#!/usr/bin/env bash
# Record the exact-head state of a review clone: HEAD, tree, index-vs-HEAD,
# worktree-vs-index (every tracked blob rehashed), untracked files, and the
# submodule gitlinks against their checked-out HEADs and clean status.
# Usage: tree_state.sh <clone> <expected-head>
set -u
clone=$1; want=$2
cd "$clone" || exit 2
rc=0
head=$(git rev-parse HEAD); tree=$(git rev-parse 'HEAD^{tree}')
echo "head=$head"; echo "tree=$tree"
[ "$head" = "$want" ] || { echo "HEAD MISMATCH"; rc=1; }
# index vs HEAD tree (mode, blob, path)
if git diff-index --cached --quiet HEAD --; then echo "index==HEAD: yes"; else echo "index==HEAD: NO"; git diff-index --cached HEAD --; rc=1; fi
# every tracked non-gitlink entry rehashed from the worktree bytes; mode checked
bad=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  [ "$mode" = 160000 ] && continue
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] && got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin) || got=missing
  else
    [ -f "$path" ] && [ ! -L "$path" ] && got=$(git hash-object --no-filters -- "$path") || got=missing
    if [ "$got" != missing ]; then
      if [ -x "$path" ]; then fm=100755; else fm=100644; fi
      [ "$fm" = "$mode" ] || { echo "MODE $path index=$mode fs=$fm"; bad=$((bad+1)); }
    fi
  fi
  [ "$got" = "$blob" ] || { echo "BLOB $path index=$blob fs=$got"; bad=$((bad+1)); }
done < <(git ls-files -s -z | tr '\0' '\n' | sed -E 's/^([0-7]+) ([0-9a-f]+) ([0-3])\t/\1 \2 \3\t/')
echo "tracked blob/mode mismatches: $bad"; [ $bad -eq 0 ] || rc=1
unt=$(git ls-files --others --exclude-standard | wc -l); echo "untracked (non-ignored) files: $unt"
[ "$unt" -eq 0 ] || { git ls-files --others --exclude-standard | head; rc=1; }
for sm in gptp-processor protocol-processor third_party/verilog-axis; do
  link=$(git ls-files -s -- "$sm" | awk '{print $2}')
  subhead=$(git -C "$sm" rev-parse HEAD 2>/dev/null || echo none)
  dirty=$(git -C "$sm" status --porcelain --untracked-files=no 2>/dev/null | wc -l)
  echo "submodule $sm gitlink=$link head=$subhead dirty_tracked=$dirty"
  [ "$link" = "$subhead" ] && [ "$dirty" -eq 0 ] || rc=1
done
echo "RESULT rc=$rc"; exit $rc

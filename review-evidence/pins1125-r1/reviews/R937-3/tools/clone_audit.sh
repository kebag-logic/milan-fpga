#!/bin/bash
# clone_audit.sh CLONE EXPECT_HEAD EXPECT_TREE: verify that the clone's tracked
# bytes, modes and index equal the commit, without trusting status flags.
set -u
C=$1; H=$2; T=$3
g() { git -C "$C" "$@"; }
echo "# clone audit at $(date -u +%FT%TZ)"
echo "HEAD $(g rev-parse HEAD) expect $H"
echo "tree $(g rev-parse 'HEAD^{tree}') expect $T"
echo "write-tree $(g write-tree)"
echo "porcelain lines: $(g status --porcelain --ignore-submodules=none | wc -l)"
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  mode=${meta%% *}; rest=${meta#* }; sha=${rest%% *}
  [ "$mode" = 160000 ] && continue
  n=$((n+1)); f="$C/$path"
  if [ "$mode" = 120000 ]; then got=$(printf '%s' "$(readlink "$f")" | git hash-object --stdin)
  else got=$(git hash-object --no-filters "$f")
       if [ -x "$f" ]; then fm=100755; else fm=100644; fi
       [ "$fm" = "$mode" ] || { echo "MODE $path $fm != $mode"; bad=$((bad+1)); }
  fi
  [ "$got" = "$sha" ] || { echo "BYTES $path"; bad=$((bad+1)); }
done < <(g ls-tree -r HEAD | awk '{print $1" "$3"\t"substr($0, index($0,"\t")+1)}')
echo "tracked non-gitlink files checked: $n, mismatches: $bad"
echo "index vs HEAD: $(g diff-index --cached HEAD | wc -l) entries differ"
echo "== gitlinks: recorded, checked-out"
g ls-tree -r HEAD | awk '$2=="commit"{print $3, $4}' | while read -r sha p; do
  if [ -e "$C/$p/.git" ]; then co=$(git -C "$C/$p" rev-parse HEAD 2>/dev/null); else co="(uninitialised)"; fi
  echo "$p recorded=$sha checkout=$co $([ "$co" = "$sha" ] && echo OK || echo -)"
done

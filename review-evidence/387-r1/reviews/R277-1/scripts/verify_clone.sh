#!/bin/sh
# Verify a review clone sits at the exact head with byte-exact tracked blobs,
# modes and index, and the required submodules at their gitlinks.
# Usage: verify_clone.sh <clone> <expected head> <expected tree>
set -u
clone=$1 head=$2 tree=$3
cd "$clone" || exit 2
rc=0
got_head=$(git rev-parse HEAD) || exit 2
got_tree=$(git rev-parse 'HEAD^{tree}') || exit 2
echo "head $got_head"
echo "tree $got_tree"
[ "$got_head" = "$head" ] || { echo "FAIL head"; rc=1; }
[ "$got_tree" = "$tree" ] || { echo "FAIL tree"; rc=1; }
# The index must describe exactly HEAD's tree.
idx_tree=$(git write-tree) || exit 2
echo "index-tree $idx_tree"
[ "$idx_tree" = "$tree" ] || { echo "FAIL index differs from HEAD tree"; rc=1; }
# No index flag may hide a change from the byte check below.
hidden=$(git ls-files -v | grep -c '^[a-zS]' || true)
echo "assume-unchanged-or-skip-worktree $hidden"
[ "$hidden" = 0 ] || { echo "FAIL hidden index flags"; rc=1; }
# Every regular tracked file hashes to its index blob, with its index mode.
bad=0
git ls-files -s | while IFS= read -r line; do
  meta=${line%%	*}; path=${line#*	}
  mode=${meta%% *}; rest=${meta#* }; blob=${rest%% *}
  case $mode in
    160000) continue ;;
    120000) got=$(printf '%s' "$(readlink "$path")" | git hash-object --stdin) ;;
    100644|100755)
      [ -f "$path" ] && [ ! -L "$path" ] || { echo "FAIL not a regular file: $path"; echo x; continue; }
      got=$(git hash-object --no-filters -- "$path")
      if [ -x "$path" ]; then fm=100755; else fm=100644; fi
      [ "$fm" = "$mode" ] || { echo "FAIL mode $path $fm != $mode"; echo x; } ;;
    *) echo "FAIL unexpected mode $mode $path"; echo x; continue ;;
  esac
  [ "$got" = "$blob" ] || { echo "FAIL bytes $path"; echo x; }
done > /tmp/.verify_clone_$$ 2>&1
bad=$(grep -c '^x$' /tmp/.verify_clone_$$ || true)
grep '^FAIL' /tmp/.verify_clone_$$ || true
rm -f /tmp/.verify_clone_$$
echo "tracked-blob-failures $bad"
[ "$bad" = 0 ] || rc=1
# Nothing untracked or ignored left behind in the superproject.
extra=$(git status --porcelain --ignored --untracked-files=all --ignore-submodules=none | wc -l)
echo "status-lines $extra"
[ "$extra" = 0 ] || { git status --porcelain --ignored --untracked-files=all | head -20; rc=1; }
# Required submodules at their gitlinks, clean including ignored files.
for sm in third_party/verilog-axis protocol-processor gptp-processor; do
  link=$(git rev-parse ":$sm")
  sh=$(git -C "$sm" rev-parse HEAD)
  dirty=$(git -C "$sm" status --porcelain --ignored --untracked-files=all | wc -l)
  shidden=$(git -C "$sm" ls-files -v | grep -c '^[a-zS]' || true)
  # every tracked submodule file hashes to the blob its own HEAD records
  sbad=$(cd "$sm" && git ls-tree -r HEAD | while IFS= read -r l; do
      m=${l%% *}; r=${l#* }; b=${r#* }; b=${b%%	*}; f=${l#*	}
      case $m in
        100644|100755) [ "$(git hash-object --no-filters -- "$f")" = "$b" ] || echo "$f" ;;
        120000) [ "$(printf '%s' "$(readlink "$f")" | git hash-object --stdin)" = "$b" ] || echo "$f" ;;
      esac
    done | wc -l)
  echo "submodule $sm gitlink $link head $sh dirty $dirty hidden $shidden blob-mismatch $sbad"
  [ "$link" = "$sh" ] && [ "$dirty" = 0 ] && [ "$shidden" = 0 ] && [ "$sbad" = 0 ] || { echo "FAIL submodule $sm"; rc=1; }
done
echo "verify_clone rc=$rc"
exit $rc

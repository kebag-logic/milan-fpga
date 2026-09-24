#!/usr/bin/env bash
# Verify a clone matches its HEAD: tracked blob bytes and modes, index, gitlinks,
# and no untracked or ignored entries. Usage: integrity.sh <repo> <expected-sha>
set -u
cd "$1" || exit 2
exp=$2; bad=0
[ "$(git rev-parse HEAD)" = "$exp" ] || { echo "HEAD mismatch"; bad=1; }
echo "HEAD $(git rev-parse HEAD) tree $(git rev-parse 'HEAD^{tree}')"
n=0
while IFS= read -r -d '' ent; do
  meta=${ent%%$'\t'*}; path=${ent#*$'\t'}
  mode=${meta%% *}; rest=${meta#* }; type=${rest%% *}; sha=${rest#* }
  if [ "$type" = commit ]; then
    echo "gitlink $path $sha"; continue
  fi
  n=$((n+1))
  if [ "$mode" = 120000 ]; then
    [ -L "$path" ] && [ "$(printf %s "$(readlink "$path")" | git hash-object --stdin)" = "$sha" ] || { echo "BAD symlink $path"; bad=1; }
  else
    [ "$(git hash-object --no-filters -- "$path")" = "$sha" ] || { echo "BAD bytes $path"; bad=1; }
    if [ -x "$path" ]; then fm=100755; else fm=100644; fi
    [ "$fm" = "$mode" ] || { echo "BAD mode $path $fm != $mode"; bad=1; }
  fi
done < <(git ls-tree -r -z HEAD)
echo "blobs checked: $n"
[ -z "$(git diff-index --cached HEAD)" ] || { echo "index differs from HEAD"; bad=1; }
u=$(git status --porcelain --ignored --untracked-files=all)
[ -z "$u" ] || { echo "untracked/ignored/modified entries:"; echo "$u"; bad=1; }
git submodule status 2>&1 | sed 's/^/submodule-status: /'
echo "result: $([ $bad = 0 ] && echo OK || echo FAIL)"
exit $bad

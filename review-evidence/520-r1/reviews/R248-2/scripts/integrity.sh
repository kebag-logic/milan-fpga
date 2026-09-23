#!/usr/bin/env bash
# Verify a clone is byte-exact at the reviewed head: HEAD/tree ids, every
# tracked blob's bytes and mode against HEAD, the index against HEAD, no
# untracked or modified paths, and the three required submodule gitlinks
# checked out at their pinned commits.
# usage: integrity.sh <clone> <expected-head> <expected-tree>
set -euo pipefail
clone="$1"; want_head="$2"; want_tree="$3"
cd "$clone"
fail=0
head="$(git rev-parse HEAD)"; tree="$(git rev-parse 'HEAD^{tree}')"
echo "head=$head"; echo "tree=$tree"
[ "$head" = "$want_head" ] || { echo "FAIL head"; fail=1; }
[ "$tree" = "$want_tree" ] || { echo "FAIL tree"; fail=1; }
# Index equals HEAD (no staged change), including modes.
if ! git diff-index --cached --quiet HEAD --; then echo "FAIL index differs from HEAD"; fail=1; fi
# Every tracked regular blob: worktree bytes hash to the HEAD blob id, mode matches.
bad=0; n=0
while IFS=$'\t' read -r meta path; do
  mode="${meta%% *}"; rest="${meta#* }"; type="${rest%% *}"; oid="${rest#* }"
  [ "$type" = blob ] || continue
  n=$((n + 1))
  if [ "$mode" = 120000 ]; then
    got="$(printf '%s' "$(readlink "$path")" | git hash-object --stdin)"
    [ -L "$path" ] || { echo "FAIL not a symlink: $path"; bad=$((bad + 1)); continue; }
  else
    [ -f "$path" ] && [ ! -L "$path" ] || { echo "FAIL missing/not regular: $path"; bad=$((bad + 1)); continue; }
    got="$(git hash-object --no-filters "$path")"
    if [ -x "$path" ]; then fm=100755; else fm=100644; fi
    [ "$fm" = "$mode" ] || { echo "FAIL mode $path $fm != $mode"; bad=$((bad + 1)); }
  fi
  [ "$got" = "$oid" ] || { echo "FAIL bytes $path"; bad=$((bad + 1)); }
done < <(git ls-tree -r --full-tree HEAD)
echo "tracked_blobs_checked=$n mismatches=$bad"
[ "$bad" -eq 0 ] || fail=1
# Porcelain status (tracked changes and untracked files; ignored files listed separately).
st="$(git status --porcelain=v1 --untracked-files=all)"
if [ -n "$st" ]; then echo "FAIL status not clean:"; echo "$st"; fail=1; else echo "status=clean"; fi
ign="$(git status --porcelain=v1 --ignored=matching --untracked-files=all | grep '^!!' || true)"
echo "ignored_paths=$(printf '%s' "$ign" | grep -c . || true)"
[ -z "$ign" ] || echo "$ign" | sed 's/^/  /'
# Required submodules: gitlink in HEAD, single stage-0 index record, checkout at pin, clean.
for sub in third_party/verilog-axis protocol-processor gptp-processor; do
  pin="$(git ls-tree HEAD "$sub" | awk '$1=="160000"{print $3}')"
  idx="$(git ls-files -s "$sub")"
  co="$(git -C "$sub" rev-parse HEAD 2>/dev/null || echo none)"
  dirty="$(git -C "$sub" status --porcelain=v1 --untracked-files=all 2>/dev/null | wc -l)"
  echo "submodule $sub pin=$pin checkout=$co dirty_lines=$dirty index=[$idx]"
  [ -n "$pin" ] && [ "$co" = "$pin" ] && [ "$dirty" -eq 0 ] \
    && [ "$idx" = "160000 $pin 0	$sub" ] || { echo "FAIL submodule $sub"; fail=1; }
done
[ "$fail" -eq 0 ] && echo "INTEGRITY OK" || { echo "INTEGRITY FAIL"; exit 1; }

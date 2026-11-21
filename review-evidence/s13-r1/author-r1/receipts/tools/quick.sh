#!/usr/bin/env bash
# quick.sh <tree> <outdir> <checks-file>: run each "name<TAB>command" line of <checks-file> in <tree>, up to QJ at once,
# each into <outdir>/<name>.log with its exit status in <outdir>/<name>.rc; then print one line per check and the
# tree's porcelain count (a check must not dirty the tree).
set -u
tree=$1; out=$2; list=$3; QJ=${QJ:-6}
. <scratch>/bin/env.sh
export TMPDIR=<scratch>/tmp PYTHONDONTWRITEBYTECODE=1 MAKEFLAGS="-j16 --no-print-directory"
mkdir -p "$out" "$TMPDIR"
run_one() {
  local name=$1 cmd=$2
  ( cd "$tree" && echo "CMD $cmd" && echo "HEAD $(git rev-parse --short=8 HEAD) START $(date +%T)" && bash -c "$cmd"; echo "rc=$?" ) > "$out/$name.log" 2>&1
  tail -n1 "$out/$name.log" | sed 's/^rc=//' > "$out/$name.rc"
}
while IFS=$'\t' read -r name cmd; do
  [ -z "$name" ] && continue
  case "$name" in \#*) continue;; esac
  while [ "$(jobs -rp | wc -l)" -ge "$QJ" ]; do wait -n; done
  run_one "$name" "$cmd" &
done < "$list"
wait
fail=0
while IFS=$'\t' read -r name cmd; do
  [ -z "$name" ] && continue
  case "$name" in \#*) continue;; esac
  rc=$(cat "$out/$name.rc" 2>/dev/null || echo '?')
  [ "$rc" = 0 ] || fail=1
  printf '%-28s rc=%s  %s\n' "$name" "$rc" "$(grep -v '^rc=' "$out/$name.log" | tail -n1 | cut -c1-150)"
done < "$list"
echo "tree porcelain: $(git -C "$tree" status --porcelain --untracked-files=all | wc -l)"
exit $fail

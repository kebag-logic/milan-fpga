#!/bin/sh
# Reviewer static checks for FPGA-gPTP #75 / PR #76 round 2.
# Independent of the PR's own checker: every local #L anchor in
# docs/SOURCE_EVIDENCE.md is resolved with git show at a given revision and the
# anchored line plus one line of context is printed, so a reader can judge
# whether it is the claimed construct. Runs read-only against a clone.
# Usage: static_checks.sh <clone> <rev> [<rev> ...]
set -eu
clone=$1; shift
for rev in "$@"; do
  echo "=== anchors at $rev ($(git -C "$clone" rev-parse "$rev"))"
  git -C "$clone" show "$rev:docs/SOURCE_EVIDENCE.md" |
    grep -n '^|' |
    while IFS= read -r row; do
      claim=$(printf '%s' "$row" | cut -d'|' -f2 | sed 's/^ *//;s/ *$//')
      printf '%s\n' "$row" | grep -o '](\.\./[^)#]*#L[0-9]*)' |
        sed 's/^](\.\.\///;s/)$//' |
        while IFS= read -r a; do
          f=${a%%#L*}; n=${a##*#L}
          l=$(git -C "$clone" show "$rev:$f" | sed -n "${n}p")
          prev=$(git -C "$clone" show "$rev:$f" | sed -n "$((n-1))p")
          printf '%-32s %s#L%s\n    L%s-1: %s\n    L%s  : %s\n' \
            "$claim" "$f" "$n" "$n" "$prev" "$n" "$l"
        done
    done
done

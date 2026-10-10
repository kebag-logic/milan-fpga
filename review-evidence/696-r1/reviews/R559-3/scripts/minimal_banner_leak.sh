#!/bin/sh
# Does a make's OWN "Entering directory" banner leak into its $(shell ...)
# capture? Minimal case, no repository files. Usage: minimal_banner_leak.sh <dir> <make>...
d=$1; shift
printf 'X := $(shell echo payload)\nall: ; @echo "captured=[$(X)]"\n' > "$d/t.mk"
for m in "$@"; do
  v=$($m --version | head -1)
  for mf in "" w; do
    for sink in tty-file pipe; do
      if [ $sink = pipe ]; then o=$(cd "$d" && MAKEFLAGS=$mf $m -f t.mk 2>/dev/null | cat)
      else (cd "$d" && MAKEFLAGS=$mf $m -f t.mk > "$d/out.txt" 2>/dev/null); o=$(cat "$d/out.txt"); fi
      echo "$v MAKEFLAGS='$mf' stdout=$sink :: $(printf '%s' "$o" | grep captured | sed "s|$d|<dir>|g")"
    done
  done
done

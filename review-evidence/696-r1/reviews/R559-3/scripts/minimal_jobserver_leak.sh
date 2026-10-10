#!/bin/sh
# Minimal case of the hosted pollution: a nested make run by $(shell), with
# --no-print-directory, inheriting MAKEFLAGS that carry a print-directory flag
# and a jobserver whose descriptors it cannot use.
# Usage: minimal_jobserver_leak.sh <dir> <make>...
d=$1; shift; mkdir -p "$d/sub"
printf 'print-x: ; @echo payload\n' > "$d/sub/Makefile"
printf 'X := $(shell $(MAKE) -s --no-print-directory -C sub print-x)\nall: ; @echo "captured=[$(X)]"\n' > "$d/n.mk"
printf 'X := $(shell MAKEFLAGS= $(MAKE) -s --no-print-directory -C sub print-x)\nall: ; @echo "captured=[$(X)]"\n' > "$d/c.mk"
for m in "$@"; do
  v=$($m --version | head -1)
  for f in n.mk c.mk; do
    for mf in "w" "w -j8 --jobserver-auth=97,98" "w -j8 --jobserver-auth=fifo:/nonexistent" " -j8 --jobserver-auth=97,98"; do
      o=$(cd "$d" && MAKEFLAGS="$mf" $m -f $f 2>/dev/null | grep captured | sed "s|$d|<dir>|g")
      echo "$v $f MAKEFLAGS='$mf' :: $o"
    done
  done
done

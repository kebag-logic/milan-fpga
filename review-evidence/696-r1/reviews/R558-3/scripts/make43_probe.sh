#!/bin/sh
# Usage: make43_probe.sh <clone> <scratchdir> <make-binary-dir>
# Reproduces the hosted derivation context with a chosen GNU make on PATH:
# inherited MAKEFLAGS=w, and a recursive `-j8` parent (the shape mutants.py
# creates: make -j8 ... integration-build -> $(MAKE) -f integration.mk -> $(shell $(MAKE) ...)).
# Each probe makefile is a disposable copy with one appended parse-only target;
# variant "noguard" drops the guard so the full captured text can be printed.
set -u
C=$1; S=$2; MB=$3; M=$C/tb/verilator/maap
mkdir -p "$S"; export PATH="$MB:$PATH"
echo "head=$(git -C "$C" rev-parse HEAD) make=$(make --version | head -1) at $(command -v make)"
mk() { { cat "$2"; printf '\nprobe-print:\n\t@echo "SRCS-WORDS=$(words $(SRCS)) NONFILE=[$(strip $(foreach w,$(SRCS),$(if $(shell test -f $(w) && echo y),,$(w))))]"\n'; } > "$S/$1.mk"; }
mk head "$M/integration.mk"
sed '/^ifneq (\$(filter-out/,/^endif/d' "$M/integration.mk" > "$S/noguard.src"; mk noguard "$S/noguard.src"
sed 's/\$(shell \$(MAKE) -s --no-print-directory/$(shell MAKEFLAGS= $(MAKE) -s --no-print-directory/' "$M/integration.mk" > "$S/sibling.src"; mk sibling "$S/sibling.src"
printf 'all:\n\t+@$(MAKE) -s -C %s -f $(PROBE) probe-print\n' "$M" > "$S/parent.mk"
for v in head noguard sibling; do
  for ctx in plain w j8 w+j8; do
    case $ctx in
      plain) out=$(cd "$M" && env -u MAKEFLAGS make -s -f "$S/$v.mk" probe-print 2>&1);;
      w)     out=$(cd "$M" && env MAKEFLAGS=w make -s -f "$S/$v.mk" probe-print 2>&1);;
      j8)    out=$(cd / && env -u MAKEFLAGS make -j8 -f "$S/parent.mk" PROBE="$S/$v.mk" 2>&1);;
      w+j8)  out=$(cd / && env MAKEFLAGS=w make -j8 -f "$S/parent.mk" PROBE="$S/$v.mk" 2>&1);;
    esac
    rc=$?
    echo "== $v $ctx rc=$rc"
    printf '%s\n' "$out" | grep -E 'SRCS-WORDS|non-files|jobserver' | cut -c1-300
  done
done

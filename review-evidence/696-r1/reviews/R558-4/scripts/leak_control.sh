#!/bin/sh
# Usage: leak_control.sh <clone> <scratchdir-from-guard_probe> <make-binary-dir>
# The hosted failure shape at b9b38961 (suite-logs-1 of run 38027027728: "jobserver
# unavailable" then "names non-files: make[2]:") needs an inherited w flag AND an
# advertised but unavailable jobserver. Reproduced here by handing the outer make
# MAKEFLAGS='w -j8 --jobserver-auth=97,98' (descriptors that are not open).
# head = exact-head integration.mk; prefix = the same file without MAKEFLAGS= (the
# b9b38961 capture form). Requires guard_probe.sh to have generated <scratch>/{head,prefix}.mk.
set -u
C=$1; S=$2; MB=$3; M=$C/tb/verilator/maap; export PATH="$MB:$PATH"
echo "head=$(git -C "$C" rev-parse HEAD) make=$(make --version | head -1)"
for v in head prefix; do for mf in 'w -j8 --jobserver-auth=97,98' '-j8 --jobserver-auth=97,98' 'w'; do
  out=$(cd "$M" && env MAKEFLAGS="$mf" make -s -f "$S/$v.mk" probe-print 2>&1); rc=$?
  echo "== $v [$mf] rc=$rc"; printf '%s\n' "$out" | grep -E 'SRCS-WORDS|--build|non-files' | sed 's#.*\*\*\* #*** #' | cut -c1-160
done; done

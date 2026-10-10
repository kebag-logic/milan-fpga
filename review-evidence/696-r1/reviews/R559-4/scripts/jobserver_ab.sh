#!/bin/sh
# Usage: jobserver_ab.sh <clone> <scratchdir> <make>...
# Parse-time A/B of the integration.mk captures with an inherited MAKEFLAGS carrying a
# print-directory flag and a jobserver whose descriptors are not open (what a nested
# make sees when python's subprocess closes the -j8 parent's jobserver fds).
# A = integration.mk from b9b38961, B = the clone's HEAD. VERILATOR=echo: nothing builds.
set -u
C=$1; S=$2; shift 2; M=$C/tb/verilator/maap; mkdir -p "$S"
git -C "$C" show b9b389611:tb/verilator/maap/integration.mk > "$S/A.mk"; cp "$M/integration.mk" "$S/B.mk"
for m in "$@"; do
  echo "#### $($m --version | head -1)"
  for v in A B; do
    for mf in "w" "w -j8 --jobserver-auth=97,98" " -j8 --jobserver-auth=97,98"; do
      out=$(cd "$M" && env -u VERILATOR_JOBS MAKEFLAGS="$mf" "$m" -s -f "$S/$v.mk" build DP_MDIR="$S/obj-$v" VERILATOR=echo 2>/dev/null); rc=$?
      echo "== $v MAKEFLAGS='$mf' rc=$rc :: $(printf '%s\n' "$out" | grep -oE 'non-files: [^ ]*|--build -j [0-9]+|Entering directory|leaked' | sort | uniq -c | tr '\n' ' ')"
      err=$(cd "$M" && env -u VERILATOR_JOBS MAKEFLAGS="$mf" "$m" -s -f "$S/$v.mk" build DP_MDIR="$S/obj-$v" VERILATOR=echo 2>&1 >/dev/null | grep -E 'non-files|jobserver' | head -2 | cut -c1-160)
      [ -n "$err" ] && echo "   stderr: $err"
    done
  done
done

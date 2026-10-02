#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R433-3: does `MAKEFLAGS=` on the root suite's nested derivations change the
# verilator command line mclk-build would run? Dry-run (-n) the head's and the
# round-2 (d81198c2) tb/verilator/milan_dp_mclk/Makefile under GNU make 4.3 and
# the host make, in several invocation contexts, and compare the --Mdir line.
# Usage: nested_derivation_equiv.sh <copy of the head> <make 4.3 dir>
set -u
T=$(cd "$1" && pwd); M43=$(cd "$2" && pwd)
cd "$T"
MK=tb/verilator/milan_dp_mclk/Makefile
cp $MK /tmp/r433_3_equiv_head.$$
git show d81198c2001756fd84c353d93c312c133c5af66b:$MK > /tmp/r433_3_equiv_r2.$$
line() { grep -- '--Mdir' | sha256sum | cut -c1-16; }
for which in make43 host; do
  if [ $which = make43 ]; then PATHX="$M43:$PATH"; else PATHX="$PATH"; fi
  for ctx in plain nested_w jobs16 cmdline_override; do
    for mk in head r2; do
      if [ $mk = head ]; then cp /tmp/r433_3_equiv_head.$$ $MK; else cp /tmp/r433_3_equiv_r2.$$ $MK; fi
      case $ctx in
        plain)            o=$(env -u MAKEFLAGS -u MAKELEVEL PATH=$PATHX make -s -C tb/verilator/milan_dp_mclk -n mclk-build 2>&1) ;;
        nested_w)         o=$(MAKEFLAGS=w MAKELEVEL=1 PATH=$PATHX make -s -C tb/verilator/milan_dp_mclk -n mclk-build 2>&1) ;;
        jobs16)           o=$(env -u MAKEFLAGS -u MAKELEVEL PATH=$PATHX make -j16 -s -C tb/verilator/milan_dp_mclk -n mclk-build 2>&1) ;;
        cmdline_override) o=$(env -u MAKEFLAGS -u MAKELEVEL PATH=$PATHX make -s -C tb/verilator/milan_dp_mclk -n mclk-build MCLK_MDIR=obj_probe 2>&1) ;;
      esac
      n=$(printf '%s\n' "$o" | grep -- '--Mdir' | grep -c 'Entering directory')
      printf '%-7s %-16s %-4s --Mdir lines=%s hash=%s polluted=%s\n' $which $ctx $mk \
        "$(printf '%s\n' "$o" | grep -c -- '--Mdir')" "$(printf '%s\n' "$o" | line)" "$n"
    done
  done
done
cp /tmp/r433_3_equiv_head.$$ $MK
rm -f /tmp/r433_3_equiv_head.$$ /tmp/r433_3_equiv_r2.$$
git diff --quiet && echo "copy restored: no tracked change" || echo "copy NOT restored"

#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R433-3 entity-shape gate probes on a disposable copy of the head, under GNU
# make 4.3 and the host make.
# Usage: gate_probes.sh <copy of the head> <dir holding a make 4.3 binary named make>
#   1. make's database for the root suite (tb/verilator/milan_dp_mclk): is it
#      complete, and which frozen shape-header prerequisite does it record?
#   2. classified_frozen_targets() for every makefile consumer of the set.
#   3. the plain gate (no --self-test) under each make.
#   4. fault probe: a stray rule prerequisite naming a DIFFERENT builder-shaped
#      header in the root suite's Makefile must still be refused under both makes
#      (the frozen-form match is not a blanket pass for that makefile).
#   5. fault probe: the root suite's nested derivation with MAKEFLAGS= removed
#      (the round-2 Makefile line) and the gate's database read under each make.
set -u
T=$(cd "$1" && pwd); M43=$(cd "$2" && pwd)
cd "$T"
MK=tb/verilator/milan_dp_mclk/Makefile
for which in make43 host; do
  if [ $which = make43 ]; then PATHX="$M43:$PATH"; else PATHX="$PATH"; fi
  echo "===== $which: $(PATH=$PATHX make --version | head -1)"
  echo "-- 1. database of $MK"
  out=$(cd tb/verilator/milan_dp_mclk && PATH=$PATHX MAKEFLAGS= make -pqrR -f Makefile 2>&1)
  printf '%s\n' "$out" | grep -c '^# Files' | sed 's/^/   "# Files" sections: /'
  printf '%s\n' "$out" | grep -E '^[^#[:space:]].*:.*adp_shape_defaults\.svh' | cut -c1-200 | sed 's/^/   rule: /'
  printf '%s\n' "$out" | grep -E 'print-srcs failed|print-dp-vflags failed' | sed 's/^/   stop: /'
  echo "-- 2. classified_frozen_targets"
  PATH=$PATHX python3 -c "
import sys; sys.path.insert(0, 'scripts')
import shape_consumer_inventory as inv
names = sorted({c for c, _ in inv.CLASSIFIED_CONSUMERS if inv.is_make_consumer(c)})
for n in names: print('  ', n, sorted(inv.classified_frozen_targets(n)))
"
  echo "-- 3. plain gate"
  PATH=$PATHX python3 scripts/check_entity_shape.py > /tmp/r433_3_plain.$$ 2>&1; echo "   rc=$?"; tail -n 2 /tmp/r433_3_plain.$$ | sed 's/^/   /'
  echo "-- 4. stray prerequisite planted in $MK"
  cp $MK /tmp/r433_3_mk.$$
  printf '\nstray-probe: obj_stray/endstation_stray/gen/adp_shape_defaults.svh\n' >> $MK
  PATH=$PATHX python3 scripts/check_entity_shape.py > /tmp/r433_3_plain.$$ 2>&1; echo "   rc=$? (must be non-zero)"
  grep -n 'obj_stray' /tmp/r433_3_plain.$$ | head -3 | sed 's/^/   /'
  cp /tmp/r433_3_mk.$$ $MK
  echo "-- 5. round-2 nested derivation (no MAKEFLAGS=) and the database read"
  sed -i 's/\$(shell MAKEFLAGS= \$(MAKE)/$(shell $(MAKE)/' $MK
  grep -c 'shell MAKEFLAGS=' $MK | sed 's/^/   MAKEFLAGS= lines left: /'
  PATH=$PATHX python3 scripts/check_entity_shape.py > /tmp/r433_3_plain.$$ 2>&1; echo "   plain gate rc=$?"
  grep -n 'milan_dp_mclk' /tmp/r433_3_plain.$$ | head -3 | sed 's/^/   /'
  out=$(cd tb/verilator/milan_dp_mclk && PATH=$PATHX MAKEFLAGS= make -pqrR -f Makefile 2>&1)
  # cut: under make 4.4 the round-2 line captures the nested make's whole
  # database (host environment included) into SRCS_DP; never publish it
  printf '%s\n' "$out" | grep -E '^[^#[:space:]].*:.*adp_shape_defaults\.svh' | cut -c1-200 | sed 's/^/   rule: /'
  printf '%s\n' "$out" | grep -E 'print-srcs failed' | sed 's/^/   stop: /'
  cp /tmp/r433_3_mk.$$ $MK
done
rm -f /tmp/r433_3_plain.$$ /tmp/r433_3_mk.$$
git diff --quiet && echo "copy restored: no tracked change" || { echo "copy NOT restored"; git diff --stat; }

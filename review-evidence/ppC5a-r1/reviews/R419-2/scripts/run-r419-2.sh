#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R419-2 reviewer runs, in the order executed. Every command ran in the
# foreground. PKT is this packet's directory, CLONE the reviewed detached
# clone at 44a6bb9082d31dbf933087ef007ad78a110e7053, VBIN a directory whose
# `verilator` is the pinned 5.050 wrapper.
set -euo pipefail
PKT=${PKT:?packet dir}
CLONE=${CLONE:?reviewed clone}
VBIN=${VBIN:?dir holding the pinned verilator}
S=$PKT/scratch
export PATH=$VBIN:$PATH TMPDIR=$S/tmp
mkdir -p "$S/head" "$S/tmp" "$PKT/receipts"

# 1. a scratch export of the exact head (the clone is never built in)
git -C "$CLONE" archive 44a6bb9082d31dbf933087ef007ad78a110e7053 | tar -x -C "$S/head"

# 2. focused suites (build parallelism capped in the scratch copy only)
sed -i 's/--build -j 0/--build -j 8/' "$S/head/tb/pp_top/Makefile" "$S/head/tb/ucpu/Makefile"
make -C "$S/head/tb/pp_top" gsi-build                > "$PKT/receipts/pp_top-gsi-build.log" 2>&1
for s in deadline hazards d3; do
  (cd "$S/head/tb/pp_top" && ./obj_dir/Vpp_top_sim --$s-only) > "$PKT/receipts/pp_top-$s.log" 2>&1
done
make -C "$S/head/tb/ucpu" run                        > "$PKT/receipts/ucpu-run.log" 2>&1
make -C "$S/head/tb/pp_top" run                      > "$PKT/receipts/pp_top-full.log" 2>&1

# 3. the lane's campaign, 55 arms in four shards of -j 2 (8 jobs at most)
sed -i 's/--build -j 8/--build -j 2/' "$S/head/tb/pp_top/Makefile" "$S/head/tb/ucpu/Makefile"
(cd "$S/head/tb/pp_top" && python3 -c "
import aecp_mutants as m
arms=[a[0] for a in m.MUTANTS]
for i in range(4): open('$S/shard%d.txt'%i,'w').write(','.join(arms[i::4]))")
for i in 0 1 2 3; do
  (cd "$S/head/tb/pp_top" && python3 aecp_mutants.py --output "$PKT/receipts/aecp-mutants/shard$i" \
     --only "$(cat "$S/shard$i.txt")" > "$PKT/receipts/aecp-mutants/shard$i.txt" 2>&1) &
done
wait

# 4. the round-1 reviewer arms (scripts/reviewer_mutants.py, unchanged from R419-1)
for g in r-registry-lock-preempted,r-effects-short r-kill-ack-keeps-owner,r-queued-counts-unsolicited \
         r-kill-latched-unsolicited,r-mvu-no-echo; do
  python3 "$PKT/scripts/reviewer_mutants.py" "$S/head" "$PKT/receipts/reviewer-mutants" "$g" \
    > "$PKT/receipts/reviewer-mutants/${g%%,*}.txt" 2>&1 &
done
wait

# 5. probes, each on its own scratch copy of hdl/ + tb/{common,pp_top}
for p in probe_hz_reachability_r2:probe:probe-hz-reachability-r2 \
         probe_dl_fault_combos:probe2:probe-dl-fault-combos \
         probe_gdi_stream_info:probe3:probe-gdi-stream-info; do
  IFS=: read -r script dir log <<< "$p"
  rm -rf "$S/$dir"; mkdir -p "$S/$dir/tb"
  cp -r "$S/head/hdl" "$S/$dir/"; cp -r "$S/head/tb/common" "$S/head/tb/pp_top" "$S/$dir/tb/"
  rm -rf "$S/$dir/tb/pp_top"/obj_*
  python3 "$PKT/scripts/$script.py" "$S/$dir" "$VBIN/verilator" > "$PKT/receipts/$log.log" 2>&1 || true
done

# 6. documentation gates and lint on the scratch export
(cd "$S/head" && for t in links matrix modmatrix params; do make -s $t > "$PKT/receipts/docs-$t.log" 2>&1; done)
(cd "$S/head" && ./scripts/lint_hdl.sh > "$PKT/receipts/lint_hdl.log" 2>&1)

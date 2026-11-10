#!/usr/bin/env bash
# rerun_waiter.sh: poll cpu_ranges.py pick every 2 s; on a free range, run capture_coherence alone on its first 4
# CPUs as unit milan-823-a753f-rerun (rerun_suites.sh, the sweep's own timeout and masked-verdict check), from
# shard 2's clone at the head.
S=<scratch>; C=<sweep-clone>2
while :; do
  R=$(python3 <management>/2026-09-23/cpu_ranges.py pick 2>/dev/null | tail -1)
  [ -n "$R" ] && break; sleep 2
done
a=${R%-*}; R4="$a-$((a+3))"
echo "$(date +%T) range $R, rerun on $R4"
systemd-run --user --unit=milan-823-a753f-rerun --collect --property=MemoryMax=10G --working-directory=$C \
  --setenv=HOME=<home> /usr/bin/taskset -c "$R4" /usr/bin/env \
  PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<shared-scratch>/a662/make43/bin:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin \
  VERILATOR=<tools>/pinned-verilator-5.050/verilator TSN_GEN_ROOT=<management>/tools/tsn-gen-deca300c \
  TMPDIR=$S/tmp-sweep "MAKEFLAGS=-j4 --no-print-directory" \
  /bin/bash -c "bash $S/gates/tools/rerun_suites.sh $S/sweep2-rerun capture_coherence > $S/sweep2-rerun.log 2>&1; echo rc=\$? >> $S/sweep2-rerun.log"
echo "$(date +%T) launched rc=$?"

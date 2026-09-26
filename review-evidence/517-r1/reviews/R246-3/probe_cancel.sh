#!/bin/sh
# Real-leg cancellation probe: SIGTERM the pool after <delay> s while the
# composed obj_notify/obj_nxn/obj_crflic legs (and the builder obj_nxn spawns)
# are running; then list any survivor whose cwd is this suite.
# usage: probe_cancel.sh <clone> <tmpdir> <delay>
D="$1/tb/verilator/milan_dp"; T="$2"; DELAY="$3"
mkdir -p "$T"
cd "$D" || exit 2
TMPDIR="$T" timeout -s TERM "$DELAY" python3 sim_pool.py --jobs=2 \
  ./obj_nxn/Vmilan_dp_nxn ./obj_crflic/Vmilan_dp_crflic ./obj_notify/Vmilan_dp_notify > "$T/replay.out" 2>&1
echo "pool_exit=$?"
survivors=0
for p in /proc/[0-9]*; do
  cwd=$(readlink "$p/cwd" 2>/dev/null) || continue
  [ "$cwd" = "$D" ] || continue
  [ "${p#/proc/}" = "$$" ] && continue
  cmd=$(tr '\0' ' ' < "$p/cmdline" 2>/dev/null)
  case "$cmd" in *probe_cancel*|"") continue;; esac
  echo "SURVIVOR ${p#/proc/}: $cmd"; survivors=$((survivors+1))
done
echo "survivors=$survivors"
ls -l obj_legs/
grep '^sim_pool:' obj_legs/replay.log

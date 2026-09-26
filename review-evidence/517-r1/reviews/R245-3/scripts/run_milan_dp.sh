#!/bin/bash
# Run the complete default milan_dp `run` target in a disposable tree copy.
# usage: run_milan_dp.sh TREE SIM_JOBS VERILATOR_JOBS CPUSET OUTDIR TOOLBIN
# Records wall clock, peak RSS (GNU time), tracked shape-header hashes before and
# after, a 1 s sample of live Vmilan_dp_* processes whose working directory is in
# TREE (ordinary legs run in the suite directory), the exit status and the log.
set -u
TREE=$1 JOBS=$2 VJ=$3 CPUS=$4 OUT=$5 TOOLBIN=$6
mkdir -p "$OUT"
cd "$TREE/tb/verilator/milan_dp" || exit 90
hdrs() { (cd "$TREE" && git ls-files 'configs/generated/*' 'hdl/common/gen/*' | xargs sha256sum); }
hdrs > "$OUT/headers-before.sha256"
env -u MILAN_COUNTER_FRAME_OUT -u MAKEFLAGS -u OBJCACHE PATH="$TOOLBIN:$PATH" verilator --version > "$OUT/verilator.txt"
python3 - "$TREE" > "$OUT/concurrency.txt" 2>/dev/null <<'PYEOF' &
import os, sys, time
tree = os.path.realpath(sys.argv[1])
excl = ("obj_notify", "obj_nxn", "obj_nxndv", "obj_nxn8", "obj_nxn4c")
while True:
    legs = []
    for e in os.listdir("/proc"):
        if not e.isdigit():
            continue
        try:
            cwd = os.readlink(f"/proc/{e}/cwd")
            argv = open(f"/proc/{e}/cmdline", "rb").read().split(b"\0")[0].decode()
            state = open(f"/proc/{e}/stat", "rb").read().rsplit(b")", 1)[1].split()[0]
        except OSError:
            continue
        if cwd.startswith(tree) and "/Vmilan_dp_" in argv and state != b"Z":
            legs.append(argv if cwd == tree + "/tb/verilator/milan_dp" else f"{argv}@{os.path.relpath(cwd, tree)}")
    ordinary = [a for a in legs if "@" not in a]
    print(int(time.time()), len(ordinary), sum(a.split("/")[1] in excl for a in ordinary), " ".join(sorted(legs)), flush=True)
    time.sleep(1)
PYEOF
SAMPLER=$!
START=$(date +%s.%N)
env -u MILAN_COUNTER_FRAME_OUT -u MAKEFLAGS -u OBJCACHE PATH="$TOOLBIN:$PATH" \
  /usr/bin/time -v -o "$OUT/time-v.txt" taskset -c "$CPUS" \
  make run SIM_JOBS="$JOBS" VERILATOR_JOBS="$VJ" > "$OUT/make.log" 2>&1
RC=$?
END=$(date +%s.%N)
kill $SAMPLER 2>/dev/null; wait $SAMPLER 2>/dev/null
hdrs > "$OUT/headers-after.sha256"
cp -r obj_legs "$OUT/obj_legs" 2>/dev/null
python3 "$TREE/scripts/suite_tally.py" --verdict "$OUT/make.log" > "$OUT/tally-verdict.txt" 2>&1; TRC=$?
{ echo "sim_jobs=$JOBS verilator_jobs=$VJ cpus=$CPUS"; echo "exit=$RC"; echo "tally_verdict_exit=$TRC";
  python3 -c "print('wall_s=%.3f' % ($END - $START))"; echo "start=$START end=$END";
  echo "headers_unchanged=$(cmp -s "$OUT/headers-before.sha256" "$OUT/headers-after.sha256" && echo yes || echo NO)"; } > "$OUT/summary.txt"
echo DONE > "$OUT/DONE"

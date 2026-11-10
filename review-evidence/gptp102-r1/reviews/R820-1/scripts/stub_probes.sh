#!/bin/bash
# Fake-toolchain probes over the FULL engine mutant list (see make_variants.py).
# usage: stub_probes.sh <tree> <receipts_dir> <cpu_list>
# Runs in the foreground; every probe writes <name>.log and <name>.rc.
set -u
TREE=$1; OUT=$2; CPUS=$3
ENG=$TREE/tb/verilator/engine
mkdir -p "$OUT"
T=$TREE/../tmp-stub; rm -rf "$T"; mkdir -p "$T"
cd "$ENG" || exit 2
run() {  # name, command...
  local n=$1; shift
  mkdir -p "$T/$n"
  TMPDIR=$T/$n taskset -c "$CPUS" "$@" > "$OUT/$n.log" 2>&1
  echo $? > "$OUT/$n.rc"
  # the driver must leave no temporary directory behind
  echo "leftover-in-TMPDIR: $(find "$T/$n" -mindepth 1 -maxdepth 1 | wc -l)" >> "$OUT/$n.log"
}
# 1. the jobs comparison test against the stubbed head and each planted fault
for v in none order print droplast abort short shared; do
  run "test-$v" python3 -I ../../mutation_jobs_test.py "stub_$v.py" &
done
wait
# 2. head stub, direct runs at several --jobs, plus the base driver stubbed;
#    directory use recorded per run
for j in 1 4 8 16; do
  PROBE_RECORD=$OUT/dirs-j$j.jsonl run "head-j$j" sh -c \
    "python3 -I stub_none.py --jobs $j > '$OUT/head-j$j.stdout'" &
done
run base-serial sh -c "python3 -I stub_base.py > '$OUT/base-serial.stdout'" &
wait
# 3. a task that raises (mutant index 5), serial and concurrent
tag5=$(python3 -I -c 'import importlib.util as u
s=u.spec_from_file_location("m","stub_none.py");m=u.module_from_spec(s);s.loader.exec_module(m)
print("".join(c if c.isalnum() else "_" for c in m.MUTATIONS[5][0]))')
for j in 1 4; do
  PROBE_RAISE=$tag5 run "raise-j$j" sh -c \
    "python3 -I stub_none.py --jobs $j > '$OUT/raise-j$j.stdout' 2> '$OUT/raise-j$j.stderr'" &
done
wait
# 4. SIGINT during a concurrent run with slow fake harness runs
mkdir -p "$T/sigint1" "$T/sigint4"
# an async job of a non-interactive shell starts with SIGINT ignored, so
# restore its default before exec, as an interactive Ctrl-C would see
for j in 1 4; do
( TMPDIR=$T/sigint$j PROBE_SLEEP=2 taskset -c "$CPUS" python3 -I -c \
    'import os,signal,sys; signal.signal(signal.SIGINT, signal.SIG_DFL); os.execvp(sys.argv[1], sys.argv[1:])' \
    python3 -I stub_none.py --jobs $j \
    > "$OUT/sigint$j.stdout" 2> "$OUT/sigint$j.stderr" & pid=$!
  sleep 5; t0=$(date +%s.%N); kill -INT $pid; wait $pid; rc=$?
  t1=$(date +%s.%N)
  echo "$rc" > "$OUT/sigint$j.rc"
  echo "exit-after-SIGINT-s: $(echo "$t1 - $t0" | bc)" > "$OUT/sigint$j.log"
  echo "leftover-in-TMPDIR: $(find "$T/sigint$j" -mindepth 1 -maxdepth 1 | wc -l)" >> "$OUT/sigint$j.log" )
done
# 5. --jobs argument handling and the default under several affinities
for a in 0 x -1 2.5; do
  python3 -I mutants.py --jobs "$a" > "$OUT/arg-$a.log" 2>&1; echo $? > "$OUT/arg-$a.rc"
done
for c in 112 112-114 112-127; do
  taskset -c $c python3 -I -c 'import importlib.util as u
s=u.spec_from_file_location("m","mutants.py");m=u.module_from_spec(s);s.loader.exec_module(m)
import os;print(len(os.sched_getaffinity(0)), m.default_jobs())' > "$OUT/default-$c.log" 2>&1
done
echo done

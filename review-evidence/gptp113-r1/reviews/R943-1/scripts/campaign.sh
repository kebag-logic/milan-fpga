#!/bin/bash
# Reviewer campaign: engine passes test (control + planted defects) and the engine's four passes,
# at base 3009f9a and head af11b3e, each in its own exported scratch tree, all at once.
# usage: campaign.sh REPO PACKET VERILATOR
set -u
REPO=$1; P=$2; VL=$3
SC=$P/scratch/runs; R=$P/receipts/runs
rm -rf "$SC"; mkdir -p "$SC" "$R"
BASE=3009f9a2a2d69375211d8355490675879033d940; HEAD=af11b3ef631eb44cdc1730cfb31bedda95c33dc5
exptree(){ mkdir -p "$SC/$1"; git -C "$REPO" archive "$2" | tar -x -C "$SC/$1"; }
sub(){ # file old new: replace exactly one occurrence or fail loudly
  python3 -I - "$1" "$2" "$3" <<'PY' || { echo "PLANT FAILED: $1"; exit 3; }
import sys; f, old, new = sys.argv[1:]; t = open(f).read()
assert t.count(old) == 1, (f, old, t.count(old)); open(f, "w").write(t.replace(old, new))
PY
}
# passes-test trees: name, commit, planted defect
pt(){ exptree "pt-$1" "$2"; }
pt head-control $HEAD; pt head-control-c0 $HEAD; pt base-control $BASE
for L in head:$HEAD base:$BASE; do
  lay=${L%%:*}; c=${L#*:}
  for m in failfast noforward exit128 merged nochdir noprctl noignore; do pt "$lay-$m" $c; done
done
for lay in head base; do
  E=$SC/pt-$lay-failfast/tb/verilator/engine/pass_run.py
  sub $E '            if not record.get("stopped") and (record.get("signal") or record.get("exit")) and not ignoring:
                stop_later(n)' '            pass'
  sub $SC/pt-$lay-noforward/tb/verilator/engine/pass_run.py '            signal.signal(signum, forward)' '            pass'
  sub $SC/pt-$lay-exit128/tb/verilator/engine/pass_run.py '    if record.get("signal"):
        reraise(record["signal"], record.get("core", False))
    return record.get("exit", 0)' '    if record.get("signal"):
        return 128 + record["signal"]
    return record.get("exit", 0)'
  sub $SC/pt-$lay-merged/tb/verilator/engine/pass_run.py 'log.write(bytes([stream])' 'log.write(bytes([1])'
  sub $SC/pt-$lay-nochdir/tb/verilator/engine/pass_run.py '    os.chdir(STATE)' '    pass'
  sub $SC/pt-$lay-noprctl/tb/verilator/engine/pass_run.py '    if not core:
        ctypes' '    if False:
        ctypes'
  sub $SC/pt-$lay-noignore/tb/verilator/engine/Makefile 'PASS = python3 pass_run.py $(if $(findstring i,$(firstword -$(MAKEFLAGS))),--ignore-errors)' 'PASS = python3 pass_run.py'
done
# engine trees
for L in head:$HEAD base:$BASE; do
  lay=${L%%:*}; c=${L#*:}
  exptree "eng-$lay-clean" $c; exptree "eng-$lay-abort" $c
  sub $SC/eng-$lay-abort/tb/verilator/engine/sim_main.cpp 'int main(int argc, char **argv) {' '#include <cstring>
#include <unistd.h>
int main(int argc, char **argv) {
    { char cwd[4096]; if (getcwd(cwd, sizeof cwd) && std::strstr(cwd, "/seedrun")) { std::puts("planted: pass 1 aborts"); std::fflush(stdout); std::abort(); } }'
done
( cd "$SC" && for d in */; do d=${d%/}; ( cd $d && find . -type f | sort | xargs sha256sum ) > "$R/$d.tree.sha256"; done )
# launch with at most $JOBS campaigns at once; each job writes its own log and rc file
JOBS=${JOBS:-12}
one(){ d=$1; n=$(basename $d)
  case $n in
    pt-head-control-c0) cmd="ulimit -c 0; /usr/bin/time -f 'wall %e s' make -C tb/verilator/engine passes-test";;
    pt-*) cmd="/usr/bin/time -f 'wall %e s' make -C tb/verilator/engine passes-test";;
    eng-*) cmd="ulimit -c 0; /usr/bin/time -f 'wall %e s' make -j4 -C tb/verilator/engine run VERILATOR=$VL OBJCACHE=";;
  esac
  ( cd $d && bash -c "$cmd" > "$R/$n.log" 2>&1; echo $? > "$R/$n.rc" )
}
export -f one; export R VL
# engine runs first (longest), then the passes tests
ls -d "$SC"/eng-* "$SC"/pt-* | xargs -P "$JOBS" -I{} bash -c 'one {}'
echo CAMPAIGN DONE > "$R/DONE"

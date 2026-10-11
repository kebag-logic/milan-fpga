#!/usr/bin/env bash
# Run scripts/run_suites.sh in TREE with the pinned simulator first on PATH and
# keep its stdout, stderr and rc under OUT. With a third argument, the run sets
# REQ_TAG_LOG to that file (the CI suites job's form), then runs the executed
# half of scripts/check-req-tags.py on the same run's output.
# usage: sweep.sh TREE OUT [EVIDENCE]
set -u
tree=$1; out=$2; ev=${3:-}
bin=${SIM_BIN:?SIM_BIN must name a directory holding the pinned verilator}
mkdir -p "$out"
export PATH="$bin:$PATH"
verilator --version >"$out/verilator.txt" 2>&1
cd "$tree" || exit 2
git rev-parse HEAD >"$out/head.txt"
if [ -n "$ev" ]; then
  rm -f "$ev"
  REQ_TAG_LOG="$ev" ./scripts/run_suites.sh >"$out/suites.txt" 2>"$out/suites.err"
  echo $? >"$out/suites.rc"
  python3 scripts/check-req-tags.py --suites "$out/suites.txt" --evidence "$ev" \
    >"$out/executed.txt" 2>&1
  echo $? >"$out/executed.rc"
else
  ./scripts/run_suites.sh >"$out/suites.txt" 2>"$out/suites.err"
  echo $? >"$out/suites.rc"
fi
echo done >"$out/DONE"

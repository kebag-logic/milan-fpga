#!/usr/bin/env bash
# Run `make` in each named suite of TREE with REQ_TAG_LOG unset and keep each
# suite's full log and rc under OUT (run_suites.sh deletes its logs).
# usage: persuite.sh TREE OUT SUITE...   (SIM_BIN from env)
set -u
tree=$1; out=$2; shift 2
export PATH="${SIM_BIN:?}:$PATH"
unset REQ_TAG_LOG
mkdir -p "$out"
for s in "$@"; do
  (cd "$tree/tb/$s" && make) >"$out/$s.log" 2>&1
  echo $? >"$out/$s.rc"
done
echo done >"$out/DONE"

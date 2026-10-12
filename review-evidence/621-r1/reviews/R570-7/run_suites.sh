#!/usr/bin/env bash
# Run named Verilator suites on a disposable copy of the candidate, the way
# scripts/run_all_suites.sh runs one (timeout + make -C), concurrently, one
# log/rc/time file per suite, with the pinned Verilator first on PATH.
# Usage: run_suites.sh <tree> <outdir> <pinned-verilator-wrapper> <suite>...
set -u
tree=$1; out=$2; wrapper=$3; shift 3
mkdir -p "$out" "$out/bin"
ln -sf "$wrapper" "$out/bin/verilator"
export PATH="$out/bin:$PATH"
verilator --version >"$out/verilator.version" 2>&1
cd "$tree" || exit 2
for suite in "$@"; do
  tmo=$(bash -c "$(sed -n '/^suite_timeout() {/,/^}/p' scripts/run_all_suites.sh); suite_timeout \"\$1\"" _ "$suite")
  echo "$tmo" >"$out/$suite.timeout"
  ( start=$(date +%s); timeout "$tmo" make -C "tb/verilator/$suite" >"$out/$suite.log" 2>&1
    echo $? >"$out/$suite.rc"; echo $(( $(date +%s) - start )) >"$out/$suite.wall" ) &
done
wait
for suite in "$@"; do echo "$suite rc=$(cat "$out/$suite.rc") wall=$(cat "$out/$suite.wall")s timeout=$(cat "$out/$suite.timeout")"; done

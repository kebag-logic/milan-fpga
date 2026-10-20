#!/usr/bin/env bash
# usage: rerun_after.sh <tree> <outdir>: wait for <outdir>/ALL.done, keep the
# refused attempts, then rerun elab_mutants and name_state with run_camps2.sh
tree=$1; out=$2
until [ -f "$out/ALL.done" ]; do sleep 30; done
for c in elab_mutants name_state; do
  for x in log rc sec; do [ -f "$out/$c.$x" ] && mv "$out/$c.$x" "$out/$c.setup-refused.$x"; done
done
mv "$out/ALL.done" "$out/ALL.first.done"
bash <scratch>/scripts/run_camps2.sh "$tree" "$out" 2 elab_mutants name_state

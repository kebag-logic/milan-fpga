#!/usr/bin/env bash
# chain.sh <head> <root> <job>...: run each docs.yml job in turn with the runner, one fresh clone each.
head=$1; root=$2; shift 2
for job in "$@"; do
  /data-2/milan/tmp/873-a763/gates/venv/bin/python3 /data-2/milan/tmp/873-a763/gates/tools/run_docs_yml.py "$head" "$job" "$root" >> "$root/chain-$job.out" 2>&1
  echo "$job runner rc=$?" >> "$root/chain-$job.out"
done

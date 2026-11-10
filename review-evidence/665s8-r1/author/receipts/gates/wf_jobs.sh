#!/bin/bash
# wf_jobs.sh <workflow> <root> <job>[:litex] ...: each job of the workflow on its own fresh clone of the gate head, in turn
: "${CPUS:?CPUS unset}"
G=$VALIDATION_STORAGE/665s8-a758b/gates; H=$(cat $G/HEAD)
wf=$1; root=$2; shift 2
for spec in "$@"; do
  job=${spec%%:*}; venv=$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin
  [ "${spec#*:}" = litex ] && venv=$WORKSPACE_HOME/litex-milan/venv/bin
  start=$(date +%s)
  taskset -c "$CPUS" $VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3 $G/run_wf.py "$wf" "$H" "$job" "$root" "$venv" >> "$root/driver.log" 2>&1
  echo "$job $? $(( $(date +%s) - start ))s" >> "$root/jobs.txt"
done
echo done >> "$root/jobs.txt"

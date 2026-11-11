#!/usr/bin/env bash
# drive.sh <name> <workflow:job[:venv][:k=v...]>...: each job, in order, through run_wf.py on a fresh clone of the head.
set -u
G=<scratch>/gates; H=$(cat $G/HEAD); n=$1; shift; W=${WF_ROOT:-$G/wf2}
mkdir -p $W/drivers
for spec in "$@"; do
  IFS=: read -r wf job venv rest <<< "$spec"
  matrix=(); [ -n "${rest:-}" ] && read -r -a matrix <<< "${rest//:/ }"
  tag="$wf-$job"; for m in "${matrix[@]}"; do tag+="-${m//=/}"; done
  if [ "$venv" = litex ]; then export WF_VENV=<litex-env>/venv/bin; else unset WF_VENV; fi
  echo "$(date -Is) start $tag" >> $W/drivers/$n.log
  python3 $G/tools/run_wf.py "$wf" "$H" "$job" $W "${matrix[@]}" > "$W/drivers/$tag.driver.log" 2>&1
  echo "$(date -Is) end $tag rc=$?" >> $W/drivers/$n.log
done
echo done >> $W/drivers/$n.log

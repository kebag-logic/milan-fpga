#!/usr/bin/env bash
# drive_tmo.sh: drive.sh with run_wf_tmo.py (one stated env override, LITEX_SIM_TIMEOUT).
set -u
G=<scratch>/gates; T=$G/tools2; H=$(cat $G/HEAD2); n=$1; shift; W=${WF_ROOT:-$G/wf4}
mkdir -p $W/drivers
for spec in "$@"; do
  IFS=: read -r wf job venv rest <<< "$spec"
  matrix=(); [ -n "${rest:-}" ] && read -r -a matrix <<< "${rest//:/ }"
  tag="$wf-$job"; for m in "${matrix[@]}"; do tag+="-${m//=/}"; done
  if [ "$venv" = litex ]; then export WF_VENV=<litex-env>/venv/bin; else unset WF_VENV; fi
  echo "$(date -Is) start $tag" >> $W/drivers/$n.log
  python3 $T/run_wf_tmo.py "$wf" "$H" "$job" $W "${matrix[@]}" > "$W/drivers/$tag.driver.log" 2>&1
  echo "$(date -Is) end $tag rc=$?" >> $W/drivers/$n.log
done
echo done >> $W/drivers/$n.log

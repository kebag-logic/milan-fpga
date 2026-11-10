#!/usr/bin/env bash
# drive.sh <head> <root> <list file>: run each "workflow job [k/n]" line of the list with run_wf.py, one after another.
set -u
H=$1; R=$2; L=$3
T=$(dirname "$(readlink -f "$0")")
while read -r wf job mat; do
  [ -z "$wf" ] && continue
  case "$wf" in \#*) continue;; esac
  if [ -n "${mat:-}" ]; then
    echo "== $(date +%T) $wf $job $mat"; python3 "$T/run_wf.py" "$wf" "$H" "$job" "$R" --matrix "$mat"
  else
    echo "== $(date +%T) $wf $job"; python3 "$T/run_wf.py" "$wf" "$H" "$job" "$R"
  fi
done < "$L"
echo "== $(date +%T) list done"

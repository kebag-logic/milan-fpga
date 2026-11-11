#!/bin/bash
# drive.sh <head> <root> <name> <job spec>... : run each "wf:job[:k/n]" spec in turn through run_wf.py
# (docs jobs through the 829 docs runner), each on its own fresh clone under <root>.
head=$1; root=$2; name=$3; shift 3
T=<scratch>/gates/tools
mkdir -p $root/drivers
for spec in "$@"; do
  IFS=: read wf job mat <<< "$spec"
  echo "== $(date +%T) $wf $job $mat" >> $root/drivers/$name.log
  if [ "$wf" = docs ]; then
    $T/../venv/bin/python3 $T/run_docs_yml.py $head $job $root/docs >> $root/drivers/$name.log 2>&1
  elif [ -n "$mat" ]; then
    $T/../venv/bin/python3 $T/wf/run_wf.py $wf $head $job $root --matrix $mat >> $root/drivers/$name.log 2>&1
  else
    $T/../venv/bin/python3 $T/wf/run_wf.py $wf $head $job $root >> $root/drivers/$name.log 2>&1
  fi
  echo "== $(date +%T) $wf $job $mat rc=$?" >> $root/drivers/$name.log
done
echo "DRIVER DONE $(date +%T)" >> $root/drivers/$name.log

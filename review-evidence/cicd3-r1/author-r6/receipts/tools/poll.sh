#!/bin/bash
# poll.sh OUT RUN...: every 60 s, each run's status into OUT/status; when all are completed, each run's jobs
# (latest attempt) into OUT/jobs-RUN.json, then exit.
O=$1; shift; mkdir -p "$O"
while :; do
  done_all=1; : > "$O/status.new"
  for r in "$@"; do
    s=$(gh run view "$r" -R kebag-logic/milan-fpga --json status,conclusion,attempt -q '[.status,.conclusion,.attempt]|@tsv' 2>/dev/null)
    echo "$(date -u +%FT%TZ) $r $s" >> "$O/status.new"
    case "$s" in completed*) ;; *) done_all=0 ;; esac
  done
  mv "$O/status.new" "$O/status"; cat "$O/status" >> "$O/status.log"
  [ $done_all = 1 ] && break
  sleep 60
done
for r in "$@"; do gh api "repos/kebag-logic/milan-fpga/actions/runs/$r/jobs?per_page=100" --paginate > "$O/jobs-$r.json"; done
echo finished > "$O/finished"

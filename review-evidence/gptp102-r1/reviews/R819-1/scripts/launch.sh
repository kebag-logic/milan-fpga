#!/bin/bash
# Start one campaign detached, with its own log, time receipt and rc file.
# usage: launch.sh <packet> <name> <cpus> <dir> <cmd...>
# Writes receipts/<name>.{stdout,stderr,time,rc,cmd}; TMPDIR is private.
set -u
PKT=$1; NAME=$2; CPUS=$3; DIR=$4; shift 4
R=$PKT/receipts; mkdir -p "$R" "$PKT/scratch/tmp/$NAME"
rm -f "$R/$NAME.rc"
printf '%s\n' "cwd=$DIR cpus=$CPUS cmd=$*" > "$R/$NAME.cmd"
( cd "$DIR" && export PATH="$PKT/scratch/bin:$PATH" TMPDIR="$PKT/scratch/tmp/$NAME" \
  && date -u +%FT%TZ > "$R/$NAME.start" \
  && /usr/bin/time -v -o "$R/$NAME.time" taskset -c "$CPUS" "$@" \
       > "$R/$NAME.stdout" 2> "$R/$NAME.stderr"; \
  echo $? > "$R/$NAME.rc"; date -u +%FT%TZ > "$R/$NAME.end" ) \
  < /dev/null > /dev/null 2>&1 &
disown
echo "launched $NAME"

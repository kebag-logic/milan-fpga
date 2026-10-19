#!/usr/bin/env bash
# usage: r2_bg.sh <record-dir> <name> <workdir> <command...>   gate.sh, detached; writes <name>.done
rec="$1"; name="$2"; shift 2
mkdir -p "$rec"
setsid nohup bash -c '"$0" "$@"; echo done > "'"$rec/$name"'.done"' <data>/tmp/pp185-a647/scripts/gate.sh "$rec" "$name" "$@" > "$rec/$name.out" 2>&1 < /dev/null &
echo launched $name

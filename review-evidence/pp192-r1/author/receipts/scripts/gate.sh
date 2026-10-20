#!/usr/bin/env bash
# usage: gate.sh <record-dir> <name> <workdir> <command...>
# Runs the command unpiped; stdout+stderr to <name>.log, exit status to <name>.rc.
rec="$1"; name="$2"; wd="$3"; shift 3
mkdir -p "$rec"
export PATH="${GATE_BIN:-<scratch>/bin}:<scratch>/venv-wd/bin:$PATH"
export LC_ALL=C.UTF-8
start=$(date +%s)
( cd "$wd" && "$@" ) > "$rec/$name.log" 2>&1
rc=$?
echo "$rc" > "$rec/$name.rc"
echo "$(( $(date +%s) - start ))" > "$rec/$name.secs"
echo "$name rc=$rc secs=$(cat "$rec/$name.secs")"

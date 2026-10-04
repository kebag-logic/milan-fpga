#!/bin/sh
# usage: bg.sh <name> <workdir> <verilator: 5050|5052> <command...>
# Runs <command> in <workdir> with the chosen Verilator, writing
# receipts/<name>.log and receipts/<name>.rc (exit status) beside this script.
set -u
name=$1; wd=$2; ver=$3; shift 3
R=$(cd "$(dirname "$0")/.." && pwd)/receipts
case $ver in
  5050) PIN=$VALIDATION_TOOLS/pinned-verilator-5.050; export PATH="$PIN:$PATH"; export VERILATOR="$PIN/verilator" ;;
  5052) export VERILATOR=/usr/bin/verilator ;;
  *) echo "bad verilator selector $ver" >&2; exit 2 ;;
esac
rm -f "$R/$name.rc"
{
  echo "# name=$name wd=$wd verilator=$($VERILATOR --version) start=$(date -u +%FT%TZ)"
  echo "# head=$(git -C "$wd" rev-parse HEAD 2>/dev/null) cmd=$*"
  cd "$wd" && "$@"
  rc=$?
  echo "# end=$(date -u +%FT%TZ) rc=$rc"
  echo $rc > "$R/$name.rc"
} > "$R/$name.log" 2>&1

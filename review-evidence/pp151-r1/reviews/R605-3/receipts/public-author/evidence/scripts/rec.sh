#!/usr/bin/env bash
# rec.sh <label> <name> <toolset: pinned|host> <dir> <cmd...>
# Runs one record in <dir>; writes <rec>/<label>/<name>.{log,rc,time,cmd}. Never pipes the command.
set -u
label=$1 name=$2 tools=$3 dir=$4; shift 4
out=<scratch>/rec/$label; mkdir -p "$out"
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
vbin=<scratch>/tools/vbin
case "$tools" in
  pinned) export PATH=<scratch>/tools/bin:$PATH ;;
  host)   export PATH=$vbin:$PATH ;;
  *) echo "bad toolset $tools" >&2; exit 2 ;;
esac
printf '%s\n' "cd $dir && $*" > "$out/$name.cmd"
{ echo "tools=$tools"; echo "verilator=$(command -v verilator) $(verilator --version 2>&1)"; echo "sv2v=$(command -v sv2v) $(sv2v --version 2>&1)"; echo "yosys=$(command -v yosys) $(yosys -V 2>&1 | cut -c1-40)"; echo "head=$(git -C "$dir" rev-parse HEAD 2>/dev/null)"; } > "$out/$name.env"
start=$(date +%s)
( cd "$dir" && /usr/bin/time -v -o "$out/$name.time" "$@" ) > "$out/$name.log" 2>&1
rc=$?
echo "$rc" > "$out/$name.rc"
echo "$(( $(date +%s) - start ))" > "$out/$name.secs"
exit 0

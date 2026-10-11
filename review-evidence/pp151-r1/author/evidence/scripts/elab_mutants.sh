#!/usr/bin/env bash
# elab_mutants.sh <tree> <toolset pinned|host> <out>: the new suite's campaign, recorded
set -u
tree=$1 tools=$2 out=$3
export VERILATOR=<tools>/pinned-verilator-5.050/verilator
case $tools in
  pinned) export PATH=<scratch>/tools/bin:$PATH ;;
  host) export PATH=<scratch>/tools/vbin:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin ;;
esac
{ echo "sv2v $(sv2v --version) yosys $(yosys -V | cut -c1-30)"; } > "$out.env"
start=$(date +%s)
python3 -B "$tree/tb/elab_guards/mutants.py" --verilator "$VERILATOR" --output "$out" --jobs 4 > "$out.log" 2>&1
echo $? > "$out.rc"; echo $(( $(date +%s) - start )) > "$out.secs"

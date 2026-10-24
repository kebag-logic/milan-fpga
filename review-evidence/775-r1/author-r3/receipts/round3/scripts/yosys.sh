#!/bin/bash
# yosys.sh <clone> <out>: syn/yosys/run.sh, the full serial gate, at the head
. <scratch>/scripts/env.sh
cd "$1" || exit 2
O=$2; mkdir -p "$O"
{ echo "head $(git rev-parse HEAD)"; git status --porcelain --untracked-files=no; yosys -V; sv2v --version; } > "$O/HEAD.txt" 2>&1
date -Is > "$O/start"
syn/yosys/run.sh > "$O/yosys.log" 2>&1
echo "rc=$?" > "$O/rc"
date -Is > "$O/end"

#!/bin/bash
# One repository gate in TREE, its log and rc under OUT.
# Usage: gate.sh TREE OUT NAME   (NAME: clean contract lint docs ucpu parser
#        engine gaskets tsngen bench)
set -u
TREE=$1 OUT=$2 NAME=$3
export PATH=<tools>/pinned-verilator-5.050:$PATH
export TMPDIR=<scratch>/tmpdir
mkdir -p "$OUT"
cd "$TREE" || exit 9
case $NAME in
  clean)    make clean ;;
  contract) make contract ;;
  lint)     make lint ;;
  docs)     make docs ;;
  ucpu)     make -C tb/verilator/ucpu ;;
  parser)   make -C tb/verilator/parser ;;
  engine)   make -C tb/verilator/engine run ;;
  gaskets)  make -C tb/verilator/gaskets ;;
  tsngen)   make -C tb/tsngen ;;
  bench)    make -C bench/arty test ;;
  *) echo "unknown gate $NAME"; exit 9 ;;
esac > "$OUT/$NAME.log" 2>&1
rc=$?
echo $rc > "$OUT/$NAME.rc"
echo "$NAME rc=$rc"

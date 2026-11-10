#!/bin/sh
# make split, then make split-mutants
set -u
cd "$1"
make -j8 split; rc=$?
echo "make split rc=$rc"
make split-mutants; rc2=$?
echo "make split-mutants rc=$rc2"
[ $rc -eq 0 ] && [ $rc2 -eq 0 ]

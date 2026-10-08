#!/bin/bash
# usage: a0_matrix.sh PACKET REPO -- A0 (acmp-init-too-many-sources) clean and planted, gcc/clang, plain/ASan.
P=$1; R=$2; S=$P/scratch/a0; O=$P/receipts/a0; mkdir -p $S $O
python3 -B $P/scripts/plant_a0.py $R/sw/firmware/ctrl $S/planted-ctrl > $O/plant.log 2>&1 || exit 3
for cc in gcc clang; do
  if [ $cc = gcc ]; then export CC=gcc CXX=g++; else export CC=clang CXX=clang++; fi
  for mode in plain asan; do
    a=""; [ $mode = asan ] && a=asan
    python3 -B $P/scripts/run_a0.py $R $R/sw/firmware/ctrl $S/clean-$cc-$mode $a > $O/clean-$cc-$mode.log 2>&1; echo $? > $O/clean-$cc-$mode.rc
    python3 -B $P/scripts/run_a0.py $R $S/planted-ctrl $S/planted-$cc-$mode $a > $O/planted-$cc-$mode.log 2>&1; echo $? > $O/planted-$cc-$mode.rc
  done
done

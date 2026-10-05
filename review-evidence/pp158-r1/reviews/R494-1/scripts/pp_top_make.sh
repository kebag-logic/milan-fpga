#!/bin/sh
# tb/pp_top make (six builds) in a fresh git-archive extraction of the head. Usage: pp_top_make.sh REPO SCRATCH OUT VERILATOR
set -u
R=$1 S=$2 OUT=$3 V=$4; T=$S/pptop; rm -rf $T; mkdir -p $T $OUT
git -C $R archive 79571006b803a4ab4af65358f0d87bc3af73180e | tar -x -C $T
make -C $T/tb/pp_top VERILATOR=$V > $OUT/pp_top-make.log 2>&1; echo $? > $OUT/pp_top-make.rc

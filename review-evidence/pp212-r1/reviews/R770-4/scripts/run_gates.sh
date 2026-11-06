#!/usr/bin/env bash
# Reproduce this review's gates. Usage:
#   run_gates.sh <processor-clone> <work-dir> <verilator>
# Builds a scratch milan-fpga parent at dev cc204c6f, pins protocol-processor
# to each of main/round-3/round-4 in turn, runs scripts/check_cpp_idiom.py
# (gate and --list) and --selftest, then runs tb/pp_top (make run) and
# tb/srp_stream_fsms (make) on a git-archive of the round-4 head.
set -u
PROC=$1; W=$2; V=$3; R=$W/receipts; mkdir -p $R $W/scratch
PARENT_DEV=cc204c6fd2349b543d73f15c97162a2c4434c86e
GPTP=135afd043309369a87ddbc8d6550aff8ec52a157
MAIN=a9e84b66d4cd0c331c8d6f2c1a71a62fcc824645
R3=834cc889cbd39f6a4f990d19059b5fbd2a2a9dd1
R4=6162885ffee5d8e8897732be6479982b8dceaec9
cd $W/scratch
git clone -q --filter=blob:none --no-checkout https://github.com/kebag-logic/milan-fpga.git parent
cd parent && git checkout -q $PARENT_DEV
git clone -q --filter=blob:none --no-checkout https://github.com/Mister-M-alt/FPGA-gPTP.git gptp-processor
git -C gptp-processor checkout -q $GPTP
git clone -q --no-checkout "$PROC" protocol-processor
git submodule init -- protocol-processor gptp-processor >/dev/null
run() { tag=$1; sha=$2
  git -C protocol-processor checkout -q $sha
  git update-index --cacheinfo 160000,$sha,protocol-processor
  git submodule status -- protocol-processor > $R/idiom-$tag.status
  python3 -I scripts/check_cpp_idiom.py > $R/idiom-$tag.log 2>&1; echo $? > $R/idiom-$tag.rc
  python3 -I scripts/check_cpp_idiom.py --list > $R/idiom-$tag.list.log 2>&1; echo $? > $R/idiom-$tag.list.rc; }
run main $MAIN; run r3 $R3; run r4 $R4
python3 -I scripts/check_cpp_idiom.py --selftest > $R/idiom-selftest.log 2>&1; echo $? > $R/idiom-selftest.rc
S=$W/scratch/src-r4; mkdir -p $S; git -C "$PROC" archive $R4 | tar -x -C $S
( cd $S/tb/pp_top && make run VERILATOR=$V > $R/pp_top-r4.log 2>&1; echo $? > $R/pp_top-r4.rc ) &
( cd $S/tb/srp_stream_fsms && make VERILATOR=$V > $R/srp_stream_fsms-r4.log 2>&1; echo $? > $R/srp_stream_fsms-r4.rc ) &
wait

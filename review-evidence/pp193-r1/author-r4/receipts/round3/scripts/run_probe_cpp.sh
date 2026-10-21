#!/usr/bin/env bash
# usage: run_probe_cpp.sh <probe.cpp> <name>: the head's hdl and tb from git
# archive, the probe as srp_stream_fsms' test entry point (it includes the
# suite), built and run; <name>.log/.rc in the round-2 records
S=<scratch>/r2
H=57fb7dd21d316ce49c305c22812de5c16d6770f6
. $S/scripts/env.sh
src=$1; name=$2; w=$S/probe-run-$name
rm -rf $w; mkdir -p $w
git -C <lane> archive $H hdl tb/common tb/srp_stream_fsms | tar -x -C $w
cp "$src" $w/tb/srp_stream_fsms/
sed -i "s/CPP  = sim_main.cpp/CPP  = $(basename $src)/" $w/tb/srp_stream_fsms/Makefile
{ echo "head $H; only the test entry point is replaced"; make -C $w/tb/srp_stream_fsms RUN_ARGS=suite; } > $S/rec/$name.log 2>&1
echo $? > $S/rec/$name.rc
rm -rf $w

#!/bin/bash
# budvar.sh NAME "USER-OPT-FLAGS" MAKEARGS...: copy the base native model to native-NAME (same depth), rebuild Vsim with the make overrides, time it
set -u
B=/data-2/milan/tmp/cicd-a839/bud/base; N=$1; U=$2; shift 2
. /data-2/milan/tmp/cicd-a839/bin/env.sh
D=$B/native-$N
rm -rf "$D"; mkdir -p "$D"
cp "$B"/native/*.cpp "$B"/native/*.h "$B"/native/*.mk "$B"/native/*.dat "$D"/ 2>/dev/null
INC="-std=c++17 -Wall -Wextra -I/data-2/milan/lanes/cicd-1/tb/common -I$B -I/data-2/milan/lanes/cicd-1/tb/verilator/fw_service_budget"
start=$(date +%s.%N)
make -j8 -C "$D" -f Vsim.mk Vsim VM_USER_CFLAGS="$U $INC" "$@" > "$D/make.log" 2>&1; rc=$?
echo "$N build rc=$rc wall=$(echo "$(date +%s.%N) - $start" | bc) size=$(stat -c %s $D/Vsim 2>/dev/null)"

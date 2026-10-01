#!/bin/sh
# Reviewer probe runner (R429-3). Usage: run_r429_mcr.sh <checkout> <scratch dir> <verilator>
# Builds the unmodified KL_media_clock_restart.sv with r429_mcr_switch.cpp and
# runs every case, at most 8 at a time; results are printed in case order.
set -e
SRC=$1; S=$2; V=$3
mkdir -p "$S"; cp "$(dirname "$0")/r429_mcr_switch.cpp" "$S/"; cd "$S"
"$V" --version
sha256sum "$SRC/hdl/ieee1722/avtp/KL_media_clock_restart.sv"
"$V" --cc --exe --build -O3 -j 8 --top-module KL_media_clock_restart \
  -GN_TALKERS_P=2 "$SRC/hdl/ieee1722/avtp/KL_media_clock_restart.sv" \
  r429_mcr_switch.cpp -o r429_mcr_switch > build.log 2>&1
echo "build rc=0"
rm -rf res; mkdir res
: > cases.txt
for LAT in 40 2000; do
  for c in design era1 era2 era3 era4 echo1 echo10 echo30 echo60 echo90 echo120 echo125 echo5000; do
    echo "$c 12500 200000 $LAT 64 4000000" >> cases.txt
  done
done
for LAT in 40 90; do
  for c in design era1 era2 era3 era4 echo10 echo60 echo125 echo5000; do
    echo "$c 100 1600 $LAT 400 40000" >> cases.txt
  done
done
i=0
while read -r line; do i=$((i+1)); printf '%03d %s\n' "$i" "$line"; done < cases.txt > numbered.txt
xargs -P 8 -L 1 sh -c './obj_dir/r429_mcr_switch $1 $2 $3 $4 $5 $6 > res/$0.txt' < numbered.txt
echo "== 100 MHz: A = 12,500 cycles (125 us), C = 200,000 (2 ms); 40 ms observed; 64 phases over one CRF period"
echo "== then scaled: A = 100, C = 1,600; 400 phases (every 4th cycle of a CRF period)"
cat res/*.txt

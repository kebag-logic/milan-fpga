#!/usr/bin/env bash
# Re-run the author's PR round 2 analyses from the published packet tools on the cold-archive raws.
# usage: reproduce_pr2.sh <packet_author_r2_dir> <archive_dir> <work_dir>
# Interface-named captures are selected by their published byte size, so no capture name is printed.
set -u
PK=$1; AR=$2; W=$3; T=$PK/tools/pr2
mkdir -p "$W"; cd "$W" || exit 2
bysize() { find "$AR/$1" -maxdepth 1 -name '*.pcap' -size "$2"c; }
RA_PEER=$(bysize rA 370480818); DB_DUT=$(bysize dB 967051444)
DA_DUT=$(bysize dA 1501053012); DA_PEER=$(bysize dA 1501066590)
run() { local tag=$1; shift; ( "$@" > "$W/$tag.out" 2>&1; echo $? > "$W/$tag.rc" ) & }
run bound  python3 -I -B $T/b21_restart_bound.py $PK/r3/runs/rA/cycles.jsonl "$RA_PEER" $AR/rA-ext/cap-lr.raw $AR/rA-ext/cap-ts.bin $W/rA-bound.json
run controls python3 -I -B $T/b21_restart_controls.py $T/b21_restart_bound.py $PK/r3/runs/rA/cycles.jsonl "$RA_PEER" $AR/rA-ext/cap-lr.raw $AR/rA-ext/cap-ts.bin $W/plant $W/rA-controls.json
run probes python3 -I -B $T/b21_probes.py $AR/probe/peer.samples $PK/tools/b21_grade.py $T/b21_grade.py $W/probes $W/probes.json
run floor  env B5_W=110 python3 -I -B $T/b21_floor_groups.py $PK/r3/selftest/mst-long/mst-long-reads.u16 $AR/mst-long/mst-long.ts $AR/mst-long/mst-long.samp $W/floor-groups.txt
run step1  python3 -I -B $T/b21_step1_verdict.py $PK/r3/selftest/mst-long/mst-long-reads.u16 $PK/r3/selftest/mst-long/mst-long-reads.json $W/step1-verdict.json
run transit python3 -I -B $T/b21_transit_crf.py "$DA_DUT" "$DA_PEER" $W/dA-transit-crf.json
( python3 -I -B $T/b21_aaf.py extract "$DB_DUT" 3cc0c60102030000 2 $W/dutlink > $W/extract.out 2>&1; echo $? > $W/extract.rc
  sha256sum $W/dutlink.samples > $W/dutlink.sha256
  ( python3 -I -B $T/b21_grade.py mcasp $AR/dB dB $W/dutlink.samples 4 $W/dB > $W/mcasp.out 2>&1; echo $? > $W/mcasp.rc ) &
  ( python3 -I -B $T/b21_exact.py $AR/dB/dB.pcm $W/dutlink.samples 4 $W/dB-exact.json > $W/exact.out 2>&1; echo $? > $W/exact.rc ) &
  wait ) &
wait
for f in "$W"/*.rc; do echo "$(basename $f .rc) rc=$(cat $f)"; done

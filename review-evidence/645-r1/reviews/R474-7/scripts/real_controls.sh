#!/bin/bash
# Usage: real_controls.sh <Vfollow_ring> <outdir>
# Four traced harness runs; each writes <name>.log, <name>.pdu.csv, <name>.servo.csv, <name>.rc
exe=$1; out=$2
run() { n=$1; shift; ( "$exe" "$@" --trace "$out/$n.pdu.csv" --servo-trace "$out/$n.servo.csv" > "$out/$n.log" 2>&1; echo $? > "$out/$n.rc" ) & }
run dup_author_repro --case b8 --dwell-s 1.0 --set-phase 0.0 --hold-s 16
run dup_own --case b8 --dwell-s 8 --set-phase 0.3 --hold-s 4
run skip_own --case b8 --dwell-s 8 --set-phase 0.3 --hold-s 4 --peer-ppm 0.82
run pullin_leg --case pullin --latency-us 210.42 --after-s 1.5
wait

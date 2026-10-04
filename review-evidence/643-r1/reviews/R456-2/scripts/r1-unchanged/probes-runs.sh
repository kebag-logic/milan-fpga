#!/bin/bash
# R456-1: the probe RUNS (builds by probes.sh/probes2.sh). Usage: probes-runs.sh PACKET
set -u
P=$1; R=$P/receipts/probes; D="$P/scripts/run_probe.py"
HP=$P/scratch/hp; C4=$P/scratch/pc4c
r() { python3 $D run "$1" "$2" --mode="$3" --log "$R/$4.log" & }
r $HP clean --law-only hp-clean-law
r $HP a2a --law-only hp-a2a-law
r $HP spp1 --law-only hp-spp1-law
r $HP spp1 --crf-only hp-spp1-crf
r $HP spm1 --law-only hp-spm1-law
r $HP tieon --law-only hp-tieon-law
r $HP tieoff --law-only hp-tieoff-law
r $HP tiespp1 --law-only hp-tiespp1-law
r $HP tiespm1 --law-only hp-tiespm1-law
r $HP boottrace --law-only hp-boottrace-law
r $HP bootnodwell --law-only hp-bootnodwell-law
r $C4 clean --law-only c4-clean-law
r $C4 a2a --law-only c4-a2a-law
r $C4 tieon --law-only c4-tieon-law
wait
echo "== runs done $(date +%T)"

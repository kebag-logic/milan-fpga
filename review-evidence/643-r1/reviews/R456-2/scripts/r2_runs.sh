#!/bin/bash
# R456-2 probe RUNS for #643 / PR #648 at 6b96391d. Usage: r2_runs.sh PACKET BATCH
# Each line of a batch is "TREE NAME MODE LOG"; MODE is a leg argument or 'full'.
# Runs go through R456-1's unchanged run_probe.py, at most JOBS (default 16) at once.
set -u
P=$1; BATCH=$2; S=$P/scratch; R=$P/receipts/probes; mkdir -p $R
D="$P/scripts/r1-unchanged/run_probe.py"
case $BATCH in
B1) cat <<EOF ;;
hp clean --law-only hp-clean-law
hp a2a --law-only hp-a2a-law
hp spp1 --law-only hp-spp1-law
hp spp1 --crf-only hp-spp1-crf
hp spm1 --law-only hp-spm1-law
hp spm1 --crf-only hp-spm1-crf
hp2 tieon --law-only hp-tieon-law
hp2 tiespp1 --law-only hp-tiespp1-law
hp2 tiespm1 --law-only hp-tiespm1-law
hp3 boottrace --law-only hp-boottrace-law
hp3 bootnodwell --law-only hp-bootnodwell-law
hp2 tie36 --law-only hp-tie36-law
pc4c clean --law-only c4-clean-law
c4b a2a --law-only c4-a2a-law
c4b tieon --law-only c4-tieon-law
c4b basec4c full c4-base-full
EOF
B2) cat <<EOF ;;
hp3 basep631 full p631-base-full
hp clean --law-boundary=2018..2035 hp-clean-lb-2018up
hp clean --law-boundary=2010..2045 hp-clean-lb-2010up
hp clean --law-boundary=2025 hp-clean-lb-2025alone
hp spm1 --law-boundary=2018..2035 hp-spm1-lb-2018up
EOF
B3) cat <<EOF ;;
hp w4 --law-boundary=1986..2066 hp-w4-lb-up
hp w4 --law-boundary=2066..1986 hp-w4-lb-down
hp3 w0 --law-boundary=1986..2066 hp-w0-lb-up
hp3 w0 --law-boundary=2066..1986 hp-w0-lb-down
hp3 spm1w0 --law-boundary=1986..2066 hp-spm1w0-lb-up
hp3 spp1w0 --law-boundary=1986..2066 hp-spp1w0-lb-up
pc4c spm1 --law-only c4-spm1-law
pc4c spp1 --law-only c4-spp1-law
EOF
B4) cat <<EOF ;;
pc4c clean --law-boundary=1986..2066 c4-clean-lb-up
pc4c clean --law-boundary=2066..1986 c4-clean-lb-down
hp clean --law-boundary=1990 hp-clean-lb-1990alone
hp clean --law-boundary=2010 hp-clean-lb-2010alone
hp clean --law-boundary=2016 hp-clean-lb-2016alone
hp clean --law-boundary=2020 hp-clean-lb-2020alone
hp clean --law-boundary=2030 hp-clean-lb-2030alone
hp clean --law-boundary=2036 hp-clean-lb-2036alone
hp clean --law-boundary=2042 hp-clean-lb-2042alone
hp clean --law-boundary=2062 hp-clean-lb-2062alone
pc4c clean --law-boundary=2016 c4-clean-lb-2016alone
pc4c clean --law-boundary=2025 c4-clean-lb-2025alone
pc4c clean --law-boundary=2036 c4-clean-lb-2036alone
pc4c spm1 --law-boundary=2018..2035 c4-spm1-lb-2018up
EOF
esac > $R/batch-$BATCH.txt
echo "== batch $BATCH start $(date +%T)"
xargs -P ${JOBS:-16} -L 1 sh -c 'python3 "$0" run "'$S'/$1" "$2" --mode="$3" --log "'$R'/$4.log"; echo "  done $4 $(cat "'$R'/$4.log.rc")"' $D < $R/batch-$BATCH.txt
echo "== batch $BATCH done $(date +%T)"

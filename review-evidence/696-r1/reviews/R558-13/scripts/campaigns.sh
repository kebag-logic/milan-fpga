#!/bin/bash
# Usage: campaigns.sh <repo> <scratch> <outdir> <name>; runs one focused campaign, writing <outdir>/<name>.log and .rc
set -u
R=$1; S=$2; O=$3; N=$4
export PATH="$S/bin:$PATH" VERILATOR="$S/bin/verilator" TMPDIR="$S/tmp/$N"
mkdir -p "$TMPDIR"
cd "$R"
{
echo "head $(git rev-parse HEAD) start $(date -u +%FT%TZ) $(verilator --version)"
case $N in
  maap_suite) VERILATOR_JOBS=4 make -C tb/verilator/maap MDIR="$S/maap_unit" ;;
  maap_integ) VERILATOR_JOBS=4 make -j4 -C tb/verilator/maap integration-build DP_MDIR="$S/maap_integ" && (cd "$S/maap_integ" && ./maap_integration) && VERILATOR_JOBS=4 make -C tb/verilator/maap coverage COV_MDIR="$S/maap_cov" ;;
  counters) cd tb/verilator/milan_dp && python3 stream_counters.py --shape 1 && python3 stream_counters.py --shape 8 ;;
  *) echo "unknown $N"; false ;;
esac
rc=$?
echo "end $(date -u +%FT%TZ) rc=$rc"
(exit $rc)
} > "$O/$N.log" 2>&1
echo $? > "$O/$N.rc"

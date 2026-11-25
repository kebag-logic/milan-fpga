#!/bin/bash
# splitrun.sh TAG CPUS REV: the hosted #1003 shape locally. Each leg, then the judge, in a fresh clone at ONE path
# (r6/wt/split, as every hosted job checks out at one path), the previous clone moved aside (never removed). A leg's
# capture goes through an artifact-like copy (hidden files left out, as upload-artifact@v4 does; no exec bits)
# into the path the judge is given. Output: r6/meas/TAG-{leg0,leg1,judge}/
set -u
T=$1; C=$2; REV=$3
R=/data-2/milan/tmp/cicd-a839/r6; P=$R/wt/split; RT=$R/rt-$T
mkdir -p "$RT"
for n in 1 2 3; do [ -e "$P" ] && mv "$P" "$P.old.$T.$(date +%s)"; done
fresh() { [ -e "$P" ] && mv "$P" "$P.$T.$1"; $R/tools/mkclone.sh split "$REV" > /dev/null; }
for leg in 0 1; do
  fresh before-leg$leg
  $R/tools/fbrun.sh "$T-leg$leg" "$C" "$P" --require-rv32 --without verilator --leg "$leg/2" --capture-out "$RT/made-$leg"
  mkdir -p "$RT/firmware-boundary-capture-$leg"
  rsync -r --exclude='.*' --chmod=D755,F644 "$RT/made-$leg/" "$RT/firmware-boundary-capture-$leg/"
  du -sb "$RT/made-$leg" "$RT/firmware-boundary-capture-$leg" >> "$R/meas/$T-leg$leg/size"
  find "$RT/made-$leg" -type f | wc -l >> "$R/meas/$T-leg$leg/size"
done
fresh before-judge
$R/tools/fbrun.sh "$T-judge" "$C" "$P" --require-rv32 --selftest --without verilator \
  --capture "$RT/firmware-boundary-capture-0" --capture "$RT/firmware-boundary-capture-1"

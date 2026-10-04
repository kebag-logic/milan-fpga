#!/bin/sh
# Usage: run_probe.sh <name>   (patch in probes/rtl or probes/tb, expected prefix in probes/expected.tsv)
# Exports HEAD's hdl and tb/{common,adp_engine} into scratch, applies one probe patch, runs tb/adp_engine.
. "$(dirname "$0")/env.sh"
set -u
n=$1
p=$(ls "$PACKET"/probes/rtl/"$n".patch "$PACKET"/probes/tb/"$n".patch 2>/dev/null | head -1)
exp=$(awk -F'\t' -v n="$n" '$1==n{print $2}' "$PACKET/probes/expected.tsv")
d="$SCRATCH/probe-$n"; rm -rf "$d"; mkdir -p "$d"
git -C "$CLONE" archive "$HEAD_SHA" hdl tb/common tb/adp_engine | tar -x -C "$d"
log="$RCPT/probe-$n.log"
{ echo "probe $n patch $(basename "$p") sha256 $(sha256sum < "$p" | cut -c1-64)"; echo "expected prefix: $exp"; } > "$log"
if ! (cd "$d" && patch -p1 --dry-run < "$p" >/dev/null && patch -p1 < "$p" >> "$log"); then
  echo "PATCH-FAILED" >> "$log"; echo 99 > "$RCPT/probe-$n.rc"; exit 99; fi
make -C "$d/tb/adp_engine" run VERILATOR="$VERILATOR" > "$d/run.log" 2>&1; rc=$?
tally=$(grep -E '^[0-9]+ checks:' "$d/run.log" | tail -1)
nf=$(grep -c '^FAIL:' "$d/run.log")
named=$(grep '^FAIL:' "$d/run.log" | sed 's/^FAIL: *//' | grep -cF -- "$exp" )
startsw=$(grep '^FAIL:' "$d/run.log" | sed 's/^FAIL: *//' | awk -v e="$exp" 'index($0,e)==1' | wc -l)
if [ "$rc" -ne 0 ] && [ -n "$tally" ] && [ "$startsw" -gt 0 ]; then v=KILLED-AS-PREDICTED
elif [ "$rc" -ne 0 ] && [ -n "$tally" ]; then v=KILLED-ELSEWHERE
elif [ "$rc" -eq 0 ]; then v=SURVIVED; else v=NO-TALLY; fi
{ echo "rc=$rc tally='$tally' failures=$nf named_prefix=$startsw verdict=$v"; grep '^FAIL:' "$d/run.log"; } >> "$log"
echo "$rc" > "$RCPT/probe-$n.rc"; echo "$n $v"

#!/usr/bin/env bash
# probe.sh NAME FILE LINE OLD NEW : clone the exact head into scratch, replace OLD
# by NEW on FILE:LINE (must match once), save the patch under probes/, build and run
# tb/srp_top (groups $PROBE_GROUPS, default applicant domjoin join onevec) and tb/srp_encoder; write probes/NAME.{patch,srp_top.log,
# srp_encoder.log,result}. A probe is KILLED when any FAIL: line appears and every
# group and the encoder printed a tally; a missing tally (build failure) is INVALID.
set -u
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
SRC=${SRC:-$REVIEWS/r802-1-pp216}
HEAD=60094a268c0df46703a3bee08c94118153634fd9
VPIN=${VPIN:-$VALIDATION_TOOLS/pinned-verilator-5.050}
name=$1; file=$2; line=$3; old=$4; new=$5
wt=$PKT/scratch/probe-$name; out=$PKT/probes/$name
rm -rf "$wt"; git clone -q "$SRC" "$wt" && git -C "$wt" checkout -q --detach $HEAD || exit 3
python3 -I - "$wt/$file" "$line" "$old" "$new" <<'PY' || { echo "INVALID (no match)" > "$out.result"; exit 4; }
import sys
p, ln, old, new = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
L = open(p).read().split('\n')
assert L[ln-1].count(old) == 1, (ln, L[ln-1])
L[ln-1] = L[ln-1].replace(old, new)
open(p, 'w').write('\n'.join(L))
PY
git -C "$wt" diff > "$out.patch"
export PATH=$VPIN:$PATH
PROBE_GROUPS=${PROBE_GROUPS:-applicant domjoin join onevec}
(cd "$wt/tb/srp_top" && make run RUN_ARGS=nonexistent-build-only >/dev/null 2>&1; rt=0; for g in $PROBE_GROUPS; do echo "== group $g"; ./obj_dir/Vsrp_top_sim $g || rt=$?; done; exit $rt) > "$out.srp_top.log" 2>&1; rt=$?
(cd "$wt/tb/srp_encoder" && make) > "$out.srp_encoder.log" 2>&1; re=$?
ng=$(echo $PROBE_GROUPS | wc -w)
nt=$(grep -Ec '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out.srp_top.log")
t2=$(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out.srp_encoder.log" | tail -1)
nf=$(cat "$out.srp_top.log" "$out.srp_encoder.log" | grep -c '^FAIL:')
if [ "$nt" -ne "$ng" ] || [ -z "$t2" ]; then verdict=INVALID
elif [ "$nf" -gt 0 ]; then verdict=KILLED
else verdict=SURVIVED; fi
fails=$(grep -h '^FAIL:' "$out.srp_top.log" "$out.srp_encoder.log" | cut -c1-90 | sort | uniq | head -6 | tr '\n' ';')
echo "$verdict groups=[$PROBE_GROUPS] srp_top rc=$rt tallies=$nt/$ng srp_encoder rc=$re [$t2] FAIL-lines=$nf first: $fails" > "$out.result"
rm -rf "$wt"

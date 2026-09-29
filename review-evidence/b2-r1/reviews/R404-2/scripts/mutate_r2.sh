#!/usr/bin/env bash
# Planted mutants for the round-2 checks. Each mutant is applied to a scratch
# copy (never to the clone or the archive extraction) and must change the
# check's output; the control (unmutated copy) must reproduce the receipt.
# Usage: mutate_r2.sh <packet dir> <archived author dir> <clone> <scratch dir>
set -u
P=$1; A=$2; C=$3; S=$4
rm -rf "$S"; mkdir -p "$S"
py() { python3 -B "$@"; }
verdict() { if [ "$1" = "$2" ]; then echo "SURVIVED"; else echo "KILLED"; fi; }
cp -r "$A" "$S/ctl"
base_ss=$(py "$P/scripts/saved_state_r2.py" "$S/ctl" | md5sum)
base_la=$(py "$P/scripts/leaveall_r2.py" "$S/ctl" | md5sum)
base_sp=$(py "$P/scripts/msrp_spacing_r2.py" "$S/ctl" | md5sum)
echo "control saved_state reproduces receipt: $( [ "$(py "$P/scripts/saved_state_r2.py" "$A" | md5sum)" = "$base_ss" ] && echo yes || echo NO)"
# M1: one action console sample reads nvm_dirty
cp -r "$S/ctl" "$S/m1"; sed -i '0,/PP_STAT=5b000c44/s//PP_STAT=5b000d44/' "$S/m1/cycles/cycle-050/console-after.txt"
o=$(py "$P/scripts/saved_state_r2.py" "$S/m1"); echo "M1 dirty bit in one sample: $(verdict "$(echo "$o" | md5sum)" "$base_ss") :: $(echo "$o" | grep 'distinct PP_STAT')"
# M2: final commit count differs
cp -r "$S/ctl" "$S/m2"; sed -i 's/commits ok=2 failed=0/commits ok=3 failed=0/' "$S/m2/restore/console-final.txt"
o=$(py "$P/scripts/saved_state_r2.py" "$S/m2"); echo "M2 final commits 3/0: $(verdict "$(echo "$o" | md5sum)" "$base_ss") :: $(echo "$o" | grep 'start == end')"
# M3: a write command in one transcript
cp -r "$S/ctl" "$S/m3"; sed -i '0,/"cmd":"GET_AVB_INFO"/s//"cmd":"SET_CLOCK_SOURCE"/' "$S/m3/cycles/cycle-010/snapshot-before.jsonl"
o=$(py "$P/scripts/saved_state_r2.py" "$S/m3"); echo "M3 SET_CLOCK_SOURCE in a transcript: $(verdict "$(echo "$o" | md5sum)" "$base_ss") :: $(echo "$o" | grep 'non-GET')"
# M4: a DUT stream input reads bound in one poll
cp -r "$S/ctl" "$S/m4"; python3 - "$S/m4/cycles/cycle-030/snapshot-before.jsonl" <<'PY'
import json,sys
p=sys.argv[1]; out=[]
for l in open(p):
    d=json.loads(l)
    if d.get('role')=='dut' and d.get('what')=='state-5-1': d['response']['conn_count']=1
    out.append(json.dumps(d))
open(p,'w').write('\n'.join(out)+'\n')
PY
o=$(py "$P/scripts/saved_state_r2.py" "$S/m4"); echo "M4 DUT input bound in one poll: $(verdict "$(echo "$o" | md5sum)" "$base_ss") :: $(echo "$o" | grep 'conn_count != 0')"
# M5: cycle 22's own LeaveAll moved 10 s later
cp -r "$S/ctl" "$S/m5"; python3 - "$S/m5/cycles/cycle-022/msrp.tsv" <<'PY'
import sys
p=sys.argv[1]; L=open(p).read().split('\n'); h=L[0].split('\t'); ti=h.index('t_s'); si=h.index('sender'); ei=h.index('event')
own={r.split('\t')[ti] for r in L[1:] if r and r.split('\t')[si]=='DUT' and r.split('\t')[ei]=='LeaveAll'}
out=[L[0]]
for r in L[1:]:
    f=r.split('\t')
    if r and f[ti] in own: f[ti]='%.9f'%(float(f[ti])+10.0)
    out.append('\t'.join(f))
open(p,'w').write('\n'.join(out))
PY
o=$(py "$P/scripts/leaveall_r2.py" "$S/m5"); echo "M5 cycle-22 own LeaveAll +10 s: $(verdict "$(echo "$o" | md5sum)" "$base_la") :: $(echo "$o" | grep -E 'PDUs < 10|cycle-022')" | tr '\n' ' '; echo
# M6: an unexplained off-grid DUT PDU in the baseline
cp -r "$S/ctl" "$S/m6"; printf '7.300000000\tDUT\tDomain\tJoinIn\t\t\n' >> "$S/m6/bind/baseline/msrp.tsv"
o=$(py "$P/scripts/msrp_spacing_r2.py" "$S/m6"); echo "M6 off-grid DUT PDU: $(verdict "$(echo "$o" | md5sum)" "$base_sp") :: $(echo "$o" | grep unexplained)"
# M7/M8: a measurement-table row and a verdict row edited in a scratch commit
git clone -q --shared "$C" "$S/clone"; git -C "$S/clone" checkout -q --detach d76763733e088cd21bbdd587927c8cf2f26cc8b3
sed -i 's/^| 57 | 0.009568 |/| 57 | 0.009569 |/' "$S/clone/docs/findings/608_75_WITHDRAWAL_AND_RESTART.md"
git -C "$S/clone" -c user.name=probe -c user.email=probe@invalid commit -qam probe
o=$(py "$P/scripts/tables_r2.py" "$S/clone" c37f1d04e39be0344dfde77e793cdfa441bd4869 HEAD "$P/scratch/pr622_body_at_review.md")
echo "M7 one per-cycle cell changed: $(echo "$o" | grep -q 'CHANGED   ## Per-cycle results' && echo KILLED || echo SURVIVED)"
sed -i 's/^| 2 | 39.3 | 17.323 |/| 2 | 39.4 | 17.323 |/' "$S/clone/docs/findings/606_FIRST_BIND_MEASUREMENT.md"
git -C "$S/clone" -c user.name=probe -c user.email=probe@invalid commit -qam probe2
o=$(py "$P/scripts/tables_r2.py" "$S/clone" c37f1d04e39be0344dfde77e793cdfa441bd4869 HEAD "$P/scratch/pr622_body_at_review.md")
echo "M8 one per-bind cell changed (page vs PR body): $(echo "$o" | grep -q "Per-bind table.*NO PAGE TABLE" && echo KILLED || echo SURVIVED)"
rm -rf "$S"

"""Check the page's initial-bind and restore statements against public records.

Usage: python3 initial_bind_check.py EVIDENCE_ROOT
Uses author/talker-setup/{analysis.json,msrp.tsv}, author/listener-setup/analysis.json,
author/census-start.jsonl and author/census-end.jsonl, and author-r2/disclosures.json.
"""
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
a1 = root / 'author'
disc = json.loads((root / 'author-r2' / 'disclosures.json').read_text())
fails = []


def check(ok, what):
    print(('PASS ' if ok else 'FAIL ') + what)
    if not ok:
        fails.append(what)


for rel, want in disc['source_hashes'].items():
    check(hashlib.sha256((a1 / rel).read_bytes()).hexdigest() == want, f'disclosure source hash {rel}')

an = json.loads((a1 / 'talker-setup/analysis.json').read_text())
resp, first = an['response_ns'], an['first_avtp_ns']
ev = [l.split('\t') for l in (a1 / 'talker-setup/msrp.tsv').read_text().splitlines()[1:]]
ev = [(int(e[0]), e[1], e[2], e[3], e[4]) for e in ev]
lat = (first - resp) / 1e9
check(abs(lat - 6.889398468) < 1e-9, f'initial talker bind latency {lat:.9f} s')
ta = [t for t, s, a, x, _ in ev if s == 'DUT' and a == 'TalkerAdvertise' and x in ('New', 'JoinIn', 'JoinMt')]
check(not [t for t in ta if t < resp], f'no DUT Talker Advertise declaration before the response ({len([t for t in ta if t < resp])})')
check(abs((ta[0] - resp) / 1e9 - 0.07923725) < 1e-9, f'first DUT TA {(ta[0]-resp)/1e9:.9f} s after the response')
gaps = [(b - a) / 1e9 for a, b in zip(ta, ta[1:]) if b < first]
print(f'INFO DUT TA declarations before first CRF: {len([t for t in ta if t < first])}; spacing s: {[round(g, 3) for g in gaps]}')
br = [(t, a, x) for t, s, a, x, _ in ev if s == 'bridge']
check(br and br[0][2] == 'LeaveAll' and abs((br[0][0] - resp) / 1e9 - 6.080007742) < 1e-9,
      f'first bridge MSRP is LeaveAll at +{(br[0][0]-resp)/1e9:.9f} s (capture time {br[0][0]/1e9:.6f} s)')
ready = [t for t, s, a, x, v in ev if s == 'bridge' and a == 'Listener' and x in ('New', 'JoinIn', 'JoinMt') and t >= resp]
check(abs((an['first_ready_since_connect_ns'] - resp) / 1e9 - 6.888605306) < 1e-9
      and abs((first - an['first_ready_since_connect_ns']) / 1e9 - 0.000793162) < 1e-9,
      f'Ready +{(an["first_ready_since_connect_ns"]-resp)/1e9:.9f} s, CRF +{(first-an["first_ready_since_connect_ns"])/1e9:.9f} s later')
dut_before_la = [t for t in ta if t < br[0][0]]
dut_after_la = [t for t in ta if br[0][0] <= t < an['first_ready_since_connect_ns']]
print(f'INFO DUT TA declarations between the response and the bridge LeaveAll: {len(dut_before_la)}; '
      f'between LeaveAll and Ready: {len(dut_after_la)} at +{[(t-resp)/1e9 for t in dut_after_la]}')
la = json.loads((a1 / 'listener-setup/analysis.json').read_text())
check(abs(la['latency_s'] - 0.198316) < 5e-7, f'initial listener bind {la["latency_s"]:.9f} s (< 1 s)')

# restore residue: every stream state descriptor, start vs end census
def states(p):
    out = {}
    for l in p.read_text().splitlines():
        r = json.loads(l)
        if str(r.get('what', '')).startswith('state-'):
            out[(r.get('role'), r['what'])] = r['response']
    return out
s0, s1 = states(a1 / 'census-start.jsonl'), states(a1 / 'census-end.jsonl')
check(set(s0) == set(s1), f'census start/end state key sets equal ({len(s0)} keys)')
diff = {k: sorted(f for f in set(s0[k]) | set(s1[k]) if f not in ('seq', 'rtt_ms', 't') and s0[k].get(f) != s1[k].get(f))
        for k in s0 if k in s1}
diff = {k: v for k, v in diff.items() if v}
for k, v in sorted(diff.items()):
    kind = lambda m: 'all-zero' if not m or set(str(m)) <= {'0'} else (
        'MAAP-range' if str(m).lower().startswith('91e0f000') else 'other')
    print(f'INFO differing fields {k}: {v}; start dmac/conn {kind(s0[k].get("dmac"))}/{s0[k].get("conn_count")} '
          f'end {kind(s1[k].get("dmac"))}/{s1[k].get("conn_count")}')
unbound = [k for k in s1 if s1[k].get('conn_count', 0) == 0]
print(f'INFO end-census states with conn_count 0: {len(unbound)} of {len(s1)}')
print('== RESULT', 'FAIL' if fails else 'PASS', f'({len(fails)} failing checks)')
sys.exit(1 if fails else 0)

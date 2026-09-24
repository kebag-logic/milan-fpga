#!/usr/bin/env python3
"""Re-check the #117 page's archive-level statements against the pinned evidence tree.

usage: archive_claims.py <archive-root: .../review-evidence/117-r1> <repo-clone> [<step3_rederive.json>]
Checks: MANIFEST.json completeness and published bytes; redaction counts (total, per packet,
path-only vs identity); `sha256sum -c` FAILED counts per packet; tcpdump logs and drops;
console transcripts and command verbs; envelope-less record counts per tap capture; the A200
binding census before/after; the daemon check; cycle 4-6 bind/unbind timing; attempt 1 guard;
PHC step vs "on"-command interval; build hashes present in the CRC table; the grader hash.
"""
import collections
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tapdec  # noqa: E402

root, repo = sys.argv[1], sys.argv[2]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
man = json.load(open(os.path.join(root, 'MANIFEST.json')))
files = {os.path.relpath(os.path.join(d, f), root) for d, _, fs in os.walk(root) for f in fs}
print('== MANIFEST.json')
print('entries', len(man), 'files on disk', len(files), 'unlisted', sorted(files - {e['file'] for e in man}))
print('published bytes match', sum(sha(os.path.join(root, e['file'])) == e['published_sha256'] for e in man), 'of', len(man))
red = [e for e in man if e['original_sha256'] != e['published_sha256']]
print('redacted', len(red), 'identity', sum(1 for e in red if e.get('identity_redacted')), 'path-only', sum(1 for e in red if not e.get('identity_redacted')),
      'per packet', dict(collections.Counter(e['file'].split('/')[0] for e in red)))
print('== sha256sum -c equivalent (packet MANIFEST.sha256 lines whose file bytes differ)')
for pk in ('bench-a200', 'bench-a202'):
    ok = bad = 0
    for ln in open(os.path.join(root, pk, 'MANIFEST.sha256')):
        if not ln.strip():
            continue
        h, _, f = ln.rstrip('\n').partition('  ')
        if sha(os.path.join(root, pk, f)) == h:
            ok += 1
        else:
            bad += 1
    print(pk, 'OK', ok, 'FAILED', bad)
print('== tcpdump logs')
logs = sorted(glob.glob(os.path.join(root, '**', 'tcpdump*.log'), recursive=True))
drops = [re.search(r'(\d+) packets dropped by kernel', open(l).read()) for l in logs]
print('logs', len(logs), 'dropped values', sorted({int(m.group(1)) for m in drops if m}), 'logs without a drop line', sum(1 for m in drops if not m))
print('== console transcripts')
cmds = collections.Counter()
nt = 0
for f in sorted(glob.glob(os.path.join(root, '**', '*.txt'), recursive=True)):
    c = re.findall(r"^### \S+ cmd='([^']*)'", open(f, encoding='latin-1').read(), flags=re.M)
    if c:
        nt += 1
        cmds.update(x.split()[0] for x in c)
print('transcripts', nt, 'commands', sum(cmds.values()), dict(sorted(cmds.items())))
print('== envelope-less records per tap capture')
for p in sorted(glob.glob(os.path.join(root, '**', '*.pcap'), recursive=True)):
    recs, ne = tapdec.tap_records(p)
    if recs:
        print(os.path.relpath(p, root), ne)
print('== A200 binding census (ACMP states)')
def acmp(f):
    return {(r['query'], r['talker'] if 'tx' in r['query'] else r['listener'], r['talker_uid'] if 'tx' in r['query'] else r['listener_uid']): r
            for r in (json.loads(l) for l in open(f) if l.strip()) if r.get('type') == 'acmp'}
a = acmp(os.path.join(root, 'bench-a200/bench/census-start.jsonl'))
b = acmp(os.path.join(root, 'bench-a200/bench/final/census-final.jsonl'))
print('states', len(a), len(b), 'same set', set(a) == set(b), 'connection counts', sorted({r['conn_count'] for r in list(a.values()) + list(b.values())}))
for k in sorted(a):
    d = {f: (a[k][f], b[k][f]) for f in a[k] if f != 't' and a[k][f] != b[k].get(f)}
    if d:
        print('field differs', k, d)
print('== daemon check file')
print(open(os.path.join(root, 'bench-a200/bench/hosts-clock-and-daemons.txt')).read().strip())
B = os.path.join(root, 'bench-a202', 'bench')
def t0(d):
    off = {}
    for fn in ('clock-before.jsonl', 'clock-after.jsonl'):
        for ln in open(os.path.join(d, fn)):
            j = json.loads(ln)
            off.setdefault(j['host'].split('>')[-1], []).append(j['offset_s_median_best5'])
    off = {h: sum(v) / len(v) for h, v in off.items()}
    ps = {}
    for ln in open(os.path.join(d, 'powerstrip.txt')):
        m = re.match(r'(?:\w+=\d+ )?(T_\w+) ([0-9.]+)', ln.strip())
        if m:
            ps[m.group(1)] = float(m.group(2))
    return off, ps
print('== cycles 4-6 bind and unbind (s after the off command, build-box clock)')
for n in (4, 5, 6):
    d = os.path.join(B, f'cycle{n}')
    off, ps = t0(d)
    T0 = ps['T_OFF_CMD'] - off['pi']
    ev = [(round(w['t'] - off['pw1'] - T0, 2), w['type'], w.get('attempt')) for w in (json.loads(l) for l in open(os.path.join(d, 'pw1-watch.jsonl'))) if w.get('type') in ('bind', 'unbind')]
    print('cycle', n, ev)
print('== attempt 1')
d = os.path.join(B, 'attempt1-aborted')
off, ps = t0(d)
lock = open(os.path.join(d, 'lock.txt')).read()
early = [float(x) for x in re.findall(r'^(\d{10}\.\d+)$', lock, flags=re.M)]
print('scheduled off-for', round(ps['T_ON_CMD'] - ps['T_OFF_CMD'], 2), '; guard "on" after', round(early[0] - ps['T_OFF_CMD'], 2), 's; PROOF_ABORT line present', 'PROOF_ABORT' in lock)
W = [json.loads(l) for l in open(os.path.join(d, 'pw1-watch.jsonl'))]
car = [(round(w['t'] - ps['T_OFF_CMD'], 2), w['value']) for w in W if w.get('type') == 'carrier']
print('carrier (s after off, NTP clocks)', car, '; up minus guard "on"', [round(c[0] - (early[0] - ps['T_OFF_CMD']), 2) for c in car if c[1] == 1 and c[0] > 0])
ok = [(round(w['t'] - ps['T_OFF_CMD'], 2), (w.get('decoded') or {}).get('gm'), (w.get('decoded') or {}).get('as_capable')) for w in W
      if w.get('what') == 'avb_info' and w.get('target') == '020000fffe000001' and w.get('status') == 'SUCCESS' and w['t'] > ps['T_OFF_CMD'] + 2]
print('first successful DUT GET_AVB_INFO polls after the outage', ok[:2])
print('== PHC step vs interval between the switch\'s power-on commands')
prev_on = early[0]
st = json.load(open(sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'receipts', 'step3_rederive.json')))
for n in range(1, 7):
    _, ps = t0(os.path.join(B, f'cycle{n}'))
    step = st[n - 1]['phc_steps'][0][1]
    print('cycle', n, 'interval', round(ps['T_ON_CMD'] - prev_on, 3), 'PHC step', step, 'sum', round(ps['T_ON_CMD'] - prev_on + step, 3))
    prev_on = ps['T_ON_CMD']
print('== build hashes in identity/expected-crc.txt (both packets identical:',
      sha(os.path.join(root, 'bench-a200/identity/expected-crc.txt')) == sha(os.path.join(root, 'bench-a202/identity/expected-crc.txt')), ')')
crc = open(os.path.join(root, 'bench-a200/identity/expected-crc.txt')).read()
for h in ('f0725eef7a361bd7dc6d692c369868f25e5d4f49f6b7267562a0b5f949ada33d', 'aaece32fc6c84f790273878350f674c142407a6b9ff2097862870784921da5fb',
          '9b077636b1d42aca660b16dce8eafa06f1e3cac842134e51ba65930d16214404', '69322600bc9dc40a698ed30d125d29d2723f51cc1b26c0f1c3abc96acb39deab',
          '71e798fc401ed3fbaac4cd43a299f23498beafa466aaa17d6773590a62fa93e2', '4db0e6da9c9c910a5ee00e56c25908c190c380799e44c846bcfb4ffc7dc045a7'):
    print(h[:8], 'in CRC table' if h in crc else 'not in CRC table')
g = subprocess.run(['git', '-C', repo, 'show', 'ede8d48ecd7c7f589a14b957951f040d92c99c70:scripts/baremetal_uart_smoke.py'], capture_output=True).stdout
print('grader at ede8d48e sha256', hashlib.sha256(g).hexdigest())

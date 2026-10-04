#!/usr/bin/env python3
"""R482-2 re-derivation of the round-2 claims of docs/findings/653_DISCONNECT_ORDER_BENCH.md.

Usage: verify_r2.py <author packet dir> <repo clone> <library source tree at v4.3.1.1>
  <author packet dir>  review-evidence/653-b11-r1/author of the lane's evidence branch
  <repo clone>         clone at the reviewed head (base 6c22d3ca, round 1 6f76d612)
  <library source>     unpacked upstream la_avdecc tarball at tag v4.3.1.1
Prints every derived figure; exits 1 if any page claim checked here is contradicted.
"""
import collections, hashlib, json, os, re, subprocess, sys

pkt, repo, lib = sys.argv[1:4]
PAGE = 'docs/findings/653_DISCONNECT_ORDER_BENCH.md'
R1, HEAD = '6f76d612a3191b77ac8a1fe2b9c66da42aeb405a', '6b83de0009673ce2c438985a0f9720f079a3715d'
bad = []


def check(ok, msg):
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok:
        bad.append(msg)


def show(rev, path):
    return subprocess.run(['git', '-C', repo, 'show', f'{rev}:{path}'], capture_output=True,
                          text=True, check=True).stdout


# 1. The library check at the tag
cpp = open(os.path.join(lib, 'src/controller/avdeccControllerImpl.cpp'), encoding='utf-8').read().split('\n')
print('avdeccControllerImpl.cpp sha256',
      hashlib.sha256(open(os.path.join(lib, 'src/controller/avdeccControllerImpl.cpp'), 'rb').read()).hexdigest())
for n in range(1590, 1591):
    print(f'{n}: {cpp[n - 1].strip()[:110]}')
for n in range(1605, 1615):
    print(f'{n}: {cpp[n - 1].rstrip()[:150]}')
check('lockedValue != unlockedValue && lockedValue != (unlockedValue + 1)' in cpp[1610],
      'line 1611 is the condition LOCKED != UNLOCKED && LOCKED != UNLOCKED + 1')
check('Invalid MEDIA_LOCKED / MEDIA_UNLOCKED counters value on STREAM_INPUT' in cpp[1612]
      and '"Milan 1.3 - 5.3.8.10"' in cpp[1612], 'line 1613 carries the quoted message and clause')
check('CompatibilityFlag::Milan' in cpp[1604], 'the check runs only for a Milan entity (line 1605)')
func = '\n'.join(cpp[1589:1630])
check(not re.search(r'[Cc]onnect|StreamInfo|isStreamRunning|getStreamInputConnection', func.split('removeCompatibilityFlag')[0]),
      'no connection-state term in updateStreamInputCounters before the flag removal')
hand = open(os.path.join(lib, 'src/controller/avdeccControllerImplHandlers.cpp'), encoding='utf-8').read().split('\n')
check('s_MilanMandatoryStreamInputCounters' in hand[34] and 'MediaUnlocked' in hand[34],
      'Handlers.cpp:35 is the mandatory STREAM_INPUT counter list')
uses = []
for root in ('src', 'include'):
    for dp, _, fs in os.walk(os.path.join(lib, root)):
        for f in fs:
            p = os.path.join(dp, f)
            for i, l in enumerate(open(p, encoding='utf-8', errors='replace'), 1):
                if 'StreamInputCounterValidFlag::MediaUnlocked' in l:
                    uses.append(f'{os.path.relpath(p, lib)}:{i}')
print('uses of StreamInputCounterValidFlag::MediaUnlocked:', sorted(uses))
check(sorted(u for u in uses if u.startswith('src/')) == ['src/controller/avdeccControllerImpl.cpp:1610',
                                                          'src/controller/avdeccControllerImplHandlers.cpp:35'],
      'in src/, exactly two uses: the check (1610) and the mandatory list (35)')
extra = sorted(u for u in uses if not u.startswith('src/'))
print('NOTE (finding RES1): uses outside src/, not named by the page\'s "one other use":', extra)


def accepted(ml, mu):
    return ml == mu or ml == mu + 1


# 2. Every STREAM_INPUT counters update the library delivered
tally = collections.Counter()
crf = {}
for s in ('s0b', 's1'):
    cyc = None
    for line in open(os.path.join(pkt, f'runs/{s}/{s}-probe.jsonl'), encoding='utf-8'):
        e = json.loads(line)
        if e['ev'] == 'cycle_begin':
            cyc = e['tag']
        if e['ev'] == 'si_counters':
            c = e['counters']
            tally[(s, e.get('who'), e.get('idx'), c['ML'], c['MU'], c.get('SI'), e['lib_conn'])] += 1
            if cyc in ('R01', 'R02') and e.get('who') == 'dut' and e.get('idx') == 1:
                crf.setdefault(cyc, []).append(('counters', e['t'], c['ML'], c['MU'], e['lib_conn']))
        if cyc in ('R01', 'R02') and e['ev'] == 'si_connection' and e.get('who', 'dut') == 'dut' \
                and e.get('idx', 1) == 1:
            crf.setdefault(cyc, []).append(('conn', e['t'], e.get('state')))
        if e['ev'] in ('compat_changed', 'diagnostics_changed', 'query_error', 'lost_unsol'):
            bad.append(f'{s} {cyc} library event {e["ev"]}')
print('\nsession who idx ML MU SI lib_conn : count  accepted')
agg = collections.Counter()
for k in sorted(tally, key=str):
    print(' ', k, ':', tally[k], accepted(k[3], k[4]))
    agg[(k[3], k[4], k[6])] += tally[k]
print('aggregate (ML, MU, lib_conn):', dict(agg))
check(set(agg) == {(0, 0, 'Connected'), (1, 0, 'Connected'), (1, 1, 'NotConnected')}
      and all(v == 23 for v in agg.values()),
      'updates are 0/0 and 1/0 while Connected and 1/1 while NotConnected, 23 each')
check(all(accepted(a, b) for a, b, _ in agg), 'the check accepts every delivered update')

# 3. CRF window: no counters update between NotConnected and the 1/1 push
for cyc, evs in sorted(crf.items()):
    t_nc = next(t for k, t, *r in evs if k == 'conn' and r[0] == 'NotConnected')
    after = [(t, ml, mu, lc) for k, t, *r in evs if k == 'counters' for ml, mu, lc in [r] if t > t_nc]
    first = after[0]
    print(f'{cyc}: NotConnected at t, first later update +{(first[0] - t_nc) / 1e3:.3f} ms carries {first[1]}/{first[2]} {first[3]}')
    check(first[1:3] == (1, 1), f'{cyc}: the first update after NotConnected carries 1/1 (none inside the window)')

# 4. The control interval from the provided decoder's C0 text
dec = open(os.path.join(pkt, 'summary/decode/b11-a535-s0b-C0.decode.txt'), encoding='utf-8').read().split('\n')
col = lambda pat: float(next(l for l in dec if re.search(pat, l)).split()[0])
own = col(r'DUT->sw\s+AECP RSP GET_COUNTERS tgt=DUT ctl=0b12')
cmd, rsp = col(r'UNBIND_RX_CMD'), col(r'UNBIND_RX_RESP')
# The decoder's column is (S - S0) / 1e6 with S the LE64 of the record's swapped words, so the true
# low-word delta in ns is dS / 2**32 (dS = column * 1e6) while the low word does not wrap.
us = lambda a, b: (b - a) * 1e6 / 2 ** 32 / 1e3
own_cmd, own_rsp, cmd_rsp = us(own, cmd), us(own, rsp), us(cmd, rsp)
print(f'\nC0 own GET_COUNTERS answer -> UNBIND_RX command  {own_cmd:.3f} us')
print(f'C0 own GET_COUNTERS answer -> UNBIND_RX response {own_rsp:.3f} us')
print(f'C0 UNBIND_RX command -> response                 {cmd_rsp:.3f} us')
order = [l.split(None, 1)[1] for l in dec if l.strip()]
i_own = next(i for i, l in enumerate(order) if 'RSP GET_COUNTERS tgt=DUT ctl=0b12' in l)
i_cmd = next(i for i, l in enumerate(order) if 'UNBIND_RX_CMD' in l)
i_rsp = next(i for i, l in enumerate(order) if 'UNBIND_RX_RESP' in l)
i_unl = next(i for i, l in enumerate(order) if i > i_rsp and 'UNSOL GET_COUNTERS' in l)
check(i_own < i_cmd < i_rsp < i_unl, 'C0 line order: own answer, command, response, unlock push')
g = json.load(open(os.path.join(pkt, 'summary/o653-grade.json')))['s0b/C0']['wire']
check(round(own_cmd, 1) == 1629.8 == g['control']['own_rsp_to_cmd_us'], 'command 1,629.8 us after the own answer (decoder and grade)')
check(round(own_rsp, 1) == 1637.3, 'response 1,637.3 us after the own answer')
check(round(cmd_rsp, 1) == g['cmd_to_rsp_us'] == 7.5, 'command to response 7.5 us')
page = show(HEAD, PAGE)
check('The UNBIND_RX command left 1,629.8 µs after the probe\'s own\nGET_COUNTERS answer, and its response 1,637.3 µs after it.' in page,
      'the page pairs 1,629.8 with the command and 1,637.3 with the response')

# 5. No measurement, figure or capture changed between round 1 and the head
old = show(R1, PAGE).split('\n')
new = page.split('\n')
row = lambda ls: [l for l in ls if l.startswith('| ') and re.search(r'\d', l)]
o_rows, n_rows = row(old), row(new)
diff_rows = [(a, b) for a, b in zip(o_rows, n_rows) if a != b]
print('\ntable rows with a digit: round 1', len(o_rows), 'head', len(n_rows), 'changed', len(diff_rows))
for a, b in diff_rows:
    print('  R1  :', a[:200]); print('  HEAD:', b[:200])
nums = lambda ls: collections.Counter(re.findall(r'\d[\d,.]*', '\n'.join(ls)))
lost = nums(old) - nums(new)
print('numeric tokens present at round 1 and absent at the head:', dict(lost))
print('numeric tokens new at the head:', dict(nums(new) - nums(old)))
hashes = lambda ls: sorted(re.findall(r'`([0-9a-f]{12,64})`', '\n'.join(ls)))
check(hashes(old) == hashes(new), 'every hash token on the page is unchanged')
caps = lambda ls: [l for l in ls if l.startswith('| `b11-a535-') or l.startswith('| C0') or re.match(r'\| [AR]\d\d ', l)]
check(caps(old) == caps(new), 'per-cycle rows and capture-hash rows are byte-identical')
print('\n' + ('ALL CHECKS PASS' if not bad else f'{len(bad)} FAILED: {bad}'))
sys.exit(1 if bad else 0)

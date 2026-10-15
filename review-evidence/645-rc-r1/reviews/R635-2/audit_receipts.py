#!/usr/bin/env python3
"""Read-only review of published data; run with the candidate repository as cwd.

Requires the two public evidence commits in the local object database.
No simulation, build, network write, or source mutation is performed.
"""
import collections
import hashlib
import json
from pathlib import Path
import re
import subprocess

PACKET = Path(__file__).resolve().parent
EVIDENCE = '512c59ba2c1a6533ee60fb2fe95f1ae3dcf43dc4'
B17 = 'bdb96b6685751a424fbbdc952726f33efd17282a'
ROOT = 'review-evidence/645-rc-r1/'
HEAD = 'fb5dd3dabd8f63cc83ff91323a76ce3adaeca89c'
OLD = '2639eecf3f94aa1a8be5c922058a05f0a48b1933'

def git(*args):
    return subprocess.check_output(['git', '--no-replace-objects', *args])

def blob(ref, path):
    return git('show', ref + ':' + path)

def main():
    manifest = json.loads(blob(EVIDENCE, ROOT + 'MANIFEST.json'))
    entries = {e['file']: e for e in manifest}
    used = {}
    def receipt(path):
        data = blob(EVIDENCE, ROOT + path)
        digest = hashlib.sha256(data).hexdigest()
        assert digest == entries[path]['published_sha256'], path
        used[path] = digest
        return data.decode()

    assert git('rev-parse', 'HEAD').decode().strip() == HEAD
    assert git('diff', OLD, HEAD, '--', 'hdl/') == b''
    print('Candidate', HEAD, 'tree', git('rev-parse', 'HEAD^{tree}').decode().strip())
    print('Delta paths:', git('diff', '--name-only', OLD, HEAD).decode().strip().replace('\n', ', '))
    print('All hdl/ entries unchanged since', OLD)

    tick = 1e6 / 48000
    bounds = []
    b17_manifest = json.loads(blob(B17, 'review-evidence/645-b17-r1/MANIFEST.json'))
    b17_entries = {r['file']: r for r in b17_manifest}
    print('\nB17 bounds from late-PDU records, retaining the published observation scope:')
    for i in range(1, 11):
        path = f'author/summary/c{i:02d}.json'
        data = blob(B17, 'review-evidence/645-b17-r1/' + path)
        digest = hashlib.sha256(data).hexdigest()
        assert digest == b17_entries[path]['published_sha256']
        used['B17/' + path] = digest
        c = json.loads(data)
        slips = c['poll']['slips']
        assert len(slips) == 1 and slips[0]['dups'] == 2 and slips[0]['skips'] == 0
        late = [r for r in c['tap']['late_pdus'] if r['late_us'] > 20]
        bursts = []
        for r in late:
            if not bursts or r['s'] - bursts[-1][-1]['s'] >= 0.001:
                bursts.append([])
            bursts[-1].append(r)
        high = max(r['late_us'] for r in bursts[0])
        later = max(r['late_us'] for b in bursts[1:] for r in b)
        low = later - tick
        assert high == slips[0]['tap_lateness_max_us']
        bounds.append((low, high))
        print(f'c{i:02d}: first={high:.3f}, later={later:.3f}, lower={low:.6f}, upper={high:.3f} us')
    low, high = bounds[4]
    assert all(lo <= low and hi >= high for lo, hi in bounds)
    assert abs(low - 9.426666666666666) < 1e-10 and high == 24.565
    print('All nine other cycle intervals contain c05; 10 us is unused in bound calculation.')

    result_re = re.compile(
        r'RESULT-645-BIND: B17 cycle (\d+) phase ([\d.]+).*?primed margin ([\d.]+)\.\.([\d.]+) us '
        r'\((inside|OUTSIDE) B17.*?arms (\d+).*?settle recentres (\d+) \(([-\d.]+) ticks.*?'
        r'render recentres (\d+), SLIP_LB \+(\d+) dups \+(\d+) skips, slipped frames (\d+) '
        r'before the ring acts and (\d+) after, first burst [\d.]+ us at \+([\d.]+) s.*?'
        r'margin after a recentre ([+\-\d.]+)\.\.([+\-\d.]+) ticks, full side ([+\-\d.]+)')
    slip_re = re.compile(r'info: B17 cycle (\d+): slip \((dup|skip)\).*?, ([+\-\d.]+) s from')

    def grid(name):
        prefix = 'author-r2/r2/campaign/' + name + '/'
        records, codes = {}, []
        for path in sorted(entries):
            if not path.startswith(prefix) or not path.endswith('.log'):
                continue
            stem = Path(path).stem
            command = json.loads(receipt(path[:-4] + '.command.json'))
            phase = float(command[command.index('--bind-phase') + 1])
            codes.append(int(receipt(path[:-4] + '.rc')))
            current = None
            for line in receipt(path).splitlines():
                m = result_re.search(line)
                if m:
                    v = m.groups()
                    key = (stem, int(v[0]))
                    current = dict(phase=phase, lo=float(v[2]), hi=float(v[3]), inside=v[4]=='inside',
                                   arms=int(v[5]), settle=int(v[6]), ticks=float(v[7]), render=int(v[8]),
                                   dups=int(v[9]), skips=int(v[10]), pre=int(v[11]), post=int(v[12]),
                                   burst=float(v[13]), empty=float(v[14]), full=float(v[16]), slips=[])
                    assert current['inside'] == (current['lo'] > low and current['hi'] < high)
                    records[key] = current
                m = slip_re.search(line)
                if m:
                    assert current is not None
                    current['slips'].append((m[2], float(m[3])))
        return records, codes

    for gridname, expected in [('16',(320,177,143,0,6)), ('32',(320,151,169,1,19)),
                                ('dense',(256,140,116,2,6))]:
        head, hc = grid('fix' + gridname)
        base, bc = grid('base' + gridname)
        assert head.keys() == base.keys()
        inside = {k:v for k,v in head.items() if v['inside']}
        outside = {k:v for k,v in head.items() if not v['inside']}
        inslips = {k:v for k,v in inside.items() if v['dups'] or v['skips']}
        outslips = {k:v for k,v in outside.items() if v['dups'] or v['skips']}
        assert (len(head),len(inside),len(outside),len(inslips),len(outslips)) == expected
        assert all(v['arms'] == v['settle'] == v['render'] == 1 and v['post'] == 0 for v in head.values())
        assert all(v['arms'] == v['settle'] == v['render'] == 0 for v in base.values())
        assert all(v['dups'] == 1 and v['skips'] == 0 for v in inslips.values())
        assert all(v['dups'] == 2 and v['skips'] == 0 for v in outslips.values())
        for key, v in head.items():
            early = [s for s in v['slips'] if s[1] < 0]
            assert early == [s for s in base[key]['slips'] if s[1] < 0], key
        print(f'\nGrid {gridname}: {len(head)} binds; head rc0 {hc.count(0)}/{len(hc)}, base rc0 {bc.count(0)}/{len(bc)}')
        print(f'Head-defined cohorts: inside {len(inside)} ({len(inslips)} +1-dup cases), outside {len(outside)} ({len(outslips)} +2-dup cases)')
        print('All early slip kind/time records equal on both datapaths to printed microsecond; zero head post-action slips.')
        print('Out-of-window slip phases:',sorted(set(v['phase'] for v in outslips.values())))
        print('Out-of-window latest early slip ms:', max((v['burst'] + t)*1000 for v in outslips.values() for _,t in v['slips']))
        for key,v in inslips.items():
            print('In-window residual:',key,'phase',v['phase'],'dups',v['dups'],'ms',[(v['burst']+t)*1000 for _,t in v['slips']])
        if gridname == '16':
            assert all(base[k]['dups'] == 2 and base[k]['skips'] == 0 and len(base[k]['slips']) == 1
                       and 0 <= base[k]['slips'][0][1] < .01 for k in inside)
            counts = collections.Counter((base[k]['dups'],base[k]['skips']) for k in outside)
            assert counts == {(2,0):43, (4,0):99, (3,0):1}
            newly = [k for k,v in head.items() if v['inside'] and v['lo'] <= 10]
            assert len(newly) == 8 and all(k[0]=='bind_j5_p05' for k in newly)
            assert {k[1] for k in newly} == {1,2,3,4,5,6,7,10}
            print('Paired base result: all 177 head-inside cases +2 at first burst; outside raw dup/skip counts',dict(counts))
            print('Base own longer pre-burst interval classifies',sum(v['inside'] for v in base.values()),'inside; paired table uses head membership.')
            print('Newly in-window cases:',newly,'lowest margin',min(head[k]['lo'] for k in newly))
            print('Head minimum empty/full margins:', min(v['empty'] for v in head.values()), min(v['full'] for v in head.values()))
            print('Head tick range:',min(v['ticks'] for v in head.values()),max(v['ticks'] for v in head.values()))

    for name in ('fr_default','fr_mutants'):
        assert int(receipt('author-r2/r2/suites/'+name+'.rc')) == 0
        log=receipt('author-r2/r2/suites/'+name+'.log')
        if name == 'fr_mutants': assert 'follow_ring mutants: 15/15 caught' in log
        print('\nPublished suite',name,': rc0')
        for line in log.splitlines():
            if ('checks:' in line or 'SETTLE CONTROL PASS' in line or 'settle control ' in line
                    or '15/15 caught' in line or '[MUTANT] NO-BIND' in line
                    or '[MUTANT] BIND-RISE' in line or '[MUTANT] FOLLOWING' in line):print(line)
    print('\nPASS: all receipt assertions; no design/simulation rerun.')
    (PACKET/'audit-inputs.sha256').write_text(''.join(f'{d}  {p}\n' for p,d in sorted(used.items())))

if __name__ == '__main__':
    main()

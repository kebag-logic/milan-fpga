#!/usr/bin/env python3
"""Recompute PR 698's current-record tables and non-overlapping ledger."""
import json
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
base = '5603c353137e90c1fa95429f6d00ef7a2298d9ee'
head = 'c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970'
plan = (root / 'docs/design/MARK_II_AREA_PLAN.md').read_text()
budget = (root / 'docs/design/AREA_BUDGET.md').read_text()
record_path = 'syn/ooc/pp_resource_baseline.json'
raw = subprocess.check_output(['git', '-C', str(root), 'show', base + ':' + record_path])
assert raw == (root / record_path).read_bytes(), 'Resource record changed'
records = json.loads(raw)['endpoints']
checks = []

def check(label, actual, expected):
    checks.append({'check': label, 'actual': actual, 'expected': expected})
    assert actual == expected, (label, actual, expected)

def rows(text):
    for line in text.splitlines():
        if line.startswith('|'):
            yield [c.strip().strip('`*') for c in line.strip('|').split('|')]

def num(s):
    return float(s.replace(',', ''))

for row in rows(plan.split('### Current processor inventory')[0]):
    if row[0] not in records:
        continue
    r = records[row[0]]['record']
    if len(row) == 2:
        check(row[0] + ' input digest', row[1], r['inputs_sha256'])
        continue
    f = r['figures']
    for i, key in enumerate(['LUT', 'FF', 'SLICE', 'RAMB36', 'RAMB18', 'BRAM_TILE', 'DSP'], 1):
        if row[i] != '--':
            check(row[0] + ' ' + key, num(row[i]), f[key])
    check(row[0] + ' timing', [num(s.strip()) for s in row[8].split('/')], [f['WNS_ns'], f['WHS_ns']])
    check(row[0] + ' BRAM arithmetic', f['RAMB36'] + f['RAMB18'] / 2, f['BRAM_TILE'])

inventory = plan.split('### Current processor inventory')[1].split('## Baseline at dev')[0]
for row in rows(inventory):
    if row[0] not in records['route-1x1']['record']['scopes']:
        continue
    for i, endpoint in enumerate(['route-1x1', 'ooc-1x1', 'ooc-8x8'], 1):
        check(endpoint + ' ' + row[0], num(row[i]), records[endpoint]['record']['scopes'][row[0]]['LUT'])

for row in rows(budget.split('### Mark II planning ledger')[1].split('### The resource gate')[0]):
    if row[0] not in records:
        continue
    f = records[row[0]]['record']['figures']
    check('budget ' + row[0], [num(row[1]), num(row[2]), *[num(x.strip()) for x in row[3].split('/')], num(row[4])],
          [f['LUT'], f['FF'], f['RAMB36'], f['RAMB18'], f['DSP']])

split = plan.split('### Default split saving basis')[1].split('### Remaining levers')[0]
scope_groups = {
    'ADP': ['u_pp/u_adp'],
    'ACMP listener and listener admission': ['u_pp/u_listener', 'u_pp/u_lsn_admit'],
    'ACMP talker': ['u_pp/u_talker'],
    'Originator': ['u_pp/u_originator'],
    'ACMP binding store': ['u_pp/u_nvm_shadow'],
    'SRP': ['u_pp/u_srp'],
    'AECP, including microcode, descriptor and D3 stores': ['u_pp/u_aecp'],
    'Notification': ['u_pp/u_notify'],
    'NVM port and arbiter': ['u_pp/u_nvm_port', 'u_pp/u_nvm_arb'],
    'Wrapper NVM backend': ['u_nvm'],
}
scopes = records['ooc-1x1']['record']['scopes']
used = [s for group in scope_groups.values() for s in group]
assert len(used) == len(set(used))
assert not any(b.startswith(a + '/') for a in used for b in used if a != b)
subtotal = sum(scopes[s]['LUT'] for s in used)
tiles = sum(scopes[s]['RAMB36'] + scopes[s]['RAMB18'] / 2 for s in used)
for row in rows(split):
    if row[0] in scope_groups:
        check('split ' + row[0], num(row[1]), sum(scopes[s]['LUT'] for s in scope_groups[row[0]]))
    if row[0] == 'Disjoint wrapper subtotal':
        check('wrapper subtotal', num(row[1]), subtotal)
    if row[0] == 'Gross reference':
        check('gross reference', num(row[1]), subtotal + 429)
check('credited BRAM release', tiles, 6.5)
check('uncredited wrapper residual', scopes['wrapper']['LUT'] - subtotal, 5501)
check('split central unrounded', subtotal + 429 - 3102 - 1000, 14005)
check('split conservative unrounded', subtotal + 429 - 3102 - 2000 - 1500, 11505)
check('split optimistic unrounded', subtotal + 429 - 3102 - 500 + 1500, 16005)

levers = {}
for row in rows(plan.split('### Remaining levers without overlap')[1].split('M3 remains a priced')[0]):
    m = re.fullmatch(r'([\d,]+) \(([\d,]+)-([\d,]+)\)', row[1]) if len(row) > 1 else None
    if m:
        levers[row[0].split(' /')[0]] = [int(s.replace(',', '')) for s in m.groups()]
levers['F0-F5, complete qualified flip / L2'] = [14000, 11500, 16000]
levers['M8b, conditional'] = levers['M8b']
levers['M3 and M10'] = [0, 0, 0]
current = [records['route-1x1']['record']['figures']['LUT']] * 3
cumulative = plan.split('### Cumulative default-image estimates')[1].split('## Lane sequence')[0]
for row in rows(cumulative):
    if row[0].isdigit() and int(row[0]) < 9:
        saving = [0, 0, 0] if row[0] == '0' else levers[row[1]]
        current = [a-b for a,b in zip(current, saving)]
        check('cumulative ' + row[1], [num(s) for s in row[3:6]], current)

budget_rows = list(rows(budget.split('These figures are estimates')[1].split('The split estimate')[0]))
expected_central = [36267, 36067, 35467, 34867, 34367, 32767, 31067, 31067, 31067]
actual_central = [int(r[2].replace(',', '')) for r in budget_rows if len(r) == 4 and r[2].replace(',', '').isdigit()]
check('budget cumulative sequence', actual_central, expected_central)
check('required target', 63400 * 0.6, 38040)
check('one-percent integer ceiling', int(38040 * 0.99), 37659)
check('baseline gap', 50267 - 38040, 12227)
check('central headroom', 38040-current[0], 6973)
check('conservative headroom', 38040-current[1], 2973)
check('central headroom percent', round((38040-current[0])/38040*100, 2), 18.33)
check('conservative headroom percent', round((38040-current[1])/38040*100, 2), 7.82)
check('conservative without smaller core', current[1] + levers['M8b'][1], 36367)
check('central without split', current[0] + 14000, 45067)
check('route slices free', 15850 - 15779, 71)
check('physical BRAM free', 135 - 87.5, 47.5)
check('policy BRAM free', 121.5 - 87.5, 34)
check('gate WNS floor from fall tolerance', round(0.299-0.25, 3), 0.049)
aecp_children = ['u_d3', 'u_dyn', 'u_store', 'u_ucpu', 'u_resp']
check('AECP own logic basis', scopes['u_pp/u_aecp']['LUT'] - sum(scopes['u_pp/u_aecp/'+s]['LUT'] for s in aecp_children), 1302)
queue_matches = [(s, v['LUT']) for s,v in scopes.items() if s.startswith('u_pp/u_dispatch/') and v['LUT'] == 421]
check('AECP queue basis count', len(queue_matches), 1)
check('retained admission basis', scopes['u_pp/u_srp/u_admission']['LUT'], 345)
mailbox = (root/'docs/design/MAILBOX_SPLIT.md').read_text().split('## Measured area')[1]
mbx_rows = [r for r in rows(mailbox) if r[0] == 'Total' and len(r) == 7]
check('mailbox replacement LUT and FF', [num(mbx_rows[0][3]),num(mbx_rows[0][6])], [3102,2946])
assert 'WNS is +0.402' in mailbox
assert '1 RAMB36, 10 RAMB18' in mailbox
check('mailbox BRAM tiles', 1 + 10/2, 6)
assert 'uses 429 LUTs and 279 FFs' in budget
for endpoint, item in records.items():
    assert 'a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb' in item['measured']
    assert '2ad2f845dd583f8310075fa2380cb60a04fd091a' in item['measured']
m3 = 0.6*scopes['u_pp/u_notify']['LUT'] + 0.7*(scopes['u_pp/u_aecp/u_d3']['LUT'] + scopes['u_pp/u_aecp/u_dyn']['LUT']) + 0.5*1302 + 0.4*421
check('M3 gross weighted estimate', round(m3, 1), 3380.3)
print(json.dumps({'head':head, 'base':base, 'checks_passed':len(checks), 'checks':checks,
                  'M3_net_estimate':m3-1000+200,
                  'limits':'Compares committed records and arithmetic; no new implementation measurement.'}, indent=2))

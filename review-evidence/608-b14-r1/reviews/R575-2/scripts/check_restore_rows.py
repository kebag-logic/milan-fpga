#!/usr/bin/env python3
"""R575-2: compare the 15 as-found rows with item 2's teardown compare and with what the
archived final records (restore/) hold.  Usage: check_restore_rows.py <author dir>"""
import json, os, sys
a = sys.argv[1]
J = lambda p: [json.loads(l) for l in open(os.path.join(a, p)) if l.strip().startswith('{')]
af = [e for e in J('item2/setup/events.jsonl') if e['kind'] == 'as-found'][0]
af = {k: v for k, v in af.items() if k not in ('t', 'mono_raw_ns', 'kind')}
td = [e for e in J('item2/teardown/events.jsonl') if e['kind'] == 'restore-compare'][0]['rows']
print('setup as-found keys', len(af), sorted(af))
print('teardown compare rows', len(td), 'all equal', all(v['equal'] for v in td.values()), 'missing from setup record', sorted(set(td) - set(af)))
p8 = [e for e in J('restore/asfound-rx.jsonl') if e.get('type') == 'acmp']
print('asfound-rx acmp rows', len(p8), [(e.get('listener_unique_id', e.get('luid')), e.get('connection_count', e.get('conn_count')), e.get('flags')) for e in p8][:6])
fin = {}
for f, key in (('restore/final-dut-in0.jsonl', 'rx-dut-0'), ('restore/final-dut-in1.jsonl', 'rx-dut-1'), ('restore/final-peer-in8.jsonl', 'rx-peer-8')):
    fin[key] = [e for e in J(f) if e.get('kind') == 'after'][-1]['rx']['conn_count']
fm = J('restore/final-maps.jsonl')
fin['rx-peer-0'] = [e for e in fm if e.get('kind') == 'after'][-1]['rx']['conn_count']
for e in fm:
    if e.get('kind') == 'audio-map':
        print('final map', e.get('descriptor_type'), e.get('descriptor_index'), 'mappings', len(e.get('mappings', [])) if 'mappings' in e else {k: v for k, v in e.items() if k not in ('t',)})
for k, v in fin.items():
    ref = af.get(k, td.get(k, {}).get('as_found'))
    if isinstance(ref, dict): ref = ref['conn_count']
    print(k, 'final conn_count', v, 'as found', ref, 'equal', v == ref)
rc = open(os.path.join(a, 'restore/restore-compare.txt')).read()
print('restore-compare.txt clock rows:', [l for l in rc.splitlines() if "'clock'" in l], 'as found clk-dut', af['clk-dut'], 'clk-peer', af['clk-peer'])
for e in fm:
    if e.get('kind') == 'audio-map':
        key = 'map-dut-0x%04x-0' % int(e['descriptor_type'], 16)
        print(key, 'final mappings', e.get('mappings'), 'as-found', af[key][1])
print('formats: final values are not in the archived restore/ records (only in the raw snapshot-final.jsonl); teardown 05:45 compare equal for all 7:', all(td[k]['equal'] for k in td if k.startswith('fmt-')))

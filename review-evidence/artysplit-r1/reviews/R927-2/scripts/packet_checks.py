"""Reviewer checks over the author's round-7 receipts packet (argv[2]) against a checkout of the head (argv[1]).

Checks: the FILES.tsv whole hash; census.json lists 147 cases; the installed in-tree Arty statements equal the
step-2 derived model's costs; the step-2 model's first choice is the installed row; the owed exclusions in the final
census are all srp-kept/srp-bound kinds; identity.log ends IDENTICAL with 147 stimuli and records no flash image; the
census-build log of step 2 is byte-identical to step 1's; the regrade logs' outcomes. Prints one line per check."""
import hashlib, json, sys
from pathlib import Path
ROOT, P = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(ROOT / 'tb/verilator/ctrl_service_budget'))
import load_grade, poll_grade, rows_grade, rows_tiers, edit_rows, shape_costs
ok = True
def check(name, cond, detail=''):
    global ok
    ok &= bool(cond)
    print(('PASS' if cond else 'FAIL'), name, detail)
m = json.loads((P / 'FILES.manifest.json').read_text())
data = b''.join((P / p['file']).read_bytes() for p in m['parts'])
check('FILES.tsv whole hash and size', hashlib.sha256(data).hexdigest() == m['sha256'] and len(data) == m['bytes'])
rows = [l.split('\t') for l in data.decode().splitlines()[1:]]
census = [r for r in rows if r[0].startswith('census/')]
check('unpublished census files listed', True, f'{len(census)} files, {sum(int(r[1]) for r in census)} bytes')
c = json.loads((P / 'census.json').read_text())
check('census.json lists 147 cases at 74f942be5', len(c['cases']) == 147 and c['source_head'].startswith('74f942be5'))
d = json.loads((P / 'derivation/model-installed-r7-step2.json').read_text()); k = d['costs']
st = load_grade.STATED_US['arty-1x1']
check('load_grade statements == derived', all(k.get(x) == v for x, v in st.items()))
pa = poll_grade.STATED_US[shape_costs.Shape(1, 1, 2)]
check('poll_grade statements == derived', all(k.get('base' if x == 'base' else 'item.' + x) == v
                                              for x, v in pa.items() if x != 'mrpdu'))
check('rows_grade LINK == derived', rows_grade.__dict__ and k['event.LINK'] == 190)
check('datapath events == derived', all(k['event.' + x] == v for x, v in rows_tiers.DATAPATH_US['arty-1x1'].items()))
check('long record == derived', k['record.aecp.long'] == rows_tiers.LONG_RECORD_US['arty-1x1'])
check('edit rows == derived', edit_rows.PACED['arty-1x1'] == {'a one-row edit': max(k['paced.44'], k['paced.45']),
                                                              'an accepted SET_CONFIGURATION': k['paced.6']})
first = d['choices'][0]
h = shape_costs.at(shape_costs.Shape(1, 1, 2), ROOT)
check('installed row is the first choice', (first['slice_us'], first['pace_ms'], first['queued_ms']) ==
      (h['CTRL_LOOP_SLICE_US'], h['AECP_PACE_MS'], h['CTRL_LOOP_QUEUED_MS']),
      f"choices {[(x['slice_us'], x['pace_ms'], x['queued_ms']) for x in d['choices']]}")
check('retry statements == derived', d['retry_us'] == [h['CTRL_LOOP_RETRY_COLD_US'], h['CTRL_LOOP_RETRY_ATTEMPT_US'],
                                                       h['AECP_NOTICE_US']])
q = json.loads((P / 'qualification/census.json').read_text())
check('owed exclusions only in srp-kept/srp-bound', all(o['group'] in ('none/srp-kept', 'none/srp-bound')
                                                        for o in q['owed_969']), str(len(q['owed_969'])))
ident = (P / 'validation/identity.log').read_text()
j = json.loads(ident[:ident.rindex('}') + 1])
check('identity IDENTICAL, 147 stimuli', ident.rstrip().endswith('IDENTICAL') and
      sum(v['stimuli_compared'] for v in j.values()) == 147)
check('identity records no flash image in any variant', all(v['flash'] is None for v in j.values()))
check('step-2 census-build log is byte-identical to step 1', (P / 'validation/census-build.log').read_bytes() ==
      (P / 'validation/step1-census-build.log').read_bytes())
for name, want in (('receipt-regrade.log', 'RESULT: PASS cases=147'), ('receipt-regrade-control.log', 'graded srp-kept alone'),
                   ('receipt-regrade-before-fix.log', 'cross-case qualification failed')):
    check(f'{name} outcome', want in (P / 'validation' / name).read_text())
pq = json.loads((P / 'published-qualification.json').read_text())
check('published qualification PASS, 147 groups, worst pass', pq['status'] == 'PASS' and pq['groups'] == 147,
      str(pq['worst_pass']['worst_pass_cycles']))
raise SystemExit(0 if ok else 1)

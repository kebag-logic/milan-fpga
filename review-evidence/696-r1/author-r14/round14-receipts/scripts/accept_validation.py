import json
from pathlib import Path
w=Path(__file__).resolve().parent
assert (w/'validation-bank.rc').exists() and (w/'validation-resume.rc').exists()
assert (w/'validation-resume.rc').read_text().strip()=='0'
original=json.loads((w/'validation/results.json').read_text())
retry=json.loads((w/'validation-resume-results.json').read_text())
refusals=[r for r in original if r['rc']]
assert len(refusals)==1 and refusals[0]['name']=='boundary' and refusals[0]['rc']==2,refusals
assert 'ModuleNotFoundError: No module named' in (w/'attempts/boundary-docenv.log').read_text()
assert len(retry)==5 and all(r['rc']==0 for r in retry)
replacement={r['name']:r for r in retry}
rows=[replacement.get(r['name'],r) for r in original]
seen={r['name'] for r in rows};rows += [r for r in retry if r['name'] not in seen]
assert len(rows)==22 and len({r['name'] for r in rows})==22 and all(r['rc']==0 for r in rows)
assert all(r['head']=='e2cd089ce2d902c73a5f7c6ae5bcee3aa84461bd' for r in rows)
record=dict(head=rows[0]['head'],initial_chain_rc=int((w/'validation-bank.rc').read_text()),setup_refusal=refusals[0],resolution='Reran the boundary gate in the installed build interpreter carrying migen; no source changes',commands=rows)
(w/'accepted-validation.json').write_text(json.dumps(record,indent=2)+'\n')
(w/'accepted-validation.rc').write_text('0\n')
print('All 22 final validation commands pass; initial environment refusal retained separately')

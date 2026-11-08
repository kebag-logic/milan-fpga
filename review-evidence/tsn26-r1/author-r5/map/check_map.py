# SPDX-License-Identifier: MIT
# usage: check_map.py TREE CAMPAIGN_RESULTS_JSON ESCAPE_JSON OUT_MD
# Checks the round 5 sentence map against a tree: every sentence of PORTING "ACMP owed bound" and of the ACMP-12
# prose has one map entry; every core sentence has a named assertion (test and streamed message in that test's
# body) and every listed plant is registered with that exact kill, CAUGHT in the campaign, and escapes once the
# tests that fail under it are excluded. Exit status 1 on any gap.
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import sentence_map as sm
tree, campaign, escape, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
errors = []
porting = (tree / 'docs/PORTING.md').read_text()
sec = porting[porting.index('### ACMP owed bound'):porting.index('## ADP input validation')]
def sentences(text, join=False):
    out = []
    lines = [l for l in text.split('\n') if l.strip()]
    for line in ([' '.join(lines)] if join else lines):
        out += re.split(r'(?<=[.;:])\s+(?=[A-Z`])', line)
    return out
req = (tree / 'docs/REQUIREMENTS.md').read_text()
prose = req[req.index('ACMP-12 originates from'):req.index('| ID | Required behavior | Clause |', req.index('ACMP-12 originates from'))]
row = [l for l in req.splitlines() if l.startswith('| ACMP-12 |')][0]
groups = [('PORTING owed bound', sentences(sec)[1:], sm.PORTING), ('ACMP-12 prose', sentences(prose, True)[1:], sm.REQUIREMENTS)]
test_src = (tree / 'tests/test_acmp.cpp').read_text()
def body(name):
    suite, test = name.split('.')
    m = re.search(r'TEST_F\(' + suite + r', ' + test + r'\) \{\n(.*?)\n\}\n', test_src, re.S)
    if not m and suite == 'AcmpOwed':
        return None
    return m.group(1) if m else None
fixture = test_src[test_src.index('class AcmpOwed : public AcmpCore {'):test_src.index('// REQ: ACMP-12, ACMP-09\nTEST_F(AcmpOwed, HeldEgressDefersTheCommandBehindTheOwedSet)')]
plants = {m['name']: m for m in json.loads((tree / 'tests/mutations.json').read_text())}
status = {r['name']: r['status'] for r in json.loads(campaign.read_text())}
esc = {r['plant']: r for r in json.loads(escape.read_text())} if escape.exists() else {}
rows = []
def check_entry(where, key, kind, pins):
    for p in pins:
        b = body(p['test'])
        if b is None:
            errors.append(f'{where}: no test {p["test"]}')
            continue
        if '"' + p['needle'] not in b and p['needle'] not in b and p['needle'] not in fixture:
            errors.append(f'{where}: needle not in {p["test"]}: {p["needle"]}')
        for name in p['plants']:
            m = plants.get(name)
            if m is None:
                errors.append(f'{where}: plant not registered: {name}'); continue
            if not any(k['test'] == p['test'] and k['needle'] == p['needle'] for k in m['kills']):
                errors.append(f'{where}: {name} is not registered with kill {p["test"]} / {p["needle"]}')
            if status.get(name) != 'CAUGHT':
                errors.append(f'{where}: {name} is {status.get(name)} in the campaign')
            e = esc.get(name)
            if e is not None and not e.get('without_its_killers', {}).get('escapes'):
                errors.append(f'{where}: {name} does not escape without its killers')
    if kind == 'core' and not any(p['plants'] for p in pins):
        errors.append(f'{where}: core sentence without a pinned plant: {key}')
for label, sents, entries in groups:
    used = set()
    for i, s in enumerate(sents, 1):
        hits = [e for e in entries if e[0] in s]
        if len(hits) != 1:
            errors.append(f'{label} sentence {i} has {len(hits)} map entries: {s[:90]}')
            continue
        key, kind, pins = hits[0]
        used.add(key)
        check_entry(f'{label} {i}', key, kind, pins)
        rows.append((label, i, s, kind, pins))
    for e in entries:
        if e[0] not in used:
            errors.append(f'{label}: map entry matches no sentence: {e[0]}')
for i, (key, kind, pins) in enumerate(sm.TABLE, 1):
    if key not in row:
        errors.append(f'ACMP-12 table clause {i} not in the requirement row: {key}')
    check_entry(f'ACMP-12 table {i}', key, kind, pins)
    rows.append(('ACMP-12 requirement', i, key, kind, pins))
def cell(s):
    return s.replace('|', '\\|').replace('\n', ' ')
md = ['| Text | # | Sentence or clause | Kind | Assertions (test: message) | Plants |', '|---|---|---|---|---|---|']
for label, i, s, kind, pins in rows:
    s = re.sub(r'\]\([^)]*\)', ']', s)
    a = '<br>'.join(f'`{p["test"].split(".")[1]}`: "{cell(p["needle"])}"' for p in pins) or '-'
    pl = ', '.join(sorted({n for p in pins for n in p['plants']})) or '-'
    md.append(f'| {label} | {i} | {cell(s)} | {kind} | {a} | {pl} |')
out.write_text('\n'.join(md) + '\n')
n_core = sum(1 for r in rows if r[3] == 'core')
print(f'{len(rows)} sentences and clauses, {n_core} core, {len({n for r in rows for p in r[4] for n in p["plants"]})} distinct plants')
print('\n'.join(errors) if errors else 'map: every sentence mapped; every core sentence pinned by a registered, caught plant')
sys.exit(1 if errors else 0)

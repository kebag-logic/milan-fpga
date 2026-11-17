"""Collect existing round-11 receipts without rerunning a build or changing the checkout.

Usage: collect_r11.py CHECKOUT SCRATCH OUTPUT
Every raw log is hashed. Large logs are represented by an explicit excerpt.
"""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

lane, scratch, out = map(Path, sys.argv[1:])
full = scratch / 'fullR11'
head = subprocess.check_output(['git', '-C', str(lane), 'rev-parse', 'HEAD'], text=True).strip()
receipt = out / 'receipts'
manifest = []


def clean(text):
    for source, replacement in ((str(scratch), '<scratch>'), (str(lane), '<checkout>'),
                                ('$WORKSPACE_HOME', '<home>'), ('/data-2/milan', '<data>'),
                                ('$VALIDATION_STORAGE', '<data>'), ('/tmp/', '<tmp>/')):
        text = text.replace(source, replacement)
    return text


def retain(source, dest):
    data = source.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    text = clean(data.decode(errors='replace'))
    mode = 'complete normalized text'
    if len(text.encode()) > 180000:
        lines = text.splitlines()
        selected = set(range(min(18, len(lines)))) | set(range(max(0, len(lines)-25), len(lines)))
        for i, line in enumerate(lines):
            if '[ESCAPED]' in line or line.startswith('[DIFF]') or 'plant srp-plus-k:' in line:
                selected.update(range(max(0, i-1), min(len(lines), i+18)))
        text = '\n'.join(f'{i+1}: {lines[i]}' for i in sorted(selected)) + '\n'
        mode = 'excerpt; raw file exceeds packet size limit'
    header = f'# Original bytes {len(data)}; sha256 {digest}\n# {mode}\n'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(header + text)
    assert dest.stat().st_size < 200000
    manifest.append({'source': source.relative_to(scratch).as_posix(),
                     'raw_bytes': len(data), 'raw_sha256': digest,
                     'receipt': dest.relative_to(out).as_posix(), 'mode': mode})


logs = full / 'wf/logs'
for source in sorted(logs.iterdir()):
    if source.is_file():
        retain(source, receipt / 'gates/workflow' / source.name)
for source in sorted((full / 'lane').iterdir()):
    if source.is_file():
        retain(source, receipt / 'gates/lane' / source.name)
retain(full / 'quick/quick-checks.txt', receipt / 'gates/quick-checks.txt')
retain(scratch / 'units/r11-Q-img.log', receipt / 'images/qimg-05a7ea82.txt')
retain(scratch / 'r11/launchG2.log', receipt / 'gates/launcher-history.txt')
for k in (1,3,4,6):
    source = scratch / f'units/r11-vretry-{k}.log'
    if source.exists():
        retain(source, receipt / f'gates/stopped-shards/shard-{k}.txt')

# Enumerate the actual workflow at the candidate; never infer success from a wrapper.
old_reasons = json.loads((out / 'scripts/not_run.json').read_text())
not_run, rows = {}, []
selected = {'rtl-fast': {'firmware-unit', 'firmware-control-mutants', 'firmware-aecp-mutants',
                        'firmware-srp-mutants', 'firmware-boundary', 'firmware-verilator'},
            'docs': {'wire-accountability', 'docs-check-no-git', 'docs-gates-0',
                     'docs-gates-1', 'docs-gates-2', 'docs-check'}}
for workflow in ('rtl-fast', 'docs', 'rtl'):
    wf = yaml.safe_load((lane / f'.github/workflows/{workflow}.yml').read_text())
    for job, body in wf['jobs'].items():
        for number, step in enumerate(body['steps']):
            if 'run' not in step:
                continue
            sid = step.get('id', f'step{number}')
            key = f'{workflow}.yml/{job}/{sid}'
            tag = f'{workflow}__{job}__{sid}'
            rc_file = logs / (tag + '.rc')
            if rc_file.exists():
                rc = int(rc_file.read_text().strip())
                first = (logs / (tag + '.log')).read_text(errors='replace').splitlines()[0]
                assert head in first, (tag, first)
                state = 'PASS' if rc == 0 else 'FAIL'
                evidence = f'workflow/{tag}.log'
            elif workflow == 'rtl' and job == 'verilator-shards' and sid == 'ci_step_21':
                rc, state = None, 'REFUSED / INCOMPLETE'
                evidence = ('Shards 1,3,4,6,10,17 refused local donor origin before affected suites ran; '
                            'fresh-clone retries 1,3,4,6 stopped on the firmware failure; 10,17 not retried. '
                            'See setup-refusals/ and stopped-retries.txt.')
            else:
                rc, state = None, 'NOT RUN'
                if job in selected.get(workflow, set()):
                    evidence = (old_reasons.get(key) or old_reasons.get(f'{workflow}.yml/{sid}')
                                or old_reasons.get(sid))
                    assert evidence, key
                elif workflow == 'rtl' and job == 'verilator-shards':
                    evidence = ('The local shard helper ran the suite command with installed prerequisites; '
                                'this hosted provisioning/recording step was not executed verbatim. '
                                'No full workflow pass is claimed; the run stopped after the firmware gate failure.')
                else:
                    evidence = ('Outside the final jobs selected by the round-11 ruling; no new execution '
                                'is claimed, and the gate failure stops further work. Hosted orchestration '
                                'also requires its hosted context.')
                evidence = clean(evidence)
                not_run[key] = evidence
            rows.append({'workflow':workflow, 'job':job, 'step':sid, 'name':step.get('name',''),
                         'state':state, 'rc':rc, 'evidence':evidence})
not_run['docs_inventory --check'] = ('No tracked docs_inventory executable exists at this head; '
                                   'the full docs jobs ran as defined. This separately requested command is NOT RUN.')
(receipt / 'gates/not_run.json').write_text(json.dumps(not_run, indent=2) + '\n')
(receipt / 'gates/workflow-steps.json').write_text(json.dumps({'head':head, 'steps':rows}, indent=2) + '\n')
table=['# Workflow run-step inventory', '', f'Head: {head}', '',
       '| Workflow | Job | Step | Result | rc | Evidence or reason |',
       '|---|---|---|---|---:|---|']
for r in rows:
    table.append('| ' + ' | '.join(str(r[k]).replace('|','/') for k in
                                  ('workflow','job','step','state','rc','evidence')) + ' |')
table += ['', f"{sum(r['rc'] is not None for r in rows)} actual step executions; "
          f"{sum(r['state']=='FAIL' for r in rows)} failed; "
          f"{sum(r['state']=='NOT RUN' for r in rows)} not run with a reason.", '']
(receipt / 'gates/workflow-steps.md').write_text('\n'.join(table))
lane_rows=[]
for rc_file in sorted((full/'lane').glob('*.rc')):
    name=rc_file.stem
    rc=int(rc_file.read_text().strip())
    expected=1 if name.endswith('_exits_1') else 0
    lane_rows.append({'gate':name,'rc':rc,'expected':expected,'pass':rc==expected})
(receipt/'gates/lane-results.json').write_text(json.dumps({'head':head,'gates':lane_rows},indent=2)+'\n')
(receipt/'gates/raw-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Collected {len(manifest)} logs/status receipts; workflow failures: '
      f'{[r["job"] for r in rows if r["state"]=="FAIL"]}; '
      f'lane failures: {[r["gate"] for r in lane_rows if not r["pass"]]}')

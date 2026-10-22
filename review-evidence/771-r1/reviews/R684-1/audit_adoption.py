#!/usr/bin/env python3
"""Reconcile published patches and measurement receipts with the reviewed tree."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

repo = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
evidence = Path(sys.argv[2]).resolve()
base = 'd77a8afdbc960d70d1ceeee9af1163624f102b16'
head = 'a97aea01449492b1f640924f5a34726f602cabed'
def git(*args):
    return subprocess.check_output(['git', '-C', str(repo), *args])
def blob(rev, path):
    return git('show', rev + ':' + path)
def check(name, condition):
    print(('PASS ' if condition else 'FAIL ') + name, flush=True)
    assert condition, name

check('head and tree', git('rev-parse', 'HEAD', 'HEAD^{tree}').decode().splitlines() ==
      [head, 'ea69f3b4c4c4b2f50a38a868b5f1dba56b248249'])
links = [line.split()[-1].decode() for line in git('diff', '--raw', base, head).splitlines()
         if line.startswith(b':160000 160000 ')]
check('only the two required donor gitlinks changed', sorted(links) == ['gptp-processor', 'protocol-processor'])
for donor, old_pin, new_pin, path in [
    ('protocol-processor', '2cbed0a987c1e68402658d69459ab7e5aa571adc', '93fb0b2d736b36588ea7321e25fba2f8819ea41f', 'hdl/top/protocol_processor_top.sv'),
    ('gptp-processor', 'e4869fd0c42889b2ac806587cc5c78afb1c33461', '55680bff3b287b9a7b0c759f51471fa617c17335', 'hdl/top/KL_gptp_engine.sv')]:
    check(donor + ' exact gitlinks', git('rev-parse', base + ':' + donor, head + ':' + donor).decode().splitlines() == [old_pin, new_pin])
    def interface(pin):
        source = subprocess.check_output(['git', '-C', str(repo / donor), 'show', pin + ':' + path]).decode()
        source = re.sub(r'/\*.*?\*/|//[^\n]*', '', source, flags=re.S)
        header = source[source.index('module '):].split(');', 1)[0]
        return re.sub(r'\s+', '', header)
    before, after = interface(old_pin), interface(new_pin)
    if donor == 'protocol-processor':
        before = before.replace('[15:0]cfg_tspec_max_frame_i', '[N_STREAM_OUT_P*16-1:0]cfg_tspec_max_frame_i')
    check(donor + ' top interface has only the supplied TSpec width adaptation', before == after)
manifest = json.loads((evidence / 'MANIFEST.json').read_text())
for row in manifest:
    check('published hash ' + row['file'],
          hashlib.sha256((evidence / row['file']).read_bytes()).hexdigest() == row['published_sha256'])
patch_names = [
    'parent-evidence-classification.patch', 'parent-adoption-milan_dp-67.patch',
    'parent-scratch-tspec-every-slot.patch', 'parent-adoption-milan_dp-gsi-g9.patch',
    'parent-adoption-gptp_shadow-85.patch', 'parent-adoption-milan_dp-85.patch',
    'parent-adoption-milan_dp-82.patch', 'parent-adoption-milan_dp_gptp-84.patch']
commits = ['8144d2885', '2dc612fbd', 'c6afca8ce', '300911eaf',
           '1e305876b', 'd255806ce', '7d9d730c6', '0e4d10b25']
patches = [(evidence / 'author' / name).read_bytes() for name in patch_names]
paths = sorted({p.decode() for patch in patches for p in re.findall(rb'^\+\+\+ b/(.+)$', patch, re.M)})
with tempfile.TemporaryDirectory(dir=packet / 'scratch', prefix='patches-') as td:
    work = Path(td)
    def populate():
        for path in paths:
            target = work / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob(base, path))
    for name, patch in zip(patch_names, patches):
        populate()
        r = subprocess.run(['git', 'apply', '--verbose', '-'], input=patch, cwd=work,
                           capture_output=True)
        check('individual contextual application ' + name, r.returncode == 0)
    populate()
    for name, patch, commit in zip(patch_names, patches, commits):
        r = subprocess.run(['git', 'apply', '--verbose', '-'], input=patch, cwd=work,
                           capture_output=True)
        check('ordered application ' + name, r.returncode == 0)
        touched = re.findall(rb'^\+\+\+ b/(.+)$', patch, re.M)
        for p in touched:
            path = p.decode()
            check('patch postimage at ' + commit + ' ' + path,
                  (work / path).read_bytes() == blob(commit, path))
    for path in paths:
        check('composed final bytes ' + path, (work / path).read_bytes() == blob(head, path))

old = json.loads(blob(base, 'syn/ooc/pp_resource_baseline.json'))
new = json.loads(blob(head, 'syn/ooc/pp_resource_baseline.json'))
for endpoint, want_delta in [('route-1x1', (770, 210)), ('ooc-1x1', (462, 177)), ('ooc-8x8', (2185, 769))]:
    o, n = old['endpoints'][endpoint], new['endpoints'][endpoint]
    check(endpoint + ' unchanged policy', {k:v for k,v in o.items() if k not in ('record', 'measured')} ==
          {k:v for k,v in n.items() if k not in ('record', 'measured')})
    check(endpoint + ' unchanged flow identity', o['record']['identity'] == n['record']['identity'])
    head_record = json.loads((evidence / 'author' / ('record-head-' + endpoint + '.json.log')).read_text())
    dev_text = (evidence / 'author' / ('record-dev-' + endpoint + '.json.log')).read_text()
    dev_record, end = json.JSONDecoder().raw_decode(dev_text)
    check(endpoint + ' dev receipt suffix', dev_text[end:].strip() in ('', 'rc=0'))
    for key in ('identity', 'figures', 'scopes', 'inputs_sha256'):
        check(endpoint + ' recorded ' + key, head_record[key] == n['record'][key])
    delta = tuple(head_record['figures'][k] - dev_record['figures'][k] for k in ('LUT', 'FF'))
    check(endpoint + ' adoption-only delta ' + str(delta), delta == want_delta)

images = json.loads((evidence / 'author/image-builds.json').read_text())
check('image receipt exact-head attribution', images['point']['parent_head'] == head)
for build in images['builds']:
    for corner in ('Slow_0C', 'Slow_85C', 'Fast_0C', 'Fast_85C'):
        wns, whs = build[corner]
        check(build['build'] + ' ' + corner + ' timing', wns >= .03 and whs >= 0)
    route = build['route_status']
    check(build['build'] + ' route and packing', route['routable nets'] == route['fully routed nets']
          and route['nets with routing errors'] == 0 and build['iob_pack']['FAIL'] == 0 and build['rc'] == 0)
rows = re.findall(r'^\w+\s+(\d+)\s+(\d+)\s+(\d+)\s*$',
                  (evidence / 'author/sweep-tally-per-suite.txt').read_text(), re.M)
check('63 published suite rows', len(rows) == 63)
check('2189520 checks, zero failures', sum(int(r[0]) for r in rows) == 2189520
      and sum(int(r[1]) for r in rows) == 0)
docs = json.loads((evidence / 'author/docs-steps-final-receipts.json').read_text())
check('docs receipt exact-head attribution', docs['head'] == docs['head_after'] == head)
check('42 executed docs steps pass; two steps explicitly skipped',
      sum(s.get('rc') == 0 and not s.get('skipped') for s in docs['steps']) == 42
      and sum(bool(s.get('skipped')) for s in docs['steps']) == 2)
print('DOC STEP STATUS', [(s['job'], s['id'], s.get('rc'), s.get('skipped')) for s in docs['steps']])
print('Audit complete')

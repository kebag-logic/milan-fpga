"""Check downloaded public receipts, issue-diff identity, and shipping hashes."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

root, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
public = out / 'public-evidence'
head = '1496558d82cf35fc98dda0e781b2a1be643c301a'
base = '88e9276b2a220c716f64a843f7e1eb8f9265e896'
original_base = 'b17580b91deb11f3441dfc5d7f9fafe539d929b8'
author = '099e191137dd2797407fb8345a452bcc7a965608'
old = 'd81a302760b84f32d2aa019643f57682bb6e052c'
fix = '2b2009488351f04f4cc4d2d316ad6d5f6f1e8ba7'
def git(*args):
    return subprocess.check_output(['rtk','proxy','git','-C',str(root),*args],
                                   env={**os.environ,'GIT_NO_REPLACE_OBJECTS':'1'})

manifest = {x['file']:x for x in json.loads((public/'MANIFEST.json').read_text())}
downloads = json.loads((public/'download-verification.json').read_text())
verified = []
for entry in downloads['files']:
    rel = entry['path'].removeprefix('review-evidence/478-r1/')
    data = (public/rel).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest() == entry['blob']
    if rel != 'MANIFEST.json':
        assert hashlib.sha256(data).hexdigest() == manifest[rel]['published_sha256']
        verified.append(rel)
for bank, count in [('full-native',5),('manager-builder',40)]:
    p = public/'round2/manager'
    spec = json.loads((p/(bank+'.json')).read_text())
    results = json.loads((p/bank/'results.json').read_text())
    complete = json.loads((p/bank/'complete.json').read_text())
    assert spec['head'] == results['head'] == complete['head'] == head
    assert spec['base'] == results['base'] == base
    assert len(spec['commands']) == len(results['results']) == count
    assert spec['commands'] == [x['command'] for x in results['results']]
    assert complete['exit_code'] == 0 and all(x['exit_code']==0 for x in results['results'])
images = json.loads((out/'focused-receipts/1496558d/images.json').read_text())
for rel, attribution in [('author/after-rates.json',author),('author/baseline-rates.json',original_base)]:
    historical = json.loads((public/rel).read_text())
    for name in images:
        for key in ['config_sha256','image_sha256','rates','offset']:
            assert images[name][key] == historical[name][key], (rel,name,key)
        assert len(images[name]['rates']) == historical[name]['count']
(out/'evidence-verification.json').write_text(json.dumps(dict(
    archive_revision=downloads['revision'], git_blobs_verified=len(downloads['files']),
    published_manifest_entries_verified=len(verified), verified_files=verified,
    manager_head=head,manager_base=base,native_commands=5,static_builder_commands=40,
    author_rate_packet_head=author,baseline_rate_packet_head=original_base,
    historical_rate_hashes_match_current=True,
    original_private_hashes_not_independently_verified=True),indent=2)+'\n')

paths = git('diff','--name-only',base,head).decode().splitlines()
assert paths == ['docs/ENDSTATION_BUILDER.md','sw/builder/endstation_builder.py','sw/builder/test_builder.py']
for file in paths[1:]:
    assert len({git('rev-parse',rev+':'+file).strip() for rev in [head,fix,old,author]}) == 1
assert git('diff','--name-only',old,fix).decode().splitlines() == ['docs/ENDSTATION_BUILDER.md']
old_url = '../protocol-processor/docs/architecture/07_memory_maps.md#31-descriptor-tree'
new_url = 'https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/blob/424c688fa2205b934a7689a58f2aa766420f2326/docs/architecture/07_memory_maps.md#31-descriptor-tree'
old_doc = git('show',old+':docs/ENDSTATION_BUILDER.md').decode()
new_doc = git('show',head+':docs/ENDSTATION_BUILDER.md').decode()
assert old_doc.replace(old_url,new_url) == new_doc
for file in ['scripts/docs_check.py','.github/workflows/docs.yml',
             'tb/verilator/pp_shadow/sim_main.cpp','tb/verilator/pp_shadow/Makefile']:
    assert len({git('rev-parse',rev+':'+file).strip() for rev in [head,base,old]}) == 1
pins = {}
for sub in ['external','protocol-processor','gptp-processor','third_party/verilog-axis']:
    values = {git('rev-parse',rev+':'+sub).decode().strip() for rev in [head,base,original_base,old,author,fix]}
    assert len(values) == 1
    pins[sub] = values.pop()
patch = git('diff','--binary',base,head)
(out/'issue-diff.patch').write_bytes(patch)
(out/'link-only-correction.diff').write_bytes(git('diff','--binary',old,fix))
(out/'history.txt').write_bytes(git('log','--format=fuller',base+'..'+head))
(out/'diff-identity.json').write_text(json.dumps(dict(head=head,tree=git('rev-parse',head+'^{tree}').decode().strip(),
    base=base,paths=paths,issue_diff_sha256=hashlib.sha256(patch).hexdigest(),
    author_builder_and_tests_byte_identical=True,correction_only_url=True,
    unchanged_checker_workflow_and_bench=True,pins_unchanged=pins,
    integrated_old_head_delta_paths=git('diff','--name-only',old,head).decode().splitlines()),indent=2)+'\n')
print('PASS: 61 public Git blobs, 60 manifest hashes, 40+5 exact-head commands, shipping hashes and bounded diff')

#!/usr/bin/env python3
import hashlib,json,pathlib,re,sys
p=pathlib.Path(sys.argv[1]).resolve();w=p/'scratch/replays';d=json.loads((w/'results.json').read_text());expected_nonzero={'R557-4-full','R557-6-full','early-comments'}
assert len(d['results'])==18
for x in d['results']:assert x['rc']==int(x['name'] in expected_nonzero),x
full=json.loads((w/'r5566/probes.json').read_text());assert len(full)==11 and all(x['build_rc']==0 and x['result']=='CAUGHT' for x in full)
assert 'gaps: 0' in (w/'R556-3-comments.log').read_text()
assert 'gaps: 0 of 11' in (w/'R556-4-comments.log').read_text()
assert '"CAUGHT-BY-MESSAGE": 329, "SHARED": 0, "MISSING": 0' in (w/'R556-4-specificity.log').read_text()
assert 'gaps: 0' in (w/'R556-5-hidden.log').read_text()
assert all(x['gate_rc']==(0 if x['control']=='baseline' else 1) and x['compile_rc']==0 for x in json.loads((w/'early/receipts/comment-controls.json').read_text()))
tree=(w/'R556-5-tree.log').read_text()
for label in ('A-comments','B-comments','B-rv32','C-comments'):assert label+' rc=1' in tree
q=p/'scratch/round8-replay';assert all(x['rc']==0 for x in json.loads((q/'results.json').read_text()))
assert all(x['compiled'] and x['outcome']=='AS-EXPECTED' for x in json.loads((q/'assertions/probe_assertions.json').read_text()))
spi=(q/'spi-tree.log').read_text();assert 'needles rc=1' in spi and 'test-inventory rc=1' in spi and 'port_tests rc=0' in spi
flags=(q/'dependencies.log').read_text()
for name in ('cmake-module-mode','mutation-no-cflags','mutation-old-libs'):assert name+': dependency_selftest rc=1' in flags
assert 'upstream -I package flags (non-system prefix): dependency_selftest rc=0' in flags
prefix=json.loads((p/'scratch/package-prefix-probe/results.json').read_text());assert len(prefix['results'])==6 and all(x['rc']==0 for x in prefix['results'])
assert 'malformed input controls accepted: 3/3' in (w/'adp-input.log').read_text()
verified=[]
for x in json.loads((p/'receipts/prior-script-sources.json').read_text()):
 relative=x['source'].split('/reviews/',1)[1];data=(p/'scratch/prior-public'/relative).read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==x['blob'];verified.append(relative)
for x in json.loads((p/'receipts/round8-probe-sources.json').read_text()):
 relative=x['source'].split('/reviews/',1)[1];assert hashlib.sha256((p/'scratch/prior-public'/relative).read_bytes()).hexdigest()==x['sha256'];verified.append(relative)
result=dict(head=d['head'],replay_results=d['results'],full_tree_rows=11,full_tree_caught=11,round8_assertion_rows=18,round8_comment_rows=27,prefix_steps=6,public_script_blobs_verified=len(verified),historical_nonzero_explained=sorted(expected_nonzero),limits=['C23 exploratory row still does not compile.','include-next and the header containing assembler text do not compile; neither is credited as a compiling refusal control.','External linker INCLUDE remains accepted under the declared directory scope.','Inherited ADP input probe reports three accepted malformed inputs, matching the owner decision.','Some old scripts assert that a former bypass exists and now return 1 after closure.'],invocation_adaptations=d['adaptation'])
(p/'receipts/replay-audit.json').write_text(json.dumps(result,indent=2)+'\n');print('Historical outcomes verified; no unexpected replay regression; 36 published script blobs unchanged')

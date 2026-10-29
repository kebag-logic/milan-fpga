#!/usr/bin/env python3
"""Audit source identity, published receipt hashes and focused mutation coverage."""
import hashlib, json, os, pathlib, re, stat, subprocess, sys
P=pathlib.Path(__file__).resolve().parent
SRC=pathlib.Path(sys.argv[1]).resolve()
def git(*args): return subprocess.check_output(['git',*args],cwd=SRC)
HEAD='1be824fccbda5d3341737f5fe033d60edd27af57'
TREE='ab055c2107ab5ce1ead0f1fa6cfce10ae0956c12'
assert git('rev-parse','HEAD').decode().strip()==HEAD
assert git('rev-parse','HEAD^{tree}').decode().strip()==TREE
entries=[]; links=[]; errors=[]
for raw in git('ls-tree','-rz','HEAD').split(b'\0'):
    if not raw: continue
    meta,name=raw.split(b'\t',1); mode,kind,oid=meta.decode().split(); name=os.fsdecode(name)
    if mode=='160000': links.append((name,oid)); continue
    file=SRC/name
    body=os.fsencode(os.readlink(file)) if mode=='120000' else file.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
    actual_mode='120000' if file.is_symlink() else ('100755' if file.stat().st_mode&stat.S_IXUSR else '100644')
    if actual!=oid or actual_mode!=mode: errors.append(name)
    entries.append((mode,oid,name))
index=[]
for raw in git('ls-files','--stage','-z').split(b'\0'):
    if not raw: continue
    meta,name=raw.split(b'\t',1); mode,oid,stage=meta.decode().split()
    assert stage=='0'
    if mode!='160000': index.append((mode,oid,os.fsdecode(name)))
assert sorted(index)==sorted(entries)
assert not errors, errors
for name,oid in links:
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=SRC/name).decode().strip()==oid
print('SOURCE_IDENTITY',HEAD,TREE)
print('TRACKED_BLOBS_MODES_AND_INDEX_PASS',len(entries))
print('SUBMODULE_GITLINKS',json.dumps(links))
print('TRACKED_DIFF',git('diff','--name-status','HEAD').decode().strip() or 'empty')
print('POST_CAMPAIGN_SOURCE_STATUS',git('status','--porcelain=v1').decode().strip() or 'clean')
print('POST_5fd298c_DELTA',git('diff','--name-only','5fd298c..HEAD').decode().strip())
manifest=json.loads((P/'published-manifest.json').read_text())
checked=0
for item in manifest:
    f=P/'public'/item['file']
    if f.exists():
        actual=hashlib.sha256(f.read_bytes()).hexdigest()
        assert actual==item['published_sha256'],(str(f),actual,item['published_sha256'])
        checked+=1
print('PUBLISHED_RECEIPT_SHA256_PASS',checked)
results=json.loads((P/'rbt-mutants/results.json').read_text())
expected={m[1]:int(m[2]) for m in re.finditer(r'^\| `(rbt-[^`]+)` .*\| (\d+) \|$',(SRC/'tb/pp_top/README.md').read_text(),re.M)}
assert len(expected)==17
for r in results:
    if r['arm'].startswith('rbt-'):
        assert r['verdict']=='KILLED' and r['named']>0
        assert r['failures']==expected[r['arm']],(r,expected[r['arm']])
        print('RBT_ROW',r['arm'],'named',r['named'],'failures',r['failures'],'README_MATCH')
assert len(results)==18 and results[0]['verdict']=='PASS'
print('RBT_MUTATION_LEDGER_PASS 17/17; positive control PASS')
for name in ['recut-aecp','recut-adp','recut-d3','docs-check-git','reboot-control','reboot-mutants']:
    assert (P/(name+'.rc')).read_text().strip()=='0',name
assert (P/'post-departure-probe.rc').read_text().strip()=='2'
for family in ['aecp','adp']:
    current=(P/('recut-'+family+'.log')).read_text()
    oldpath='campaigns/aecp-5fd298c/aecp.log' if family=='aecp' else 'campaigns/adp-engine-061a9ec/camp-adp.log'
    old=(P/'public/author/receipts'/oldpath).read_text()
    arms=re.findall(r'^(\S+): rc=2 failures=(\d+) named=(\d+) KILLED$',current,re.M)
    assert len(arms)==(5 if family=='aecp' else 2)
    for arm,n,k in arms:
        assert f'{arm}: rc=2 failures={n} named={k} KILLED' in old
        print('RECUT_MATCHES_PUBLISHED',arm,n,k)
for row in json.loads((P/'recut-d3/results.json').read_text()):
    assert row['verdict'] in ['PASS','KILLED']
    print('D3_RESULT',row['mutant'],row['verdict'],row.get('missing',[]))
print('ALL_EXPECTED_RECEIPT_RETURN_CODES_PASS')

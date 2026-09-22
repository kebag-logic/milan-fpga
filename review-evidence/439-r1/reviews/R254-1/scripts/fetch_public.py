import base64, concurrent.futures, hashlib, json, pathlib, subprocess
out = pathlib.Path(__file__).resolve().parent.parent
entries = json.loads((out / 'public/evidence-tree.json').read_text())['tree']
prefix = 'review-evidence/439-r1/'
auth = {'commands.jsonl','original-command-failures.txt','mutation-results.json','logs/baseline-check.stdout','logs/baseline-selftest.stdout','logs/final-check.stdout','logs/final-selftest.stdout','logs/mutation-accept-content-drift.stderr','logs/mutation-accept-missing-record.stderr','logs/py-idiom.stderr'}
selected = [e for e in entries if e['type']=='blob' and (e['path'].startswith(prefix+'source/manager/') and ('/full-suite-logs/' not in e['path']) or e['path'].removeprefix(prefix+'author/') in auth)]
def fetch(e):
    argv=['rtk','proxy','gh','api','repos/kebag-logic/milan-fpga/git/blobs/'+e['sha']]
    r=subprocess.run(argv, capture_output=True, check=True)
    b=base64.b64decode(json.loads(r.stdout)['content'])
    digest=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
    assert digest==e['sha']
    dest=out/'public/evidence'/e['path'].removeprefix(prefix)
    dest.parent.mkdir(parents=True,exist_ok=True); dest.write_bytes(b)
    return {'path':str(dest.relative_to(out)), 'git_blob':digest, 'bytes':len(b), 'argv':argv,'exit':r.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    receipts=list(pool.map(fetch,selected))
(out/'receipts/public-downloads.json').write_text(json.dumps(receipts,indent=2)+'\n')
print('Verified public Git blobs:',len(receipts))

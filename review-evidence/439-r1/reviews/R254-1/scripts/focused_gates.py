import json, os, pathlib, subprocess, sys, time
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve();logs=out/'receipts/gates';logs.mkdir(exist_ok=True)
commands=[['python3','-B','scripts/docs_check.py'],['python3','-B','scripts/gen_toc.py','--check'],['python3','-B','scripts/gen_toc.py','--verify-anchors'],['python3','-B','scripts/check_py_idiom.py'],['python3','-B','scripts/check_em_dash.py','--base','483a133ed08867ea0d300d2b4a027b5b48a4282f'],['git','diff','--check','483a133ed08867ea0d300d2b4a027b5b48a4282f','f01f237d4b48c7b1ed59c80aca51430901791624']]
results=[]
for i,cmd in enumerate(commands,1):
 argv=['rtk','proxy',*cmd];start=time.time();r=subprocess.run(argv,cwd=root,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),timeout=120)
 (logs/f'{i}.stdout').write_bytes(r.stdout);(logs/f'{i}.stderr').write_bytes(r.stderr)
 results.append({'argv':argv,'exit':r.returncode,'seconds':round(time.time()-start,3),'stdout':f'receipts/gates/{i}.stdout','stderr':f'receipts/gates/{i}.stderr'})
(out/'receipts/gate-results.json').write_text(json.dumps(results,indent=2)+'\n')
assert all(r['exit']==0 for r in results),results
print('PASS: six focused docs, idiom and diff checks')

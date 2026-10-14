import pathlib,sys,os,shutil,json,subprocess,yaml
root=pathlib.Path(sys.argv[1]);p=pathlib.Path(__file__).resolve().parent
os.environ['CI_IMAGE_SHFMT']=str(p/'scratch/shfmt');d=p/'scratch/drift';d.mkdir(parents=True,exist_ok=True)
for n in ('sources.lock.json','command-table.json','syntax-census.json'):
 out=d/'ci/image'/n;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/'ci/image'/n,out)
w=d/'.github/workflows/probe.yml';w.parent.mkdir(parents=True,exist_ok=True)
w.write_text(yaml.safe_dump({'jobs':{'check':{'steps':[{'run':'python3 -m pip install probe==1.0'}]}}}))
python=str(p/'scratch/reference/bin/python3');script=str(root/'scripts/ci_tool_inventory.py')
def run(mode):
 r=subprocess.run([python,script,'--root',str(d),mode],text=True,capture_output=True);return {'rc':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
results={'baseline_write':run('--write'),'baseline_check':run('--check')};inventory=d/'ci/image/tool-inventory.json';original=inventory.read_text();v=json.loads(original)
v['tools']=[];inventory.write_text(json.dumps(v));results['missing']=run('--check')
v=json.loads(original);v['tools'].append({'tool':'unused','kind':'pip','pin':'1.0'});inventory.write_text(json.dumps(v));results['orphan']=run('--check')
inventory.write_text(original);w.write_text(w.read_text().replace('probe==1.0','probe==2.0'));results['pin_change']=run('--check')
assert all(results[k]['rc']==2 for k in ('missing','orphan','pin_change'))
(p/'drift-controls.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))

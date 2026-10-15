#!/usr/bin/env python3
import contextlib,io,json,os,pathlib,sys,tempfile
root=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(__file__).resolve().parent
os.environ['CI_IMAGE_SHFMT']=str(out/'scratch/shfmt');sys.path.insert(0,str(root/'scripts'))
import ci_tool_inventory as inventory
from ci_inventory_patterns_selftest import Fixture
results=[]
with tempfile.TemporaryDirectory(dir=out/'scratch',prefix='drift-') as tmp:
 f=Fixture(pathlib.Path(tmp));f.run('python3 -m pip install example==1.0');f.check('clean fixture')
 target=f.root/inventory.OUTPUT;clean=json.loads(target.read_text())
 for name in ['missing','orphan','new-workflow-tool']:
  altered=json.loads(json.dumps(clean));f.run('python3 -m pip install example==1.0')
  if name=='missing':altered['tools']=[]
  elif name=='orphan':altered['tools'].append({'tool':'unused','pin':'1'})
  else:f.run('python3 -m pip install example==1.0 another==1.0')
  target.write_text(inventory.serialized(altered));sys.argv=['inventory','--root',str(f.root),'--check'];buf=io.StringIO()
  with contextlib.redirect_stdout(buf),contextlib.redirect_stderr(buf):rc=inventory.main()
  results.append({'name':name,'rc':rc,'output':buf.getvalue()});assert rc==2
text=json.dumps(results,indent=2)+'\n';(out/'drift-controls.json').write_text(text);print(text)

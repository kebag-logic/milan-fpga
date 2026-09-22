import subprocess,sys,io,tarfile,json,hashlib,ast
from pathlib import Path
out=Path(__file__).parent;checkout=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
revs={'head':'a769d9dbc937fb324c4726e60dee5b2f7ad349e3','base':'88e9276b2a220c716f64a843f7e1eb8f9265e896','historical-good':'b7d0bbcd','historical-bad':'da71309c'}
def git(*args):return subprocess.check_output(['rtk','proxy','git','-C',str(checkout),*args])
for label,rev in revs.items():
 dst=out/'scratch'/label;dst.mkdir(parents=True,exist_ok=True)
 tarfile.open(fileobj=io.BytesIO(git('archive',rev))).extractall(dst,filter='data')
patch=git('diff','--binary',revs['base'],revs['head']);assert patch==git('diff','--binary','ec34fcde','1576f089')
(out/'issue-delta.patch').write_bytes(patch)
checks={'issue_delta_equal':True,'patch_sha256':hashlib.sha256(patch).hexdigest()}
for name in ['aem_maps.py','gen_aem_store.py']:
 def normalize(path):
  module=ast.parse(path.read_text());nodes=[]
  for n in module.body:
   if isinstance(n,ast.Expr) and isinstance(n.value,ast.Constant) and isinstance(n.value.value,str):continue
   if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and (n.name.startswith('_selftest') or n.name in ['_map_fixture','self_test']):continue
   if isinstance(n,ast.ImportFrom) and n.module=='collections.abc' and name=='gen_aem_store.py':continue
   if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='KNOWN_MAP_DEVIATIONS' for t in n.targets):continue
   nodes.append(ast.dump(n,include_attributes=False))
  return nodes
 checks[name]=normalize(out/'scratch/base/avdecc'/name)==normalize(out/'scratch/head/avdecc'/name);assert checks[name]
for path in ['protocol-processor','gptp-processor','avdecc/aem_specs.py','avdecc/aem_assemble.py','avdecc/aem_descriptors.py','configs','hdl','sw/builder']:
 checks[path]=git('rev-parse',revs['head']+':'+path)==git('rev-parse',revs['base']+':'+path);assert checks[path]
(out/'static-equivalence.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Four snapshots prepared; full issue delta equal; production AST and shipping input trees unchanged')

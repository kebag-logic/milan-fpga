import ast,json,subprocess,sys,hashlib
from pathlib import Path
OUT=Path(__file__).resolve().parent; REPO=Path('$VALIDATION_STORAGE/reviews/r237-437-r1')
BASE='88e9276b2a220c716f64a843f7e1eb8f9265e896';HEAD='65df1df50a80cd5f540a93d8f0cfabc97da3da75'
def git(*args):return subprocess.check_output(['rtk','proxy','git','-C',str(REPO),*args])
def compare(name,rows):
 inp=OUT/(name+'-inputs.json');inp.write_text(json.dumps(rows,indent=2))
 for label in ['base','head']:
  subprocess.run(['rtk','proxy','python3','-B',str(OUT/'classify.py'),str(OUT/'scratch'/label),str(inp),str(OUT/(name+'-'+label+'.json'))],check=True)
 a=json.loads((OUT/(name+'-base.json')).read_text());b=json.loads((OUT/(name+'-head.json')).read_text())
 differences=[k for k in a if a[k]!=b[k]]
 return {'population':len(rows),'differences':differences,'base_sha256':hashlib.sha256((OUT/(name+'-base.json')).read_bytes()).hexdigest(),'head_sha256':hashlib.sha256((OUT/(name+'-head.json')).read_bytes()).hexdigest()}
summary={}
for label,rev in [('original-corpus',BASE),('updated-corpus',HEAD)]:
 paths=git('ls-tree','-r','--name-only',rev).decode().splitlines()
 rows=[{'id':p,'path':p,'page':git('show',rev+':'+p).decode().replace('\r\n','\n').replace('\r','\n')} for p in paths if p.endswith('.md')]
 summary[label]=compare(label,rows)
sys.dont_write_bytecode=True;sys.path.insert(0,str(OUT/'scratch/base'));import gen_toc_cases as c;import gen_toc_closer_cases as d
families={n:getattr(c,n+'_arms')() for n in ['walk','tag','guard','heading','predecessor','provenance','refusal']};families['I440']=d.closer_arms()
rows=[{'id':str(i)+' '+name,'page':page} for i,(name,page,_) in enumerate([arm for group in families.values() for arm in group])]
summary['prior-arms']=compare('prior-arms',rows)
summary['families']={k:len(v) for k,v in families.items()}
summary['closer-byte-identical']=git('show',BASE+':scripts/gen_toc_closer_cases.py')==git('show',HEAD+':scripts/gen_toc_closer_cases.py')
def funcs(rev):
 tree=ast.parse(git('show',rev+':scripts/check_em_dash.py'))
 return {n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name!='selftest'}
summary['em-dash-all-nonselftest-functions-classes-identical']=funcs(BASE)==funcs(HEAD)
summary['changed-objects']=git('diff','--raw',BASE,HEAD).decode()
(OUT/'preservation-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
assert all(not summary[x]['differences'] for x in ['original-corpus','updated-corpus','prior-arms'])

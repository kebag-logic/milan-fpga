import sys,json,types,hashlib
from pathlib import Path
sys.path.insert(0,sys.argv[1])
import gen_toc as g, gen_toc_cases as c, gen_toc_closer_cases as k

def fingerprint(v):
 if isinstance(v,types.CodeType):return {a:fingerprint(getattr(v,a)) for a in ("co_code","co_consts","co_names","co_varnames","co_freevars","co_argcount")}
 if isinstance(v,types.FunctionType):return dict(code=fingerprint(v.__code__),defaults=fingerprint(v.__defaults__),closure=[fingerprint(x.cell_contents) for x in v.__closure__ or ()])
 if isinstance(v,bytes):return v.hex()
 if isinstance(v,(tuple,list)):return [fingerprint(x) for x in v]
 if isinstance(v,(int,str,bool,type(None),float)):return v
 return str(type(v))
rows=[]
for fam in g.ARM_FAMILIES:
 arms=k.closer_arms() if fam=="I440" else getattr(c,fam+"_arms")()
 for name,page,holds in arms:
  rows.append(dict(family=fam,name=name,page=page,holds=fingerprint(holds)))
print(json.dumps(dict(arms=rows,labels=k._label_rows()),indent=2))

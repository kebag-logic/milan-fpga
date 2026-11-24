from pathlib import Path
import ast,hashlib,json,re,subprocess
root=Path.cwd();out=Path('$VALIDATION_STORAGE/artysplit-a829/r4/refined')
base='4a89ddcdb18bdfaafc9e999daeee1e7ba56274a2'
old=lambda p:subprocess.check_output(['git','show',base+':'+p],text=True)
p='sw/firmware/ctrl/loop/ctrl_loop.h'
pattern=re.compile(r'^(#(?:el)?if CTRL_LOOP_SHAPE\(([^)]+)\)[^\n]*\n.*?)(?=^#(?:elif|else))',re.M|re.S)
a={k:v for v,k in pattern.findall(old(p))};b={k:v for v,k in pattern.findall((root/p).read_text())}
rows=[dict(shape=k,identical=v==b[k],sha256=hashlib.sha256(v.encode()).hexdigest()) for k,v in a.items()]
assert len(rows)==4 and all(x['identical'] for x in rows)
checks=[]
for f,names in [('load_grade.py',['STATED_US','STATED_US_DONOR']),('poll_grade.py',['ONE','TWO','EIGHT_ONE']),('rows_grade.py',['ROW_COSTS']),('rows_tiers.py',['DATAPATH_US','LONG_RECORD_US']),('edit_rows.py',['PACED'])]:
 p='tb/verilator/ctrl_service_budget/'+f
 def assigns(s):
  return {t.id:n.value for n in ast.parse(s).body if isinstance(n,ast.Assign) for t in n.targets if isinstance(t,ast.Name) and t.id in names}
 old_text,new_text=old(p),(root/p).read_text()
 aa,bb=assigns(old_text),assigns(new_text)
 for name,v in aa.items():
  new=bb[name]
  if isinstance(v,ast.Dict):
   newer={ast.literal_eval(k):ast.dump(x,include_attributes=False) for k,x in zip(new.keys,new.values)}
   assert all(newer[ast.literal_eval(k)]==ast.dump(x,include_attributes=False) for k,x in zip(v.keys,v.values)),(f,name)
   source_rows={ast.literal_eval(k):ast.get_source_segment(new_text,x) for k,x in zip(new.keys,new.values)}
   assert all(source_rows[ast.literal_eval(k)]==ast.get_source_segment(old_text,x)
              for k,x in zip(v.keys,v.values)),(f,name,'existing row source bytes')
  else:assert ast.dump(v,include_attributes=False)==ast.dump(new,include_attributes=False),(f,name)
 checks.append(dict(file=p,unchanged=names))
report=dict(status='PASS',baseline=base,existing_shape_blocks=rows,existing_cost_tables=checks,
            cost_row_proof='Every existing dictionary value retains its exact source bytes as well as its syntax tree')
(out/'old-row-identity.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS: four original shape blocks byte-identical; existing cost rows unchanged.')

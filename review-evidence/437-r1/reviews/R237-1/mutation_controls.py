import ast,json,shutil,subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
OUT=Path(__file__).resolve().parent
parsed=ast.parse((OUT/'public-packet/author/mutations.py').read_text())
mutants=ast.literal_eval(next(n.value for n in parsed.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='MUTANTS' for t in n.targets)))
expected=['two spaces','two spaces','one space outside item','two spaces','padding outside','tab padding columns','code padding uses one','four padding columns','empty item ends at blank','empty item gains content','empty item ignores padding','nested item retains outer column','sibling replaces column','fresh dedented paragraph ends item','lazy line retains item','fenced marker is inert','noninterrupting ordinal is no item']
def run(args):
 (name,old,new),named=args;dest=OUT/'scratch/mutants'/name;shutil.copytree(OUT/'scratch/head',dest,dirs_exist_ok=True)
 path=dest/'gen_toc.py';src=path.read_text();assert src.count(old)==1
 path.write_text(src.replace(old,new));row={'mutation':name,'replace':old,'with':new,'required_named_arm':named,'checks':[]}
 for gate in ['gen_toc.py','check_em_dash.py']:
  cmd=['rtk','proxy','python3','-B',str(dest/gate),'--selftest'];p=subprocess.run(cmd,capture_output=True,text=True,timeout=45);log=p.stdout+p.stderr
  (dest/(gate+'.log')).write_text(log)
  hit='[I437 '+named+']' in log
  row['checks'].append({'gate':gate,'exit':p.returncode,'named_defect_detected':hit,'log':str((dest/(gate+'.log')).relative_to(OUT)),'failures':[l for l in log.splitlines() if 'I437' in l]})
  row['checks'][-1]['exit_expected'] = p.returncode==(1 if gate=='gen_toc.py' else 2)
 return row
with ThreadPoolExecutor(max_workers=2) as pool:rows=list(pool.map(run,zip(mutants,expected)))
(OUT/'mutation-results.json').write_text(json.dumps(rows,indent=2));print(json.dumps([{'mutation':r['mutation'],'required_named_arm':r['required_named_arm'],'checks':[{k:c[k] for k in ['gate','exit','named_defect_detected']} for c in r['checks']]} for r in rows],indent=2))

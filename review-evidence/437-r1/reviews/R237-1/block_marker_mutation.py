import json,shutil,subprocess
from pathlib import Path
OUT=Path(__file__).resolve().parent;dest=OUT/'scratch/block-marker-only';shutil.copytree(OUT/'scratch/head',dest,dirs_exist_ok=True)
p=dest/'gen_toc.py';src=p.read_text();old='label == TEXT and after == HELD';new='label != TEXT or after == HELD';assert src.count(old)==1;p.write_text(src.replace(old,new))
checks=[]
for gate in ['gen_toc.py','check_em_dash.py']:
 cmd=['rtk','proxy','python3','-B',str(dest/gate),'--selftest'];r=subprocess.run(cmd,capture_output=True,text=True)
 (OUT/('block-marker-only-'+gate+'.log')).write_text(r.stdout+r.stderr);checks.append({'gate':gate,'exit':r.returncode,'output':r.stdout+r.stderr})
rows=[{'id':'fenced-marker-indented-closer','page':'```\n- fake item\n  ```\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n'}, {'id':'comment-marker-indented-closer','page':'<!--\n- fake item\n  -->\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n'}, {'id':'HTML-marker-indented-closer','page':'<div>\n- fake item\n  </div>\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n'}]
(OUT/'block-marker-inputs.json').write_text(json.dumps(rows,indent=2))
for label,path in [('head',OUT/'scratch/head'),('mutant',dest)]:
 subprocess.run(['rtk','proxy','python3','-B',str(OUT/'classify.py'),str(path),str(OUT/'block-marker-inputs.json'),str(OUT/('block-marker-'+label+'.json'))],check=True)
summary={'replace':old,'with':new,'shipped_selftests':checks,'controls':{}}
for label in ['head','mutant']:
 data=json.loads((OUT/('block-marker-'+label+'.json')).read_text());summary['controls'][label]={k:[h[1] for h in v['headings']] for k,v in data.items()}
(OUT/'block-marker-summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))

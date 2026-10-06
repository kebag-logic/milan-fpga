#!/usr/bin/env python3
"""Measure only the touched notification module at its count-one default."""
import argparse, concurrent.futures, json, pathlib, subprocess
p=argparse.ArgumentParser(); p.add_argument('--repo',required=True); a=p.parse_args()
packet=pathlib.Path(__file__).resolve().parents[1]; logs=packet/'receipts/notify-stats'; logs.mkdir(parents=True,exist_ok=True)
def measure(item):
 name,rev=item; work=packet/'scratch'/('stats-'+name); work.mkdir(exist_ok=True)
 files=[]
 for src in ['hdl/common/pp_pkg.sv','hdl/aecp/KL_aecp_notify.sv']:
  path=work/pathlib.Path(src).name; path.write_bytes(subprocess.check_output(['git','show',rev+':'+src],cwd=a.repo)); files.append(str(path))
 with (work/'all.v').open('w') as out, (logs/(name+'-convert.log')).open('w') as err: r=subprocess.run(['sv2v',*files],stdout=out,stderr=err)
 assert r.returncode==0
 cmd=['yosys','-p',f'read_verilog {work}/all.v; hierarchy -check -top KL_aecp_notify; proc; opt_clean; tee -o {logs}/{name}.json stat -json']
 with (logs/(name+'.log')).open('w') as out: r=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT)
 (logs/(name+'.rc')).write_text(str(r.returncode)+'\n'); assert r.returncode==0
 return name,json.loads((logs/(name+'.json')).read_text())
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool: data=dict(pool.map(measure,[('base','e6a759deeb70b2d7de1b3336e9f080bc85d4f0a8'),('head','cb730a2f9dd7e4f60a03a38d4b47b569e68da8df')]))
b=data['base']['modules']['\\KL_aecp_notify']; h=data['head']['modules']['\\KL_aecp_notify']; changes={k:[b.get(k),h.get(k)] for k in sorted(b.keys()|h.keys()) if b.get(k)!=h.get(k)}
result=dict(cell_types_identical=b['num_cells_by_type']==h['num_cells_by_type'],changes=changes)
(logs/'comparison.json').write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result)); assert result['cell_types_identical']

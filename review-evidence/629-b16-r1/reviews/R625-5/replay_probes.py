#!/usr/bin/env python3
"""Replay byte-identical public review probes concurrently, without touching the source tree."""
import concurrent.futures,hashlib,json,pathlib,subprocess,sys
repo,packet,out=map(lambda s:pathlib.Path(s).resolve(),sys.argv[1:4])
names=[('r624-4','probe_escape_forms.py','5c2dbc691e469d236227bc90d4d131ad1fc116f0b002813c02beef2374ae3c26'),('r625-4','probe_coverage.py','e8749cbecfe73ef6f07261d1416122094d51745954a62fa6851d4e0521dfd0fb'),('r625-3','probe_figure_coverage.py','f4c4d91bdfea9b6428e3e5a587ba87577003cc9e67ba08c852149d2ec3cddb32')]
def run(item):
 n,f,h=item; src=packet/'tools/review-probes'/f
 assert hashlib.sha256(src.read_bytes()).hexdigest()==h
 d=out/'scratch'/n;(d/'receipts').mkdir(parents=True,exist_ok=True)
 args=[repo,packet,d/'scratch',d/'out.json'] if n=='r624-4' else [repo,packet,d]
 p=subprocess.run([sys.executable,'-I',str(src),*map(str,args)],capture_output=True,text=True,timeout=550)
 file=d/({'r624-4':'out.json','r625-4':'coverage-probes.json','r625-3':'receipts/figure-coverage-probes.json'}[n])
 data=file.read_text()
 log=p.stdout+p.stderr
 for a,b in [(str(packet),'<packet>'),(str(out),'<review>'),(str(repo),'<repo>')]:
  data=data.replace(a,b);log=log.replace(a,b)
 (out/f'receipts/{n}-probes.json').write_text(data)
 (out/f'receipts/{n}-probes.log').write_text(log)
 (out/f'receipts/{n}-probes.rc').write_text(str(p.returncode)+'\n')
 return {'name':n,'sha256':h,'rc':p.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: result=list(pool.map(run,names))
(out/'receipts/prior-probe-reruns.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

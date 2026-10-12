#!/usr/bin/env python3
"""Run the public evidence check and controls concurrently; all subprocesses are joined."""
import concurrent.futures, json, pathlib, subprocess, sys
repo, packet, out = map(pathlib.Path, sys.argv[1:4])
repo, packet, out = repo.resolve(), packet.resolve(), out.resolve()
(out/'receipts').mkdir(parents=True,exist_ok=True)
(out/'scratch').mkdir(exist_ok=True)
page=repo/'docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md'
check=packet/'tools/check_b16_figures.py'
commands={'figures':[check,page,packet,out/'receipts/figures-rows.tsv',out/'receipts/figures-coverage.tsv','--repo',repo]}
for n in (3,4,5):
 commands[f'r{n}-controls']=[packet/f'tools/r{n}_check_controls.py',check,page,packet,out/f'scratch/r{n}-controls',out/f'receipts/r{n}-controls.json']
commands['self-probes']=[packet/'tools/r5_self_probes.py',check,page,packet,out/'scratch/self-probes',out/'receipts/self-probes.json']
def run(item):
 name,args=item
 p=subprocess.run([sys.executable,'-I',*map(str,args)],capture_output=True,text=True,timeout=550)
 t=p.stdout+p.stderr
 for src,label in [(str(packet),'<packet>'),(str(out),'<review>'),(str(repo),'<repo>')]: t=t.replace(src,label)
 (out/f'receipts/{name}.log').write_text(t)
 (out/f'receipts/{name}.rc').write_text(str(p.returncode)+'\n')
 return dict(name=name,rc=p.returncode)
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: result=list(pool.map(run,commands.items()))
(out/'receipts/checks.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))

sys.exit(0 if all(x["rc"]==0 for x in result) else 1)

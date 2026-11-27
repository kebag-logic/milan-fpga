"""Run one census case of a built variant as the window runner does, into OUT; print its log path."""
import json,subprocess,sys
from pathlib import Path
root=Path.cwd(); sys.path.insert(0,str(root/'tb/verilator/ctrl_service_budget'))
import build,run,scenario,bind_save,rows_tiers
directory,name,out=Path(sys.argv[1]),sys.argv[2],Path(sys.argv[3])
spec=build.reused(directory); spec['measurement_pace_ms']=rows_tiers.built_constants(root,'arty-1x1')[-1]
g=next(g for g in run.all_groups(scenario.point('arty-1x1',spec),spec) if g.name==name)
out.mkdir(parents=True,exist_ok=True); script=out/(name+'.txt'); script.write_text(g.script()); log=out/(name+'.log')
env=bind_save.environment(g.save,run.journal_of(out,g))
with log.open('w') as sink:
    rc=subprocess.run([str(directory/'native/Vsim'),str(script),spec.get('flash_image') or '-'],cwd=directory/'gateware',stdout=sink,stderr=subprocess.STDOUT,env=env).returncode
graded,refusals,misses=run.graded([g],[log],spec,out)
print(json.dumps(dict(rc=rc,refusals=refusals,misses=misses,late=run.notice_misses(graded,1),stated=run.stated_misses(graded))))

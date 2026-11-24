import sys,json,re,shutil
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"tb/verilator/ctrl_service_budget"))
import run,scenario
root=Path("$VALIDATION_STORAGE/artysplit-a829/r4"); allrows=[]
for name in ("arm-a","arm-b","arm-a-full","arm-every"):
 d=root/name;spec=json.loads((d/"build.json").read_text());groups=run.all_groups(scenario.point("arty-1x1",spec),spec)
 done=[];logs=[];out=d/"monitor";out.mkdir(exist_ok=True)
 for g in groups:
  log=d/"results"/(g.name+".log")
  if not log.exists():continue
  with log.open("rb") as f:
   f.seek(max(0,log.stat().st_size-4000));tail=f.read().decode(errors="replace")
  if "RESULT: PASS" not in tail:continue
  done.append(g);logs.append(log)
  j=d/"results"/(g.name+".journal")
  if j.exists():shutil.copyfile(j,out/j.name)
 results,refusals,misses=run.graded(done,logs,spec,out)
 shares=run.share_misses(results)
 late=run.save_misses(results)+run.burst_misses(results)+run.notice_misses(results,spec["interfaces"])
 row=dict(arm=name,groups=len(results),refusals=refusals,misses=misses,share=shares,late=late,
          worst_pass_cycles=max([g["passes"]["worst"]["cycles"] for g in results] or [0]))
 allrows.append(row);print(json.dumps(row),flush=True)
(root/"monitor.json").write_text(json.dumps(allrows,indent=2)+"\n")

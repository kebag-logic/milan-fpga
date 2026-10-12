#!/usr/bin/env python3
"""Run focused offline controls concurrently. Usage: run_checks.py REPO AUTHOR_PACKET OUTPUT"""
import concurrent.futures, json, subprocess, sys
from pathlib import Path
repo, packet, out = map(lambda x: Path(x).resolve(), sys.argv[1:])
scratch=out/"scratch"/"checks"; receipts=out/"receipts"
scratch.mkdir(parents=True,exist_ok=True); receipts.mkdir(exist_ok=True)
page=repo/"docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
check=packet/"tools/check_b16_figures.py"
tasks={}
for n in (3,4,5,6):
 tasks[f"r{n}-controls"]=[packet/f"tools/r{n}_check_controls.py",check,page,packet,scratch/f"r{n}-controls",receipts/f"r{n}-controls.json"]
probes=packet/"tools/review-probes"
for name,script,args in [
 ("r624-4","probe_escape_forms.py",lambda d:[repo,packet,d/"scratch",d/"result.json"]),
 ("r625-4","probe_coverage.py",lambda d:[repo,packet,d]),
 ("r625-3","probe_figure_coverage.py",lambda d:[repo,packet,d]),
 ("r624-5-row3200","probe_row3200.py",lambda d:[repo,packet,d/"scratch",d/"result.json"]),
 ("r624-5-escapes","probe_r624_5_escapes.py",lambda d:[repo,packet,d/"scratch",d/"result.json"]),
 ("r625-5-comment","probe_comment_separator.py",lambda d:[repo,packet,d])]:
 d=scratch/name; (d/"receipts").mkdir(parents=True,exist_ok=True); (d/"scratch").mkdir(exist_ok=True)
 tasks[name]=[probes/script,*args(d)]
def run(item):
 name,args=item
 with (receipts/f"{name}.log").open("w") as f:
  p=subprocess.run([sys.executable,"-I",*map(str,args)],stdout=f,stderr=subprocess.STDOUT,timeout=540)
 (receipts/f"{name}.rc").write_text(str(p.returncode)+"\n")
 return name,p.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
 results=dict(ex.map(run,tasks.items()))
for name in tasks:
 if name.startswith("r6-controls"): continue
 d=scratch/name
 candidates=[d/"result.json",d/"coverage-probes.json",d/"receipts/figure-coverage-probes.json",d/"receipts/comment-probe.json"]
 for p in candidates:
  if p.exists(): (receipts/f"{name}.json").write_bytes(p.read_bytes())
(receipts/"focused-status.json").write_text(json.dumps(results,indent=2)+"\n")
print(json.dumps(results,indent=2))

import concurrent.futures,json,subprocess,sys,os
from pathlib import Path
r=Path(__file__).resolve().parent
commands=json.loads(os.path.expandvars((r/"docs-commands.json").read_text()))
def run(pair):
 index,item=pair
 return subprocess.run([sys.executable,str(r/"run.py"),f"docs-{index:02d}",*item["command"]]).returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(run,enumerate(commands)))
raise SystemExit(any(results))

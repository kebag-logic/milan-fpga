#!/usr/bin/env python3
import concurrent.futures,os,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]).resolve();packet=Path(sys.argv[2]).resolve()
env={**os.environ,"TMPDIR":str(packet/"scratch"),"PYTHONDONTWRITEBYTECODE":"1"}
commands={
"coverage":[sys.executable,"-B",str(root/"sw/firmware/gtest/fw_coverage.py"),"--check","--jobs","8","--keep",str(packet/"scratch/coverage")],
"sample":[sys.executable,"-B",str(packet/"scripts/sample_mutations.py"),str(root),str(packet)]}
def run(item):
 name,argv=item
 with (packet/"receipts"/(name+".log")).open("w") as log:
  log.write("COMMAND: "+" ".join(argv).replace(str(root),"<checkout>").replace(str(packet),"<packet>")+"\n");log.flush()
  rc=subprocess.run(argv,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
 (packet/"receipts"/(name+".rc")).write_text(str(rc)+"\n")
 print(name,rc,flush=True);return rc
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:rcs=list(pool.map(run,commands.items()))
sys.exit(int(any(rcs)))

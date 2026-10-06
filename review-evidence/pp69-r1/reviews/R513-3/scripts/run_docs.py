#!/usr/bin/env python3
"""Read-only documentation gates in the checkout; fixtures go under scratch."""
import json,pathlib,subprocess,sys,os
src=pathlib.Path(sys.argv[1]).resolve();out=pathlib.Path(sys.argv[2]).resolve()
env=os.environ.copy();env.update(TMPDIR=str(out/"scratch/tmp"),PYTHONDONTWRITEBYTECODE="1")
args=["make","-j16","links","params","ids","figures","modmatrix"]
with (out/"receipts/docs.log").open("w") as log:
 log.write("command: "+json.dumps(args)+"\n");log.flush()
 rc=subprocess.run(args,cwd=src,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
(out/"receipts/docs.rc").write_text(str(rc)+"\n")
raise SystemExit(rc)

#!/usr/bin/env python3
import pathlib,subprocess,sys,os
p=pathlib.Path(__file__).resolve().parent;repo=pathlib.Path(sys.argv[1]).resolve();dest=p/'scratch/docs-source'
if not dest.exists():
 subprocess.run(['git','clone','--shared','--no-checkout',str(repo),str(dest)],check=True)
 subprocess.run(['git','checkout','--detach','b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad'],cwd=dest,check=True)
env=os.environ.copy();env['TMPDIR']=str(p/'scratch/tmp')
with (p/'receipts/docs-check-checkout.log').open('w') as log:
 rc=subprocess.run(['make','-j16','check'],cwd=dest,env=env,stdout=log,stderr=subprocess.STDOUT).returncode
(p/'receipts/docs-check-checkout.rc').write_text(str(rc)+'\n')
raise SystemExit(rc)

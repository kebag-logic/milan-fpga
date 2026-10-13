#!/usr/bin/env python3
"""Prepare the exact-head offline fixture source under packet scratch only."""
import io,pathlib,subprocess,sys,tarfile
p=pathlib.Path(__file__).resolve().parent.parent;repo=pathlib.Path(sys.argv[1]).resolve()
head=subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
assert head=='73b8dcd667aa5bf1254e828dd1dd7217c8a103ce'
(p/'scratch/tmp').mkdir(parents=True,exist_ok=True);(p/'receipts').mkdir(exist_ok=True)
out=p/'scratch/pristine';out.mkdir(parents=True,exist_ok=True)
archive=subprocess.check_output(['git','-C',str(repo),'archive',head,'scripts','.github','docs','AGENTS.md','CONTRIBUTING.md','REQUIREMENTS.md','.gitmodules'])
with tarfile.open(fileobj=io.BytesIO(archive)) as tf:tf.extractall(out,filter='data')
(p/'scripts/sandbox.sh').chmod(0o755)
print('Exact-head fixture source prepared under packet scratch.')

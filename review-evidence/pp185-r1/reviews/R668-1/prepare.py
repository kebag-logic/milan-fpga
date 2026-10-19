#!/usr/bin/env python3
"""Prepare disposable exact-head sources without modifying the supplied checkout."""
import io,os,pathlib,subprocess,sys,tarfile
p=pathlib.Path(__file__).resolve().parent
repo=pathlib.Path(sys.argv[1]).resolve()
head='b0f6f9c3b5107c49e2323b9009d3c9b56ade51ad'
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()==head
(p/'receipts').mkdir(exist_ok=True); (p/'scratch/tmp').mkdir(parents=True,exist_ok=True)
dest=p/'scratch/source'; dest.mkdir(parents=True,exist_ok=True)
archive=subprocess.check_output(['git','archive',head],cwd=repo)
with tarfile.open(fileobj=io.BytesIO(archive)) as t: t.extractall(dest,filter='data')
sim=os.environ.get('REVIEW_SIM','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
v=subprocess.check_output([sim,'--version'],text=True)
assert '5.050' in v,v
(p/'receipts/simulator-identity.txt').write_text(v)
print('Prepared exact-head archive and verified simulator identity.')

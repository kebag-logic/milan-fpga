#!/usr/bin/env python3
"""Export the exact reviewed tree only into packet scratch, without changing the checkout."""
import io,pathlib,subprocess,sys,tarfile
packet=pathlib.Path(__file__).resolve().parent.parent
root=pathlib.Path(sys.argv[1]).resolve()
head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
assert head=='b341e875d87c6aa2be355bad17f373782517f723',head
target=packet/'scratch/pristine'
assert not target.exists(), 'Use a fresh packet scratch directory for reproduction'
target.mkdir(parents=True)
raw=subprocess.check_output(['git','-C',str(root),'archive',head])
with tarfile.open(fileobj=io.BytesIO(raw)) as archive:archive.extractall(target,filter='data')
print('prepared exact-head scratch/pristine')

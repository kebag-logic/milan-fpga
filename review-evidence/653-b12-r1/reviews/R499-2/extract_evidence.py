"""Extract only public operator evidence, never other reviewers' reports.

Usage: python3 -B extract_evidence.py CHECKOUT REVIEW_OUTPUT
The two public commits must already exist in the checkout's object store.
Disposable copies go exclusively below REVIEW_OUTPUT/scratch.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

repo, output = map(Path, sys.argv[1:])
for ref, prefix, dest in [
    ('9649a107657bdc77d1c47d7ce735e6a282394235','review-evidence/653-b12-r1/author/','public-r1/author'),
    ('871fc1ae68e2fcdfa7abb134956973b455c8bee5','review-evidence/653-b12-r1/author-r2/','public-r2'),
]:
    paths = subprocess.check_output(['git','-C',str(repo),'ls-tree','-r','--name-only',ref,prefix],text=True).splitlines()
    for path in paths:
        rel=Path(path.removeprefix(prefix))
        assert not rel.is_absolute() and '..' not in rel.parts
        target=output/'scratch'/dest/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(subprocess.check_output(['git','-C',str(repo),'show',ref+':'+path]))
    print(json.dumps(dict(commit=ref,files=len(paths),destination='scratch/'+dest)))

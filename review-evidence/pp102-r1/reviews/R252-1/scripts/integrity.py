#!/usr/bin/env python3
"""Compare every tracked byte/kind/mode and index entry with immutable HEAD."""
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
from collect import BASE, CHECKOUT, HEAD, OUT, blob_hash, capture

def verify(label):
    replace_refs = capture(f'raw/{label}-replace-refs.txt',['git','--no-replace-objects','for-each-ref','refs/replace'])
    assert not replace_refs, 'Replacement refs must not alter immutable identity'
    identity = capture(f'raw/{label}-identity.txt', ['git','--no-replace-objects','rev-parse','HEAD','HEAD^{tree}','HEAD^']).decode().splitlines()
    assert identity == [HEAD,'0547903adc17449dfb4f0c2610a23e6adb4ff6a2',BASE], identity
    tree = capture(f'raw/{label}-tree.raw',['git','--no-replace-objects','ls-tree','-rz',HEAD])
    index = capture(f'raw/{label}-index.raw',['git','ls-files','--stage','-z'])
    expected_index = {}
    for item in index.split(b'\0'):
        if item:
            meta, path = item.split(b'\t',1)
            mode, oid, stage = meta.decode().split()
            assert stage == '0'
            expected_index[path.decode()] = (mode, oid)
    records, gitlinks = [], []
    for item in tree.split(b'\0'):
        if not item: continue
        meta, name = item.split(b'\t',1)
        mode, kind, oid = meta.decode().split()
        rel = name.decode(); path = CHECKOUT/rel
        assert expected_index.pop(rel) == (mode,oid), rel
        if mode == '160000':
            gitlinks.append({'path':rel,'oid':oid})
            actual = capture(f'raw/{label}-gitlink-{len(gitlinks)}.txt',['git','-C',str(path),'rev-parse','HEAD']).decode().strip()
            assert actual == oid
            continue
        st = path.lstat()
        if mode == '120000':
            assert stat.S_ISLNK(st.st_mode),rel
            b = os.fsencode(os.readlink(path)); actual_mode = mode
        else:
            assert stat.S_ISREG(st.st_mode),rel
            b = path.read_bytes()
            actual_mode = '100755' if st.st_mode & 0o111 else '100644'
        assert actual_mode == mode and blob_hash(b) == oid,rel
        records.append({'path':rel,'kind':kind,'mode':mode,'git_blob':oid,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'index_matches':True,'worktree_matches':True})
    assert not expected_index
    status = capture(f'raw/{label}-status.txt',['git','status','--porcelain=v2','--branch']).decode()
    assert status == f'# branch.oid {HEAD}\n# branch.head (detached)\n',status
    flags = capture(f'raw/{label}-index-flags.txt',['git','ls-files','-v']).decode().splitlines()
    assert all(line.startswith('H ') for line in flags), 'Index has hidden/sparse/unmerged entries'
    capture(f'raw/{label}-ignored.txt',['git','status','--short','--ignored'])
    capture(f'raw/{label}-diff-check.txt',['git','diff','--check',BASE,HEAD])
    result = {'head':HEAD,'tree':identity[1],'base':BASE,'tracked_files':len(records),'gitlinks':gitlinks,'all_match':True,'files':records}
    (OUT/f'raw/{label}-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
    print(label,len(records),'tracked files: bytes/kind/mode/index PASS; gitlinks:',gitlinks)

if __name__ == '__main__': verify(sys.argv[1])

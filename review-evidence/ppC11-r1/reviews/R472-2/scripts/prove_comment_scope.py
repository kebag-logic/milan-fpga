#!/usr/bin/env python3
"""Verify all C11 HDL/test source changes are comment-only."""
import argparse
import hashlib
from pathlib import Path
import re
import subprocess

def main():
    p=argparse.ArgumentParser()
    p.add_argument('repo',type=Path)
    p.add_argument('scratch',type=Path)
    p.add_argument('simulator',type=Path)
    a=p.parse_args()
    repo=a.repo.resolve(); dest=a.scratch.resolve()/'preprocess';dest.mkdir(exist_ok=True)
    def git(*args):
        return subprocess.check_output(['git','-C',str(repo),*args])
    codefiles=[x for x in git('diff','--name-only','ead80360','HEAD','--','hdl','tb').decode().splitlines() if Path(x).suffix in ('.sv','.cpp')]
    assert len(codefiles)==4,codefiles
    for rel in codefiles:
        outputs=[]
        for rev in ['c050d971','HEAD']:
            src=git('show',rev+':'+rel)
            f=dest/(rev+'-'+Path(rel).name);f.write_bytes(src)
            if rel.endswith('.sv'):
                command=[str(a.simulator),'-E','-P',str(f)]
            else:
                command=['g++','-fpreprocessed','-E','-P',str(f)]
            result=subprocess.check_output(command)
            outputs.append(result)
        assert outputs[0]==outputs[1],rel
        print('COMMENT_ONLY',rel,'preprocessed_sha256',hashlib.sha256(outputs[0]).hexdigest())
    lane_pre=git('ls-tree','-r','3d5a201','--','hdl','tb').decode().splitlines()
    # Except the four comment files and their READMEs, C11 changes no executable source.
    changed=git('diff','--name-only','c050d971','3d5a201','--','hdl','tb').decode().splitlines()
    print('C11_HDL_TB_CHANGED',changed)
    assert set(changed)==set(codefiles+['tb/side_port/README.md','tb/tx_slots/README.md'])
    # Main's source and test content is retained verbatim except these four comments.
    for rel in git('ls-tree','-r','--name-only','ead80360','--','hdl','tb').decode().splitlines():
        if rel in changed:
            continue
        assert git('rev-parse','ead80360:'+rel)==git('rev-parse','HEAD:'+rel),rel
    print('ALL_OTHER_MERGED_HDL_TB_BLOBS_IDENTICAL_TO_MAIN_ead80360')

if __name__=='__main__':
    main()

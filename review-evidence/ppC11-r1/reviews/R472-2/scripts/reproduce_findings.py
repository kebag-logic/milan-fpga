#!/usr/bin/env python3
"""Minimal reproductions in a disposable exact-head clone; no source fix."""
import argparse
from pathlib import Path
import subprocess
import sys

def main():
    p=argparse.ArgumentParser()
    p.add_argument('tree',type=Path)
    a=p.parse_args(); root=a.tree.resolve()
    def run(label, *args):
        r=subprocess.run([sys.executable,str(root/'scripts/check-ids.py'),*args],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print(label,'rc',r.returncode);print(r.stdout,end='')
        return r.returncode
    def make_ids(label, expected):
        r=subprocess.run(['make','-j16','ids'],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        print(label,'make ids rc',r.returncode); print(r.stdout,end='')
        assert r.returncode==expected
    page=root/'tb/adp_engine/tb_adp_top.sv'
    original=page.read_bytes()
    assert b'T-ADP-\n//                DELAY-START' in original
    try:
        page.write_bytes(original.replace(b'T-ADP-\n//                DELAY-START',b'T-ADP-\n//                DELAY(-STRT)',1))
        assert run('F3 actual existing line-break changed to optional missing suffix')==0
        make_ids('F3 composed missing ID',0)
        page.write_bytes(original.replace(b'T-ADP-\n//                DELAY-START',b'T-ADP-DELAY(-STRT)',1))
        assert run('F3 same optional ID without line-break')==1
        make_ids('F3 one-line missing ID control',2)
    finally:
        page.write_bytes(original)
    script=root/'scripts/check-ids.py';code=script.read_text()
    stray=root/'tb/r472-minimal.txt'
    assert not stray.exists()
    for label,old,new,use in [
      ('F4 missing minus-one operand','return token in rows or (token.endswith("-1") and token[:-2] in rows)',
       'return token in rows or token.endswith("-1")','P-R472-MISSING-1\n'),
      ('F4 missing line-broken optional member','if optional:\n                yield line, f"{token}-{optional.group(1)}", "id"',
       'if optional:\n                if "\\n" not in optional.group(0):\n                    yield line, f"{token}-{optional.group(1)}", "id"','T-ADP-DELAY(-\n// MISSING)\n'),
    ]:
        try:
            stray.write_text(use)
            assert run(label+' healthy scanner')==1
            stray.unlink()
            assert old in code
            script.write_text(code.replace(old,new))
            assert run(label+' weakened scanner selftest','--selftest')==0
            stray.write_text(use)
            assert run(label+' weakened scanner real tree')==0
        finally:
            script.write_text(code);stray.unlink(missing_ok=True)

if __name__=='__main__':
    main()

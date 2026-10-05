#!/usr/bin/env python3
"""Recheck the optional hardening cases explicitly retained by public round 1."""
import argparse
from pathlib import Path
import subprocess
import sys

def main():
    p=argparse.ArgumentParser();p.add_argument('tree',type=Path);a=p.parse_args();root=a.tree.resolve()
    path=root/'scripts/check-ids.py';code=path.read_text()
    mutants=[
      ('only-tb','SCAN_DIRS = ("docs", "hdl", "tb")','SCAN_DIRS = ("tb",)'),
      ('no-hdl','SCAN_DIRS = ("docs", "hdl", "tb")','SCAN_DIRS = ("docs", "tb")'),
      ('no-docs','SCAN_DIRS = ("docs", "hdl", "tb")','SCAN_DIRS = ("hdl", "tb")'),
      ('whole-master-page','return "\\n".join(lines)','return body'),
      ('duplicate-master-row','if name in rows:','if False:'),
      ('empty-master-table','if not rows:','if False:'),
      ('any-tail','return token in rows or (token.endswith("-1") and token[:-2] in rows)',
       'return token in rows or token.rsplit("-", 1)[0] in rows'),
      ('unreadable-master','print("ids: master tables unreadable, FAILURES")\n        return 1',
       'print("ids: master tables unreadable, FAILURES")\n        return 0'),
    ]
    try:
        for name,old,new in mutants:
            assert old in code,name
            path.write_text(code.replace(old,new))
            r=subprocess.run([sys.executable,str(path),'--selftest'],cwd=root,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            print('PRIOR_CONTROL',name,'selftest_rc',r.returncode);print(r.stdout,end='')
            assert r.returncode==1,(name,r.stdout)
            path.write_text(code)
    finally:
        path.write_text(code)

if __name__=='__main__':
    main()

#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
import fcntl,json,os,pathlib,subprocess,sys,time
base=pathlib.Path(os.environ.get('REVIEW_LIMITER_ROOT', pathlib.Path(__file__).resolve().parent.parent))
name=pathlib.Path(sys.argv[0]).name
mapping=json.loads((base/'tool-paths.json').read_text())
while True:
    for i in range(16):
        f=(base/'job-slots'/str(i)).open('a')
        try: fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError: f.close();continue
        args=sys.argv[1:]
        env=os.environ.copy()
        if name=='clang-18' and 'REVIEW_CLANG18_LIBRARY_PATH' in env:
            env['LD_LIBRARY_PATH']=env['REVIEW_CLANG18_LIBRARY_PATH']
        if name=='cppcheck': args=['-j1' if a=='-j16' else a for a in args]
        result=subprocess.run([mapping[name],*args],env=env)
        sys.exit(result.returncode)
    time.sleep(0.05)

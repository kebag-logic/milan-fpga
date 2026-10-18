#!/usr/bin/env python3
import pathlib,subprocess,sys
p=pathlib.Path(__file__).resolve().parent
s=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else p/'scratch/source'
with (p/'docs-check.log').open('w') as f:r=subprocess.run(['make','-j16','check'],cwd=s,stdout=f,stderr=subprocess.STDOUT)
(p/'docs-check.rc').write_text(str(r.returncode)+'\n');print('docs-check rc='+str(r.returncode))

#!/usr/bin/env python3
"""Run permitted documentation/static gates concurrently; all children joined."""
import concurrent.futures, os, pathlib, subprocess, sys
root=pathlib.Path(sys.argv[1]).resolve()
out=pathlib.Path(sys.argv[2]).resolve()
compiler_dir=sys.argv[3] if len(sys.argv)>3 else ''
env=dict(os.environ, TMPDIR=str(out/'scratch'/'tmp'), PATH=(compiler_dir+':' if compiler_dir else '')+os.environ['PATH'])
jobs={
 'docs': ['make','-j16','check'],
 'static': ['bash','-c','python3 scripts/gen_matrix.py --check && python3 scripts/check_upc_map.py && python3 scripts/check_m9_opcodes.py --selftest && python3 scripts/check_m9_opcodes.py'],
 'hdl-lint': ['bash','scripts/lint_hdl.sh'],
}
def run(item):
 name,cmd=item
 with (out/(name+'.log')).open('w') as f:
  result=subprocess.run(cmd,cwd=root,env=env,stdout=f,stderr=subprocess.STDOUT)
 (out/(name+'.rc')).write_text(str(result.returncode)+'\n')
 print(name, result.returncode, flush=True)
 return result.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 results=list(ex.map(run,jobs.items()))
sys.exit(any(results))

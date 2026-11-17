from pathlib import Path
import subprocess, sys
src=Path('<source>')
dest=Path(sys.argv[2]); head=sys.argv[1]
def run(*args, cwd=None):
    return subprocess.check_output(args, cwd=cwd, text=True).strip()
assert not dest.exists()
run('git','clone','-q','--shared','--no-checkout',str(src),str(dest))
run('git','checkout','-q','--detach',head,cwd=dest)
for line in run('git','config','--file','.gitmodules','--get-regexp',r'^submodule\..*\.path$',cwd=dest).splitlines():
    dep=line.split()[1]
    run('git','config',f'submodule.{dep}.url',str(src/dep),cwd=dest)
run('git','-c','protocol.file.allow=always','submodule','update','-q','--init',cwd=dest)
assert run('git','status','--porcelain','--untracked-files=all',cwd=dest)==''
assert run('git','rev-parse','HEAD',cwd=dest)==head
print('clean clone',head)
print(run('git','submodule','status',cwd=dest))

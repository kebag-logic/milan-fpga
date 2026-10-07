import concurrent.futures, os, pathlib, subprocess, sys, tarfile
root=pathlib.Path(sys.argv[1]).resolve(); packet=pathlib.Path(sys.argv[2]).resolve()
scratch=packet/'scratch'; receipts=packet/'receipts'; copy=scratch/'rtl-copy'
copy.mkdir(exist_ok=True)
archive=scratch/'source.tar'
with archive.open('wb') as f: subprocess.run(['git','-C',str(root),'archive','HEAD'],stdout=f,check=True)
with tarfile.open(archive) as t: t.extractall(copy,filter='data')
verilator=os.environ.get('REVIEW_VERILATOR','$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
version=subprocess.check_output([verilator,'--version'],text=True); assert 'Verilator 5.050' in version
(receipts/'compiler-identity.txt').write_text(version)
env=dict(os.environ,TMPDIR=str(scratch),PYTHONDONTWRITEBYTECODE='1')
def run(name,args,cwd):
    with (receipts/(name+'.log')).open('w') as f:
        f.write('Command: '+repr(args)+'\n'); f.flush()
        r=subprocess.run(args,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
    (receipts/(name+'.rc')).write_text(str(r.returncode)+'\n')
    print(name,r.returncode,flush=True); return r.returncode
def rtl():
    cwd=copy/'tb/verilator/mbx'
    flags=subprocess.check_output(['make','-s','print-vflags'],cwd=cwd,text=True).splitlines()
    # Override only parallelism; keep every checked-in build flag.
    vf='--cc --exe --build -j 4 --top-module tb_mbx_top -Wall -Wno-fatal -Werror-USERERROR -Werror-PINMISSING -Werror-UNDRIVEN -Wno-DECLFILENAME -Wno-UNUSEDPARAM -Wno-UNUSEDSIGNAL -CFLAGS "-std=c++17 -O2 -Wall -Wextra -I'+str(copy/'sw/firmware/ctrl/mbx')+'"'
    failures=0
    for target in ['run-wb','run-axil','run-cosim','run-if2']:
        failures+=run(target,['make','-j16',target,'VERILATOR='+verilator,'VFLAGS='+vf],cwd)!=0
    return failures
def native():
    return run('native',['python3',str(packet/'scripts/native.py'),str(root),str(scratch/'native')],root)
def generator():
    return sum(run(name,['python3','sw/mailbox/gen_mailbox.py',*opts],root)!=0 for name,opts in [('generator-check',['--check','--crosscheck']),('generator-selftest',['--selftest'])])
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results=[f.result() for f in [pool.submit(rtl),pool.submit(native),pool.submit(generator)]]
sys.exit(int(any(results)))

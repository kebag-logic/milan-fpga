#!/usr/bin/env python3
"""Focused exact-revision probes; disposable exports only, maximum 16 compile jobs."""
import concurrent.futures, io, pathlib, subprocess, sys, tarfile
ROOT=pathlib.Path(__file__).resolve().parent
CLONE=pathlib.Path(sys.argv[1]).resolve()
HEAD='7b424cdfe111a426f00517ff471246b4b9650726'
SIM='$VALIDATION_TOOLS/pinned-verilator-5.050/verilator'
assert subprocess.check_output(['git','-C',str(CLONE),'rev-parse','HEAD'],text=True).strip()==HEAD
identity=subprocess.check_output([SIM,'--version'],text=True)
assert 'Verilator 5.050' in identity
(ROOT/'simulator-identity.txt').write_text(identity)
archive=subprocess.check_output(['git','-C',str(CLONE),'archive',HEAD,'hdl','tb'])
tasks=[('fsm','srp_stream_fsms','probe_parked_leave.py'),('wire','srp_top','probe_parked_leave_wire.py'),('parked-fsm','srp_stream_fsms','parked-probe.cpp'),('parked-wire','srp_top','parked-wire-probe.cpp'),('lower-index','srp_stream_fsms','probe-s2.cpp'),('collisions','srp_stream_fsms','probe-parked-pairs.cpp')]
def run(task):
    name,suite,probe=task
    tree=ROOT/'scratch'/('probe-'+name);tree.mkdir(parents=True,exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar: tar.extractall(tree,filter='data')
    dest=tree/'tb'/suite
    mk=dest/'Makefile';text=mk.read_text().replace('-j 0','-j 4')
    if probe.endswith('.py'):
        subprocess.run([sys.executable,'-I',str(ROOT/'probes'/probe),str(tree)],check=True,stdout=subprocess.DEVNULL)
    else:
        (dest/probe).write_bytes((ROOT/'probes'/probe).read_bytes())
        text=text.replace('CPP  = sim_main.cpp','CPP  = '+probe)
    mk.write_text(text)
    log=ROOT/(name+'.log')
    with log.open('w') as out:
        out.write('Exact source '+HEAD+'; disposable test entry or insertion only.\n');out.flush()
        rc=subprocess.run(['make','-j16','run','VERILATOR='+SIM,'RUN_ARGS='+('share' if suite=='srp_top' else 'suite')],cwd=dest,stdout=out,stderr=subprocess.STDOUT).returncode
    (ROOT/(name+'.rc')).write_text(str(rc)+'\n')
    lines=[s for s in log.read_text().splitlines() if s.startswith(('PROBE','FAIL','PASS','old_sink=')) or 'checks:' in s or 'checks,' in s or 'peer' in s and not s.startswith(('g++','c++'))]
    return name,rc,lines
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    results=list(pool.map(run,tasks))
with (ROOT/'probe-summary.txt').open('w') as out:
    for name,rc,lines in results:
        out.write(f'{name}: rc={rc}\n'+'\n'.join(lines)+'\n')
        print(name,'rc',rc)
sys.exit(any(rc for _,rc,_ in results))

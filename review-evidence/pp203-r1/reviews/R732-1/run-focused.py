#!/usr/bin/env python3
"""Reproduce focused checks in disposable copies; never edit the source checkout."""
import concurrent.futures, importlib.util, json, os, pathlib, shutil, subprocess, sys, tarfile
sys.dont_write_bytecode = True
P = pathlib.Path(__file__).resolve().parent
SRC = pathlib.Path(sys.argv[1]).resolve()
S = P / 'scratch'
S.mkdir(exist_ok=True)
PIN = os.environ.get('REVIEW_VERILATOR', '$VALIDATION_TOOLS/pinned-verilator-5.050/verilator')
env = dict(os.environ, TMPDIR=str(S), MAKEFLAGS='-j16', PYTHONDONTWRITEBYTECODE='1')
wrapper = S / 'compiler-limit'
wrapper.write_text('#!/usr/bin/env python3\nimport os,sys\na=sys.argv[1:]\nfor i in range(len(a)-1):\n if a[i] == "-j": a[i+1]="2"\nos.execv('+repr(PIN)+', ['+repr(PIN)+']+a)\n')
wrapper.chmod(0o755)
def run(name, cmd, cwd=SRC):
    with (P / (name+'.log')).open('w') as f:
        f.write('COMMAND '+json.dumps(cmd)+'\n'); f.flush()
        r = subprocess.run(cmd, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT)
    (P / (name+'.rc')).write_text(str(r.returncode)+'\n')
    print(name, r.returncode, flush=True)
    return r.returncode
def tree(name):
    dest=S/name
    if dest.exists(): shutil.rmtree(dest)
    if not dest.exists():
        dest.mkdir()
        archive=S/(name+'.tar')
        with archive.open('wb') as f: subprocess.run(['git','archive','HEAD'],cwd=SRC,stdout=f,check=True)
        with tarfile.open(archive) as t: t.extractall(dest,filter='data')
        archive.unlink()
    return dest
def bench():
    d=tree('focused')
    cmd=['make','-j16','-C','tb/pp_top','reboot','VERILATOR='+str(wrapper)]
    if run('reboot-control',cmd,d): return
    f=d/'tb/pp_top/sim_main.cpp'
    text=f.read_text()
    needle='          queued_answers);\n'
    assert text.count(needle)==1
    extra='''
    long final_departure = -1;
    for (const auto& e : io.tx_log)
      if (departing(e.second)) final_departure = long(e.first);
    int late_frames = 0;
    for (const auto& e : io.tx_log) {
      if (final_departure >= 0 && long(e.first) > final_departure) {
        ++late_frames;
        printf("POST_DEPARTURE frame cycle=%llu departure=%ld request=%ld ethertype=%02x%02x subtype=%02x mt=%02x opcode=%04x unsolicited=%u\\n",
               (unsigned long long)e.first, final_departure, io.reboot_rise_t,
               e.second[12], e.second[13], e.second[14], e.second[15],
               aecp(e.second) ? ct(e.second) : 0,
               aecp(e.second) ? unsigned(e.second[36] >> 7) : 0);
      }
    }
    CHECK(final_departure >= 0 && late_frames == 0,
          "PROBE no control-plane frame after ENTITY_DEPARTING while reset is withheld (%d frames)", late_frames);
'''
    f.write_text(text.replace(needle,needle+extra))
    with (P/'post-departure-probe.patch').open('w') as out:
        subprocess.run(['diff','-u','--label','a/tb/pp_top/sim_main.cpp','--label','b/tb/pp_top/sim_main.cpp',str(SRC/'tb/pp_top/sim_main.cpp'),str(f)],stdout=out)
    run('post-departure-probe',cmd,d)
def mutants():
    spec=importlib.util.spec_from_file_location('campaign',SRC/'tb/pp_top/aecp_dispatch_mutants.py')
    m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    arms=','.join(x[0] for x in m.MUTANTS if x[0].startswith('rbt-'))
    run('reboot-mutants',['python3',str(SRC/'tb/pp_top/aecp_dispatch_mutants.py'),'--jobs','2','--only',arms,'--output',str(P/'rbt-mutants'),'--verilator',str(wrapper)])
def docs():
    d=S/'docs-git'
    if not d.exists():
        subprocess.run(['git','clone','--quiet','--no-hardlinks',str(SRC),str(d)],check=True)
    run('docs-check-git',['make','-j16','check'],d)
run('compiler-identity',[PIN,'--version'])
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    jobs=[pool.submit(x) for x in (bench,mutants,docs)]
    for j in jobs: j.result()

import ast, importlib.util, os, pathlib, subprocess, sys, time
ROOT = pathlib.Path('/data/milan/reviews/r213-498-r4')
TMP = pathlib.Path('/data/milan/tmp/498-review-R213-r4')
BASE = '07294a76e833f1831d9fcbceb8123b8380c4ae76'
def load(base=False, expose=False):
    path = ROOT / 'sw/builder/test_builder.py'
    source = subprocess.check_output(['git','show',BASE+':sw/builder/test_builder.py'], cwd=ROOT, text=True) if base else path.read_text()
    tree = ast.parse(source)
    if expose:
        gate = next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name == 'test_baremetal_profile_contract')
        cut = next(i for i,n in enumerate(gate.body) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='baseline_census_verdict' for t in n.targets))
        gate.body = gate.body[:cut] + [ast.Return(ast.Call(ast.Name('locals',ast.Load()),[],[]))]
        ast.fix_missing_locations(tree)
    name = 'review_base' if base else 'review_candidate'
    mod = importlib.util.module_from_spec(importlib.util.spec_from_file_location(name,path))
    sys.modules[name] = mod
    exec(compile(tree,str(path),'exec'),mod.__dict__)
    mod.OUT = TMP / ('base-out' if base else 'candidate-out')
    mod.OUT.mkdir(exist_ok=True)
    return mod

def launch(mode, command):
    env = os.environ.copy()
    env.update(TMPDIR=str(TMP/'tmp'), PYTHONDONTWRITEBYTECODE='1', MAKEFLAGS='-j8', CCACHE_DIR=str(TMP/'ccache'))
    if mode != 'present':
        home = TMP/(mode+'-home'); home.mkdir(exist_ok=True)
        bindir = TMP/(mode+'-bin'); bindir.mkdir(exist_ok=True)
        for directory in os.get_exec_path():
            path = pathlib.Path(directory)
            if not path.is_dir(): continue
            for target in path.iterdir():
                if target.name.startswith('riscv') and (mode=='absent' or not target.name.startswith('riscv64-elf-')): continue
                link = bindir/target.name
                if target.is_file() and os.access(target,os.X_OK) and not link.exists(): link.symlink_to(target)
        env.update(HOME=str(home),PATH=str(bindir))
    os.sched_setaffinity(0,set(range(64,80)))
    return subprocess.call(command,env=env,cwd=ROOT)

if __name__ == '__main__':
    if sys.argv[1] == 'launch':
        sys.exit(launch(sys.argv[2],sys.argv[3:]))
    mod = load(base='--base' in sys.argv)
    names = [n for n in sys.argv[1:] if not n.startswith('--')]
    for name in names:
        start=time.monotonic(); print('RUN',name,flush=True)
        getattr(mod,name)()
        print('COMPLETE',name,'seconds',round(time.monotonic()-start,2),flush=True)
    print('REGISTERED SKIPS',mod.SKIPPED,flush=True)

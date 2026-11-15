"""List repo files in the import closure of the hooks self-test and intersect with a changed-file list.
Usage: python3 -I import_closure.py <repo> <changed-list>"""
import sys, os, re
repo, changed = os.path.abspath(sys.argv[1]), sys.argv[2]
d = os.path.join(repo, 'tb/verilator/ctrl_service_hooks')
sys.path.insert(0, d)
os.chdir(d)
import importlib
importlib.import_module('hooks_selftest')
files = sorted({os.path.relpath(m.__file__, repo) for m in list(sys.modules.values())
                if getattr(m, '__file__', None) and os.path.abspath(m.__file__).startswith(repo + os.sep)})
ch = {l.strip() for l in open(changed) if l.strip()}
print('closure files:', len(files))
for f in files: print(('CHANGED ' if f in ch else '        ') + f)
print('## textual header/doc reads in closure naming a changed file')
for f in files:
    t = open(os.path.join(repo, f)).read()
    for c in ch:
        b = os.path.basename(c)
        for m in re.finditer(re.escape(b), t):
            line = t.count('\n', 0, m.start()) + 1
            src = t.splitlines()[line - 1].strip()
            if not src.startswith('#') and ('read' in src or "'" + b in src or '/' + b in src):
                print(f'{f}:{line}: {src[:160]}')

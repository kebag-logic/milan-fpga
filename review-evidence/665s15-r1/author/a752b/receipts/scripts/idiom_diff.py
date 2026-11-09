"""Per changed Python file: idiom findings at base and in the working tree, and the sites new here."""
import subprocess, sys
sys.path.insert(0, 'scripts')
import check_py_idiom as c
base = sys.argv[1]
files = subprocess.run(['git', 'diff', '--name-only', base, '--', '*.py'], capture_output=True, text=True).stdout.split()
for rel in files:
    try:
        old = subprocess.run(['git', 'show', f'{base}:{rel}'], capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        old = ''
    new = open(rel).read()
    oc, os_ = c.scan(old, rel)
    nc, ns = c.scan(new, rel)
    diff = {k: nc[k] - oc[k] for k in nc if nc[k] != oc[k]}
    if diff:
        print(rel, diff)
        for k in diff:
            print('   ', k, [s for s in ns.get(k, [])][:12] if isinstance(ns, dict) else '')

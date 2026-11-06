#!/usr/bin/env python3
"""The one shape the supersede rule's group term decides: the named group's own probe unmeasured while another group
measured the path on that interface. usage: group_shape.py <clone> <scratch>. At the head it stays a refusal."""
import shutil, subprocess, sys
from pathlib import Path
clone, scratch = Path(sys.argv[1]), Path(sys.argv[2])
H = 'tb/verilator/ctrl_service_hooks'
BODY = '''
import sys
sys.path.insert(0, sys.argv[1])
import hooks_selftest as s
lost = dict(probe='hooks-disc-aging.tmr_no_adp.if1', path=['acmp.tmr_no_adp', 1], status='no start', reason='late')
row = dict(s.row('disc', 2.0, probe='acmp.tmr_no_adp.if1'), path=['acmp.tmr_no_adp', 1], interface=1, status='measured')
got = s.graded_with({'acmp-disc': [row], 'hooks-disc-aging': [lost]})
print('refusals', got['refusals'], 'superseded', got['superseded'])
'''
for name, new in (('head', None), ('group term dropped', "if by and any((x['path'], x['interface']) == tuple(r['path']) for x in rows):")):
    tree = scratch / 'group_shape'
    shutil.rmtree(tree, ignore_errors=True); tree.mkdir(parents=True)
    subprocess.run(f'git -C {clone} archive HEAD tb sw scripts | tar -x -C {tree}', shell=True, check=True)
    if new:
        p = tree / H / 'run.py'; t = p.read_text()
        old = "if by and any((x['group'], x['path'], x['interface']) == (by, *r['path']) for x in rows):"
        assert t.count(old) == 1; p.write_text(t.replace(old, new))
    g = subprocess.run([sys.executable, '-B', '-c', BODY, str(tree / H)], capture_output=True, text=True)
    print(name, '=>', g.stdout.strip() or g.stderr[-300:])
    shutil.rmtree(tree, ignore_errors=True)

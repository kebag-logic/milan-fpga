#!/usr/bin/env python3
"""Reviewer's own source twins, written from the rule text, each on a disposable copy. usage: twins_spot.py <clone> <scratch>"""
import concurrent.futures as cf, re, shutil, subprocess, sys
from pathlib import Path
CLONE, SCRATCH = Path(sys.argv[1]), Path(sys.argv[2])
H = 'tb/verilator/ctrl_service_hooks'
R, K = f'{H}/run.py', f'{H}/hooks.py'
T = {
 'next_adp_record: any interface': (K, "if k == CH['adp'] and inter == interface and c > after),", "if k == CH['adp'] and c > after),"),
 'next_adp_record: any channel': (K, "if k == CH['adp'] and inter == interface and c > after),", "if inter == interface and c > after),"),
 'next_adp_record: not after': (K, "if k == CH['adp'] and inter == interface and c > after),", "if k == CH['adp'] and inter == interface and c >= after),"),
 'disc_decided_ms: one service': (K, "return TMR_DELAY_MAX_MS + 2 * bound_ms('disc')", "return TMR_DELAY_MAX_MS + bound_ms('disc')"),
 'disc_decided_ms: no service': (K, "return TMR_DELAY_MAX_MS + 2 * bound_ms('disc')", "return TMR_DELAY_MAX_MS"),
 'adopted: any bit of the word': (K, "return bool((value >> field.lsb) & ((1 << field.width) - 1))", "return bool(value)"),
 'plant_findings: no colon': (R, "if finding.startswith(plant_wanted(plant) + ':')]", "if finding.startswith(plant_wanted(plant))]"),
 'gm_steps: id read in decimal': (K, "return [(int(s.split()[1]), int(s.split()[2], 16)) for s in group.steps if s.startswith('gm ')]", "return [(int(s.split()[1]), int(s.split()[2])) for s in group.steps if s.startswith('gm ')]"),
}
def one(name, spec):
    path, old, new = spec
    tree = SCRATCH / re.sub(r'\W+', '_', name)
    shutil.rmtree(tree, ignore_errors=True); tree.mkdir(parents=True)
    subprocess.run(f'git -C {CLONE} archive HEAD tb sw scripts | tar -x -C {tree}', shell=True, check=True)
    p = tree / path; text = p.read_text()
    if old is None:
        step = "    g.add(f'wait cycles {refilled_ms() * MS}', 'gap 1', 'mark composed')\n"
        parts = text.split(step); assert len(parts) == 3, len(parts)
        repl = "    g.add('gap 1', 'mark composed')\n"
        text = parts[0] + (repl if 'notify' in name else step) + parts[1] + (repl if 'counters' in name else step) + parts[2]
    else:
        if text.count(old) != 1: return name, f'ANCHOR {text.count(old)}', [], [], ''
        text = text.replace(old, new)
    p.write_text(text)
    g = subprocess.run([sys.executable, '-B', str(tree / H / 'run.py'), '--self-test'], capture_output=True, text=True)
    o = g.stdout + g.stderr
    fails = [x[5:100] for x in o.splitlines() if x.startswith('FAIL ')]
    esc = [x.split(': ESCAPED')[0][7:] for x in o.splitlines() if ': ESCAPED ' in x]
    tail = next((x for x in o.splitlines() if 'self-test:' in x), o[-200:])
    shutil.rmtree(tree, ignore_errors=True)
    return name, g.returncode, fails, esc, tail
with cf.ThreadPoolExecutor(8) as ex:
    res = list(ex.map(lambda kv: one(*kv), T.items()))
for name, rc, fails, esc, tail in res:
    print(f"{'SURVIVES' if rc == 0 else 'KILLED'} | {name} | rc={rc} | {tail}")
    for x in fails: print('    check fails:', x)
    for x in esc: print('    mutant escapes:', x)
print('survivors:', sum(r[1] == 0 for r in res), 'of', len(res))

#!/usr/bin/env python3
"""Reviewer's own source twins, written from the rule text, each on a disposable copy. usage: twins_spot.py <clone> <scratch>"""
import concurrent.futures as cf, re, shutil, subprocess, sys
from pathlib import Path
CLONE, SCRATCH = Path(sys.argv[1]), Path(sys.argv[2])
H = 'tb/verilator/ctrl_service_hooks'
R, K = f'{H}/run.py', f'{H}/hooks.py'
T = {
 'hook_row: W not added': (R, "bound = hooks.bound_ms(row['family']) + row['wait_ms']", "bound = hooks.bound_ms(row['family'])"),
 'hook_row: verdict drops unbounded': (R, "bound_ms=bound, within=not unbounded and row['ms'] <= bound, unbounded=unbounded,", "bound_ms=bound, within=row['ms'] <= bound, unbounded=unbounded,"),
 'hook_row: unanswered not unbounded': (R, "unbounded = bool(row.get('starved') or row.get('unanswered'))", "unbounded = bool(row.get('starved'))"),
 'hook_row: starved not unbounded': (R, "unbounded = bool(row.get('starved') or row.get('unanswered'))", "unbounded = bool(row.get('unanswered'))"),
 'hook_row: margin drops the wait': (R, "margin_ms=round(timeout - row['wait_ms'] - row['ms'], 5), ahead", "margin_ms=round(timeout - row['ms'], 5), ahead"),
 'hook_row: margin from zero': (R, "margin_ms=round(timeout - row['wait_ms'] - row['ms'], 5), ahead", "margin_ms=round(0.0 - row['wait_ms'] - row['ms'], 5), ahead"),
 'held_row: verdict always within': (R, "bound_ms=bound, within=held['ms'] <= bound, unbounded=False", "bound_ms=bound, within=True, unbounded=False"),
 'held_row: margin drops the wait': (R, "margin_ms=round(hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], 5), ahead=0)", "margin_ms=round(hooks.COUNTERS_NORMATIVE_MS - held['ms'], 5), ahead=0)"),
 'held missing: finding by name dropped': (R, "if r.get('missing'):\n            findings.append(f\"LATE {r['hook']}: {r['probe']}: the held push was never sent\")\n        elif not r['within']:", "if not r['within']:"),
 'held missing: slack ignores missing': (R, "if r['unbounded'] or r.get('missing'):", "if r['unbounded']:"),
 'slack ignores unbounded': (R, "if r['unbounded'] or r.get('missing'):", "if r.get('missing'):"),
 'narrow: boundary <=': (R, "elif r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES:", "elif r['slack_cycles'] <= hooks.LAYOUT_SWING_CYCLES:"),
 'ordering findings dropped': (R, "        findings += c['findings']\n", "        pass\n"),
 'buckets: no wait in notify group': (K, None, None),
 'buckets: no wait in counters group': (K, None, None),
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

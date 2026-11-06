#!/usr/bin/env python3
"""R784-3 probes: source mutants of run.py/hooks.py and deletion probes of hooks_selftest.py.

usage: r3_probes.py TREE WORKDIR
TREE is a clean export of the head. Each case copies the harness directory into WORKDIR, applies one exact text
edit, runs the self-test in a child process and records its verdict line, the failed checks and escaped mutants.
"""
import re, shutil, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

tree, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
H = 'tb/verilator/ctrl_service_hooks'

def line_del(text, needle):
    """Replace the expect statement containing needle by pass."""
    lines = text.split('\n')
    i = next(n for n, l in enumerate(lines) if needle in l)
    while not lines[i].lstrip().startswith('expect('):
        i -= 1
    j, depth = i, 0
    while True:
        depth += lines[j].count('(') - lines[j].count(')')
        if depth <= 0:
            break
        j += 1
    ind = lines[i][:len(lines[i]) - len(lines[i].lstrip())]
    lines[i:j + 1] = [ind + 'pass']
    return '\n'.join(lines)

GRP = "any((x['group'], x['path'], x['interface']) == (by, *r['path']) for x in rows)"
SRC = {
 # the six named source mutants, restated from the ruling's names
 'hp-row-ms-zero': ('run.py', "interface=0, family='notify', ms=held['ms'], cpu_cycles=cycles", "interface=0, family='notify', ms=0.0, cpu_cycles=cycles"),
 'hp-ms': ('run.py', "interface=0, family='notify', ms=held['ms'], cpu_cycles=cycles", "interface=0, family='notify', ms=held['ms'] + 1, cpu_cycles=cycles"),
 's-narrow-le': ('run.py', "narrow = sum(r['within'] and r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES for r in mine)", "narrow = sum(r['within'] and r['slack_cycles'] <= hooks.LAYOUT_SWING_CYCLES for r in mine)"),
 'hm-cycles': ('run.py', "ms=0.0, cpu_cycles=0, wait_ms=0.0,", "ms=0.0, cpu_cycles=7, wait_ms=0.0,"),
 'hm-wait': ('run.py', "ms=0.0, cpu_cycles=0, wait_ms=0.0,", "ms=0.0, cpu_cycles=0, wait_ms=7.0,"),
 'hm-margin': ('run.py', "normative_ms=hooks.COUNTERS_NORMATIVE_MS, margin_ms=0.0, ahead=0, missing=True", "normative_ms=hooks.COUNTERS_NORMATIVE_MS, margin_ms=7.0, ahead=0, missing=True"),
 # the narrow boundary in the finding as well as in the summary
 'finding-narrow-le': ('run.py', "elif r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES:", "elif r['slack_cycles'] <= hooks.LAYOUT_SWING_CYCLES:"),
 'finding-narrow-minus1': ('run.py', "elif r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES:", "elif r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES - 1:"),
 's-narrow-minus1': ('run.py', "narrow = sum(r['within'] and r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES for r in mine)", "narrow = sum(r['within'] and r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES - 1 for r in mine)"),
 # the supersede rule, field by field: the rule is (group, path, interface)
 'sup-any-group': ('run.py', GRP, "any((x['path'], x['interface']) == tuple(r['path']) for x in rows)"),
 'sup-any-interface': ('run.py', GRP, "any((x['group'], x['path']) == (by, r['path'][0]) for x in rows)"),
 'sup-any-path': ('run.py', GRP, "any((x['group'], x['interface']) == (by, r['path'][1]) for x in rows)"),
 'sup-group-only': ('run.py', GRP, "any(x['group'] == by for x in rows)"),
 'sup-no-row-needed': ('run.py', GRP, "True"),
 'sup-table-any-path': ('run.py', "by = hooks.SUPERSEDED.get(r['path'][0])", "by = 'hooks-disc-aging'"),
 # the amended column: a verdict that reads it, by row class
 'verdict-queued-60': ('run.py', "bound_ms=bound, within=not unbounded and row['ms'] <= bound, unbounded=unbounded,", "bound_ms=bound, within=not unbounded and row['ms'] <= (60.0 if row['path'][0].startswith('counters.all') else bound), unbounded=unbounded,"),
 'verdict-descriptor-60': ('run.py', "bound_ms=bound, within=not unbounded and row['ms'] <= bound, unbounded=unbounded,", "bound_ms=bound, within=not unbounded and row['ms'] <= (60.0 if row['path'][0].startswith('counters.all.') else bound), unbounded=unbounded,"),
 'verdict-srp-20': ('run.py', "bound_ms=bound, within=not unbounded and row['ms'] <= bound, unbounded=unbounded,", "bound_ms=bound, within=not unbounded and row['ms'] <= (20.0 + row['wait_ms'] if hook == 'H-SRP' else bound), unbounded=unbounded,"),
 'narrow-finding-reads-column': ('run.py', "elif r['slack_cycles'] < hooks.LAYOUT_SWING_CYCLES:", "elif r['slack_cycles'] + round((hooks.amended_ms(r, 2) - r['bound_ms']) * spec['cpu_hz'] / 1000) < hooks.LAYOUT_SWING_CYCLES:"),
 'summary-misses-read-column': ('run.py', "misses=sum(not r['within'] for r in mine)", "misses=sum(r['ms'] > hooks.amended_ms(r, 2) or r['unbounded'] for r in mine)"),
 # the held row fields the README says are not read
 'held-row-text': ('run.py', "row='GET_COUNTERS push, held until 1 s after the last departure, from its eligibility (H-COUNTERS)',", "row='x',"),
 'held-ahead': ('run.py', "margin_ms=round(hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], 5), ahead=0)", "margin_ms=round(hooks.COUNTERS_NORMATIVE_MS - held['wait_ms'] - held['ms'], 5), ahead=9)"),
}
ARM = "the window opens before the arm"
VERD, LATE = "'the amended bounds graded a path'", "f'findings {late}'"
OTHER, PATH = "f'other interface: {got}'", "f'another path: {got}'"
DEL = {
 'B-arm-rule': [ARM],
 'C-verdict-only': [VERD],
 'C-verdict-and-late': [VERD, LATE],
 'E-other-interface-only': [OTHER],
 'E-other-and-path': [OTHER, PATH],
 'N-narrow-count': ["narrow fits, not 1"],
 'N-slack-pin-only': ["the rows are not at the swing"],
 'H-service': ["not its service"],
 'H-missing-service': ["a push never sent records a service"],
 'H-labels-both': ["f'held row {identity}'", "f'missing row {identity}'"],
}

def run(name, edit):
    d = work / name
    if d.exists():
        shutil.rmtree(d)
    (d / 'tb/verilator').mkdir(parents=True)
    for sub in ('ctrl_service_hooks', 'ctrl_service_budget', 'ctrl_split_boot'):
        if (tree / 'tb/verilator' / sub).exists():
            shutil.copytree(tree / 'tb/verilator' / sub, d / 'tb/verilator' / sub)
    for link in tree.iterdir():
        if link.name != 'tb':
            (d / link.name).symlink_to(link)
    for sub in (tree / 'tb').iterdir():
        if sub.name != 'verilator':
            (d / 'tb' / sub.name).symlink_to(sub)
    for sub in (tree / 'tb/verilator').iterdir():
        if not (d / 'tb/verilator' / sub.name).exists():
            (d / 'tb/verilator' / sub.name).symlink_to(sub)
    edit(d / H)
    p = subprocess.run([sys.executable, '-B', str(d / H / 'hooks_selftest.py')], capture_output=True, text=True, cwd='/tmp')
    out = p.stdout + p.stderr
    tail = [l for l in out.splitlines() if 'self-test:' in l] or out.splitlines()[-1:]
    fails = [l[:150] for l in out.splitlines() if l.startswith('FAIL ')]
    esc = [l[:120] for l in out.splitlines() if 'ESCAPED' in l and l.startswith('MUTANT')]
    return name, p.returncode, tail[0] if tail else '', fails, esc

def src_edit(item):
    f, old, new = item
    def go(h):
        t = (h / f).read_text()
        assert t.count(old) == 1, (f, old, t.count(old))
        (h / f).write_text(t.replace(old, new))
    return go

def del_edit(needles):
    def go(h):
        p = h / 'hooks_selftest.py'
        t = p.read_text()
        for n in needles:
            t = line_del(t, n)
        p.write_text(t)
    return go

cases = [('control', lambda h: None)] + [(k, src_edit(v)) for k, v in SRC.items()] + [('del-' + k, del_edit(v)) for k, v in DEL.items()]
with ThreadPoolExecutor(12) as pool:
    results = list(pool.map(lambda c: run(*c), cases))
for name, rc, tail, fails, esc in results:
    kind = 'KILLED' if rc else 'SURVIVES'
    print(f'{name}: rc {rc} {kind}: {tail}')
    for x in fails: print('    ' + x)
    for x in esc: print('    ' + x)
